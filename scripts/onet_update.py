# /// script
# requires-python = ">=3.10"
# dependencies = ["requests"]
# ///
"""
O*NET Database Update Tool

Check for new O*NET database releases and download updated Excel files.
Tracks the current version in references/.version.

Usage:
    uv run scripts/onet_update.py              # Check + download if newer
    uv run scripts/onet_update.py --check      # Check only, don't download
    uv run scripts/onet_update.py --force       # Re-download current version
    uv run scripts/onet_update.py --version     # Show current local version
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
import time
import xml.etree.ElementTree as ET
from pathlib import Path

import requests

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

REFERENCES_DIR = Path(__file__).resolve().parent.parent / "references"
VERSION_FILE = REFERENCES_DIR / ".version"

RSS_URL = "https://www.onetcenter.org/rss/whatsnew.xml"
DATABASE_PAGE_URL = "https://www.onetcenter.org/database.html"
DOWNLOAD_BASE = "https://www.onetcenter.org/dl_files/database"

# All 40 Excel files in the O*NET database release.
DATABASE_FILES = [
    "Abilities to Work Activities.xlsx",
    "Abilities to Work Context.xlsx",
    "Abilities.xlsx",
    "Alternate Titles.xlsx",
    "Basic Interests to RIASEC.xlsx",
    "Content Model Reference.xlsx",
    "DWA Reference.xlsx",
    "Education, Training, and Experience Categories.xlsx",
    "Education, Training, and Experience.xlsx",
    "Emerging Tasks.xlsx",
    "IWA Reference.xlsx",
    "Interests Illustrative Activities.xlsx",
    "Interests Illustrative Occupations.xlsx",
    "Interests.xlsx",
    "Job Zone Reference.xlsx",
    "Job Zones.xlsx",
    "Knowledge.xlsx",
    "Level Scale Anchors.xlsx",
    "Occupation Data.xlsx",
    "Occupation Level Metadata.xlsx",
    "RIASEC Keywords.xlsx",
    "Related Occupations.xlsx",
    "Sample of Reported Titles.xlsx",
    "Scales Reference.xlsx",
    "Skills to Work Activities.xlsx",
    "Skills to Work Context.xlsx",
    "Skills.xlsx",
    "Survey Booklet Locations.xlsx",
    "Task Categories.xlsx",
    "Task Ratings.xlsx",
    "Task Statements.xlsx",
    "Tasks to DWAs.xlsx",
    "Technology Skills.xlsx",
    "Tools Used.xlsx",
    "UNSPSC Reference.xlsx",
    "Work Activities.xlsx",
    "Work Context Categories.xlsx",
    "Work Context.xlsx",
    "Work Styles.xlsx",
    "Work Values.xlsx",
]

SESSION = requests.Session()
SESSION.headers.update({"User-Agent": "onet-skill-updater/1.0"})


# ---------------------------------------------------------------------------
# Version detection
# ---------------------------------------------------------------------------

def _version_to_path_segment(version: str) -> str:
    """Convert '30.2' to 'db_30_2'."""
    return "db_" + version.replace(".", "_")


def get_local_version() -> str | None:
    """Read the locally stored version from references/.version."""
    if VERSION_FILE.exists():
        text = VERSION_FILE.read_text().strip()
        return text if text else None
    return None


def _set_local_version(version: str) -> None:
    """Write the version to references/.version."""
    VERSION_FILE.write_text(version + "\n")


def detect_latest_version_rss() -> str | None:
    """Detect latest O*NET database version from the What's New RSS feed."""
    try:
        resp = SESSION.get(RSS_URL, timeout=15)
        resp.raise_for_status()
    except requests.RequestException as exc:
        print(f"  Warning: RSS feed unavailable ({exc})", file=sys.stderr)
        return None

    try:
        root = ET.fromstring(resp.content)
    except ET.ParseError:
        return None

    # Look through items for a database release announcement.
    for item in root.findall("./channel/item"):
        title_el = item.find("title")
        desc_el = item.find("description")
        text = ""
        if title_el is not None and title_el.text:
            text += title_el.text
        if desc_el is not None and desc_el.text:
            text += " " + desc_el.text

        match = re.search(r"O\*?NET\s+(\d+\.\d+)\s+Database", text)
        if match:
            return match.group(1)

    return None


def detect_latest_version_page() -> str | None:
    """Detect latest version by scraping the database page header."""
    try:
        resp = SESSION.get(DATABASE_PAGE_URL, timeout=15)
        resp.raise_for_status()
    except requests.RequestException as exc:
        print(f"  Warning: Database page unavailable ({exc})", file=sys.stderr)
        return None

    match = re.search(r"O\*?NET\s+(\d+\.\d+)\s+Database", resp.text)
    if match:
        return match.group(1)
    return None


def detect_latest_version() -> str | None:
    """Detect the latest available O*NET database version.

    Tries RSS first (lightweight), falls back to page scraping.
    """
    print("Checking for latest O*NET database version...")

    version = detect_latest_version_rss()
    if version:
        print(f"  Found version {version} via RSS feed")
        return version

    version = detect_latest_version_page()
    if version:
        print(f"  Found version {version} via database page")
        return version

    print("  Error: Could not detect latest version from any source", file=sys.stderr)
    return None


