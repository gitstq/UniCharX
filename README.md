<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License">
  <img src="https://img.shields.io/badge/Zero%20Dependencies-✓-brightgreen.svg" alt="Zero Dependencies">
</p>

<p align="center">
  <a href="README.md">简体中文</a> | <a href="README_EN.md">English</a> | <a href="README_TW.md">繁體中文</a>
</p>

<h1 align="center">🚀 UniCharX</h1>

<p align="center">
  <strong>轻量级Unicode字符智能搜索CLI引擎</strong><br>
  <sub>Zero Dependencies • Fuzzy Search • TUI Dashboard • Category Filter</sub>
</p>

---

## 🎉 项目介绍

**UniCharX** 是一款**零依赖**、**跨平台**的Unicode字符智能搜索命令行工具。它帮助开发者、设计师和内容创作者快速查找、探索和使用Unicode字符。

### 🎯 解决的痛点

- 🔍 **字符查找困难**：在海量Unicode字符中快速定位目标字符
- 📝 **名称记忆负担**：支持模糊搜索，无需记住精确名称
- 🖥️ **终端工作流中断**：无需离开终端即可完成字符查找
- 📋 **复制粘贴繁琐**：一键复制字符到剪贴板

### ✨ 自研差异化亮点

- 🚀 **零依赖设计**：纯Python标准库实现，无需安装额外依赖
- 🔮 **智能模糊匹配**：基于编辑距离的模糊搜索算法
- 📊 **TUI仪表板**：支持Rich库的美观终端输出
- 🏷️ **分类过滤**：按Unicode类别和区块精确筛选
- 💡 **交互模式**：实时搜索，即时反馈
- 📤 **多格式输出**：支持JSON、Markdown、纯文本输出

---

## ✨ 核心特性

| 特性 | 描述 |
|------|------|
| 🔍 **智能搜索** | 支持精确匹配和模糊匹配，快速定位目标字符 |
| 📁 **分类浏览** | 按Unicode类别（符号、字母、数字等）浏览字符 |
| 🧱 **区块筛选** | 按Unicode区块（表情符号、数学符号等）过滤 |
| 💻 **交互模式** | 实时搜索终端界面，支持命令操作 |
| 📋 **剪贴板支持** | 一键复制字符到系统剪贴板 |
| 📤 **多格式输出** | JSON、Markdown、详细文本等多种输出格式 |
| 🎨 **彩色输出** | 支持Rich库的美观终端显示 |
| ⚡ **零依赖** | 仅使用Python标准库，安装即用 |

---

## 🚀 快速开始

### 📋 环境要求

- **Python 3.8+**
- 无需额外依赖（可选：`rich` 用于彩色输出）

### 📦 安装

```bash
# 从PyPI安装（推荐）
pip install unicharx

# 从GitHub安装
pip install git+https://github.com/gitstq/UniCharX.git

# 本地开发安装
git clone https://github.com/gitstq/UniCharX.git
cd UniCharX
pip install -e .
```

### 🎮 基本使用

```bash
# 搜索字符
unicharx heart

# 模糊搜索
unicharx -f arrw

# 按类别过滤
unicharx -c Sm plus

# 交互模式
unicharx -i

# 查看字符详情
unicharx --info U+2764

# 随机字符
unicharx --random

# 列出所有类别
unicharx --categories

# 列出所有区块
unicharx --blocks
```

---

## 📖 详细使用指南

### 🔍 搜索命令

```bash
# 基本搜索
unicharx star

# 模糊搜索（容错拼写）
unicharx -f hert
unicharx --fuzzy arw

# 设置模糊阈值
unicharx -f -t 0.5 hert

# 限制结果数量
unicharx arrow -l 10
```

### 📁 分类过滤

```bash
# 数学符号
unicharx -c Sm

# 货币符号
unicharx -c Sc

# 数字
unicharx -c Nd
```

**常用类别代码：**

| 代码 | 描述 |
|------|------|
| `Lu` | 大写字母 |
| `Ll` | 小写字母 |
| `Nd` | 十进制数字 |
| `Sm` | 数学符号 |
| `Sc` | 货币符号 |
| `So` | 其他符号 |
| `Po` | 标点符号 |

### 💻 交互模式

```bash
unicharx -i
```

**交互命令：**

| 命令 | 功能 |
|------|------|
| `:cat [类别]` | 按类别列出字符 |
| `:block [名称]` | 按区块列出字符 |
| `:random` | 显示随机字符 |
| `:categories` | 列出所有类别 |
| `:blocks` | 列出所有区块 |
| `:help` | 显示帮助 |
| `quit` / `exit` | 退出交互模式 |

### 📤 输出格式

```bash
# JSON输出
unicharx heart --json

# Markdown表格
unicharx star --markdown

# 详细输出
unicharx arrow -v
```

### 📋 剪贴板操作

```bash
# 搜索并复制第一个结果
unicharx heart --copy
```

---

## 💡 设计思路

### 🏗️ 技术架构

```
UniCharX/
├── unicharx/
│   ├── __init__.py      # 包入口
│   ├── core.py          # 核心搜索引擎
│   └── cli.py           # 命令行接口
├── tests/
│   └── test_core.py     # 单元测试
├── pyproject.toml       # 项目配置
└── README.md            # 文档
```

### 🔧 核心模块

- **UniCharX Engine**：Unicode字符索引与搜索引擎
- **CharInfo**：字符信息数据结构
- **CLI Interface**：命令行参数解析与输出格式化

### 🎯 设计原则

1. **零依赖优先**：最大化使用Python标准库
2. **性能优化**：字符索引缓存，LRU缓存
3. **可扩展性**：模块化设计，易于添加新功能
4. **用户友好**：丰富的命令选项，清晰的输出格式

---

## 📦 打包与部署

### 本地打包

```bash
# 构建wheel包
pip install build
python -m build

# 安装测试
pip install dist/unicharx-1.0.0-py3-none-any.whl
```

### 发布到PyPI

```bash
pip install twine
twine upload dist/*
```

---

## 🤝 贡献指南

欢迎贡献代码、报告问题或提出建议！

1. Fork 本仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'feat: add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

---

## 📄 开源协议

本项目采用 **MIT License** 开源协议。

---

## 🙏 致谢

灵感来源于对高效Unicode字符搜索工具的需求，感谢Python标准库提供的强大Unicode支持。

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/gitstq">gitstq</a>
</p>
