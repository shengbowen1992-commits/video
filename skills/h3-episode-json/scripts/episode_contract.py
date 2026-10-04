"""Portable canvas JSON contract, aligned with the local H3 importer on 2026-10-04.

This authoring subset requires explicit durations and LoRA lists. Rendering and
the full runtime configuration remain the consuming workflow's responsibility.
Only Python's standard library is needed. Windows paths can be checked on Linux.
"""
import copy
import math
from pathlib import PurePosixPath, PureWindowsPath
import re


def require(condition, message):
    if not condition:
        raise ValueError(message)


def fields(value, required, optional, label):
    require(isinstance(value, dict), f"{label} 必须是对象")
    missing = set(required) - set(value)
    require(not missing, f"{label} 必须显式填写: {', '.join(sorted(missing))}")
    extra = set(value) - set(required) - set(optional)
    require(not extra, f"{label} 有未知或应留在画布的字段: {', '.join(sorted(extra))}")


def number(value, label, low, high, integer=False):
    require(type(value) in (int, float), f"{label} 必须是数字")
    require(low <= value <= high and math.isfinite(value), f"{label} 范围为 {low}..{high}")
    require(not integer or type(value) is int, f"{label} 必须是整数")


def parse_document(data):
    fields(data, ('version', 'episode_id', 'title', 'shots'), (), 'JSON')
    doc = copy.deepcopy(data)
    require(type(doc['version']) is int and doc['version'] == 1, 'version 必须为整数 1')
    require(isinstance(doc['episode_id'], str) and re.fullmatch(r'[A-Za-z0-9_-]{1,80}', doc['episode_id']),
            'episode_id 只能用 1–80 位英文字母、数字、下划线、连字符')
    require(isinstance(doc['title'], str), 'title 必须是文字')
    shots = doc['shots']
    require(isinstance(shots, list) and 1 <= len(shots) <= 64, 'shots 必须包含 1–64 段')
    for index, shot in enumerate(shots, 1):
        label = f'第 {index} 段'
        fields(shot, ('id', 'duration_sec', 'first_frame', 'prompt', 'loras'), ('seed',), label)
        require(type(shot['id']) is int and shot['id'] == index, f'{label} id 必须为 {index}')
        require(isinstance(shot['prompt'], str) and shot['prompt'].strip(), f'{label} prompt 不能为空')
        number(shot['duration_sec'], f'{label} duration_sec', 5, 15)
        require(abs(shot['duration_sec'] * 24 - round(shot['duration_sec'] * 24)) < 1e-7,
                f'{label} 时长必须落在 24 FPS 帧边界')
        if shot.get('seed') is not None:
            number(shot['seed'], f'{label} seed', 0, 2**64 - 1, True)
        loras = shot['loras']
        require(isinstance(loras, list) and len(loras) <= 4, f'{label} loras 最多 4 项')
        names = set()
        for item in loras:
            fields(item, ('name', 'strength'), (), f'{label} LoRA')
            name = item['name']
            require(isinstance(name, str) and name.strip() and name not in names,
                    f'{label} LoRA 名称为空或重复')
            number(item['strength'], f'{label} {name} strength', -10, 10)
            names.add(name)
        frame = shot['first_frame']
        fields(frame, ('type',), ('path',), f'{label} first_frame')
        require(frame['type'] in ('image', 'previous_tail'), f'{label} 首帧只能是 image 或 previous_tail')
        if frame['type'] == 'previous_tail':
            require(index > 1, '第 1 段不能使用上一段尾帧')
            require('path' not in frame, f'{label} previous_tail 不应再填写 path')
        else:
            name = frame.get('path')
            require(isinstance(name, str) and name.strip(), f'{label} image 缺少 path')
            path = PureWindowsPath(name) if re.match(r'^[A-Za-z]:', name) else PurePosixPath(name)
            require(path.is_absolute() and not name.startswith(('\\\\', '//')),
                    f'{label} path 请填写本机图片完整路径，例如 F:/素材/001.png')
            require(path.suffix.lower() in ('.png', '.jpg', '.jpeg', '.webp'), f'{label} 图片须为 PNG/JPEG/WebP')
            frame['path'] = path.as_posix()
    return doc
