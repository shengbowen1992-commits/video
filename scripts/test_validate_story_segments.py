"""Behavioral checks for the output envelope, using synthetic opaque prompts only."""

import contextlib
import copy
import io
import json
from pathlib import Path
import tempfile
import unittest

from validate_story_segments import main, validate_data


def story(count=4):
    return {"global_prompt": "", "segments": [
        {"id": i, "title": f"segment {i}", "raw_prompt": True,
         "prompt": 'opaque text: 中文 "quoted" \\ path\n<Picture 2> <Video 1>'}
        for i in range(1, count + 1)
    ]}


class EnvelopeTests(unittest.TestCase):
    def test_counts_are_dynamic(self):
        for count in (1, 4, 6, 40):
            with self.subTest(count=count):
                self.assertEqual(validate_data(story(count)), count)

    def test_validation_and_json_roundtrip_preserve_opaque_text(self):
        original = story()
        saved = json.loads(json.dumps(original, ensure_ascii=False))
        before = copy.deepcopy(saved)
        validate_data(saved)
        self.assertEqual(saved, before)
        self.assertEqual(saved, original)

    def test_rejects_invalid_roots(self):
        for data in (None, [], {}, {"version": 3, "sets": []},
                     {"global_prompt": "", "segments": []},
                     {"global_prompt": "", "segments": "not an array"}):
            with self.subTest(data_type=type(data).__name__), self.assertRaises(ValueError):
                validate_data(data)

    def test_rejects_ignored_global_rules_and_runtime_fields(self):
        for field, value in (("global_prompt", "not used by raw mode"), ("width", 576)):
            data = story()
            data[field] = value
            with self.subTest(field=field), self.assertRaises(ValueError):
                validate_data(data)

    def test_rejects_nonconsecutive_and_noninteger_ids(self):
        for value in (0, 2, "1", True, 1.0):
            data = story()
            data["segments"][0]["id"] = value
            with self.subTest(value=value), self.assertRaises(ValueError):
                validate_data(data)
        data = story()
        data["segments"][1]["id"] = 1
        with self.assertRaises(ValueError):
            validate_data(data)

    def test_rejects_nontrue_raw_mode(self):
        for value in (False, "true", 1, None):
            data = story()
            data["segments"][0]["raw_prompt"] = value
            with self.subTest(value=value), self.assertRaises(ValueError):
                validate_data(data)

    def test_requires_nonempty_text_fields(self):
        for field in ("title", "prompt"):
            for value in (None, {}, 3, "", " \n\t"):
                data = story()
                data["segments"][0][field] = value
                with self.subTest(field=field, value=value), self.assertRaises(ValueError):
                    validate_data(data)

    def test_rejects_missing_and_extra_segment_fields(self):
        data = story()
        del data["segments"][0]["prompt"]
        with self.assertRaises(ValueError):
            validate_data(data)
        for field in ("prompt_en", "duration_seconds", "subject_definitions"):
            data = story()
            data["segments"][0][field] = "not a supported outer field"
            with self.subTest(field=field), self.assertRaises(ValueError):
                validate_data(data)

    def test_optional_seed_bounds(self):
        for value in (0, 2**63 - 1):
            data = story()
            data["segments"][0]["seed"] = value
            self.assertEqual(validate_data(data), 4)
        for value in (-1, 2**63, True, 1.0, "1"):
            data = story()
            data["segments"][0]["seed"] = value
            with self.subTest(value=value), self.assertRaises(ValueError):
                validate_data(data)

    def run_cli(self, text):
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

    def test_cli_is_read_only_and_does_not_print_prompt(self):
        code, output = self.run_cli("\ufeff" + json.dumps(story(6)))
        self.assertEqual(code, 0)
        self.assertIn("segments=6", output)
        self.assertIn("prompt_content_validated=false", output)
        self.assertNotIn("opaque text", output)

    def test_invalid_json_never_echoes_input(self):
        for text in ('{"PRIVATE_SENTINEL": ', '{"global_prompt":"","segments":NaN}',
                     '{"global_prompt":"","global_prompt":"PRIVATE_SENTINEL","segments":[]}'):
            code, output = self.run_cli(text)
            self.assertEqual(code, 1)
            self.assertNotIn("PRIVATE_SENTINEL", output)


if __name__ == "__main__":
    unittest.main()
