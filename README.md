# Xiaoyuzhou FM Podcast Downloader & Transcriber

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License">
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg" alt="Platform">
  <img src="https://img.shields.io/badge/GUI-PyQt5-orange.svg" alt="GUI Framework">
  <img src="https://img.shields.io/badge/Speech--Recognition-Whisper-purple.svg" alt="Speech Recognition">
</p>

<p align="center">
  <a href="README.zh.md">中文文档</a> | <a href="#english-documentation">English Documentation</a>
</p>

---

<a id="english-documentation"></a>

## 📖 Project Introduction

Xiaoyuzhou FM Podcast Downloader & Transcriber is a desktop application that allows users to download podcast audio from the Xiaoyuzhou platform and transcribe it into text or SRT subtitle format. The tool features a modern interface design, supports GPU-accelerated transcription, and provides a convenient solution for podcast enthusiasts and content creators.

## ✨ Key Features

- **Podcast Download**: One-click download of audio files via Xiaoyuzhou podcast links
- **Audio Playback**: Built-in simple player for previewing downloaded podcasts
- **Smart Transcription**: Convert audio to text using advanced speech recognition technology
- **Multiple Format Support**: Output in TXT plain text or SRT subtitle format
- **GPU Acceleration**: CUDA support for significantly faster transcription
- **Progress Display**: Real-time download and transcription progress
- **Beautiful Interface**: Modern UI design, simple and intuitive operation

## 🏗️ Project Architecture

```
xiaoyuzhou-podcast-tool/
├── main.py                 # Application entry point
├── requirements.txt        # Project dependencies
├── README.md              # English documentation
├── README.zh.md           # Chinese documentation
└── src/                   # Source code directory
    ├── download.py        # Podcast download functionality
    ├── transcribe.py      # Audio transcription functionality
    ├── ui/                # UI components
    │   ├── main_window.py # Main application window
    │   └── widgets.py     # Custom UI widgets
    ├── utils/             # Utility functions
    │   ├── audio.py       # Audio processing utilities
    │   └── config.py      # Configuration management
    └── resources/         # Application resources
        ├── icons/         # UI icons
        └── styles/        # CSS stylesheets
```

## 🛠️ Installation Guide

### Prerequisites

- Python 3.10
- Chrome browser (for Selenium driver)
- (Optional) NVIDIA GPU with CUDA support (for accelerated transcription)

### Installation Steps

1. **Clone or download this repository**

```bash
git clone https://github.com/AIResearcherHZ/Xiaoyuzhou-FM-Podcast-tool.git
cd Xiaoyuzhou-FM-Podcast-tool
```

2. **Create a virtual environment (recommended)**

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python -m venv venv
source venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Install Chrome WebDriver**

Ensure Chrome browser is installed, then download the appropriate ChromeDriver version from [the official site](https://sites.google.com/chromium.org/driver/) that matches your Chrome version.

Place the ChromeDriver executable in your system PATH or in the project directory.

5. **Run the application**

```bash
python main.py
```

## 📝 Usage Instructions

### Download Podcast

1. Copy a Xiaoyuzhou podcast link (e.g., https://www.xiaoyuzhoufm.com/episode/xxxx)
2. Paste it into the application's link input field
3. Click the "Start Download" button
4. Wait for the download to complete (progress will be displayed)

### Preview Playback

1. After downloading, the audio will be available in the player section
2. Use the play/pause, seek, and volume controls to preview the audio
3. The waveform visualization helps you navigate through the audio content

### Transcribe Audio

1. Select the running device (CPU or CUDA, if available)
2. Choose the output format (TXT or SRT)
3. Select the language model size (tiny, base, small, medium, large)
4. Click the "Start Transcription" button
5. Monitor the transcription progress in real-time

### Save Results

1. After transcription is complete, you can view the transcription results in the text area
2. Edit the text if needed (for corrections or formatting)
3. Click the "Save Transcription File" button to save locally
4. Choose your preferred save location and filename

## 🚀 Technology Stack

- **GUI Framework**: PyQt5
- **Audio Processing**: pydub
- **Web Scraping**: Selenium
- **Speech Recognition**: faster-whisper (based on OpenAI's Whisper model)
- **Parallel Processing**: PyQt QThread
- **HTTP Requests**: requests

## 🔮 Future Plans

- Support for batch downloading and transcription
- Add support for more podcast platforms
- Implement intelligent segmentation and speaker recognition in transcriptions
- Provide more language model options
- Develop cross-platform installation packages
- Add transcription result editing functionality
- Implement cloud storage integration
- Add subtitle synchronization tools
- Create a plugin system for extensibility

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Commit your changes**
   ```bash
   git commit -m 'Add some amazing feature'
   ```
4. **Push to the branch**
   ```bash
   git push origin feature/amazing-feature
   ```
5. **Open a Pull Request**

Please make sure to update tests as appropriate and follow the code style guidelines.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [OpenAI Whisper](https://github.com/openai/whisper) for the speech recognition model
- [faster-whisper](https://github.com/guillaumekln/faster-whisper) for the optimized Whisper implementation
- [PyQt5](https://www.riverbankcomputing.com/software/pyqt/) for the GUI framework
- [Selenium](https://www.selenium.dev/) for web automation
- [xiaoyuzhoufm](https://www.xiaoyuzhoufm.com/) for the amazing podcast platform
