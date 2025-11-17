import argparse
import subprocess
import sys
from pathlib import Path


def build_site() -> None:
    print("Building MkDocs site (strict)...", flush=True)
    subprocess.run(["mkdocs", "build", "--strict"], check=True)


def find_print_html(site_dir: Path) -> Path:
    candidates = [
        site_dir / "print" / "index.html",
        site_dir / "print" / "print.html",
        site_dir / "print" / "site.html",
        site_dir / "print_page" / "index.html",
        site_dir / "print.html",
    ]
    for p in candidates:
        if p.exists():
            return p
    raise FileNotFoundError("Printable HTML not found (checked site/print/ and site/print_page/).")


def ensure_playwright_browser() -> None:
    try:
        # Check playwright import first
        import playwright  # noqa: F401

        # Try to launch to see if browsers are installed
        from playwright.sync_api import sync_playwright

        with sync_playwright() as p:
            # If Chromium is not installed, this will throw
            p.chromium.launch(headless=True).close()
    except Exception:
        print("Installing Playwright Chromium (one-time step)...", flush=True)
        subprocess.run([sys.executable, "-m", "playwright", "install", "chromium"], check=True)


def export_pdf(print_html: Path, output_pdf: Path) -> None:
    from playwright.sync_api import sync_playwright

    file_url = print_html.resolve().as_uri()
    print(f"Exporting print page to PDF via Playwright: {output_pdf}")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        # Load local file and wait for network quiet; give JS time to render diagrams
        page.goto(file_url, wait_until="load")
        page.wait_for_load_state("networkidle")
        # Allow extra time for Mermaid/rendered components if needed
        page.wait_for_timeout(3000)
        page.pdf(
            path=str(output_pdf),
            format="A4",
            print_background=True,
            margin={"top": "12mm", "right": "12mm", "bottom": "16mm", "left": "12mm"},
        )
        browser.close()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Export MkDocs site to a single PDF without a system browser."
    )
    parser.add_argument(
        "--output", "-o", default="whatwatt-go-documentation.pdf", help="Output PDF path"
    )
    parser.add_argument("--site-dir", default="site", help="Built site directory (default: site)")
    args = parser.parse_args()

    site_dir = Path(args.site_dir)
    output_pdf = Path(args.output)

    build_site()
    print_html = find_print_html(site_dir)
    ensure_playwright_browser()
    export_pdf(print_html, output_pdf)
    print(f"PDF generated: {output_pdf.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
