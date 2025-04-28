# 小宇宙FM 播客下载与转录工具

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License">
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg" alt="Platform">
  <img src="https://img.shields.io/badge/GUI-PyQt5-orange.svg" alt="GUI框架">
  <img src="https://img.shields.io/badge/语音识别-Whisper-purple.svg" alt="语音识别">
</p>

<p align="center">
  <a href="README.md">English Documentation</a> | <a href="#中文文档">中文文档</a>
</p>

---

<a id="中文文档"></a>

### 📖 项目介绍

小宇宙FM播客下载与转录工具是一个桌面应用程序，允许用户从小宇宙平台下载播客音频，并将其转录为文本或SRT字幕格式。该工具采用现代化的界面设计，支持GPU加速转录，为播客爱好者和内容创作者提供了便捷的解决方案。

### ✨ 主要功能

- **播客下载**：通过小宇宙播客链接一键下载音频文件
- **音频播放**：内置简易播放器，可预览下载的播客
- **智能转录**：使用先进的语音识别技术将音频转录为文本
- **多格式支持**：支持TXT纯文本和SRT字幕格式输出
- **GPU加速**：支持CUDA加速，大幅提升转录速度
- **进度显示**：实时显示下载和转录进度
- **美观界面**：现代化UI设计，操作简单直观

## 🏗️ 项目架构

```
xiaoyuzhou-podcast-tool/
├── main.py                 # 应用程序入口点
├── requirements.txt        # 项目依赖
├── README.md              # 英文文档
├── README.zh.md           # 中文文档
└── src/                   # 源代码目录
    ├── download.py        # 播客下载功能
    ├── transcribe.py      # 音频转录功能
    ├── ui/                # UI组件
    │   ├── main_window.py # 主应用窗口
    │   └── widgets.py     # 自定义UI控件
    ├── utils/             # 实用工具函数
    │   ├── audio.py       # 音频处理工具
    │   └── config.py      # 配置管理
    └── resources/         # 应用资源
        ├── icons/         # UI图标
        └── styles/        # CSS样式表
```

### 🛠️ 安装指南

#### 前置要求

- Python 3.10
- Chrome浏览器（用于Selenium驱动）
- （可选）NVIDIA GPU 及 CUDA 支持（用于加速转录）

#### 安装步骤

1. **克隆或下载本仓库**

```bash
git clone https://github.com/AIResearcherHZ/Xiaoyuzhou-FM-Podcast-tool.git
cd Xiaoyuzhou-FM-Podcast-tool
```

2. **创建虚拟环境（推荐）**

```bash
# Windows系统
python -m venv venv
venv\Scripts\activate

# macOS/Linux系统
python -m venv venv
source venv/bin/activate
```

3. **安装依赖包**

```bash
pip install -r requirements.txt
```

4. **安装Chrome WebDriver**

确保已安装Chrome浏览器，然后从[官方网站](https://sites.google.com/chromium.org/driver/)下载与您的Chrome版本匹配的ChromeDriver。

将ChromeDriver可执行文件放置在系统PATH中或项目目录中。

5. **运行应用程序**

```bash
python main.py
```

## 📝 使用方法

### 下载播客

1. 复制小宇宙播客链接（例如：https://www.xiaoyuzhoufm.com/episode/xxxx）
2. 粘贴到应用程序的链接输入框
3. 点击"开始下载"按钮
4. 等待下载完成（将显示进度）

### 播放预览

1. 下载完成后，音频将在播放器部分可用
2. 使用播放/暂停、进度条和音量控制预览音频
3. 波形可视化帮助您浏览音频内容

### 转录音频

1. 选择运行设备（CPU或CUDA，如果可用）
2. 选择输出格式（TXT或SRT）
3. 选择语言模型大小（tiny、base、small、medium、large）
4. 点击"开始转录"按钮
5. 实时监控转录进度

### 保存结果

1. 转录完成后，您可以在文本区域查看转录结果
2. 如有需要，可以编辑文本（用于修正或格式化）
3. 点击"保存转录文件"按钮保存到本地
4. 选择您偏好的保存位置和文件名

### 🚀 技术栈

- **GUI框架**：PyQt5
- **音频处理**：pydub
- **网页抓取**：Selenium
- **语音识别**：faster-whisper（基于OpenAI的Whisper模型）
- **并行处理**：PyQt QThread
- **HTTP请求**：requests

## 🔮 未来计划

- 支持批量下载和转录
- 添加更多播客平台支持
- 实现转录文本的智能分段和说话人识别
- 提供更多语言模型选择
- 开发跨平台安装包
- 添加转录结果编辑功能
- 实现云存储集成
- 添加字幕同步工具
- 创建插件系统以提高扩展性

## 🤝 贡献指南

欢迎贡献！以下是您可以提供帮助的方式：

1. **Fork 仓库**
2. **创建特性分支**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **提交您的更改**
   ```bash
   git commit -m '添加一些很棒的特性'
   ```
4. **推送到分支**
   ```bash
   git push origin feature/amazing-feature
   ```
5. **提交 Pull Request**

请确保适当地更新测试，并遵循代码风格指南。

## ✨ 灵感来源

这个项目的灵感来源于播客爱好者对内容归档和检索的需求。小宇宙作为中文世界最大的播客平台之一，拥有丰富的内容资源，但缺乏便捷的下载和转录工具。本项目旨在填补这一空白，让用户能够更方便地保存和利用播客内容。

## 📄 许可证

本项目采用 MIT 许可证 - 详情请参阅 [LICENSE](LICENSE) 文件。

## 🙏 致谢

- [OpenAI Whisper](https://github.com/openai/whisper) 提供语音识别模型
- [faster-whisper](https://github.com/guillaumekln/faster-whisper) 提供优化的Whisper实现
- [PyQt5](https://www.riverbankcomputing.com/software/pyqt/) 提供GUI框架
- [Selenium](https://www.selenium.dev/) 提供网页自动化
- [小宇宙FM](https://www.xiaoyuzhoufm.com/) 提供优质的播客平台
