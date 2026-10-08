"""Regression tests for the default Plan 5 tail-lineart static prompt contract."""

import contextlib
import copy
import io
import json
from pathlib import Path
import tempfile
import unittest

from validate_tailchain_prompts import main, validate_tailchain_data


HEADINGS = (
    "subject_definitions:",
    "summary:",
    "retention_analysis:",
    "detailed_description:",
    "overall_soundscape:",
    "non_diegetic_music:",
)


def prompt(index: int) -> str:
    picture3 = "" if index == 1 else "\n<Picture 3> is the previous accepted tail-lineart opening geometry reference."
    return (
        "subject_definitions:\n"
        "<Subject 1> comes from <Picture 1>.\n"
        f"<Subject 2> comes from <Picture 2>.{picture3}\n\n"
        "summary:\n[reference generation] Synthetic test prompt.\n\n"
        "retention_analysis:\nSynthetic retention.\n\n"
        "detailed_description:\n"
        "Continuity State Lock:\n"
        "Wardrobe/Body State: synthetic known state.\n"
        "Color/Material State: synthetic stable palette.\n"
        "Lighting/Exposure State: synthetic stable lighting.\n"
        "[Shot 1] Synthetic visible action.\n\n"
        "overall_soundscape:\nSynthetic room tone.\n\n"
        "non_diegetic_music:\nN/A"
    )


def story(count: int = 3):
    return {
        "global_prompt": "",
        "segments": [
            {"id": i, "title": f"segment {i}", "raw_prompt": True, "prompt": prompt(i)}
            for i in range(1, count + 1)
        ],
    }


class TailchainPromptContractTests(unittest.TestCase):
    def test_accepts_valid_default_profile(self):
        data = story(4)
        before = copy.deepcopy(data)
        self.assertEqual(validate_tailchain_data(data), 4)
        self.assertEqual(data, before)

    def test_segment_one_must_not_mention_picture3(self):
        data = story()
        data["segments"][0]["prompt"] += "\n<Picture 3>"
        with self.assertRaises(ValueError):
            validate_tailchain_data(data)

    def test_continuations_require_picture3(self):
        data = story()
        data["segments"][1]["prompt"] = data["segments"][1]["prompt"].replace(
            "\n<Picture 3> is the previous accepted tail-lineart opening geometry reference.", ""
        )
        with self.assertRaises(ValueError):
            validate_tailchain_data(data)

    def test_every_segment_requires_both_identity_pictures(self):
        for reference in ("<Picture 1>", "<Picture 2>"):
            data = story()
            data["segments"][1]["prompt"] = data["segments"][1]["prompt"].replace(reference, "<Missing>")
            with self.subTest(reference=reference), self.assertRaises(ValueError):
                validate_tailchain_data(data)

    def test_default_plan5_rejects_video1(self):
        data = story()
        data["segments"][2]["prompt"] += "\n<Video 1>"
        with self.assertRaises(ValueError):
            validate_tailchain_data(data)

    def test_every_segment_requires_one_state_lock_before_shot1(self):
        data = story()
        data["segments"][1]["prompt"] = data["segments"][1]["prompt"].replace(
            "Continuity State Lock:\n", "", 1
        )
        with self.assertRaises(ValueError):
            validate_tailchain_data(data)

        data = story()
        data["segments"][1]["prompt"] += "\nContinuity State Lock:"
        with self.assertRaises(ValueError):
            validate_tailchain_data(data)

        data = story()
        prompt_text = data["segments"][1]["prompt"]
        prompt_text = prompt_text.replace("Continuity State Lock:\n", "", 1)
        prompt_text += "\nContinuity State Lock:"
        data["segments"][1]["prompt"] = prompt_text
        with self.assertRaises(ValueError):
            validate_tailchain_data(data)

    def test_six_headings_are_exact_and_ordered(self):
        data = story()
        data["segments"][1]["prompt"] += "\nsummary:"
        with self.assertRaises(ValueError):
            validate_tailchain_data(data)

        data = story()
        text = data["segments"][1]["prompt"]
        a = text.index("summary:")
        b = text.index("retention_analysis:")
        before_summary = text[:a]
        summary_block = text[a:b]
        retention_block = text[b:text.index("detailed_description:")]
        rest = text[text.index("detailed_description:"):]
        data["segments"][1]["prompt"] = before_summary + retention_block + summary_block + rest
        with self.assertRaises(ValueError):
            validate_tailchain_data(data)

    def run_cli(self, text: str):
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", suffix=".json", delete=False) as f:
            f.write(text)
            path = Path(f.name)
        try:
            out, err = io.StringIO(), io.StringIO()
            with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
                code = main([str(path)])
            self.assertEqual(path.read_bytes(), text.encode("utf-8"))
            return code, out.getvalue() + err.getvalue()
        finally:
            path.unlink()

    def test_cli_is_read_only_and_never_echoes_prompt(self):
        data = story()
        data["segments"][1]["prompt"] += "\nPRIVATE_SENTINEL <Video 1>"
        code, output = self.run_cli(json.dumps(data, ensure_ascii=False))
        self.assertEqual(code, 1)
        self.assertNotIn("PRIVATE_SENTINEL", output)

        code, output = self.run_cli(json.dumps(story(), ensure_ascii=False))
        self.assertEqual(code, 0)
        self.assertIn("static_prompt_contract=true", output)
        self.assertIn("semantic_continuity_validated=false", output)


if __name__ == "__main__":
    unittest.main()
