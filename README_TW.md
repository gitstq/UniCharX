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
  <strong>輕量級Unicode字元智慧搜尋CLI引擎</strong><br>
  <sub>零依賴 • 模糊搜尋 • TUI儀表板 • 分類過濾</sub>
</p>

---

## 🎉 專案介紹

**UniCharX** 是一款**零依賴**、**跨平台**的Unicode字元智慧搜尋命令列工具。它幫助開發者、設計師和內容創作者快速查找、探索和使用Unicode字元。

### 🎯 解決的痛點

- 🔍 **字元查找困難**：在海量Unicode字元中快速定位目標字元
- 📝 **名稱記憶負擔**：支援模糊搜尋，無需記住精確名稱
- 🖥️ **終端工作流中斷**：無需離開終端即可完成字元查找
- 📋 **複製貼上繁瑣**：一鍵複製字元到剪貼簿

### ✨ 自研差異化亮點

- 🚀 **零依賴設計**：純Python標準庫實現，無需安裝額外依賴
- 🔮 **智慧模糊匹配**：基於編輯距離的模糊搜尋演算法
- 📊 **TUI儀表板**：支援Rich庫的美觀終端輸出
- 🏷️ **分類過濾**：按Unicode類別和區塊精確篩選
- 💡 **互動模式**：即時搜尋，即時回饋
- 📤 **多格式輸出**：支援JSON、Markdown、純文字輸出

---

## ✨ 核心特性

| 特性 | 描述 |
|------|------|
| 🔍 **智慧搜尋** | 支援精確匹配和模糊匹配，快速定位目標字元 |
| 📁 **分類瀏覽** | 按Unicode類別（符號、字母、數字等）瀏覽字元 |
| 🧱 **區塊篩選** | 按Unicode區塊（表情符號、數學符號等）過濾 |
| 💻 **互動模式** | 即時搜尋終端介面，支援命令操作 |
| 📋 **剪貼簿支援** | 一鍵複製字元到系統剪貼簿 |
| 📤 **多格式輸出** | JSON、Markdown、詳細文字等多種輸出格式 |
| 🎨 **彩色輸出** | 支援Rich庫的美觀終端顯示 |
| ⚡ **零依賴** | 僅使用Python標準庫，安裝即用 |

---

## 🚀 快速開始

### 📋 環境要求

- **Python 3.8+**
- 無需額外依賴（可選：`rich` 用於彩色輸出）

### 📦 安裝

```bash
# 從PyPI安裝（推薦）
pip install unicharx

# 從GitHub安裝
pip install git+https://github.com/gitstq/UniCharX.git

# 本地開發安裝
git clone https://github.com/gitstq/UniCharX.git
cd UniCharX
pip install -e .
```

### 🎮 基本使用

```bash
# 搜尋字元
unicharx heart

# 模糊搜尋
unicharx -f arrw

# 按類別過濾
unicharx -c Sm plus

# 互動模式
unicharx -i

# 查看字元詳情
unicharx --info U+2764

# 隨機字元
unicharx --random

# 列出所有類別
unicharx --categories

# 列出所有區塊
unicharx --blocks
```

---

## 📖 詳細使用指南

### 🔍 搜尋命令

```bash
# 基本搜尋
unicharx star

# 模糊搜尋（容錯拼寫）
unicharx -f hert
unicharx --fuzzy arw

# 設定模糊閾值
unicharx -f -t 0.5 hert

# 限制結果數量
unicharx arrow -l 10
```

### 📁 分類過濾

```bash
# 數學符號
unicharx -c Sm

# 貨幣符號
unicharx -c Sc

# 數字
unicharx -c Nd
```

**常用類別代碼：**

| 代碼 | 描述 |
|------|------|
| `Lu` | 大寫字母 |
| `Ll` | 小寫字母 |
| `Nd` | 十進位數字 |
| `Sm` | 數學符號 |
| `Sc` | 貨幣符號 |
| `So` | 其他符號 |
| `Po` | 標點符號 |

### 💻 互動模式

```bash
unicharx -i
```

**互動命令：**

| 命令 | 功能 |
|------|------|
| `:cat [類別]` | 按類別列出字元 |
| `:block [名稱]` | 按區塊列出字元 |
| `:random` | 顯示隨機字元 |
| `:categories` | 列出所有類別 |
| `:blocks` | 列出所有區塊 |
| `:help` | 顯示說明 |
| `quit` / `exit` | 退出互動模式 |

### 📤 輸出格式

```bash
# JSON輸出
unicharx heart --json

# Markdown表格
unicharx star --markdown

# 詳細輸出
unicharx arrow -v
```

### 📋 剪貼簿操作

```bash
# 搜尋並複製第一個結果
unicharx heart --copy
```

---

## 💡 設計思路

### 🏗️ 技術架構

```
UniCharX/
├── unicharx/
│   ├── __init__.py      # 套件入口
│   ├── core.py          # 核心搜尋引擎
│   └── cli.py           # 命令列介面
├── tests/
│   └── test_core.py     # 單元測試
├── pyproject.toml       # 專案配置
└── README.md            # 文件
```

### 🔧 核心模組

- **UniCharX Engine**：Unicode字元索引與搜尋引擎
- **CharInfo**：字元資訊資料結構
- **CLI Interface**：命令列參數解析與輸出格式化

### 🎯 設計原則

1. **零依賴優先**：最大化使用Python標準庫
2. **效能最佳化**：字元索引快取，LRU快取
3. **可擴展性**：模組化設計，易於添加新功能
4. **使用者友善**：豐富的命令選項，清晰的輸出格式

---

## 📦 打包與部署

### 本地打包

```bash
# 建構wheel包
pip install build
python -m build

# 安裝測試
pip install dist/unicharx-1.0.0-py3-none-any.whl
```

### 發布到PyPI

```bash
pip install twine
twine upload dist/*
```

---

## 🤝 貢獻指南

歡迎貢獻程式碼、報告問題或提出建議！

1. Fork 本儲存庫
2. 建立功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交變更 (`git commit -m 'feat: add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 建立 Pull Request

---

## 📄 開源協議

本專案採用 **MIT License** 開源協議。

---

## 🙏 致謝

靈感來源於對高效Unicode字元搜尋工具的需求，感謝Python標準庫提供的強大Unicode支援。

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/gitstq">gitstq</a>
</p>
