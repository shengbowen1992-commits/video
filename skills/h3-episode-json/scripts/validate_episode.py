"""Read-only, standalone canvas JSON / H3 I2VA checks; optional runtime verification."""
import argparse
import importlib
import json
from pathlib import Path
import re
import sys
import urllib.request

sys.path.insert(0, str(Path(__file__).resolve().parent))
from episode_contract import parse_document


PREFIX = (
    "For the target video, at 0.00 seconds into the target video, "
    "<Picture 1> (from [Shot 1]) is fully referenced."
)
SECTIONS = (
    "integrated_multimodal_description",
    "overall_soundscape",
    "non_diegetic_music",
)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, f"JSON 字段重复: {key}")
        result[key] = value
    return result


def reject_constant(value):
    raise ValueError(f"JSON 不接受非常规数字: {value}")


def check_prompt(prompt, duration, label):
    prompt = prompt.replace("\r\n", "\n")
    require(prompt.startswith(PREFIX + "\n\n"), f"{label}: 缺少官方 I2VA 首行或其后的空行")
    body = prompt[len(PREFIX) + 2:]
    matches = list(re.finditer(r"(?m)^(\w+):[ \t]*", body))
    require([match[1] for match in matches] == list(SECTIONS), f"{label}: 三个字段须各出现一次并按官方顺序排列")
    require(matches[0].start() == 0, f"{label}: 首行之后应直接开始 integrated_multimodal_description")
    values = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(body)
        value = body[match.end():end]
        require(value.strip(), f"{label}: {match[1]} 不能为空")
        if index < len(matches) - 1:
            require(value.endswith("\n\n"), f"{label}: 字段之间应空一行")
        values.append(value.strip())
    visual = values[0]
    require(visual.startswith("[Shot 1] "), f"{label}: 本段正文应从 [Shot 1] 开始")
    require(not re.match(r"\[Shot 1\]\s+(?:At\s+)?\d{2}:\d{2}", visual, re.I),
            f"{label}: [Shot 1] 后不加起始时间戳")
    require("<Picture 1>" in visual, f"{label}: 正文应锚定本段 <Picture 1>")
    refs = re.findall(r"<(Picture|Video|Audio)\s+(\d+)>", prompt)
    require(all(kind == "Picture" and number == "1" for kind, number in refs),
            f"{label}: 当前单首帧模式只有 <Picture 1>")
    require(not re.search(r"\b(?:subject_definitions|retention_analysis|detailed_description|summary):", prompt),
            f"{label}: 不应混入 Ref2VA 字段")
    shots = list(re.finditer(r"\[Shot (\d+)\]", visual))
    require([int(match[1]) for match in shots] == list(range(1, len(shots) + 1)),
            f"{label}: 段内镜头编号须从 1 连续递增")
    previous_time = 0
    for match in shots[1:]:
        time = re.match(r" At (\d{2}):([0-5]\d)\.(\d{3}),", visual[match.end():])
        require(time, f"{label}: 后续镜头须用 [Shot N] At 00:03.500, 格式")
        seconds = int(time[1]) * 60 + int(time[2]) + int(time[3]) / 1000
        require(previous_time < seconds < duration, f"{label}: 切镜时间须递增并落在该段秒数内")
        previous_time = seconds


