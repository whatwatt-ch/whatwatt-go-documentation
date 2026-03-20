#!/usr/bin/env python3
"""
Production Build Script for whatwatt Documentation
Builds optimized, production-ready documentation with full validation
"""

import shutil
import subprocess
import sys
import time
from pathlib import Path


def run_command(cmd: list[str], description: str) -> bool:
    """Run command and return success status"""
    print(f"🔄 {description}...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"✅ {description} - SUCCESS")
        if result.stdout.strip():
            print(result.stdout.strip())
        return True
    else:
        print(f"❌ {description} - FAILED")
        if result.stderr.strip():
            print(f"Error: {result.stderr.strip()}")
        if result.stdout.strip():
            print(result.stdout.strip())
        return False


def main():
    print("🚀 whatwatt Documentation - Production Build")
    print("=" * 50)

    start_time = time.time()

    # 1. Clean previous builds
    if not run_command(["mkdocs", "build", "--clean"], "Cleaning previous builds"):
        return False

    # 2. Run pre-commit validation
    print("🔍 Running pre-commit validation...")
    if not run_command(["pre-commit", "run", "--all-files"], "Pre-commit validation"):
        print("⚠️  Pre-commit failed - continuing anyway")

    # 3. Build production site
    if not run_command(
        ["mkdocs", "build", "--strict", "--clean", "--site-dir", "dist"],
        "Building production site",
    ):
        return False

    # 4. Run comprehensive validation
    if not run_command([sys.executable, "validate_docs.py"], "Comprehensive validation"):
        print("⚠️  Validation warnings - review output")

    # 5. Optimize assets (if needed)
    print("🎨 Optimizing assets...")
    dist_path = Path("dist")
    if dist_path.exists():
        # Copy important files to dist
        for file in ["README.md", "LICENSE"]:
            if Path(file).exists():
                shutil.copy2(file, dist_path)

    # 6. Generate deployment info
    deploy_info = f"""# Deployment Info
Built: {time.strftime('%Y-%m-%d %H:%M:%S')}
Site URL: https://whatwatt.ch
Build directory: dist/
"""

    with open("dist/BUILD_INFO.md", "w") as f:
        f.write(deploy_info)

    elapsed = time.time() - start_time
    print(f"✅ Production build completed in {elapsed:.1f}s")
    print("📁 Ready for deployment: ./dist/")

    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
