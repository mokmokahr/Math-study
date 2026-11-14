#!/usr/bin/env python3
"""Render Manim scenes and attach their MP4s to a GitHub issue."""

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path, help="Manim Python file")
    parser.add_argument("--issue", type=int, help="GitHub issue number")
    parser.add_argument("--dry-run", action="store_true", help="Render without uploading")
    args = parser.parse_args()
    source = args.file.expanduser().resolve()
    if not source.is_file() or source.suffix != ".py":
        parser.error(f"not a Python file: {source}")
    if not args.dry_run and not args.issue:
        parser.error("--issue is required unless --dry-run is used")

    output = ROOT / ".manim-output"
    output.mkdir(exist_ok=True)
    work = Path(tempfile.mkdtemp(dir=output, prefix=f"{source.stem}-"))
    subprocess.run(
        [
            sys.executable, "-m", "manimlib", str(source),
            "-a", "-l", "-w", "--video_dir", str(work),
        ],
        cwd=ROOT,
        check=True,
    )
    videos = sorted(work.rglob("*.mp4"))
    if not videos:
        parser.error("Manim finished without producing MP4 files")

    print("Rendered:")
    for video in videos:
        print(f"  {video}")
    if args.dry_run:
        return

    gh = shutil.which("gh")
    if not gh:
        parser.error("install GitHub CLI and run `gh auth login` first")
    repo = subprocess.check_output(
        [gh, "repo", "view", "--json", "nameWithOwner", "--jq", ".nameWithOwner"],
        cwd=ROOT,
        text=True,
    ).strip()
    subprocess.run([gh, "issue", "view", str(args.issue), "-R", repo], check=True)
    if input(f"Upload videos to {repo} issue #{args.issue}? [y/N] ").lower() not in ("y", "yes"):
        print("Cancelled; rendered files are kept in", work)
        return

    marker = f"manim-upload-{work.name}"
    body = f"Manim videos from `{source.name}`:\n\n" + "\n\n".join(
        f"![]({video.resolve()})" for video in videos
    ) + f"\n\n<!-- {marker} -->\n"
    subprocess.run(
        [
            gh, "issue", "comment", str(args.issue), "-R", repo,
            "--body-file", "-", *sum((["--attach", str(v)] for v in videos), []),
        ],
        input=body,
        text=True,
        check=True,
    )

    comments = subprocess.check_output(
        [
            gh, "api", "--paginate", "--jq",
            f'.[] | select(.body | contains("{marker}")) | [.html_url, .body] | @json',
            f"repos/{repo}/issues/{args.issue}/comments",
        ],
        text=True,
    ).splitlines()
    if not comments:
        raise RuntimeError("Uploaded comment, but could not retrieve its video links.")
    comment_url, comment = json.loads(comments[-1])
    links = re.findall(r"https://github\.com/user-attachments/assets/[^\s<>)\"]+", comment)
    print("Comment:", comment_url)
    for video, link in zip(videos, links):
        print(f"{video.stem}: {link}")
    print("Local videos:", work)


if __name__ == "__main__":
    try:
        main()
    except (OSError, subprocess.CalledProcessError, RuntimeError) as error:
        sys.exit(str(error))