def validate(path, project_root=None, check_images=False, comfy_url=None):
    require(path.suffix.lower() == ".json", "文件扩展名应为 .json")
    require(path.stat().st_size <= 2 * 1024 * 1024, "JSON 超过 2 MiB")
    data = json.loads(path.read_text(encoding="utf-8-sig"), object_pairs_hook=unique_object,
                      parse_constant=reject_constant)
    require(isinstance(data, dict), "JSON 顶层必须是对象")
    require(set(data) == {"version", "episode_id", "title", "shots"},
            "画布参数版顶层应仅含 version、episode_id、title、shots")
    require(type(data["version"]) is int and data["version"] == 1, "version 应为整数 1")
    document = parse_document(data)
    if project_root is not None:
        module_path = project_root / "h3_episode" / "json_import.py"
        require(module_path.is_file(), f"找不到指定的真实导入器: {module_path}")
        sys.path.insert(0, str(project_root))
        importer = importlib.import_module("h3_episode.json_import")
        require(Path(importer.__file__).resolve() == module_path.resolve(),
                "已载入不同项目的 h3_episode，请在新进程中运行校验")
        importer.parse_document(data)
    notes = []
    image_paths = []
    lora_names = set()
    for raw, shot in zip(data["shots"], document["shots"]):
        label = f"第 {shot['id']} 段"
        require("duration_sec" in raw, f"{label}: 必须显式填写 duration_sec")
        require("loras" in raw, f"{label}: 必须显式填写 loras，无附加 LoRA 用 []")
        require(set(raw) <= {"id", "duration_sec", "first_frame", "prompt", "seed", "loras"},
                f"{label}: 采样模式等生成参数应留在画布")
        check_prompt(shot["prompt"], shot["duration_sec"], label)
        for lora in shot["loras"]:
            lora_names.add(lora["name"])
            require(not re.search(r"h3.*turbo.*(?:4|8)step", lora["name"], re.I),
                    f"{label}: H3 4/8 步加速 LoRA 应由画布控制")
        if shot["first_frame"]["type"] == "image":
            image_paths.append(Path(shot["first_frame"]["path"]))
    if check_images:
        from PIL import Image
        for image_path in image_paths:
            require(image_path.is_absolute(), f"当前系统无法访问此绝对图片路径: {image_path}")
            require(not str(image_path.resolve()).startswith(("\\\\", "//")), "图片不能解析到网络共享")
            require(image_path.is_file(), f"图片不存在: {image_path}")
            with Image.open(image_path) as image:
                image.verify()
        notes.append("图片存在且可解码；尚未核对画布尺寸和首帧描述。")
    else:
        notes.append("未检查图片是否存在、能否解码，以及是否匹配画布尺寸和首帧描述。")
    lora_checked = False
    if lora_names and comfy_url:
        request = urllib.request.Request(comfy_url.rstrip("/") + "/object_info/LoraLoaderModelOnly",
                                         headers={"Accept": "application/json"}, method="GET")
        with urllib.request.urlopen(request, timeout=10) as response:
            info = json.load(response)
        installed = info["LoraLoaderModelOnly"]["input"]["required"]["lora_name"][0]
        require(isinstance(installed, list) and all(isinstance(name, str) for name in installed),
                "ComfyUI 返回的 LoRA 清单格式异常")
        missing_loras = sorted(lora_names - set(installed))
        require(not missing_loras, "ComfyUI 中找不到 LoRA: " + "、".join(missing_loras))
        lora_checked = True
    elif lora_names:
        notes.append("尚未通过 ComfyUI 核对附加 LoRA 名称。")
    notes.append("格式校验不代表模型兼容性、触发词、图像语义或生成效果已验证；未提交视频生成。")
    if project_root is None:
        notes.append("使用随技能提供的协议检查；未调用 ComfyUI 整集项目的实际导入器。")
    return {"ok": True, "episode_id": document["episode_id"], "shot_count": len(document["shots"]),
            "durations_sec": [shot["duration_sec"] for shot in document["shots"]],
            "planned_total_sec": sum(shot["duration_sec"] for shot in document["shots"]),
            "runtime_importer_checked": project_root is not None,
            "image_files_checked": check_images, "lora_names": sorted(lora_names),
            "lora_names_checked": lora_checked, "notes": notes}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("json_file", type=Path)
    parser.add_argument("--project-root", type=Path, help="可选：额外调用已安装整集项目的真实导入器")
    parser.add_argument("--check-images", action="store_true")
    parser.add_argument("--comfy-url", help="仅 GET 读取 LoRA 清单，不排队生成")
    args = parser.parse_args()
    try:
        result = validate(args.json_file, args.project_root, args.check_images, args.comfy_url)
    except (ValueError, OSError, ImportError, KeyError, TypeError) as error:
        print(json.dumps({"ok": False, "error": str(error)}, ensure_ascii=False, indent=2))
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
