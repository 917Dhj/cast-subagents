# 将 `cast-subagents` 改造成可开源 Codex 插件的完整说明

日期：2026-04-26

本文面向当前仓库：

```text
/Users/dinghongjing/Documents/Playground/cast-subagents
```

目标是把它整理成一个可以开源到 GitHub、并能让用户通过 Codex 的 marketplace 机制安装的插件仓库。

## 结论先行

你现在的仓库已经具备 Codex 插件的核心结构：

```text
.codex-plugin/plugin.json
skills/using-cast-subagents/SKILL.md
skills/cast-subagents/SKILL.md
README.md
LICENSE
evals/
references/
```

还需要补齐的是“发布面”和“安装面”：

1. 补 `.agents/plugins/marketplace.json`，让这个 GitHub 仓库本身可以作为 Codex marketplace 被用户添加。
2. 补 `assets/`，给插件提供图标、logo，便于在 Codex 插件列表中展示。
3. 补强 `.codex-plugin/plugin.json` 的发布元数据，例如 `repository`、`homepage`、作者 URL、图标路径等。
4. 更新 `README.md`，写清楚安装、刷新、卸载、测试方式。
5. 增加发布配套文件，例如 `CHANGELOG.md`、`SECURITY.md`、可选的 `CODE_OF_CONDUCT.md`。
6. 在发布前跑一轮本地安装测试和 GitHub 安装测试。

注意：截至 2026-04-26，OpenAI 官方文档仍然写着官方 Plugin Directory 的自助发布和管理是 coming soon。也就是说，你现在可以让用户通过 `codex plugin marketplace add <owner>/<repo>` 安装你的 GitHub marketplace，但还不能自己把插件直接提交进官方 `openai-curated` 插件目录。

## 官方机制的关键点

Codex 插件由几个部分组成：

- `.codex-plugin/plugin.json`：必需，插件 manifest。
- `skills/`：可选但你的插件主要依赖它，里面放一个或多个 `SKILL.md`。
- `.mcp.json`：可选，如果插件提供 MCP server 配置才需要。
- `.app.json`：可选，如果插件绑定 App/connector 才需要。
- `assets/`：可选但发布时建议提供，用于图标、logo、截图。

Marketplace 是另一个 JSON 目录文件：

```text
.agents/plugins/marketplace.json
```

用户通过下面命令添加 marketplace：

```bash
codex plugin marketplace add <owner>/<repo>
```

然后在 Codex Desktop 的 Plugins 页面，或 Codex CLI 的 `/plugins` 页面中选择这个 marketplace 并安装插件。

## 推荐仓库结构

建议把当前仓库整理成下面这样：

```text
cast-subagents/
├─ .codex-plugin/
│  └─ plugin.json
├─ .agents/
│  └─ plugins/
│     └─ marketplace.json
├─ assets/
│  ├─ icon.png
│  └─ logo.png
├─ skills/
│  ├─ using-cast-subagents/
│  │  └─ SKILL.md
│  └─ cast-subagents/
│     └─ SKILL.md
├─ references/
│  ├─ decision-rules.md
│  ├─ examples-negative.md
│  ├─ examples-positive.md
│  ├─ handoff-schema.md
│  ├─ role-lineups.md
│  └─ suggestion-contract.md
├─ evals/
│  ├─ prompts.yaml
│  ├─ results-template.md
│  ├─ rubric.md
│  └─ scenarios.md
├─ README.md
├─ CHANGELOG.md
├─ LICENSE
├─ SECURITY.md
└─ CODE_OF_CONDUCT.md
```

其中：

- `.codex-plugin/plugin.json` 是插件本体入口。
- `.agents/plugins/marketplace.json` 是让仓库成为可添加 marketplace 的入口。
- `assets/` 建议放真实图标，不要只留空目录。
- `references/` 和 `evals/` 可以继续保留，它们对开源用户理解和验证行为很有帮助。
- 当前仓库里的根目录 `SKILL.md` 可以保留为 legacy skill 入口，但建议在 README 里说明真正的插件入口是 `skills/`。
- 当前仓库里的 `agents/openai.yaml` 不属于官方插件结构的必需文件。若保留，建议在 README 里标成 experimental 或 internal，避免用户误以为安装插件必须依赖它。

