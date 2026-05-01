---
name: /superpowers-install
id: superpowers-install
category: Workflow
description: 通过 Cursor 插件市场安装或重装 Superpowers（obra/superpowers），获得官方 skills 与更新通道
---

本仓库已**不再**在 `.cursor/skills/superpowers/` 内置副本；请用 **Cursor 插件市场** 安装，由插件提供 skills（与 [官方仓库](https://github.com/obra/superpowers) 同步）。

## 你要对用户说明的安装步骤（中文）

### 1. 用「插件」命令安装（推荐）

在 **Cursor Agent 对话输入框**里直接输入（整行发送）：

```text
/add-plugin superpowers
```

按提示完成安装。若提示已安装，可选择更新或先卸载再装（见下）。

### 2. 用界面搜索安装

- 打开 Cursor 的 **插件市场 / Plugins**（具体入口随版本可能在：命令面板、设置侧栏或 Agent 面板的插件入口）。
- 搜索 **`superpowers`**，选择 **obra/superpowers** 相关插件安装。

### 3. 重装（重新拉取 skills）

- 在已安装插件列表中找到 **Superpowers**，先 **卸载**，再重复上面 **步骤 1 或 2** 安装；或在市场页对该插件执行 **更新**（若有）。

### 4. 验证

新开一个 Agent 会话，说例如：

- 「帮我规划这个功能」
- 「我们系统性地排查这个 bug」

代理应能按 Superpowers 的 workflow 调用对应 skill（见[官方 README 工作流说明](https://github.com/obra/superpowers#the-basic-workflow)）。

### 5. 后续更新

官方说明：通过插件更新即可同步 skills，例如 Claude Code 侧为 `/plugin update superpowers`；**Cursor 请以界面中的「更新插件」或市场页为准**。

---

## Agent 行为要求

若用户运行了本命令（`/superpowers-install`）：

1. 用简短中文复述上述步骤，强调 **`/add-plugin superpowers` 是在 Agent 输入框发送**，不是终端命令。
2. 不要假设项目内仍存在 `.cursor/skills/superpowers/` 下的文件；skills 来自 **已安装的 Cursor 插件**。
3. 若用户仍想用文件方式引用，可说明：安装插件后，skills 由 Cursor/插件注入；若需固定引用，可到官方仓库查看对应 `skills/*/SKILL.md` 内容。
