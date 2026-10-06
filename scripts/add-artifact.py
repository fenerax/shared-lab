"""Import one explicitly selected standalone HTML artifact and rebuild the index."""
from __future__ import annotations

import argparse
from datetime import date
from html import escape
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"


def build_index(projects: list[dict]) -> None:
    rows = []
    for project in sorted(projects, key=lambda p: p["updated"], reverse=True):
        stamp = date.fromisoformat(project["updated"])
        label = f"Updated {stamp.day} {stamp.strftime('%B %Y')}"
        rows.append(
            '<li class="project"><a href="' + escape(project["slug"], quote=True) + '/">'
            '<span><span class="project-title">' + escape(project["title"]) + '</span>'
            '<span class="description">' + escape(project["description"]) + '</span></span>'
            '<time datetime="' + stamp.isoformat() + '">' + label + '</time></a></li>'
        )
    if not rows:
        rows.append('<li class="project"><p>No projects have been published yet.</p></li>')
    template = (ROOT / "templates/index.html").read_text(encoding="utf-8")
    (DOCS / "index.html").write_text(template.replace("{{PROJECTS}}", "\n".join(rows)), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("html", type=Path, help="self-contained, standalone HTML file to publish")
    parser.add_argument("--slug", required=True, help="URL path, e.g. rs3/revenants")
    parser.add_argument("--title", required=True)
    parser.add_argument("--description", required=True)
    parser.add_argument("--updated", default=date.today().isoformat())
    parser.add_argument("--notes", type=Path, help="optional trusted HTML footer")
    parser.add_argument("--replace", action="store_true")
    args = parser.parse_args()
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*(?:/[a-z0-9]+(?:-[a-z0-9]+)*)*", args.slug):
        parser.error("slug must contain lowercase URL-safe path segments")
    if args.html.is_symlink() or not args.html.is_file():
        parser.error("source must be a regular file")
    document = args.html.read_text(encoding="utf-8")
    if not re.search(r"<html\b", document, re.I) or not re.search(r"<body\b[^>]*>", document, re.I):
        parser.error("export the fragment as a full standalone HTML document first")
    date.fromisoformat(args.updated)
    if not re.search(r'rel=["\']icon["\']', document, re.I):
        document = re.sub(r"</head\s*>", lambda _: '<link rel="icon" href="data:,">\n</head>', document, count=1, flags=re.I)
    destination = DOCS / args.slug / "index.html"
    if destination.exists() and not args.replace:
        parser.error("project already exists; use --replace to update it")
    home = "../" * len(args.slug.split("/"))
    chrome = (ROOT / "templates/project-chrome.html").read_text(encoding="utf-8").replace("{{HOME}}", home)
    document = re.sub(r"(<body\b[^>]*>)", lambda match: match.group(1) + "\n" + chrome, document, count=1, flags=re.I)
    if args.notes:
        notes = args.notes.read_text(encoding="utf-8")
        document = re.sub(r"</body\s*>", lambda _: notes + "\n</body>", document, count=1, flags=re.I)
    projects = json.loads((ROOT / "projects.json").read_text(encoding="utf-8"))
    projects = [project for project in projects if project["slug"] != args.slug]
    projects.append(dict(slug=args.slug, title=args.title, description=args.description, updated=args.updated))
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(document, encoding="utf-8")
    (ROOT / "projects.json").write_text(json.dumps(projects, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    build_index(projects)
    print(f"Imported {args.slug}; review docs/ before pushing to publish.")


if __name__ == "__main__":
    main()