## 改造 `.codex-plugin/plugin.json`

你当前的 `plugin.json` 已经可以工作。发布前建议补充 GitHub 和展示信息。

建议模板如下，把 `<...>` 替换成你的真实信息：

```json
{
  "name": "cast-subagents",
  "version": "0.1.0",
  "description": "Suggest-only subagent delegation guidance for Codex tasks.",
  "author": {
    "name": "<Your Name>",
    "url": "https://github.com/<your-github-user>"
  },
  "homepage": "https://github.com/<your-github-user>/cast-subagents",
  "repository": "https://github.com/<your-github-user>/cast-subagents",
  "license": "MIT",
  "keywords": [
    "codex",
    "plugin",
    "subagents",
    "delegation",
    "review",
    "planning",
    "skills"
  ],
  "skills": "./skills/",
  "interface": {
    "displayName": "Cast Subagents",
    "shortDescription": "Suggest subagent lineups without auto-spawning them.",
    "longDescription": "Use Cast Subagents to decide when a Codex task merits a subagent lineup, present one concise recommendation, and require explicit approval before delegation.",
    "developerName": "<Your Name>",
    "category": "Coding",
    "capabilities": [
      "Interactive",
      "Read"
    ],
    "websiteURL": "https://github.com/<your-github-user>/cast-subagents",
    "privacyPolicyURL": "https://github.com/<your-github-user>/cast-subagents/blob/main/PRIVACY.md",
    "termsOfServiceURL": "https://github.com/<your-github-user>/cast-subagents/blob/main/LICENSE",
    "defaultPrompt": [
      "Review this branch for bugs, tests, security, and risk.",
      "Map code paths and verify docs before changing code."
    ],
    "brandColor": "#10A37F",
    "composerIcon": "./assets/icon.png",
    "logo": "./assets/logo.png",
    "screenshots": []
  }
}
```

说明：

- `name` 不要随便改。Codex 会用它作为插件标识和技能 namespace。
- `version` 建议遵循 SemVer，例如 `0.1.0`、`0.2.0`、`1.0.0`。
- `skills` 路径必须相对插件根目录，并以 `./` 开头。
- 你的插件是建议型 instruction-only 插件，`capabilities` 用 `["Interactive", "Read"]` 比较合适；不要标 `Write`，除非之后真的提供写文件或执行修改的能力。
- 如果暂时没有 `PRIVACY.md`，可以先不填 `privacyPolicyURL`，或者补一个简短的隐私说明文件。

## 新增 `.agents/plugins/marketplace.json`

如果你希望这个插件仓库本身就是 marketplace，创建：

```text
.agents/plugins/marketplace.json
```

内容建议如下：

```json
{
  "name": "cast-subagents-marketplace",
  "interface": {
    "displayName": "Cast Subagents"
  },
  "plugins": [
    {
      "name": "cast-subagents",
      "source": {
        "source": "url",
        "url": "https://github.com/<your-github-user>/cast-subagents.git",
        "ref": "main"
      },
      "policy": {
        "installation": "AVAILABLE",
        "authentication": "ON_INSTALL"
      },
      "category": "Coding"
    }
  ]
}
```

这是最适合你当前仓库的方案：插件本体就在 GitHub 仓库根目录，所以 marketplace entry 用 `"source": "url"`。

用户安装时：

```bash
codex plugin marketplace add <your-github-user>/cast-subagents
```

然后打开 Codex 插件列表，选择 `Cast Subagents` marketplace，安装 `cast-subagents` 插件。

## 如果想做成更像 `superpowers` 的双仓库结构

`superpowers` 的模式更像是：

1. 一个插件本体仓库，例如 `obra/superpowers`。
2. 一个 marketplace 仓库，例如 `obra/superpowers-marketplace`。

你也可以采用这种方式：

```text
cast-subagents/                 # 插件本体仓库
├─ .codex-plugin/plugin.json
├─ skills/
└─ ...

cast-subagents-marketplace/     # marketplace 仓库
└─ .agents/plugins/marketplace.json
```

marketplace 仓库里的 `.agents/plugins/marketplace.json` 写：

