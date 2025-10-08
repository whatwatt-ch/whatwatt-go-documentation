#!/usr/bin/env python3
"""
Documentation Validation Suite
Comprehensive validation for markdown documentation using multiple tools
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path


class Colors:
    """ANSI color codes for terminal output"""

    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"


def run_command(cmd: list[str], description: str, critical: bool = True) -> tuple[bool, str]:
    """Run a command and return success status and output"""
    try:
        print(f"{Colors.BLUE}[*] {description}...{Colors.END}")
        # Use shell=True for npx/mkdocs on Windows so PATH is correct
        use_shell = False
        if os.name == "nt" and (cmd[0] == "npx" or cmd[0] == "mkdocs"):
            use_shell = True
        result = subprocess.run(
            cmd, capture_output=True, text=True, cwd=Path.cwd(), shell=use_shell
        )

        if result.returncode == 0:
            print(f"{Colors.GREEN}[+] {description} - PASSED{Colors.END}")
            if result.stdout.strip():
                print(f"{Colors.WHITE}{result.stdout.strip()}{Colors.END}")
            return True, result.stdout
        else:
            status_icon = "[-]" if critical else "[!]"
            status_text = "FAILED" if critical else "WARNINGS"
            # Print status line (wrapped for ruff line-length)
            msg = (
                f"{Colors.RED if critical else Colors.YELLOW}{status_icon} "
                f"{description} - {status_text}{Colors.END}"
            )
            print(msg)
            if result.stderr.strip():
                err = result.stderr.strip()
                print(f"{Colors.RED if critical else Colors.YELLOW}{err}{Colors.END}")
            if result.stdout.strip():
                print(f"{Colors.WHITE}{result.stdout.strip()}{Colors.END}")
            return False, result.stderr + result.stdout

    except FileNotFoundError:
        print(f"{Colors.RED}[-] {description} - TOOL NOT FOUND{Colors.END}")
        print(f"{Colors.RED}Command not found: {' '.join(cmd)}{Colors.END}")
        return False, f"Tool not found: {cmd[0]}"
    except Exception as e:
        print(f"{Colors.RED}[-] {description} - ERROR: {e}{Colors.END}")
        return False, str(e)


def validate_markdown_syntax() -> bool:
    """Validate Markdown syntax with markdownlint-cli2"""
    return run_command(
        ["npx", "markdownlint-cli2", "**/*.md", "!node_modules", "!dist"],
        "Markdown syntax validation (markdownlint-cli2)",
        critical=True,
    )[0]


def validate_mkdocs_build() -> bool:
    """Validate MkDocs build in strict mode"""
    mkdocs_path = None
    if os.name == "nt":
        mkdocs_path = str(Path(".venv") / "Scripts" / "mkdocs.exe")
    else:
        mkdocs_path = str(Path(".venv") / "bin" / "mkdocs")
    if not Path(mkdocs_path).exists():
        mkdocs_path = "mkdocs"  # fallback to global
    return run_command(
        [mkdocs_path, "build", "--clean", "--strict"],
        "MkDocs build validation (strict mode)",
        critical=True,
    )[0]


def validate_links_site() -> bool:
    """Validate links in built site using broken-link-checker against local server"""
    import subprocess
    import time

    import requests

    # Build site first
    site_path = Path("site")
    if not site_path.exists():
        print(f"{Colors.YELLOW}[!]  Site directory not found, building first...{Colors.END}")
        if not run_command(["mkdocs", "build", "--clean"], "Building site for link checking")[0]:
            return False

    # Check if site was built successfully
    index_path = site_path / "index.html"
    if not index_path.exists():
        warn = (
            f"{Colors.YELLOW}[!]  site/index.html not found after build, "
            f"skipping link check.{Colors.END}"
        )
        print(warn)
        return False

    # Start mkdocs serve in background
    print(f"{Colors.BLUE}[*] Starting local server for link validation...{Colors.END}")
    server_process = None
    try:
        # Start mkdocs serve on port 8000
        server_process = subprocess.Popen(
            ["mkdocs", "serve", "-a", "127.0.0.1:8000"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        # Wait for server to start (max 10 seconds)
        server_url = "http://127.0.0.1:8000"
        for attempt in range(20):  # 20 attempts * 0.5s = 10s timeout
            try:
                response = requests.get(server_url, timeout=2)
                if response.status_code == 200:
                    print(f"{Colors.GREEN}[+] Local server started at {server_url}{Colors.END}")
                    break
            except requests.exceptions.RequestException:
                pass
            time.sleep(0.5)
        else:
            print(f"{Colors.RED}[-] Failed to start local server after 10 seconds{Colors.END}")
            return False

        # Run broken-link-checker against the local server
        result = run_command(
            ["npx", "blc", server_url, "--recursive", "--requests", "5"],
            "Link validation (broken-link-checker)",
            critical=False,
        )
        return result[0]

    finally:
        # Always stop the server
        if server_process:
            print(f"{Colors.BLUE}[*] Stopping local server...{Colors.END}")
            server_process.terminate()
            try:
                server_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                server_process.kill()
                server_process.wait()


def validate_language_style() -> bool:
    """Validate language and style with Vale"""
    # First sync Vale styles if needed
    vale_config = Path(".vale.ini")
    if vale_config.exists():
        print(f"{Colors.BLUE}[*] Syncing Vale styles...{Colors.END}")
        run_command(["vale", "sync"], "Vale styles sync", critical=False)

    # Find all Markdown files in docs/
    md_files = list(Path("docs").rglob("*.md"))
    if not md_files:
        print(f"{Colors.YELLOW}[!]  No Markdown files found for Vale validation.{Colors.END}")
        return True
    cmd = ["vale"] + [str(f) for f in md_files]
    return run_command(cmd, "Language and style validation (Vale)", critical=False)[0]


def run_openapi_validation() -> bool:
    """Run OpenAPI validation"""
    try:
        from prance import ResolvingParser  # type: ignore

        print(f"{Colors.BLUE}[*] OpenAPI specification validation...{Colors.END}")

        openapi_file = Path("openapi/api.yaml")
        if not openapi_file.exists():
            print(f"{Colors.RED}[-] OpenAPI specification validation - FAILED{Colors.END}")
            print(f"{Colors.RED}OpenAPI file not found: {openapi_file}{Colors.END}")
            return False

        try:
            parser = ResolvingParser(str(openapi_file))
            spec = parser.specification
            print(f"{Colors.GREEN}[+] OpenAPI specification validation - PASSED{Colors.END}")
            version = spec.get("openapi", "unknown") if spec else "unknown"
            print(f"{Colors.WHITE}Validated OpenAPI {version} specification{Colors.END}")
            return True
        except Exception as e:
            print(f"{Colors.RED}[-] OpenAPI specification validation - FAILED{Colors.END}")
            print(f"{Colors.RED}Validation error: {str(e)}{Colors.END}")
            return False

    except ImportError:
        print(f"{Colors.YELLOW}[!]  OpenAPI validation skipped - Prance not available{Colors.END}")
        return True  # Don't fail if Prance is not available


def main():
    """Main validation function"""
    parser = argparse.ArgumentParser(description="Documentation Validation Suite")
    parser.add_argument(
        "--skip-markdown", action="store_true", help="Skip markdown syntax validation"
    )
    parser.add_argument("--skip-mkdocs", action="store_true", help="Skip MkDocs build validation")
    parser.add_argument("--skip-links", action="store_true", help="Skip link validation")
    parser.add_argument("--skip-style", action="store_true", help="Skip language/style validation")
    parser.add_argument("--skip-openapi", action="store_true", help="Skip OpenAPI validation")
    parser.add_argument("--fast", action="store_true", help="Skip slow validations (links, style)")

    args = parser.parse_args()

    print(f"{Colors.BOLD}{Colors.CYAN}")
    print("=" * 70)
    print("DOCUMENTATION VALIDATION SUITE")
    print("=" * 70)
    print(f"{Colors.END}")

    results = []

    # 1. Markdown syntax validation
    if not args.skip_markdown:
        results.append(("Markdown Syntax", validate_markdown_syntax()))

    # 2. MkDocs build validation
    if not args.skip_mkdocs:
        results.append(("MkDocs Build", validate_mkdocs_build()))

    # 3. OpenAPI validation
    if not args.skip_openapi:
        results.append(("OpenAPI Validation", run_openapi_validation()))

    # 4. Link validation (can be slow)
    if not args.skip_links and not args.fast:
        results.append(("Link Validation", validate_links_site()))

    # 5. Language/style validation (can be slow)
    if not args.skip_style and not args.fast:
        results.append(("Language/Style", validate_language_style()))

    # Summary
    print(f"\n{Colors.BOLD}{Colors.CYAN}")
    print("=" * 70)
    print("VALIDATION SUMMARY")
    print("=" * 70)
    print(f"{Colors.END}")

    passed = 0
    failed = 0

    for check_name, success in results:
        if success:
            print(f"{Colors.GREEN}[+] {check_name.ljust(25)} PASSED{Colors.END}")
            passed += 1
        else:
            print(f"{Colors.RED}[-] {check_name.ljust(25)} FAILED{Colors.END}")
            failed += 1

    total = passed + failed
    if total > 0:
        success_rate = (passed / total) * 100
        print(
            f"\n{Colors.BOLD}[*] Success Rate: {success_rate:.1f}% ({passed}/{total}){Colors.END}"
        )

        if failed == 0:
            print(f"{Colors.GREEN}{Colors.BOLD}[+] All validations passed!{Colors.END}")
            return True
        else:
            print(f"{Colors.RED}{Colors.BOLD}[-] {failed} validation(s) failed{Colors.END}")
            return False
    else:
        print(f"{Colors.YELLOW}[!]  No validations were run{Colors.END}")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
