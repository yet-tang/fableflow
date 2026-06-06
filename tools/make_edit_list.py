#!/usr/bin/env python3
"""Generate a Jianying assembly CSV from storyboard and asset manifest."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("episode_dir", type=Path)
    args = parser.parse_args()

    episode_dir = args.episode_dir.resolve()
    storyboard = json.loads((episode_dir / "storyboard.json").read_text(encoding="utf-8"))
    manifest = json.loads((episode_dir / "asset-manifest.json").read_text(encoding="utf-8"))
    asset_by_shot: dict[str, dict] = {}
    for asset in manifest["assets"]:
        for shot_id in asset["shot_ids"]:
            asset_by_shot[shot_id] = asset

    output = episode_dir / "edit-list.csv"
    fields = [
        "shot_id", "start_sec", "end_sec", "duration_sec", "asset", "asset_strategy",
        "camera_motion", "transition", "subtitle", "voiceover", "sound", "continuity"
    ]
    with output.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for shot in storyboard["shots"]:
            asset = asset_by_shot.get(shot["shot_id"], {})
            writer.writerow({
                "shot_id": shot["shot_id"],
                "start_sec": shot["start_sec"],
                "end_sec": shot["end_sec"],
                "duration_sec": shot["duration_sec"],
                "asset": asset.get("filename", ""),
                "asset_strategy": asset.get("strategy", shot["asset_strategy"]),
                "camera_motion": shot["camera_motion"],
                "transition": shot["transition"],
                "subtitle": shot["subtitle"],
                "voiceover": shot["voiceover"],
                "sound": shot["sound"],
                "continuity": shot["continuity"],
            })

    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