```json
{
  "name": "cast-subagents-marketplace",
  "interface": {
    "displayName": "Cast Subagents"
  },
  "plugins": [
    {
      "name": "cast-subagents",
      "source": {
        "source": "url",
        "url": "https://github.com/<your-github-user>/cast-subagents.git",
        "ref": "main"
      },
      "policy": {
        "installation": "AVAILABLE",
        "authentication": "ON_INSTALL"
      },
      "category": "Coding"
    }
  ]
}
```

用户安装时添加 marketplace 仓库：

```bash
codex plugin marketplace add <your-github-user>/cast-subagents-marketplace
```

优点：

- marketplace 可以同时管理多个插件。
- 插件仓库和插件目录仓库职责分离。
- 后续发布多个 Codex 插件时更清晰。

缺点：

- 多一个仓库，维护成本略高。
- 对当前只有一个插件的阶段来说不是必需。

当前建议：先用单仓库方案。等你以后有多个 Codex 插件，再拆独立 marketplace 仓库。

## 如果插件放在仓库子目录

如果未来你的仓库变成一个插件集合，例如：

```text
codex-plugins/
├─ .agents/plugins/marketplace.json
└─ plugins/
   └─ cast-subagents/
      ├─ .codex-plugin/plugin.json
      └─ skills/
```

那么 marketplace entry 应使用 `"source": "git-subdir"`：

```json
{
  "name": "cast-subagents",
  "source": {
    "source": "git-subdir",
    "url": "https://github.com/<your-github-user>/codex-plugins.git",
    "path": "./plugins/cast-subagents",
    "ref": "main"
  },
  "policy": {
    "installation": "AVAILABLE",
    "authentication": "ON_INSTALL"
  },
  "category": "Coding"
}
```

你当前不是这个结构，所以不需要这样做。

## README 应该包含的内容

建议把 README 调整成公开用户视角，至少包含这些章节：

```text
# Cast Subagents

## What it does
## What it does not do
## Installation
## Usage
## Example prompts
## Development
## Evaluation
## Release process
## License
```

安装说明建议写成：

````md
## Installation

Add this repository as a Codex marketplace:

```bash
codex plugin marketplace add <your-github-user>/cast-subagents
```

Then open the Codex plugin directory:

```text
/plugins
```

Select the `Cast Subagents` marketplace and install the `cast-subagents` plugin.

Start a new Codex thread after installation.
````

刷新说明：

````md
## Updating

```bash
codex plugin marketplace upgrade cast-subagents-marketplace
```

Then reinstall or refresh the plugin from the Codex plugin directory if needed, and start a new thread.
````

卸载说明：

````md
## Uninstalling

Open `/plugins`, select the installed plugin, and choose uninstall.

To remove the marketplace:

```bash
codex plugin marketplace remove cast-subagents-marketplace
```
````

## 发布前检查清单

发布前建议逐项确认：

- [ ] `.codex-plugin/plugin.json` 存在并 JSON 合法。
- [ ] `plugin.json` 的 `name`、`version`、`description` 稳定。
- [ ] `plugin.json` 的 `skills` 指向 `./skills/`。
- [ ] 所有 `skills/*/SKILL.md` 都有 frontmatter，包含 `name` 和 `description`。
- [ ] `.agents/plugins/marketplace.json` 存在并 JSON 合法。
- [ ] marketplace entry 包含 `policy.installation`、`policy.authentication`、`category`。
- [ ] marketplace 的 Git URL 指向公开仓库。
- [ ] README 有安装、使用、更新、卸载说明。
- [ ] LICENSE 存在。
- [ ] CHANGELOG 存在，记录 `0.1.0`。
- [ ] assets 图标存在，且 `plugin.json` 路径正确。
- [ ] 本地安装测试通过。
- [ ] GitHub 远程安装测试通过。
- [ ] 至少跑过 smoke eval，并把当前限制写进 README。

## 本地测试流程

在提交 GitHub 前，先在本机用本地路径测试 marketplace。

从仓库根目录执行：

```bash
codex plugin marketplace add /Users/dinghongjing/Documents/Playground/cast-subagents
```

然后打开 Codex：

```text
/plugins
```

选择你的 marketplace，安装插件。

也可以用 debug prompt 检查新会话是否能发现技能：

```bash
codex debug prompt-input | rg "cast-subagents:cast-subagents|cast-subagents:using-cast-subagents|Cast Subagents"
```

