from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "SKILL.md"
README = ROOT / "README.md"
OPENAI_YAML = ROOT / "agents" / "openai.yaml"
WORKFLOW = ROOT / "references" / "workflow.md"
HOST_ROUTING = ROOT / "references" / "host-routing.md"
STATE_SCRIPT = ROOT / "scripts" / "project_state.py"

STAGES = (
    "START",
    "BRIEF",
    "BENCHMARKS",
    "WRITING_PACK",
    "SCRIPT",
    "VOICE",
    "STORYBOARD",
    "VISUAL_STYLE",
    "CHARACTER_ANCHORS",
    "IMAGE_PROMPTS",
    "IMAGE_GENERATION",
    "ASSET_QC",
    "MUSIC",
    "PREVIEW",
    "FINAL_RENDER",
    "FEEDBACK",
)


class ArticleAlignmentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.skill = SKILL.read_text(encoding="utf-8")
        cls.workflow = WORKFLOW.read_text(encoding="utf-8")
        cls.host_routing = HOST_ROUTING.read_text(encoding="utf-8")

    def test_required_public_files_exist(self) -> None:
        required = (
            "SKILL.md",
            "agents/openai.yaml",
            "assets/brief-template.md",
            "assets/handoff-template.md",
            "assets/storyboard-template.csv",
            "assets/writing-pack-manifest.md",
            "references/host-routing.md",
            "references/state-schema.md",
            "references/workflow.md",
            "scripts/project_state.py",
        )
        for relative in required:
            self.assertTrue((ROOT / relative).is_file(), relative)

    def test_guided_turn_contract_is_explicit(self) -> None:
        for label in (
            "现在进行到：",
            "我现在会做：",
            "你现在只需要：",
            "完成后我会交付：",
            "确认后下一步：",
        ):
            self.assertIn(label, self.skill)
        self.assertIn("Never dump the whole workflow", self.skill)
        self.assertIn("Ask only what blocks the current stage", self.skill)

    def test_skill_is_discoverable_after_install(self) -> None:
        frontmatter = self.skill.split("---", 2)[1]
        description = next(
            line.removeprefix("description: ")
            for line in frontmatter.splitlines()
            if line.startswith("description: ")
        )
        self.assertTrue(description.startswith("Use when "), description)

        openai_yaml = OPENAI_YAML.read_text(encoding="utf-8")
        self.assertIn("$image-story-video-wizard", openai_yaml)
        self.assertIn("主动分步引导", openai_yaml)

    def test_readme_has_one_message_install_route(self) -> None:
        readme = README.read_text(encoding="utf-8")
        self.assertIn("一句话安装", readme)
        self.assertIn("skill-installer", readme)
        self.assertIn(
            "https://github.com/aaronyi97/image-story-video-wizard", readme
        )
        self.assertIn("仓库根目录", readme)

    def test_every_stage_has_action_request_delivery_and_gate(self) -> None:
        for index, stage in enumerate(STAGES):
            start = self.workflow.index(f"## {stage}")
            end = (
                self.workflow.index(f"## {STAGES[index + 1]}")
                if index + 1 < len(STAGES)
                else len(self.workflow)
            )
            section = self.workflow[start:end]
            for marker in (
                "**Enter when:**",
                "**Skill acts:**",
                "**Ask now:**",
                "**Deliver:**",
                "**Gate:**",
            ):
                self.assertIn(marker, section, f"{stage} missing {marker}")

    def test_state_machine_matches_runtime(self) -> None:
        spec = importlib.util.spec_from_file_location("project_state", STATE_SCRIPT)
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.assertEqual(STAGES, module.STAGES)
        self.assertIn(" → ".join(STAGES), self.skill)

    def test_article_specific_guidance_is_present(self) -> None:
        self.assertIn("Kimi K3", self.host_routing)
        self.assertIn("Max", self.host_routing)
        self.assertIn("1M", self.host_routing)
        self.assertIn("official application", self.workflow)
        self.assertIn("one prompt and one image per fresh conversation", self.workflow)
        self.assertIn("7–15 days", self.workflow)
        self.assertIn("three to five stable, accepted scripts", self.workflow)

    def test_state_cli_initializes_and_validates(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            project = Path(temp_dir) / "sample"
            init = subprocess.run(
                [
                    sys.executable,
                    str(STATE_SCRIPT),
                    "init",
                    str(project),
                    "--title",
                    "Sample",
                    "--host",
                    "codex",
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(0, init.returncode, init.stderr)
            state_file = project / "PROJECT_STATE.json"
            state = json.loads(state_file.read_text(encoding="utf-8"))
            self.assertEqual("START", state["current_stage"])
            self.assertEqual("BRIEF", state["next_stage"])

            validate = subprocess.run(
                [sys.executable, str(STATE_SCRIPT), "validate", str(state_file)],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(0, validate.returncode, validate.stderr)
            self.assertEqual("VALID", validate.stdout.strip())

            overwrite = subprocess.run(
                [
                    sys.executable,
                    str(STATE_SCRIPT),
                    "init",
                    str(project),
                    "--title",
                    "Sample",
                    "--host",
                    "codex",
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(2, overwrite.returncode)


if __name__ == "__main__":
    unittest.main()
