import sys
import os
import time
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QPushButton, QLabel, QLineEdit, QProgressBar, QComboBox,
                             QTextEdit, QFileDialog, QGroupBox, QRadioButton, QMessageBox
                             )
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QUrl
from PyQt5.QtGui import QFont
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from pydub import AudioSegment

from src.download import fetch_audio_file
from src.transcribe import transcribe_audio

# 检测CUDA是否可用
def is_cuda_available():
    try:
        import torch
        return torch.cuda.is_available()
    except ImportError:
        return False


class DownloadThread(QThread):
    progress_signal = pyqtSignal(float)
    finished_signal = pyqtSignal(str, str)
    error_signal = pyqtSignal(str)
    
    def __init__(self, url):
        super().__init__()
        self.url = url
        
    def run(self):
        try:
            def update_progress(progress):
                self.progress_signal.emit(progress)
                
            audio_path, podcast_title = fetch_audio_file(self.url, update_progress)
            self.finished_signal.emit(audio_path, podcast_title)
        except Exception as e:
            self.error_signal.emit(str(e))


class TranscribeThread(QThread):
    progress_signal = pyqtSignal(str)
    finished_signal = pyqtSignal(str, float)
    error_signal = pyqtSignal(str)
    
    def __init__(self, audio_path, output_format, device):
        super().__init__()
        self.audio_path = audio_path
        self.output_format = output_format
        self.device = device
        
    def run(self):
        try:
            self.progress_signal.emit("转录中...")
            start_time = time.time()
            
            # 设置输出文件名
            podcast_title = os.path.basename(self.audio_path).split('-')[0]
            output_file = f"{podcast_title}.{self.output_format}"
            
            # 开始转录
            transcribe_audio(
                self.audio_path,
                output_file,
                self.output_format,
                self.device
            )
            
            # 计算耗时
            elapsed_time = time.time() - start_time
            
            # 读取转录结果
            with open(output_file, "r", encoding="utf-8") as f:
                transcript = f.read()
                
            self.finished_signal.emit(transcript, elapsed_time)
        except Exception as e:
            self.error_signal.emit(str(e))


def format_duration(seconds):
    """将秒数转换为可读的时分秒格式"""
    seconds = round(seconds)  # 四舍五入到整数秒
    
    hours = seconds // 3600
    remaining = seconds % 3600
    minutes = remaining // 60
    seconds = remaining % 60
    
    time_parts = []
    if hours > 0:
        time_parts.append(f"{hours}小时")
    if minutes > 0 or hours > 0:  # 如果有小时也显示分钟
        time_parts.append(f"{minutes}分")
    time_parts.append(f"{seconds}秒")
    
    return "".join(time_parts)


class PodcastApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.audio_path = None
        self.podcast_title = None
        self.transcript = None
        self.media_player = QMediaPlayer()
        
        self.init_ui()
        
    def init_ui(self):
        # 设置窗口属性
        self.setWindowTitle("小宇宙FM 播客下载与转录工具")
        self.setGeometry(100, 100, 900, 700)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QGroupBox {
                border: 1px solid #cccccc;
                border-radius: 5px;
                margin-top: 10px;
                font-weight: bold;
                background-color: white;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
            }
            QPushButton {
                background-color: #4a86e8;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #3a76d8;
            }
            QPushButton:disabled {
                background-color: #cccccc;
            }
            QLineEdit, QTextEdit, QComboBox {
                border: 1px solid #cccccc;
                border-radius: 4px;
                padding: 5px;
                background-color: white;
            }
            QProgressBar {
                border: 1px solid #cccccc;
                border-radius: 4px;
                text-align: center;
                background-color: white;
            }
            QProgressBar::chunk {
                background-color: #4a86e8;
                width: 10px;
                margin: 0.5px;
            }
            QLabel {
                color: #333333;
            }
        """)
        
        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # 标题标签
        title_label = QLabel("小宇宙FM 播客下载与转录工具")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("margin-bottom: 15px; color: #4a86e8;")
        main_layout.addWidget(title_label)
        
        # 下载部分
        download_group = QGroupBox("第一步：下载播客")
        download_layout = QVBoxLayout(download_group)
        download_layout.setContentsMargins(15, 20, 15, 15)
        download_layout.setSpacing(10)
        
        # URL输入
        url_layout = QHBoxLayout()
        url_label = QLabel("请输入小宇宙播客链接：")
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("粘贴小宇宙播客链接到这里...")
        url_layout.addWidget(url_label)
        url_layout.addWidget(self.url_input)
        download_layout.addLayout(url_layout)
        
        # 下载按钮和进度条
        download_progress_layout = QHBoxLayout()
        self.download_btn = QPushButton("开始下载")
        self.download_btn.clicked.connect(self.start_download)
        self.download_progress = QProgressBar()
        self.download_progress.setRange(0, 100)
        self.download_progress.setValue(0)
        download_progress_layout.addWidget(self.download_btn)
        download_progress_layout.addWidget(self.download_progress)
        download_layout.addLayout(download_progress_layout)
        
        # 下载状态
        self.download_status = QLabel("")
        download_layout.addWidget(self.download_status)
        
        main_layout.addWidget(download_group)
        
        # 音频信息部分
        self.audio_info_group = QGroupBox("播客信息")
        self.audio_info_group.setVisible(False)
        audio_info_layout = QVBoxLayout(self.audio_info_group)
        audio_info_layout.setContentsMargins(15, 20, 15, 15)
        
        self.podcast_title_label = QLabel()
        self.audio_length_label = QLabel()
        self.audio_size_label = QLabel()
        
        audio_info_layout.addWidget(self.podcast_title_label)
        audio_info_layout.addWidget(self.audio_length_label)
        audio_info_layout.addWidget(self.audio_size_label)
        
        # 音频播放控制
        audio_controls_layout = QHBoxLayout()
        self.play_btn = QPushButton("播放")
        self.play_btn.clicked.connect(self.toggle_play)
        audio_controls_layout.addWidget(self.play_btn)
        audio_info_layout.addLayout(audio_controls_layout)
        
        main_layout.addWidget(self.audio_info_group)
        
        # 转录部分
        transcribe_group = QGroupBox("第二步：转录音频")
        transcribe_layout = QVBoxLayout(transcribe_group)
        transcribe_layout.setContentsMargins(15, 20, 15, 15)
        transcribe_layout.setSpacing(10)
        
        # 提示信息
        transcribe_info = QLabel("提示: CPU模式下一分钟的音频大约需要10秒钟转录时间，CUDA模式下约需3-4秒")
        transcribe_info.setStyleSheet("color: #666666; font-style: italic;")
        transcribe_layout.addWidget(transcribe_info)
        
        # 设备和格式选择
        options_layout = QHBoxLayout()
        
        device_layout = QVBoxLayout()
        device_label = QLabel("选择运行设备：")
        self.device_combo = QComboBox()
        self.device_combo.addItem("CPU")
        
        # 检测并添加CUDA选项
        if is_cuda_available():
            self.device_combo.addItem("CUDA")
            cuda_info = QLabel("检测到CUDA可用，使用GPU可加速转录")
            cuda_info.setStyleSheet("color: green; font-style: italic;")
            device_layout.addWidget(cuda_info)
        
        device_layout.addWidget(device_label)
        device_layout.addWidget(self.device_combo)
        options_layout.addLayout(device_layout)
        
        format_layout = QVBoxLayout()
        format_label = QLabel("选择输出格式：")
        self.format_layout = QHBoxLayout()
        self.txt_radio = QRadioButton("TXT")
        self.srt_radio = QRadioButton("SRT")
        self.txt_radio.setChecked(True)
        self.format_layout.addWidget(self.txt_radio)
        self.format_layout.addWidget(self.srt_radio)
        format_layout.addWidget(format_label)
        format_layout.addLayout(self.format_layout)
        options_layout.addLayout(format_layout)
        
        transcribe_layout.addLayout(options_layout)
        
        # 转录按钮
        self.transcribe_btn = QPushButton("开始转录")
        self.transcribe_btn.setEnabled(False)
        self.transcribe_btn.clicked.connect(self.start_transcribe)
        transcribe_layout.addWidget(self.transcribe_btn)
        
        # 转录状态
        self.transcribe_status = QLabel("")
        transcribe_layout.addWidget(self.transcribe_status)
        
        main_layout.addWidget(transcribe_group)
        
        # 转录结果
        result_group = QGroupBox("转录结果")
        result_layout = QVBoxLayout(result_group)
        result_layout.setContentsMargins(15, 20, 15, 15)
        
        self.transcript_text = QTextEdit()
        self.transcript_text.setReadOnly(True)
        self.transcript_text.setPlaceholderText("转录结果将显示在这里...")
        result_layout.addWidget(self.transcript_text)
        
        # 保存按钮
        self.save_btn = QPushButton("保存转录文件")
        self.save_btn.setEnabled(False)
        self.save_btn.clicked.connect(self.save_transcript)
        result_layout.addWidget(self.save_btn)
        
        main_layout.addWidget(result_group)
        
        # 设置各部分的比例
        main_layout.setStretch(0, 0)  # 标题
        main_layout.setStretch(1, 1)  # 下载部分
        main_layout.setStretch(2, 1)  # 音频信息
        main_layout.setStretch(3, 2)  # 转录部分
        main_layout.setStretch(4, 3)  # 转录结果
    
    def start_download(self):
        url = self.url_input.text().strip()
        if not url:
            QMessageBox.warning(self, "警告", "请输入有效的播客链接")
            return
        
        # 禁用下载按钮，防止重复点击
        self.download_btn.setEnabled(False)
        self.download_status.setText("正在下载...")
        self.download_progress.setValue(0)
        
        # 创建并启动下载线程
        self.download_thread = DownloadThread(url)
        self.download_thread.progress_signal.connect(self.update_download_progress)
        self.download_thread.finished_signal.connect(self.download_finished)
        self.download_thread.error_signal.connect(self.download_error)
        self.download_thread.start()
    
    def update_download_progress(self, progress):
        self.download_progress.setValue(int(progress * 100))
    
    def download_finished(self, audio_path, podcast_title):
        self.audio_path = audio_path
        self.podcast_title = podcast_title
        
        # 更新UI
        self.download_status.setText("下载完成！")
        self.download_btn.setEnabled(True)
        
        # 显示音频信息
        self.podcast_title_label.setText(f"播客标题：{podcast_title}")
        
        # 获取音频时长和大小
        audio = AudioSegment.from_file(audio_path)
        duration = audio.duration_seconds
        readable_duration = format_duration(duration)
        file_size_mb = os.path.getsize(audio_path) / 1024 / 1024
        
        self.audio_length_label.setText(f"音频长度：{readable_duration}")
        self.audio_size_label.setText(f"音频大小：{file_size_mb:.2f} MB")
        
        # 设置媒体播放器
        self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(audio_path)))
        
        # 显示音频信息组件并启用转录按钮
        self.audio_info_group.setVisible(True)
        self.transcribe_btn.setEnabled(True)
    
    def download_error(self, error_msg):
        self.download_status.setText(f"下载失败：{error_msg}")
        self.download_btn.setEnabled(True)
        QMessageBox.critical(self, "错误", f"下载失败：{error_msg}")
    
    def toggle_play(self):
        if self.media_player.state() == QMediaPlayer.PlayingState:
            self.media_player.pause()
            self.play_btn.setText("播放")
        else:
            self.media_player.play()
            self.play_btn.setText("暂停")
    
    def start_transcribe(self):
        if not self.audio_path:
            QMessageBox.warning(self, "警告", "请先下载播客")
            return
        
        # 禁用转录按钮，防止重复点击
        self.transcribe_btn.setEnabled(False)
        self.transcribe_status.setText("准备转录...")
        
        # 获取选项
        device = self.device_combo.currentText().lower()
        output_format = "txt" if self.txt_radio.isChecked() else "srt"
        
        # 创建并启动转录线程
        self.transcribe_thread = TranscribeThread(self.audio_path, output_format, device)
        self.transcribe_thread.progress_signal.connect(self.update_transcribe_status)
        self.transcribe_thread.finished_signal.connect(self.transcribe_finished)
        self.transcribe_thread.error_signal.connect(self.transcribe_error)
        self.transcribe_thread.start()
        
        # 显示预计时间
        audio = AudioSegment.from_file(self.audio_path)
        audio_length_minutes = audio.duration_seconds / 60
        
        # 根据设备类型调整预计时间（GPU加速约为CPU的3倍）
        time_factor = 2 if device == "cuda" else 6  # CUDA设备每分钟约2秒，CPU每分钟约6秒
        estimated_time = audio_length_minutes * time_factor
        
        self.transcribe_status.setText(f"转录中... 预计需要 {estimated_time/60:.2f} 分钟")
    
    def update_transcribe_status(self, status):
        self.transcribe_status.setText(status)
    
    def transcribe_finished(self, transcript, elapsed_time):
        self.transcript = transcript
        
        # 更新UI
        self.transcribe_status.setText(f"转录完成！耗时：{elapsed_time:.2f}秒")
        self.transcribe_btn.setEnabled(True)
        
        # 显示转录结果
        self.transcript_text.setText(transcript)
        self.save_btn.setEnabled(True)
    
    def transcribe_error(self, error_msg):
        self.transcribe_status.setText(f"转录失败：{error_msg}")
        self.transcribe_btn.setEnabled(True)
        QMessageBox.critical(self, "错误", f"转录失败：{error_msg}")
    
    def save_transcript(self):
        if not self.transcript:
            return
        
        # 获取保存路径
        output_format = "txt" if self.txt_radio.isChecked() else "srt"
        default_name = f"{self.podcast_title}.{output_format}"
        file_path, _ = QFileDialog.getSaveFileName(
            self, "保存转录文件", default_name, f"文本文件 (*.{output_format})")
        
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(self.transcript)
                QMessageBox.information(self, "成功", f"转录文件已保存到：{file_path}")
            except Exception as e:
                QMessageBox.critical(self, "错误", f"保存失败：{str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PodcastApp()
    window.show()
    sys.exit(app.exec_())