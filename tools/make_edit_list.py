#!/usr/bin/env python3
"""Generate a Jianying assembly CSV from storyboard, image and video manifests."""

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
    image_manifest = json.loads((episode_dir / "asset-manifest.json").read_text(encoding="utf-8"))
    video_path = episode_dir / "video-manifest.json"
    video_manifest = json.loads(video_path.read_text(encoding="utf-8")) if video_path.exists() else {"clips": []}

    image_by_shot: dict[str, dict] = {}
    for asset in image_manifest["assets"]:
        for shot_id in asset["shot_ids"]:
            image_by_shot[shot_id] = asset

    clip_by_shot: dict[str, dict] = {}
    for clip in video_manifest["clips"]:
        for shot_id in clip["shot_ids"]:
            clip_by_shot[shot_id] = clip

    output = episode_dir / "edit-list.csv"
    fields = [
        "shot_id", "start_sec", "end_sec", "duration_sec", "video_clip", "video_mode",
        "reference_image", "camera_motion", "transition", "subtitle", "voiceover", "sound",
        "native_audio_policy", "edit_instruction", "continuity"
    ]
    with output.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for shot in storyboard["shots"]:
            image = image_by_shot.get(shot["shot_id"], {})
            clip = clip_by_shot.get(shot["shot_id"], {})
            writer.writerow({
                "shot_id": shot["shot_id"],
                "start_sec": shot["start_sec"],
                "end_sec": shot["end_sec"],
                "duration_sec": shot["duration_sec"],
                "video_clip": clip.get("filename", ""),
                "video_mode": clip.get("mode", "still_fallback"),
                "reference_image": image.get("filename", ""),
                "camera_motion": shot["camera_motion"],
                "transition": shot["transition"],
                "subtitle": shot["subtitle"],
                "voiceover": shot["voiceover"],
                "sound": shot["sound"],
                "native_audio_policy": clip.get("audio_mode", "silent"),
                "edit_instruction": clip.get("edit_instruction", "使用参考图做静帧微动。"),
                "continuity": shot["continuity"],
            })

    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