如果修改了插件内容，需要刷新 marketplace 或重新安装插件，再开启新会话。

## GitHub 远程测试流程

推送到 GitHub 后，用远程仓库测试：

```bash
codex plugin marketplace add <your-github-user>/cast-subagents
codex plugin marketplace upgrade cast-subagents-marketplace
```

然后打开：

```text
/plugins
```

安装插件后，开启一个新会话，用这些 prompt 做 smoke test：

```text
Review this branch for bugs, test gaps, security risks, and maintainability.
```

预期：插件应该建议一个 read-only 的 subagent lineup，并询问用户是否批准。

```text
Fix this typo.
```

预期：插件不应该提 subagent，应该正常处理小任务。

```text
Don't use subagents for this task.
```

预期：插件应该保持静默，不建议 subagent。

## Release 流程

建议采用简单的 release 流程：

1. 更新 `.codex-plugin/plugin.json` 的 `version`。
2. 更新 `CHANGELOG.md`。
3. 跑本地 marketplace 安装测试。
4. 跑 GitHub 远程 marketplace 安装测试。
5. 打 Git tag：

```bash
git tag v0.1.0
git push origin main --tags
```

6. 在 GitHub 创建 Release，说明：

- 插件做什么。
- 如何安装。
- 当前限制。
- 已知问题。

## 关于版本 pinning

发布早期可以让 marketplace entry 使用：

```json
"ref": "main"
```

这样用户总是拿到最新版本，适合测试期。

等插件稳定后，可以考虑让 marketplace 指向 tag：

```json
"ref": "v0.1.0"
```

这样安装结果更可复现。

如果使用独立 marketplace 仓库，可以在每次 release 后把 `ref` 更新为新的 tag。

## 当前仓库的具体待办

针对你现在的仓库，建议按这个顺序做：

1. 创建 `assets/`，放入 `icon.png` 和 `logo.png`。
2. 更新 `.codex-plugin/plugin.json`，补 `homepage`、`repository`、`author.url`、`interface.websiteURL`、图标路径。
3. 创建 `.agents/plugins/marketplace.json`。
4. 新增 `CHANGELOG.md`。
5. 新增 `SECURITY.md`。
6. 可选新增 `PRIVACY.md`，说明这是 instruction-only 插件，不主动收集数据。
7. 更新 README，加入 GitHub marketplace 安装说明。
8. 运行本地安装测试。
9. 推送到 GitHub。
10. 运行远程安装测试。

## 建议的 `CHANGELOG.md`

```md
# Changelog

## 0.1.0

- Initial public release.
- Add suggest-only subagent delegation policy.
- Add broad entry skill and detailed policy skill.
- Add evaluation prompts and rubric.
```

## 建议的 `SECURITY.md`

```md
# Security Policy

## Supported Versions

The latest release on `main` is supported during the pre-1.0 phase.

## Reporting a Vulnerability

Please open a private security advisory on GitHub or contact the maintainer.

This plugin is instruction-only. It does not install runtime dependencies, start services, define MCP servers, or request external credentials.
```

## 建议的 `PRIVACY.md`

```md
# Privacy

Cast Subagents is an instruction-only Codex plugin.

It does not collect, store, or transmit data by itself. It contains bundled skills that guide Codex behavior inside the user's existing Codex session.

Any data handling is governed by the user's Codex environment, installed tools, and approval settings.
```

## 官方目录上架的现实边界

当前能做到：

- 开源插件仓库。
- 让用户添加你的 GitHub marketplace。
- 让用户从 Codex 插件列表安装你的插件。
- 像 `superpowers` 一样准备好插件 manifest、skills、assets、README 和 release。

当前不能保证做到：

- 自助把插件发布进官方 Codex Plugin Directory。
- 自助出现在 `openai-curated` marketplace。

原因是 OpenAI 官方文档当前仍说明：官方 public plugin publishing 和 self-serve publishing/management 还在 coming soon。

## 参考资料

- OpenAI Codex Build plugins: https://developers.openai.com/codex/plugins/build
- OpenAI Codex Plugins: https://developers.openai.com/codex/plugins
- Superpowers plugin repo: https://github.com/obra/superpowers
- Superpowers plugin manifest: https://raw.githubusercontent.com/obra/superpowers/main/.codex-plugin/plugin.json
