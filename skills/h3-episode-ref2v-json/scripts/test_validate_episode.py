"""Three-picture authoring behavior; synthetic data only, no renders."""
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
EXAMPLE = json.loads((SKILL / 'assets/episode.example.json').read_text(encoding='utf-8'))


class RefEpisodeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / 'episode.json'
        self.data = copy.deepcopy(EXAMPLE)

    def save(self):
        self.path.write_text(json.dumps(self.data, ensure_ascii=False), encoding='utf-8')

    def test_skill_isolated_with_standard_library_only(self):
        isolated = Path(self.temp.name) / 'standalone'
        shutil.copytree(SKILL, isolated, ignore=shutil.ignore_patterns('__pycache__'))
        result = subprocess.run([sys.executable, '-I', '-S', '-X', 'utf8',
                                 str(isolated / 'scripts/validate_episode.py'),
                                 str(isolated / 'assets/episode.example.json')],
                                cwd=self.temp.name, capture_output=True, text=True, encoding='utf-8')
        self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
        report = json.loads(result.stdout)
        self.assertEqual(report['durations_sec'], [10, 8, 10])
        self.assertEqual(report['planned_total_sec'], 28)
        self.assertEqual(report['opening_frame_constraint'], 'reference_only')
        self.assertFalse(report['runtime_importer_checked'])

    def test_duration_and_loras_are_explicit(self):
        for field in ('duration_sec', 'loras'):
            self.data = copy.deepcopy(EXAMPLE)
            del self.data['shots'][0][field]
            self.save()
            with self.subTest(field=field), self.assertRaisesRegex(ValueError, field):
                validate(self.path)

    def test_duration_and_count_limits(self):
        for duration in (4, 16, True, 5.01):
            self.data['shots'][0]['duration_sec'] = duration
            self.save()
            with self.subTest(duration=duration), self.assertRaises(ValueError):
                validate(self.path)
        for count in (0, 64, 65):
            self.data = copy.deepcopy(EXAMPLE)
            self.data['shots'] = [copy.deepcopy(EXAMPLE['shots'][0]) for _ in range(count)]
            for index, shot in enumerate(self.data['shots'], 1):
                shot['id'] = index
            self.save()
            if count == 64:
                self.assertEqual(validate(self.path)['shot_count'], 64)
            else:
                with self.subTest(count=count), self.assertRaises(ValueError):
                    validate(self.path)

    def test_first_tail_and_invalid_image_paths_rejected(self):
        for frame in ({'type': 'previous_tail'}, {'type': 'image', 'path': 'relative.png'},
                      {'type': 'image', 'path': '//server/share/a.png'},
                      {'type': 'image', 'path': 'F:relative.png'},
                      {'type': 'image', 'path': 'https://example.com/a.png'}):
            self.data['shots'][0]['first_frame'] = frame
            self.save()
            with self.subTest(frame=frame), self.assertRaises(ValueError):
                validate(self.path)

    def test_tail_path_cannot_override_previous_result(self):
        self.data['shots'][1]['first_frame']['path'] = 'F:/a.png'
        self.save()
        with self.assertRaisesRegex(ValueError, '不应再填写 path'):
            validate(self.path)

    def test_canvas_and_identity_configuration_stays_outside_json(self):
        for key, value in [('width', 576), ('female', 'F:/female.png'), ('identity_references', {})]:
            self.data = copy.deepcopy(EXAMPLE)
            self.data[key] = value
            self.save()
            with self.subTest(key=key), self.assertRaises(ValueError):
                validate(self.path)

    def test_old_i2v_prompt_is_rejected(self):
        self.data['shots'][0]['prompt'] = (
            'For the target video, at 0.00 seconds into the target video, <Picture 1> '
            '(from [Shot 1]) is fully referenced.\n\nintegrated_multimodal_description: '
            '[Shot 1] A woman nods.\n\noverall_soundscape: N/A\n\nnon_diegetic_music: N/A')
        self.save()
        with self.assertRaisesRegex(ValueError, '六个 Ref2VA 字段'):
            validate(self.path)

    def test_extra_or_missing_reference_is_rejected(self):
        original = EXAMPLE['shots'][0]['prompt']
        for prompt in (original.replace('<Picture 3>', '<Picture 4>'),
                       original + '\n<Audio 1> is unbound.',
                       original.replace('<Picture 2>', '<Picture 1>')):
            self.data['shots'][0]['prompt'] = prompt
            self.save()
            with self.subTest(prompt=prompt[-50:]), self.assertRaises(ValueError):
                validate(self.path)

    def test_section_order_duplicates_and_empty_values_rejected(self):
        original = EXAMPLE['shots'][0]['prompt']
        for prompt in (original.replace('summary:', 'subject_definitions:', 1),
                       original.replace('non_diegetic_music:\nN/A', 'non_diegetic_music:\n'),
                       'summary:\nWrong order\n\n' + original):
            self.data['shots'][0]['prompt'] = prompt
            self.save()
            with self.subTest(prompt=prompt[:40]), self.assertRaises(ValueError):
                validate(self.path)

    def test_cut_times_follow_segment_duration(self):
        original = EXAMPLE['shots'][0]['prompt']
        for stamp in ('00:03.500', '00:10.000', '00:00.000'):
            self.data['shots'][0]['prompt'] = original.replace('\n\noverall_soundscape:',
                f' [Shot 2] At {stamp}, the camera cuts closer.\n\noverall_soundscape:')
            self.save()
            if stamp == '00:03.500':
                self.assertTrue(validate(self.path)['ok'])
            else:
                with self.subTest(stamp=stamp), self.assertRaisesRegex(ValueError, '切镜时间'):
                    validate(self.path)

    def test_first_shot_has_no_timestamp(self):
        self.data['shots'][0]['prompt'] = self.data['shots'][0]['prompt'].replace(
            '[Shot 1] Begin', '[Shot 1] At 00:00.000, Begin')
        self.save()
        with self.assertRaisesRegex(ValueError, '起始时间戳'):
            validate(self.path)

    def test_accelerator_lora_cannot_enter_content_array(self):
        self.data['shots'][0]['loras'] = [{'name': 'minimax_h3_ref2v_turbo_8step.safetensors', 'strength': 1}]
        self.save()
        with self.assertRaisesRegex(ValueError, '画布控制'):
            validate(self.path)

    def test_lora_name_verification_uses_get_only(self):
        self.data['shots'][0]['loras'] = [{'name': 'style.safetensors', 'strength': .6}]
        self.save()
        def response(request, timeout):
            self.assertEqual(request.method, 'GET')
            self.assertEqual(request.full_url, 'http://localhost:8188/object_info/LoraLoaderModelOnly')
            return io.BytesIO(json.dumps({'LoraLoaderModelOnly': {'input': {'required': {
                'lora_name': [['style.safetensors']]}}}}).encode())
        with patch('urllib.request.urlopen', response):
            self.assertTrue(validate(self.path, comfy_url='http://localhost:8188')['lora_names_checked'])
            self.data['shots'][0]['loras'][0]['name'] = 'missing.safetensors'
            self.save()
            with self.assertRaisesRegex(ValueError, '找不到 LoRA'):
                validate(self.path, comfy_url='http://localhost:8188')

    def test_check_images_requires_both_global_references(self):
        self.save()
        with self.assertRaisesRegex(ValueError, '同时提供'):
            validate(self.path, check_images=True)

    def test_valid_images_and_corrupt_global_reference(self):
        try:
            from PIL import Image
        except ImportError:
            self.skipTest('Optional Pillow is unavailable')
        opening = Path(self.temp.name) / 'opening.png'
        female = Path(self.temp.name) / 'female.png'
        male = Path(self.temp.name) / 'male.png'
        for image in (opening, female, male):
            Image.new('RGB', (32, 32)).save(image)
        for shot in self.data['shots']:
            if shot['first_frame']['type'] == 'image':
                shot['first_frame']['path'] = opening.as_posix()
        self.save()
        self.assertTrue(validate(self.path, check_images=True, female_reference=female,
                                 male_reference=male)['image_files_checked'])
        with self.assertRaisesRegex(ValueError, '本机绝对路径'):
            validate(self.path, check_images=True, female_reference=Path('relative.png'), male_reference=male)
        with self.assertRaisesRegex(ValueError, 'PNG/JPEG/WebP'):
            validate(self.path, check_images=True, female_reference=Path(self.temp.name) / 'female.gif', male_reference=male)
        male.write_bytes(b'not an image')
        with self.assertRaises(OSError):
            validate(self.path, check_images=True, female_reference=female, male_reference=male)

    def test_requested_runtime_check_does_not_fall_back(self):
        self.save()
        with self.assertRaisesRegex(ValueError, '找不到指定的真实导入器'):
            validate(self.path, project_root=Path(self.temp.name))

    def test_duplicate_fields_and_non_json_numbers_rejected(self):
        for raw in ('{"version":1,"version":1}', '{"version":NaN}'):
            self.path.write_text(raw, encoding='utf-8')
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                validate(self.path)


if __name__ == '__main__':
    unittest.main()