# ---------------------------------------------------------------------------
# Download
# ---------------------------------------------------------------------------

def _download_url(version: str, filename: str) -> str:
    """Build the download URL for a specific file and version."""
    segment = _version_to_path_segment(version)
    # URL-encode spaces as %20 for the filename
    encoded = filename.replace(" ", "%20")
    return f"{DOWNLOAD_BASE}/{segment}_excel/{encoded}"


def download_file(version: str, filename: str) -> bool:
    """Download a single file. Returns True on success."""
    url = _download_url(version, filename)
    dest = REFERENCES_DIR / filename

    try:
        resp = SESSION.get(url, timeout=60, stream=True)
        resp.raise_for_status()
    except requests.RequestException as exc:
        print(f"  FAILED: {filename} ({exc})", file=sys.stderr)
        return False

    # Write to a temp file first, then rename for atomicity.
    tmp = dest.with_suffix(".tmp")
    try:
        with open(tmp, "wb") as f:
            for chunk in resp.iter_content(chunk_size=65536):
                f.write(chunk)
        tmp.rename(dest)
        return True
    except OSError as exc:
        print(f"  FAILED to write {filename}: {exc}", file=sys.stderr)
        if tmp.exists():
            tmp.unlink()
        return False


def download_all(version: str) -> tuple[int, int]:
    """Download all database files for a given version.

    Returns (success_count, failure_count).
    """
    REFERENCES_DIR.mkdir(parents=True, exist_ok=True)

    total = len(DATABASE_FILES)
    success = 0
    failed = 0

    for i, filename in enumerate(DATABASE_FILES, 1):
        pct = i * 100 // total
        print(f"  [{pct:3d}%] Downloading {filename}...", end="", flush=True)

        if download_file(version, filename):
            print(" OK")
            success += 1
        else:
            print(" FAILED")
            failed += 1

        # Be polite to the server.
        if i < total:
            time.sleep(0.2)

    return success, failed


# ---------------------------------------------------------------------------
# Database rebuild
# ---------------------------------------------------------------------------

BUILD_SCRIPT = Path(__file__).resolve().parent / "onet_build_db.py"


def _rebuild_database() -> None:
    """Rebuild the SQLite database from downloaded Excel files."""
    if not BUILD_SCRIPT.exists():
        print(
            f"  Warning: Build script not found at {BUILD_SCRIPT}. "
            f"Run manually: uv run scripts/onet_build_db.py",
            file=sys.stderr,
        )
        return

    print("\nRebuilding SQLite database...")
    result = subprocess.run(
        ["uv", "run", str(BUILD_SCRIPT)],
        cwd=str(BUILD_SCRIPT.parent.parent),
    )
    if result.returncode != 0:
        print(
            "  Warning: Database rebuild failed. "
            "Run manually: uv run scripts/onet_build_db.py",
            file=sys.stderr,
        )
    else:
        print("Database rebuild complete.")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Check for and download O*NET database updates.",
        epilog="Examples:\n"
        "  uv run scripts/onet_update.py              # Update to latest\n"
        "  uv run scripts/onet_update.py --check       # Check only\n"
        "  uv run scripts/onet_update.py --force        # Re-download\n"
        "  uv run scripts/onet_update.py --version      # Show local version\n",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check for updates without downloading",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Re-download even if already at latest version",
    )
    parser.add_argument(
        "--version",
        action="store_true",
        dest="show_version",
        help="Show current local database version and exit",
    )
    parser.add_argument(
        "--set-version",
        metavar="VER",
        help="Manually set the local version (e.g., after a manual download)",
    )

    args = parser.parse_args()

    # --- Show version ---
    if args.show_version:
        local = get_local_version()
        if local:
            print(f"O*NET database version: {local}")
        else:
            print("No version file found. Run an update first.")
        sys.exit(0)

    # --- Set version manually ---
    if args.set_version:
        if not re.match(r"^\d+\.\d+$", args.set_version):
            print(f"Error: Invalid version format '{args.set_version}'. Expected X.Y (e.g., 30.2)",
                  file=sys.stderr)
            sys.exit(1)
        _set_local_version(args.set_version)
        print(f"Local version set to {args.set_version}")
        sys.exit(0)

    # --- Check / Update ---
    local = get_local_version()
    if local:
        print(f"Current local version: {local}")
    else:
        print("No local version found (first run)")

    latest = detect_latest_version()
    if not latest:
        sys.exit(1)

    if local == latest and not args.force:
        print(f"\nAlready up to date (version {latest}). Use --force to re-download.")
        sys.exit(0)

    if local and local != latest:
        print(f"\nNew version available: {latest} (current: {local})")
    elif args.force:
        print(f"\nForce re-downloading version {latest}...")

    if args.check:
        print("Run without --check to download.")
        sys.exit(0)

    # --- Download ---
    print(f"\nDownloading O*NET {latest} database ({len(DATABASE_FILES)} files)...")
    print()

    success, failed = download_all(latest)
    print()

    if failed == 0:
        _set_local_version(latest)
        print(f"Update complete. Version: {latest}")
        print(f"  {success} files downloaded to {REFERENCES_DIR}/")
        _rebuild_database()
    else:
        print(f"Update finished with errors: {success} OK, {failed} failed.", file=sys.stderr)
        print("Version file NOT updated due to failures. Re-run to retry.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
