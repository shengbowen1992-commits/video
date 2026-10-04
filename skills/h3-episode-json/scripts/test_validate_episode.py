"""Behavioral checks using neutral synthetic examples; no ComfyUI or network needed."""
import copy
import io
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
from validate_episode import validate


SKILL = Path(__file__).resolve().parents[1]
EXAMPLE = json.loads((SKILL / 'assets' / 'episode.example.json').read_text(encoding='utf-8'))


class EpisodeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / 'episode.json'

    def save(self, data):
        self.path.write_text(json.dumps(data, ensure_ascii=False), encoding='utf-8')

    def test_complete_skill_works_in_isolation_with_standard_library_only(self):
        isolated = Path(self.temp.name) / 'h3-episode-json'
        shutil.copytree(SKILL, isolated, ignore=shutil.ignore_patterns('__pycache__'))
        result = subprocess.run([sys.executable, '-I', '-S', '-X', 'utf8',
                                 str(isolated / 'scripts' / 'validate_episode.py'),
                                 str(isolated / 'assets' / 'episode.example.json')],
                                cwd=self.temp.name, capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        report = json.loads(result.stdout)
        self.assertEqual(report['durations_sec'], [8, 6, 10])
        self.assertEqual(report['planned_total_sec'], 24)
        self.assertFalse(report['runtime_importer_checked'])
        self.assertFalse(report['image_files_checked'])

    def test_explicit_duration_and_loras_required(self):
        for key in ('duration_sec', 'loras'):
            data = copy.deepcopy(EXAMPLE)
            del data['shots'][0][key]
            self.save(data)
            with self.subTest(field=key), self.assertRaisesRegex(ValueError, key):
                validate(self.path)

    def test_limits_and_frame_boundary(self):
        for duration in (4, 16, True, 5.01):
            data = copy.deepcopy(EXAMPLE)
            data['shots'][0]['duration_sec'] = duration
            self.save(data)
            with self.subTest(duration=duration), self.assertRaises(ValueError):
                validate(self.path)
        for duration in (5, 5.5, 15):
            data = copy.deepcopy(EXAMPLE)
            data['shots'][0]['duration_sec'] = duration
            self.save(data)
            self.assertTrue(validate(self.path)['ok'])

    def test_segment_count_bounds(self):
        for count in (0, 64, 65):
            data = copy.deepcopy(EXAMPLE)
            data['shots'] = [copy.deepcopy(EXAMPLE['shots'][0]) for _ in range(count)]
            for index, shot in enumerate(data['shots'], 1):
                shot['id'] = index
            self.save(data)
            if count == 64:
                self.assertEqual(validate(self.path)['shot_count'], 64)
            else:
                with self.subTest(count=count), self.assertRaises(ValueError):
                    validate(self.path)

    def test_invalid_first_frames(self):
        invalid = [{'type': 'previous_tail'},
                   {'type': 'image', 'path': 'relative.png'},
                   {'type': 'image', 'path': '//server/share/001.png'},
                   {'type': 'image', 'path': 'https://example.org/001.png'},
                   {'type': 'image', 'path': 'F:relative.png'}]
        for frame in invalid:
            data = copy.deepcopy(EXAMPLE)
            data['shots'][0]['first_frame'] = frame
            self.save(data)
            with self.subTest(frame=frame), self.assertRaises(ValueError):
                validate(self.path)
        data = copy.deepcopy(EXAMPLE)
        data['shots'][1]['first_frame']['path'] = 'F:/001.png'
        self.save(data)
        with self.assertRaisesRegex(ValueError, '不应再填写 path'):
            validate(self.path)

    def test_canvas_settings_rejected(self):
        data = copy.deepcopy(EXAMPLE)
        data['width'] = 576
        self.save(data)
        with self.assertRaises(ValueError):
            validate(self.path)
        data = copy.deepcopy(EXAMPLE)
        data['shots'][0]['sampling_profile'] = '4step'
        self.save(data)
        with self.assertRaises(ValueError):
            validate(self.path)

    def test_prompt_structure_and_reference_scope(self):
        original = EXAMPLE['shots'][0]['prompt']
        invalid = [original.split('\n\n', 1)[1],
                   original.replace('overall_soundscape:', 'non_diegetic_music:', 1),
                   original.replace('<Picture 1>', '<Picture 2>'),
                   original.replace('[Shot 1] Live-action', '[Shot 1] At 00:00.000, Live-action')]
        for prompt in invalid:
            data = copy.deepcopy(EXAMPLE)
            data['shots'][0]['prompt'] = prompt
            self.save(data)
            with self.subTest(prompt_prefix=prompt[:30]), self.assertRaises(ValueError):
                validate(self.path)

    def test_cut_times_stay_inside_segment(self):
        for stamp in ('00:03.500', '00:08.000', '00:00.000'):
            data = copy.deepcopy(EXAMPLE)
            data['shots'][0]['prompt'] = data['shots'][0]['prompt'].replace(
                '\n\noverall_soundscape:',
                f' [Shot 2] At {stamp}, the camera cuts to the desk.\n\noverall_soundscape:')
            self.save(data)
            if stamp == '00:03.500':
                self.assertTrue(validate(self.path)['ok'])
            else:
                with self.subTest(time=stamp), self.assertRaisesRegex(ValueError, '切镜时间'):
                    validate(self.path)

    def test_lora_constraints(self):
        item = {'name': 'style.safetensors', 'strength': 0.6}
        for loras in ([item, item], [{'name': 'x', 'strength': True}],
                      [{'name': 'x', 'strength': 11}],
                      [{'name': str(i), 'strength': 1} for i in range(5)],
                      [{'name': 'minimax_h3_fl2v_turbo_4step.safetensors', 'strength': 1}]):
            data = copy.deepcopy(EXAMPLE)
            data['shots'][0]['loras'] = loras
            self.save(data)
            with self.subTest(loras=loras), self.assertRaises(ValueError):
                validate(self.path)

    def test_lora_catalog_check_only_reads(self):
        data = copy.deepcopy(EXAMPLE)
        data['shots'][0]['loras'] = [{'name': 'style.safetensors', 'strength': 0.6}]
        self.save(data)
        def response(request, timeout):
            self.assertEqual(request.method, 'GET')
            self.assertEqual(request.full_url, 'http://localhost:8188/object_info/LoraLoaderModelOnly')
            return io.BytesIO(json.dumps({'LoraLoaderModelOnly': {'input': {'required': {
                'lora_name': [['style.safetensors']]}}}}).encode())
        with patch('urllib.request.urlopen', response):
            self.assertTrue(validate(self.path, comfy_url='http://localhost:8188')['lora_names_checked'])
            data['shots'][0]['loras'][0]['name'] = 'missing.safetensors'
            self.save(data)
            with self.assertRaisesRegex(ValueError, '找不到 LoRA'):
                validate(self.path, comfy_url='http://localhost:8188')

    def test_explicit_runtime_check_does_not_fall_back(self):
        self.save(EXAMPLE)
        with self.assertRaisesRegex(ValueError, '找不到指定的真实导入器'):
            validate(self.path, project_root=Path(self.temp.name))

    def test_duplicate_keys_and_nonstandard_numbers(self):
        for text in ('{"version":1,"version":1}', '{"version":NaN}'):
            self.path.write_text(text, encoding='utf-8')
            with self.subTest(text=text), self.assertRaises(ValueError):
                validate(self.path)

    def test_bad_image_is_rejected_when_image_checks_requested(self):
        try:
            import PIL
        except ImportError:
            self.skipTest('Optional Pillow is not installed')
        data = copy.deepcopy(EXAMPLE)
        bad_image = Path(self.temp.name) / 'not-a-real-image.png'
        bad_image.write_bytes(b'not an image')
        for shot in data['shots']:
            if shot['first_frame']['type'] == 'image':
                shot['first_frame']['path'] = bad_image.as_posix()
        self.save(data)
        with self.assertRaises(OSError):
            validate(self.path, check_images=True)


if __name__ == '__main__':
    unittest.main()
