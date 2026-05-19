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
  <strong>Lightweight Unicode Character Intelligent Search CLI Engine</strong><br>
  <sub>Zero Dependencies • Fuzzy Search • TUI Dashboard • Category Filter</sub>
</p>

---

## 🎉 Introduction

**UniCharX** is a **zero-dependency**, **cross-platform** Unicode character intelligent search command-line tool. It helps developers, designers, and content creators quickly find, explore, and use Unicode characters.

### 🎯 Problems Solved

- 🔍 **Hard to find characters**: Quickly locate target characters among massive Unicode characters
- 📝 **Name memory burden**: Fuzzy search supported, no need to remember exact names
- 🖥️ **Terminal workflow interruption**: Find characters without leaving the terminal
- 📋 **Tedious copy-paste**: One-click copy to clipboard

### ✨ Unique Highlights

- 🚀 **Zero-dependency design**: Pure Python standard library implementation
- 🔮 **Intelligent fuzzy matching**: Edit-distance-based fuzzy search algorithm
- 📊 **TUI Dashboard**: Beautiful terminal output with Rich library support
- 🏷️ **Category filtering**: Precise filtering by Unicode category and block
- 💡 **Interactive mode**: Real-time search with instant feedback
- 📤 **Multi-format output**: JSON, Markdown, plain text output support

---

## ✨ Core Features

| Feature | Description |
|---------|-------------|
| 🔍 **Smart Search** | Exact and fuzzy matching to quickly locate target characters |
| 📁 **Category Browse** | Browse characters by Unicode category (symbols, letters, numbers, etc.) |
| 🧱 **Block Filter** | Filter by Unicode block (emoji, math symbols, etc.) |
| 💻 **Interactive Mode** | Real-time search terminal interface with command support |
| 📋 **Clipboard Support** | One-click copy characters to system clipboard |
| 📤 **Multi-format Output** | JSON, Markdown, detailed text and other output formats |
| 🎨 **Color Output** | Beautiful terminal display with Rich library support |
| ⚡ **Zero Dependencies** | Uses only Python standard library, install and use |

---

## 🚀 Quick Start

### 📋 Requirements

- **Python 3.8+**
- No additional dependencies required (optional: `rich` for colored output)

### 📦 Installation

```bash
# Install from PyPI (Recommended)
pip install unicharx

# Install from GitHub
pip install git+https://github.com/gitstq/UniCharX.git

# Local development installation
git clone https://github.com/gitstq/UniCharX.git
cd UniCharX
pip install -e .
```

### 🎮 Basic Usage

```bash
# Search characters
unicharx heart

# Fuzzy search
unicharx -f arrw

# Filter by category
unicharx -c Sm plus

# Interactive mode
unicharx -i

# View character details
unicharx --info U+2764

# Random characters
unicharx --random

# List all categories
unicharx --categories

# List all blocks
unicharx --blocks
```

---

## 📖 Detailed Usage Guide

### 🔍 Search Commands

```bash
# Basic search
unicharx star

# Fuzzy search (tolerates typos)
unicharx -f hert
unicharx --fuzzy arw

# Set fuzzy threshold
unicharx -f -t 0.5 hert

# Limit result count
unicharx arrow -l 10
```

### 📁 Category Filtering

```bash
# Math symbols
unicharx -c Sm

# Currency symbols
unicharx -c Sc

# Numbers
unicharx -c Nd
```

**Common Category Codes:**

| Code | Description |
|------|-------------|
| `Lu` | Letter, uppercase |
| `Ll` | Letter, lowercase |
| `Nd` | Number, decimal digit |
| `Sm` | Symbol, math |
| `Sc` | Symbol, currency |
| `So` | Symbol, other |
| `Po` | Punctuation, other |

### 💻 Interactive Mode

```bash
unicharx -i
```

**Interactive Commands:**

| Command | Function |
|---------|----------|
| `:cat [category]` | List characters by category |
| `:block [name]` | List characters by block |
| `:random` | Show random characters |
| `:categories` | List all categories |
| `:blocks` | List all blocks |
| `:help` | Show help |
| `quit` / `exit` | Exit interactive mode |

### 📤 Output Formats

```bash
# JSON output
unicharx heart --json

# Markdown table
unicharx star --markdown

# Verbose output
unicharx arrow -v
```

### 📋 Clipboard Operations

```bash
# Search and copy first result
unicharx heart --copy
```

---

## 💡 Design Philosophy

### 🏗️ Technical Architecture

```
UniCharX/
├── unicharx/
│   ├── __init__.py      # Package entry
│   ├── core.py          # Core search engine
│   └── cli.py           # Command-line interface
├── tests/
│   └── test_core.py     # Unit tests
├── pyproject.toml       # Project configuration
└── README.md            # Documentation
```

### 🔧 Core Modules

- **UniCharX Engine**: Unicode character indexing and search engine
- **CharInfo**: Character information data structure
- **CLI Interface**: Command-line argument parsing and output formatting

### 🎯 Design Principles

1. **Zero-dependency first**: Maximize use of Python standard library
2. **Performance optimization**: Character index caching, LRU cache
3. **Extensibility**: Modular design, easy to add new features
4. **User-friendly**: Rich command options, clear output formats

---

## 📦 Packaging and Deployment

### Local Packaging

```bash
# Build wheel package
pip install build
python -m build

# Install for testing
pip install dist/unicharx-1.0.0-py3-none-any.whl
```

### Publish to PyPI

```bash
pip install twine
twine upload dist/*
```

---

## 🤝 Contributing

Contributions, bug reports, and suggestions are welcome!

1. Fork this repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Create a Pull Request

---

## 📄 License

This project is licensed under the **MIT License**.

---

## 🙏 Acknowledgments

Inspired by the need for efficient Unicode character search tools. Thanks to the Python standard library for its powerful Unicode support.

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/gitstq">gitstq</a>
</p>
