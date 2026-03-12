# 插件安装指南

> 这份指南会一步步教你如何安装和使用插件，即使你是第一次接触也没关系，跟着做就行。

---

## 在开始之前，你需要准备什么？

1. **安装 Claude Code**：Claude Code 是一个在终端（就是电脑上那个黑色的命令行窗口）里运行的 AI 编程助手。如果你还没有安装，请先参考 [官方安装指南](https://docs.anthropic.com/en/docs/claude-code) 完成安装和登录。
2. **确认版本**：你的 Claude Code 需要是支持插件功能的较新版本。

---

## 第一步：添加插件市场

打开 Claude Code 后，输入下面这行命令，然后按回车：

```
/plugin marketplace add intelli-train-ai/cc-skills
```

> 这行命令的作用是：告诉 Claude Code "去这个地方找可以安装的插件"，就像在手机上添加了一个应用商店。

---

## 第二步：安装你想要的插件

### 有哪些插件可以装？

| 插件名称 | 用来做什么 | 包含的功能 |
|----------|-----------|-----------|
| `document-skills` | 处理办公文档 | Excel 表格、Word 文档、PowerPoint 幻灯片、PDF 文件 |
| `example-skills` | 各种实用小工具合集 | 算法艺术、品牌指南、画布设计、文档协作、前端设计、内部通讯、MCP 构建器、技能创建器、Slack GIF 创建器、主题工厂、Web 构件构建器、Web 应用测试 |
| `claude-api` | Claude API 开发文档 | 帮你用 Claude API 写程序 |

### 方法一：直接输入命令安装（推荐）

在 Claude Code 里输入以下命令，选你需要的那个就行：

```bash
# 想处理 Excel、Word、PPT、PDF？装这个：
/plugin install document-skills@anthropic-agent-skills

# 想要各种实用工具？装这个：
/plugin install example-skills@anthropic-agent-skills

# 想用 Claude API 开发程序？装这个：
/plugin install claude-api@anthropic-agent-skills
```

> 提示：`#` 开头的是注释说明，不需要输入，只需要输入 `/plugin install ...` 那一行。

### 方法二：通过菜单安装（更直观）

如果你不想记命令，也可以用菜单来操作：

1. 输入 `/plugin` 然后按回车，会弹出插件管理菜单
2. 选择 `Browse and install plugins`（浏览并安装插件）
3. 选择 `anthropic-agent-skills`
4. 勾选你想要安装的插件
5. 选择 `Install now`（立即安装）

---

## 安装到哪里？（可选，初学者可以跳过这部分）

插件可以安装在三个不同的"位置"，决定了谁能用、在哪能用：

| 安装位置 | 怎么装 | 效果 |
|---------|--------|------|
| **个人全局**（默认） | 直接装，不加任何参数 | 只有你自己能用，但在你所有的项目里都能用 |
| **项目共享** | 命令末尾加 `--scope project` | 团队里每个人都能用，但只在这个项目里生效 |
| **仅自己当前项目** | 命令末尾加 `--scope local` | 只有你自己能用，也只在当前项目里生效 |

举个例子：

```bash
# 默认安装（个人全局）— 最常用，推荐新手使用
/plugin install document-skills@anthropic-agent-skills

# 安装到项目里，和同事共享
/plugin install document-skills@anthropic-agent-skills --scope project

# 只装在当前项目，只有我自己用
/plugin install document-skills@anthropic-agent-skills --scope local
```

> 如果你不确定选哪个，直接用默认的就好，不需要加任何参数。

---

## 怎么使用已安装的插件？

安装好之后，你不需要做任何特别的操作。在和 Claude Code 对话时，直接用自然语言告诉它你想做什么就行了。比如：

- **处理 PDF**："帮我提取 report.pdf 里的文字"
- **做 Excel 表格**："帮我创建一份销售报表"
- **写 Word 文档**："帮我生成一份合同"
- **做 PPT**："帮我做一份项目介绍的幻灯片"
- **用 Claude API**："帮我用 Claude API 做一个聊天机器人"
- **建 MCP 服务器**："为我的数据库创建一个 MCP 服务器"

---

## 插件管理：查看、禁用、卸载

```bash
# 查看我装了哪些插件
/plugin

# 暂时不想用某个插件（不删除，只是关掉）
/plugin disable document-skills@anthropic-agent-skills

# 彻底卸载某个插件
/plugin uninstall document-skills@anthropic-agent-skills
```
