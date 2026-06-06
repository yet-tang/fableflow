#!/usr/bin/env python3
"""Generate an SRT subtitle file from storyboard.json."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def timestamp(seconds: float) -> str:
    milliseconds = round(seconds * 1000)
    hours, milliseconds = divmod(milliseconds, 3_600_000)
    minutes, milliseconds = divmod(milliseconds, 60_000)
    secs, milliseconds = divmod(milliseconds, 1000)
    return f"{hours:02}:{minutes:02}:{secs:02},{milliseconds:03}"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("episode_dir", type=Path)
    args = parser.parse_args()

    episode_dir = args.episode_dir.resolve()
    storyboard = json.loads((episode_dir / "storyboard.json").read_text(encoding="utf-8"))
    blocks: list[str] = []
    index = 1
    for shot in storyboard["shots"]:
        text = shot.get("subtitle", "").strip()
        if not text:
            continue
        blocks.append(
            f"{index}\n{timestamp(float(shot['start_sec']))} --> {timestamp(float(shot['end_sec']))}\n{text}\n"
        )
        index += 1

    output = episode_dir / "subtitles.srt"
    output.write_text("\n".join(blocks), encoding="utf-8")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
