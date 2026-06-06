#!/usr/bin/env python3
"""Validate FableFlow structured artifacts against their JSON Schemas."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_BY_FILENAME = {
    "episode-brief.json": "episode-brief.schema.json",
    "concept-sheet.json": "concept-sheet.schema.json",
    "story-options.json": "story-options.schema.json",
    "decision.json": "decision.schema.json",
    "script.json": "script.schema.json",
    "storyboard.json": "storyboard.schema.json",
    "asset-manifest.json": "asset-manifest.schema.json",
    "publish-pack.json": "publish-pack.schema.json",
}


def load_json(path: Path) -> object:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"无法读取 JSON：{exc}") from exc


def iter_targets(scope: Path) -> list[Path]:
    if scope.is_file():
        return [scope]
    return sorted(
        path
        for path in scope.rglob("*.json")
        if path.name in SCHEMA_BY_FILENAME and "schemas" not in path.parts
    )


def validate_cross_file_rules(episode_dir: Path) -> list[str]:
    errors: list[str] = []
    storyboard_path = episode_dir / "storyboard.json"
    manifest_path = episode_dir / "asset-manifest.json"
    script_path = episode_dir / "script.json"

    if storyboard_path.exists():
        storyboard = load_json(storyboard_path)
        shots = storyboard.get("shots", [])  # type: ignore[union-attr]
        expected_start = 0.0
        duration_sum = 0.0
        seen_ids: set[str] = set()
        for shot in shots:
            shot_id = shot["shot_id"]
            if shot_id in seen_ids:
                errors.append(f"{storyboard_path}: 重复 shot_id {shot_id}")
            seen_ids.add(shot_id)
            if abs(float(shot["start_sec"]) - expected_start) > 0.01:
                errors.append(
                    f"{storyboard_path}: {shot_id} start_sec 应为 {expected_start:g}，实际为 {shot['start_sec']}"
                )
            computed = float(shot["end_sec"]) - float(shot["start_sec"])
            if abs(computed - float(shot["duration_sec"])) > 0.01:
                errors.append(f"{storyboard_path}: {shot_id} duration_sec 与起止时间不一致")
            expected_start = float(shot["end_sec"])
            duration_sum += float(shot["duration_sec"])
        if abs(duration_sum - float(storyboard["total_duration_sec"])) > 0.01:  # type: ignore[index]
            errors.append(f"{storyboard_path}: 镜头总时长与 total_duration_sec 不一致")

    if storyboard_path.exists() and manifest_path.exists():
        storyboard = load_json(storyboard_path)
        manifest = load_json(manifest_path)
        shot_ids = {s["shot_id"] for s in storyboard["shots"]}  # type: ignore[index]
        covered = {sid for a in manifest["assets"] for sid in a["shot_ids"]}  # type: ignore[index]
        missing = sorted(shot_ids - covered)
        unknown = sorted(covered - shot_ids)
        if missing:
            errors.append(f"{manifest_path}: 未覆盖镜头 {', '.join(missing)}")
        if unknown:
            errors.append(f"{manifest_path}: 引用了不存在的镜头 {', '.join(unknown)}")

    if script_path.exists():
        script = load_json(script_path)
        voiceover = script["full_voiceover"]  # type: ignore[index]
        concept_path = episode_dir / "episode-brief.json"
        if concept_path.exists():
            concept_name = load_json(concept_path)["concept_name"]  # type: ignore[index]
            first_index = voiceover.find(concept_name)
            declared = int(script["reveal_first_character_index"])  # type: ignore[index]
            if first_index != declared:
                errors.append(
                    f"{script_path}: reveal_first_character_index={declared}，实际首次出现位置={first_index}"
                )

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("scope", nargs="?", default=str(ROOT), help="文件或目录，默认整个仓库")
    args = parser.parse_args()
    scope = Path(args.scope).resolve()

    targets = iter_targets(scope)
    if not targets:
        print("未找到可校验的 FableFlow JSON 资产。")
        return 1

    schema_cache: dict[str, object] = {}
    errors: list[str] = []
    for target in targets:
        schema_name = SCHEMA_BY_FILENAME[target.name]
        schema = schema_cache.setdefault(schema_name, load_json(ROOT / "schemas" / schema_name))
        try:
            instance = load_json(target)
        except ValueError as exc:
            errors.append(f"{target}: {exc}")
            continue
        validator = Draft202012Validator(schema, format_checker=FormatChecker())
        for error in sorted(validator.iter_errors(instance), key=lambda e: list(e.path)):
            location = ".".join(str(x) for x in error.absolute_path) or "<root>"
            errors.append(f"{target.relative_to(ROOT)} [{location}]: {error.message}")

    episode_dirs = sorted({p.parent for p in targets if "episodes" in p.parts})
    for episode_dir in episode_dirs:
        errors.extend(validate_cross_file_rules(episode_dir))

    if errors:
        print("校验失败：")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"校验通过：{len(targets)} 个结构化资产。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
