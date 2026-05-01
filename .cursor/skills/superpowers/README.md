# Superpowers Skills（项目内副本）

本目录内容来自开源项目 [obra/superpowers](https://github.com/obra/superpowers) 的 `skills/`，与 Cursor **插件市场安装的 Superpowers** 可并存；需要**可 `@` 的固定路径**或**随仓库版本管理**时，以本目录为准。

## 在 Cursor 里怎么用

### 1. 用 `@` 附加某个 Skill（推荐）

在 **Agent 对话输入框**输入 `@`，选择文件或粘贴路径，指向具体 `SKILL.md`，例如：

```text
.cursor/skills/superpowers/brainstorming/SKILL.md
.cursor/skills/superpowers/writing-plans/SKILL.md
.cursor/skills/superpowers/test-driven-development/SKILL.md
```

模型会按该文件中的流程执行。

### 2. 用自然语言说明

直接说明「按 Superpowers 的 brainstorming / TDD 流程」，若未附加 `SKILL.md`，执行严格度可能不如 `@` 引用。

### 3. 与官方插件的关系

- 若已安装 Cursor 插件 **Superpowers**，插件也会提供一套 skills；**二者可能版本略有差异**。
- 更新本目录：可从 [superpowers 仓库](https://github.com/obra/superpowers) 拉取最新 `skills/` 覆盖，或重新执行项目里约定的同步方式。

### 4. 安装插件（可选）

在 Agent 输入框发送 `/add-plugin superpowers`，或在插件市场搜索 **superpowers**。更详细的步骤见项目命令：`.cursor/commands/superpowers-install.md`（对话中可输入 `/superpowers-install`）。

---

## 本目录包含的 Skills

| 子目录 | 用途简述 |
|--------|----------|
| `brainstorming` | 写代码前澄清需求、分段设计 |
| `writing-plans` | 将设计拆成可执行任务与验证步骤 |
| `executing-plans` | 分批执行计划与人机检查点 |
| `subagent-driven-development` | 子代理开发与两阶段评审 |
| `dispatching-parallel-agents` | 并行子代理工作流 |
| `test-driven-development` | 红-绿-重构 TDD |
| `systematic-debugging` | 系统化调试 |
| `verification-before-completion` | 完成前验证 |
| `requesting-code-review` | 发起代码评审 |
| `receiving-code-review` | 响应评审意见 |
| `using-git-worktrees` | Git worktree 隔离分支 |
| `finishing-a-development-branch` | 分支收尾与合并选项 |
| `using-superpowers` | 技能系统总览与优先级 |
| `writing-skills` | 编写新 skill 的指南 |

---

## 许可

上游为 **MIT License**，见 [superpowers/LICENSE](https://github.com/obra/superpowers/blob/main/LICENSE)。
