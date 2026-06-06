#!/usr/bin/env python3
"""Create a new episode workspace from the repository template."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--id", required=True, dest="episode_id", help="例如 EP002")
    parser.add_argument("--slug", required=True, help="例如 sunk-cost")
    parser.add_argument("--concept", required=True, help="概念中文名")
    args = parser.parse_args()

    if not args.episode_id.startswith("EP") or not args.episode_id[2:].isdigit():
        parser.error("--id 必须形如 EP002")

    target = ROOT / "episodes" / f"{args.episode_id}-{args.slug}"
    if target.exists():
        parser.error(f"目录已存在：{target}")

    shutil.copytree(ROOT / "templates" / "episode", target)
    descriptions = {
        "images": "gpt-image-2 角色、场景与镜头参考帧",
        "video-clips": "通过 G4 的 Seedance 视频片段",
        "audio": "旁白、环境音和临时混音",
        "export": "剪映审片版与正式成片"
    }
    for name, description in descriptions.items():
        folder = target / name
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "README.md").write_text(
            f"# {name.title()}\n\n本目录用于存放{description}；大体积媒体默认不提交。\n",
            encoding="utf-8",
        )

    brief_path = target / "episode-brief.json"
    brief = json.loads(brief_path.read_text(encoding="utf-8"))
    brief["episode_id"] = args.episode_id
    brief["slug"] = args.slug
    brief["concept_name"] = args.concept
    brief["prompt_versions"]["seedance_video_package"] = "0.2.0"
    brief_path.write_text(json.dumps(brief, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(target.relative_to(ROOT))
    print("下一步：补全 episode-brief.json，并完成 G1 审核。")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
