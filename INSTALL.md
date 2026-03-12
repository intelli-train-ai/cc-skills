# 插件安装指南

## 前置条件

- 已安装并完成认证的 [Claude Code CLI](https://docs.anthropic.com/en/docs/claude-code)
- Claude Code 版本需支持插件功能

## 第一步：添加插件市场

```
/plugin marketplace add intelli-train-ai/cc-skills
```

> 将本仓库注册为 Claude Code 的插件市场源。

## 第二步：安装插件

### 可用插件

| 插件 | 说明 | 包含技能 |
|------|------|----------|
| `document-skills` | 文档处理套件 | Excel、Word、PowerPoint、PDF |
| `example-skills` | 示例技能合集 | 算法艺术、品牌指南、画布设计、文档协作、前端设计、内部通讯、MCP 构建器、技能创建器、Slack GIF 创建器、主题工厂、Web 构件构建器、Web 应用测试 |
| `claude-api` | Claude API 与 SDK 文档 | Claude API |

### 命令行安装

```bash
# 文档处理技能
/plugin install document-skills@anthropic-agent-skills

# 示例技能
/plugin install example-skills@anthropic-agent-skills

# Claude API 技能
/plugin install claude-api@anthropic-agent-skills
```

### 交互式安装

1. 运行 `/plugin` 打开插件管理器
2. 选择 `Browse and install plugins`
3. 选择 `anthropic-agent-skills`
4. 选择想要安装的插件
5. 选择 `Install now`

## 安装范围

插件支持三种安装范围：

| 范围 | 参数 | 配置位置 | 是否共享 | 适用场景 |
|------|------|----------|----------|----------|
| **用户级**（默认） | _(无)_ | `~/.claude/` | 否 | 个人使用，对所有项目生效 |
| **项目级** | `--scope project` | `.claude/settings.json` | 是（Git 跟踪） | 团队共享 |
| **本地级** | `--scope local` | `.claude/settings.local.json` | 否（Git 忽略） | 仅本人在当前项目使用 |

```bash
# 用户级（默认）— 在你的所有项目中可用
/plugin install document-skills@anthropic-agent-skills

# 项目级 — 通过 Git 与团队共享
/plugin install document-skills@anthropic-agent-skills --scope project

# 本地级 — 仅你本人在当前项目可用
/plugin install document-skills@anthropic-agent-skills --scope local
```

优先级：**本地级 > 项目级 > 用户级**

## 使用方式

安装后，在对话中直接提及相关技能即可。示例：

```
# PDF
"使用 PDF 技能提取 report.pdf 中的文本"

# Excel
"使用 Excel 技能创建一份销售报表"

# Word
"使用 Word 技能生成一份合同文档"

# PowerPoint
"使用 PowerPoint 技能制作一份项目演示文稿"

# Claude API
"帮我使用 Claude API 构建一个应用"

# MCP 构建器
"为我的数据库创建一个 MCP 服务器"
```

## 插件管理

```bash
# 查看已安装的插件
/plugin

# 禁用插件
/plugin disable document-skills@anthropic-agent-skills

# 卸载插件
/plugin uninstall document-skills@anthropic-agent-skills
```
