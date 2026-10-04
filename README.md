# H3 视频技能库

每个 skill 都放在 `skills/<名称>/` 中，入口、脚本、参考资料和模板各自独立。按用途选择一个目录安装，无需把整个仓库当作一个 skill。

| Skill | 用途 | 输出 / 适用工作流 |
| --- | --- | --- |
| [h3-episode-json](skills/h3-episode-json/SKILL.md) | 为 H3 官方 I2V 格式编写整集分段 JSON，明确每段秒数、图片路径或上段尾帧、附加 LoRA | `shots` JSON；用于“整集JSON-外置分辨率与原生加速参数”工作流 |
| [h3-episode-ref2v-json](skills/h3-episode-ref2v-json/SKILL.md) | 为双人物 Ref2V 整集编写 JSON：女主/男主全局参考，Picture 3 为开场图或上段尾帧，逐段秒数与内容 LoRA | `shots` JSON；prompt 使用官方 Ref2VA 六字段；用于“整集JSON-Ref2V-双人物全局-Picture3开场参考”工作流 |
| [h3-tailchain-continuity](skills/h3-tailchain-continuity/SKILL.md) | Ref2VA 分段提示词、Opening State 文字承接及旧版尾帧序列 | 默认 `story_segments.json`；原版方案五两张人物身份图；兼容显式选择的旧版 `sequence.json` |
| [h3-adult-action-prompting](skills/h3-adult-action-prompting/README.md) | 已有的成年虚构角色提示词资料与双语规范 | 中英文 H3 文档；语料、说明和维护脚本保留在自己的目录 |

各 skill 的输入约定彼此独立。两种 `shots` JSON 分别对应 I2VA 三字段和 Ref2VA 六字段 prompt，应选择匹配的工作流；`segments`、旧版 `sets/clips` 不应混用。

## 目录

```text
skills/
  h3-episode-json/
    SKILL.md
    agents/
    assets/
    references/
    scripts/
  h3-tailchain-continuity/
    SKILL.md
    README.md
    agents/
    references/
    scripts/
  h3-episode-ref2v-json/
    SKILL.md
    agents/
    assets/
    references/
    scripts/
  h3-adult-action-prompting/
    SKILL.md
    SKILL.en.md
    SKILL.zh-CN.md
    README.md
    agents/
    references/
    scripts/
scripts/
  check_skill_layout.py       # 仓库维护检查，不属于任何生成技能
```

## 安装一个 skill

复制所选 skill 的**整个目录**，保留其中的相对路径。不要只复制 `SKILL.md`，也不要把几个 skill 的 `references` 或 `scripts` 合并在一起。

- OpenCode：全局 `<OpenCode 配置目录>/skills/<名称>/`，或项目 `.opencode/skills/<名称>/`。配置目录遵循运行环境的 `XDG_CONFIG_HOME`；当前这台机器使用 `F:/OpenCode/data/config/opencode/skills/`。
- Codex：`$CODEX_HOME/skills/<名称>/`，未设置时通常为 `~/.codex/skills/<名称>/`。
- 其他支持 `SKILL.md` 的工具：按其技能目录约定复制完整目录。

例如，在仓库根目录通过 PowerShell 安装新 skill 到当前机器的 OpenCode：

```powershell
$skillName = 'h3-episode-json'
$skillDestination = Join-Path 'F:\OpenCode\data\config\opencode\skills' $skillName
if (Test-Path -LiteralPath $skillDestination) { throw '目标已存在，请先备份或比较版本。' }
Copy-Item -LiteralPath (Join-Path 'skills' $skillName) -Destination $skillDestination -Recurse
```

在 OpenCode 中说明“使用 h3-episode-json，把下面分镜生成 JSON”；在 Codex 中可使用 `$h3-episode-json`。现有会话未发现新技能时，重新启动客户端。

## 独立使用与依赖

- `h3-episode-json` 的 JSON / I2VA 结构检查只需 Python 3.10+ 标准库，不依赖其他 skill、本机固定盘符或 ComfyUI。图片解码检查需 Pillow；显式传入 `--project-root` 时才调用已有 H3 整集项目解析器，并需要该项目依赖。生成视频仍需要对应的 ComfyUI 工作流、节点和模型，本仓库不分发它们。
- `h3-episode-ref2v-json` 自带 Ref2VA 三图编写规范、模板和独立标准库校验器。检查真实图片时同时提供两张全局身份图；显式传入 `--project-root` 时调用 Ref2V 项目的真实导入器。Picture 3 为开场参考约束，不保证生成首帧与图片逐像素相同。
- `h3-tailchain-continuity` 的两个 JSON 校验脚本随目录提供，使用 Python 3.10+，不读取兄弟 skill。
- `h3-adult-action-prompting` 已随包提供现有中英文资料。普通使用不需要运行翻译构建脚本；其历史维护工具的网络与翻译依赖见该目录说明，原来停止的翻译 workflow 继续保持停止状态。

## 从旧目录迁移

以前根目录的 `SKILL.md`、`agents/`、`references/`、技能脚本及原 README 已迁到 `skills/h3-tailchain-continuity/`。根目录现在是技能目录索引，不再作为可安装 skill。旧链接或安装路径应加上 `skills/h3-tailchain-continuity/` 前缀。

根目录曾重复存放的 `references/prompting-guide.json` 与 `skills/h3-adult-action-prompting/references/prompting-guide.json` 内容完全一致，现仅保留后一份；原语料仍可通过该路径和 Git 历史访问。

## 维护检查

```sh
python scripts/check_skill_layout.py
python -m unittest discover -s skills/h3-tailchain-continuity/scripts -p 'test_*.py'
python -m unittest discover -s skills/h3-episode-json/scripts -p 'test_*.py'
python skills/h3-episode-json/scripts/validate_episode.py skills/h3-episode-json/assets/episode.example.json
python -m unittest discover -s skills/h3-episode-ref2v-json/scripts -p 'test_*.py'
python skills/h3-episode-ref2v-json/scripts/validate_episode.py skills/h3-episode-ref2v-json/assets/episode.example.json
```

检查只验证目录边界、文件引用、JSON 格式和脚本行为；不会提交视频、翻译语料或调用生成模型。
