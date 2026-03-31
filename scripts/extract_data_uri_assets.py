import argparse
import base64
import json
import sys
from pathlib import Path
from urllib.parse import unquote_to_bytes

DEFAULT_TEMPLATE = {
    "editor.svg": "",
    "icon-run.svg": "",
    "icon-stop.svg": "",
    "icon-load.svg": "",
    "icon-save.svg": "",
    "icon-open.svg": "",
    "icon-clear-console.svg": "",
}

MIME_EXTENSIONS = {
    "image/svg+xml": ".svg",
    "image/png": ".png",
    "image/jpeg": ".jpg",
    "image/webp": ".webp",
    "image/gif": ".gif",
}


def parse_data_uri(data_uri: str) -> tuple[str, bytes]:
    if not data_uri.startswith("data:"):
        raise ValueError("Value must start with 'data:'")

    header, _, payload = data_uri.partition(",")
    if not _:
        raise ValueError("Data URI must contain a comma separating metadata and payload")

    metadata = header[5:]
    parts = metadata.split(";") if metadata else []
    mime_type = parts[0] if parts and "/" in parts[0] else "text/plain"
    is_base64 = "base64" in parts[1:]

    if is_base64:
        return mime_type, base64.b64decode(payload)

    return mime_type, unquote_to_bytes(payload)


def choose_output_name(name: str, mime_type: str) -> str:
    path = Path(name)
    if path.suffix:
        return name

    extension = MIME_EXTENSIONS.get(mime_type)
    if extension is None:
        raise ValueError(f"Cannot infer file extension for MIME type: {mime_type}")
    return f"{name}{extension}"


def write_template(template_path: Path) -> None:
    template_path.parent.mkdir(parents=True, exist_ok=True)
    template_path.write_text(json.dumps(DEFAULT_TEMPLATE, indent=2) + "\n", encoding="utf-8")


def load_manifest(manifest_path: Path) -> dict[str, str]:
    with manifest_path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)

    if not isinstance(data, dict):
        raise ValueError("Manifest must be a JSON object mapping output file names to data URIs")

    manifest: dict[str, str] = {}
    for name, value in data.items():
        if not isinstance(name, str) or not name:
            raise ValueError("Manifest keys must be non-empty strings")
        if not isinstance(value, str):
            raise ValueError(f"Manifest value for '{name}' must be a string")
        manifest[name] = value.strip()
    return manifest


def extract_assets(manifest: dict[str, str], output_dir: Path) -> int:
    output_dir.mkdir(parents=True, exist_ok=True)
    created = 0

    for requested_name, data_uri in manifest.items():
        if not data_uri:
            print(f"Skipping {requested_name}: empty value", flush=True)
            continue

        mime_type, content = parse_data_uri(data_uri)
        output_name = choose_output_name(requested_name, mime_type)
        output_path = output_dir / output_name
        output_path.write_bytes(content)
        created += 1
        print(f"Wrote {output_path} ({mime_type})", flush=True)

    return created


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Decode data URI image assets from a JSON manifest into regular files."
    )
    parser.add_argument(
        "manifest",
        nargs="?",
        default="scripts/berry_icons.template.json",
        help="Path to JSON manifest mapping output file names to data URIs",
    )
    parser.add_argument(
        "--output-dir",
        default="docs/55-berry/img",
        help="Directory where decoded files will be written",
    )
    parser.add_argument(
        "--write-template",
        action="store_true",
        help="Write the default Berry icon manifest template and exit",
    )
    args = parser.parse_args()

    manifest_path = Path(args.manifest)
    output_dir = Path(args.output_dir)

    if args.write_template:
        write_template(manifest_path)
        print(f"Template written to {manifest_path.resolve()}", flush=True)
        return 0

    if not manifest_path.exists():
        print(
            f"Manifest not found: {manifest_path}. Run with --write-template first.",
            file=sys.stderr,
            flush=True,
        )
        return 1

    try:
        manifest = load_manifest(manifest_path)
        created = extract_assets(manifest, output_dir)
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr, flush=True)
        return 1

    if created == 0:
        print("No files were created. Fill the manifest with data URIs and try again.", flush=True)
        return 1

    print(f"Created {created} file(s) in {output_dir.resolve()}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
