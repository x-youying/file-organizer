import sys
import os
import base64
import pandas as pd
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QPushButton, QLabel, QFileDialog, 
                            QTableWidget, QTableWidgetItem, QMessageBox, 
                            QComboBox, QLineEdit, QGroupBox, QCheckBox, 
                            QTextEdit, QSplitter, QMenu, QMenuBar)
from PyQt6.QtCore import Qt, QUrl, QByteArray
from PyQt6.QtGui import QDesktopServices, QPixmap, QIcon
import shutil
from pathlib import Path
from datetime import datetime

class FileOrganizerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("文件整理工具1.0")
        self.setGeometry(100, 100, 1200, 800)
        
        # 添加菜单栏
        self.create_menu_bar()
        
        # 初始化变量
        self.excel_path = None
        self.folder_path = None
        self.duplicate_files = []
        self.selected_columns = {} 
        self.name_format = "{name}" 
        self.duplicate_rules = [] 
        self.duplicate_handle_mode = "rename" 
        
        self.init_ui()
        self.set_icon()

    def set_icon(self):
        base64_icon_str = "AAABAAEAgIAAAAEAIAAoCAEAFgAAACgAAACAAAAAAAEAAAEAIAAAAAAAAAABAHudAAB7nQAAAAAAAAAAAAD///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Avv7+wLy8vIC9PT0Avb29gL19fUC9fX1AvX19QL19fUC9fX1AvX19QL19fUC9fX1AvX19QL19fUC9fX1AvX19QL19fUC9fX1AvX19QL19fUC9fX1AvX19QL19fUC9fX1AvX19QL19fUC9fX1AvX19QL19fUC9fX1AvX19QL19fUC9fX1AvX19QL19fUC9fX1AvX19QL19fUC9fX1AvX19QL19fUC9fX1AvX19QL19fUC9fX1AvX19QL19fUC9fX1AvX19QL19fUC9fX1AvX19QL19fUC9fX1AvX19QL19fUC9fX1AvX19QL19fUC9fX1AvX19QL19fUC9fX1AvX19QL19fUC9fX1AvX19QL19fUC9fX1AvX19QL19fUC9fX1AvX19QL19fUC9fX1AvX19QL19fUC9fX1AvX19QL19fUC9fX1AvX19QL19fUC9fX1AvX19QL19fUC9fX1AvX19QL19fUC9fX1AvX19QL19fUC9fX1AvX19QL19fUC9fX1AvX19QL19fUC+vr6Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL9/f0C////Au3t7QJnZ2cFVlZWBm5ubgVpaWkFZGRkBWRkZAVkZGQFZGRkBWRkZAVkZGQFZGRkBWRkZAVkZGQFZGRkBWRkZAVkZGQFZGRkBWRkZAVkZGQFZGRkBWRkZAVkZGQFZGRkBWRkZAVkZGQFZGRkBWRkZAVkZGQFZGRkBWRkZAVkZGQFZGRkBWRkZAVkZGQFZGRkBWRkZAVkZGQFZGRkBWRkZAVkZGQFZGRkBWRkZAVkZGQFZGRkBWRkZAVkZGQFZGRkBWRkZAVkZGQFZGRkBWRkZAVkZGQFZGRkBWRkZAVkZGQFZGRkBWRkZAVkZGQFZGRkBWRkZAVkZGQFZGRkBWRkZAVkZGQFZGRkBWRkZAVkZGQFZGRkBWRkZAVkZGQFZGRkBWRkZAVkZGQFZGRkBWRkZAVkZGQFZGRkBWRkZAVkZGQFZGRkBWRkZAVkZGQFZGRkBWRkZAVkZGQFZGRkBWRkZAVkZGQFZGRkBWRkZAVkZGQFZGRkBWRkZAVkZGQFZGRkBWRkZAVkZGQFZGRkBWVlZQVYWFgGXFxcBcPDwwP///8C/Pz8Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C+/v7Av///wKqqqoDYGBgBEtLSwBRUVEAenp6AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAGRkZABXV1cAYWFhA4iIiAT///8C+fn5Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av39/QL///8CxMTEA2lpaQMAAAAABwcHQAICApQBAQG3AQEBsQEBAakBAQGqAQEBqgEBAaoBAQGqAQEBqgEBAaoBAQGqAQEBqgEBAaoBAQGqAQEBqgEBAaoBAQGqAQEBqgEBAaoBAQGqAQEBqgEBAaoBAQGqAQEBqgEBAaoBAQGqAQEBqgEBAaoBAQGqAQEBqgEBAaoBAQGqAQEBqgEBAaoBAQGqAQEBqgEBAaoBAQGqAQEBqgEBAaoBAQGqAQEBqgEBAaoBAQGqAQEBqgEBAaoBAQGqAQEBqgEBAaoBAQGqAQEBqgEBAaoBAQGqAQEBqgEBAaoBAQGqAQEBqgEBAaoBAQGqAQEBqgEBAaoBAQGqAQEBqgEBAaoBAQGqAQEBqgEBAaoBAQGqAQEBqgEBAaoBAQGqAQEBqgEBAaoBAQGqAQEBqgEBAaoBAQGqAQEBqgEBAaoBAQGqAQEBqgEBAaoBAQGqAQEBqgEBAaoBAQGqAQEBqgEBAaoBAQGqAQEBqgEBAaoBAQGqAQEBqgEBAaoBAQGqAQEBqgEBAakBAQGqAQEBmQUFBVYdHR0I////AJOTkwT///8C+vr6Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C/Pz8AsHBwQP///8BISEhCAEBAaQAAAD/AAAA/gAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD+AAAA/wEBAc4ICAgjAAAAAI2NjQT///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wLh4eECj4+PBAAAAAABAQGjAAAA/wAAAPoAAAD7AAAA/AAAAPwAAAD8AAAA/AAAAPwAAAD8AAAA/AAAAPwAAAD8AAAA/AAAAPwAAAD8AAAA/AAAAPwAAAD8AAAA/AAAAPwAAAD8AAAA/AAAAPwAAAD8AAAA/AAAAPwAAAD8AAAA/AAAAPwAAAD8AAAA/AAAAPwAAAD8AAAA/AAAAPwAAAD8AAAA/AAAAPwAAAD8AAAA/AAAAPwAAAD8AAAA/AAAAPwAAAD8AAAA/AAAAPwAAAD8AAAA/AAAAPwAAAD8AAAA/AAAAPwAAAD8AAAA/AAAAPwAAAD8AAAA/AAAAPwAAAD8AAAA/AAAAPwAAAD8AAAA/AAAAPwAAAD8AAAA/AAAAPwAAAD8AAAA/AAAAPwAAAD8AAAA/AAAAPwAAAD8AAAA/AAAAPwAAAD8AAAA/AAAAPwAAAD8AAAA/AAAAPwAAAD8AAAA/AAAAPwAAAD8AAAA/AAAAPwAAAD8AAAA/AAAAPwAAAD8AAAA/AAAAPwAAAD8AAAA/AAAAPwAAAD8AAAA/AAAAPsAAAD7AAAA/wAAANkQEBATAAAAAKKiogP+/v4C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////AmpqagUAAAAABAQEQwAAAP8AAAD7AAAA/gAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD5AAAA/wEBAYYAAAAAX19fBfn5+QL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL7+/sCV1dXBgAAAAACAgKSAAAA/wAAAPsAAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP0AAAD/AAAA03p6egP///8BxcXFA////wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////AvLy8gJubm4FAAAAAAEBAbcAAAD/AAAA/AAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/gAAAP8AAAD2CgoKIAAAAACKiooE////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C9PT0AmlpaQUAAAAAAQEBsQAAAP8AAAD8AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/QAAAP8EBARJAAAAAGNjYwX///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL19fUCZGRkBQAAAAABAQGpAAAA/wAAAPwAAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD7AAAA/wICAnkAAAAAU1NTBv7+/gL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////AvX19QJkZGQFAAAAAAEBAaoAAAD/AAAA/AAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wEAAP8BAQD/AQEA/wEBAP8BAQD/AQEA/wEBAP8BAQD/AQEA/wEBAP8BAQD/AQEA/wEBAP8BAQD/AQEA/wEBAP8BAQD/AQEA/wEBAP8BAQD/AQEA/wEBAP8BAQD/AQEA/wEBAP8BAQD/AQEA/wEBAP8BAQD/AQEA/wEBAP8BAQD/AQEA/wEBAP8BAQD/AQEA/wEBAP8BAQD/AQEA/wEBAP8BAQD/AQEA/wEBAP8BAQD/AQEA/wEBAP8BAQD/AQEA/wEBAP8BAQD/AQEA/wEBAP8BAQD/AQEA/wEBAP8BAQD/AQEA/wEBAP8BAQD/AQEA/wEBAP8BAQD/AQEA/wEBAP8BAQD/AQEA/wEBAP8BAQD/AQEA/wEBAP8BAQD/AQEA/wEBAP8BAQD/AQEA/wEBAP8BAQD/AQEA/wEBAP8BAQD/AQEA/wEBAP8BAQD/AQEA/wEBAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAPwAAAD/AAAAqgAAAABoaGgF8/PzAv///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C9fX1AmRkZAUAAAAAAQEBqgAAAP8AAAD8AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/QAAAP8AAADVY2NjBP///wHDw8MD////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL19fUCZGRkBQAAAAABAQGqAAAA/wAAAPwAAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8KBQL/EgkD/xAJA/8RCQP/EQkD/xEJA/8RCQP/EQkD/xEJA/8RCQP/EQkD/xEJA/8RCQP/EQkD/xEJA/8RCQP/EQkD/xEJA/8RCQP/EQkD/xEJA/8RCQP/EQkD/xEJA/8RCQP/EQkD/xEJA/8RCQP/EQkD/xEJA/8RCQP/EQkD/xEJA/8RCQP/EQkD/xEJA/8RCQP/EQkD/xEJA/8RCQP/EQkD/xEJA/8RCQP/EQkD/xEJA/8RCQP/EQkD/xEJA/8RCQP/EQkD/xEJA/8RCQP/EQkD/xEJA/8RCQP/EQkD/xEJA/8RCQP/EQkD/xEJA/8RCQP/EQkD/xEJA/8RCQP/EQkD/xEJA/8RCQP/EQkD/xEJA/8RCQP/EQkD/xEJA/8RCQP/EQkD/xEJA/8RCQP/EQkD/xEJA/8RCQP/EQkD/xEJA/8RCQP/EAkD/xAJA/8RCQP/BQIB/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD+AAAA/wAAAPYKCgogAAAAAIqKigT///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////AvX19QJkZGQFAAAAAAEBAaoAAAD/AAAA/AAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8EAgH/AAAA/1owEf/9hy//630r/+5/LP/ufyz/7n8s/+5/LP/ufyz/7n8s/+5/LP/ufyz/7n8s/+5/LP/ufyz/7n8s/+5/LP/ufyz/7n8s/+5/LP/ufyz/7n8s/+5/LP/ufyz/7n8s/+5/LP/ufyz/7n8s/+5/LP/ufyz/7n8s/+5/LP/ufyz/7n8s/+5/LP/ufyz/7n8s/+5/LP/ufyz/7n8s/+5/LP/ufyz/7n8s/+5/LP/ufyz/7n8s/+5/LP/ufyz/7n8s/+5/LP/ufyz/7n8s/+5/LP/ufyz/7n8s/+5/LP/ufyz/7n8s/+5/LP/ufyz/7n8s/+5/LP/ufyz/7n8s/+5/LP/ufyz/7n8s/+5/LP/ufyz/7n8s/+5/LP/ufyz/7n8s/+5/LP/ufyz/7n8s/+5/LP/ufyz/7n8s/+5/LP/ufyz/7n8s/+5/LP/ufyz/630r//2HL/9gMxL/AAAA/wQCAf8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD9AAAA/wQEBEkAAAAAY2NjBf///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C9fX1AmRkZAUAAAAAAQEBqgAAAP8AAAD8AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wIBAP8AAAD/KhcI//2KMP//izD//oow//+KMP//ijD//4ow//+KMP//ijD//4ow//+KMP//ijD//4ow//+KMP//ijD//4ow//+KMP//ijD//4ow//+KMP//ijD//4ow//+KMP//ijD//4ow//+KMP//ijD//4ow//+KMP//ijD//4ow//+KMP//ijD//4ow//+KMP//ijD//4ow//+KMP//ijD//4ow//+KMP//ijD//4ow//+KMP//ijD//4ow//+KMP//ijD//4ow//+KMP//ijD//4ow//+KMP//ijD//4ow//+KMP//ijD//4ow//+KMP//ijD//4ow//+KMP//ijD//4ow//+KMP//ijD//4ow//+KMP//ijD//4ow//+KMP//ijD//4ow//+KMP//ijD//4ow//+KMP//ijD//4ow//+KMP//ijD//4ow//+KMP/7iC///5Qz/5dSHP8AAAD/BAIB/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAPsAAAD/AgICeQAAAABTU1MG/v7+Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL19fUCZGRkBQAAAAABAQGqAAAA/wAAAPwAAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AQAA/wAAAP8DAgH/1XMo//+MMP/8hi7//ocv//6HL//+hy///ocv//6HL//+hy///ocv//6HL//+hy///ocv//6HL//+hy///ocv//6HL//+hy///ocv//6HL//+hy///ocv//6HL//+hy///ocv//6HL//+hy///ocv//6HL//+hy///ocv//6HL//+hy///ocv//6HL//+hy///ocv//6HL//+hy///ocv//6HL//+hy///ocv//6HL//+hy///ocv//6HL//+hy///ocv//6HL//+hy///ocv//6HL//+hy///ocv//6HL//+hy///ocv//6HL//+hy///ocv//6HL//+hy///ocv//6HL//+hy///ocv//6HL//+hy///ocv//6HL//+hy///ocv//6HL//+hy///ocv//6HL//+hy///ocv//6HL//+hy///ocv//uGLv//jjH/xmol/wAAAP8BAQD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/AAAAP8AAACqAAAAAGhoaAXz8/MC////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////AvX19QJkZGQFAAAAAAEBAaoAAAD/AAAA/AAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AwIB/wAAAP+fVh7//5Ey//uGLv//iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///ocv//+LMP/sfiv/EQkD/wAAAP8BAQD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD9AAAA/wAAANVjY2ME////AcPDwwP///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C9fX1AmRkZAUAAAAAAQEBqgAAAP8AAAD8AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8EAgH/AAAA/2E1Ev//kTL//IYu//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///ogv//+LMP82HQr/AAAA/wMBAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP4AAAD/AAAA9goKCiAAAAAAioqKBP///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL19fUCZGRkBQAAAAABAQGqAAAA/wAAAPwAAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wIBAP8AAAD/KhcI//yHL///iC///ogv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL//8hi7//5Ey/2U3E/8AAAD/BAIB/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP0AAAD/BAQESQAAAABjY2MF////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////AvX19QJkZGQFAAAAAAEBAaoAAAD/AAAA/AAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AQAA/wAAAP8DAgH/1nMo//+NMf/9hy///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//uGLv//kTL/l1Ec/wAAAP8EAgH/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA+wAAAP8CAgJ5AAAAAFNTUwb+/v4C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C9fX1AmRkZAUAAAAAAQEBqgAAAP8AAAD8AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AwIB/wAAAP+fVh7//5Ey//uGLv//iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///Icv//+OMf/GaiX/AAAA/wEBAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD8AAAA/wAAAKoAAAAAaGhoBfPz8wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL19fUCZGRkBQAAAAABAQGqAAAA/wAAAPwAAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8EAgH/AAAA/2E1Ev//kTL//IYu//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL//+hy///4sw/+x+K/8RCQP/AAAA/wEBAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP0AAAD/AAAA1WNjYwT///8Bw8PDA////wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////AvX19QJkZGQFAAAAAAEBAaoAAAD/AAAA/AAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wIBAP8AAAD/KhcI//yHL///iC///ogv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL//+iC///4sw/zYdCv8AAAD/AwEA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/gAAAP8AAAD2CgoKIAAAAACKiooE////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C9fX1AmRkZAUAAAAAAQEBqgAAAP8AAAD8AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AQAA/wAAAP8DAgH/1nMo//+NMf/9hy///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//yGLv//kTL/ZTcT/wAAAP8EAgH/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/QAAAP8EBARJAAAAAGNjYwX///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL19fUCZGRkBQAAAAABAQGqAAAA/wAAAPwAAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AwIB/wAAAP+fVh7//5Ey//uGLv//iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC//+4Yu//+RMv+XURz/AAAA/wQCAf8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD7AAAA/wICAnkAAAAAU1NTBv7+/gL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////AvX19QJkZGQFAAAAAAEBAaoAAAD/AAAA/AAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8EAgH/AAAA/2E1Ev//kTL//IYu//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL//8hy///44x/8dqJf8AAAD/AQEA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAPwAAAD/AAAAqgAAAABoaGgF8/PzAv///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C9fX1AmRkZAUAAAAAAQEBqgAAAP8AAAD8AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wIBAP8AAAD/KhcI//yHL///iC///ogv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//6HL///izD/7H4r/xEJA/8AAAD/AQEA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/QAAAP8AAADVY2NjBP///wHDw8MD////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL19fUCZGRkBQAAAAABAQGqAAAA/wAAAPwAAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AQAA/wAAAP8DAgH/1nMo//+NMf/9hy///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//6IL///izD/Nh0K/wAAAP8DAQD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD+AAAA/wAAAPYKCgogAAAAAIqKigT///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////AvX19QJkZGQFAAAAAAEBAaoAAAD/AAAA/AAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AwIB/wAAAP+fVh7//5Ey//uGLv//iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///IYu//+RMv9lNxP/AAAA/wQCAf8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD9AAAA/wQEBEkAAAAAY2NjBf///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C9fX1AmRkZAUAAAAAAQEBqgAAAP8AAAD8AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8EAgH/AAAA/2E1Ev//kTL//IYu//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL//7hi7//5Ey/5dRHP8AAAD/BAIB/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAPsAAAD/AgICeQAAAABTU1MG/v7+Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL19fUCZGRkBQAAAAABAQGqAAAA/wAAAPwAAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wIBAP8AAAD/KhcI//yHL///iC///ogv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//yHL///jjH/x2ol/wAAAP8BAQD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/AAAAP8AAACqAAAAAGhoaAXz8/MC////Av///wL///8C////Av///wL///8C////Av///wL///8C////AvX19QJkZGQFAAAAAAEBAaoAAAD/AAAA/AAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AQAA/wAAAP8DAgH/1nMo//+NMf/9hy///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///ocv//+LMP/sfiv/EQkD/wAAAP8BAQD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD9AAAA/wAAANVjY2ME////AcPDwwP///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C9fX1AmRkZAUAAAAAAQEBqgAAAP8AAAD8AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AwIB/wAAAP+fVh7//5Ey//uGLv//iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///ogv//+LMP82HQr/AAAA/wMBAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP4AAAD/AAAA9goKCiAAAAAAioqKBP///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL19fUCZGRkBQAAAAABAQGqAAAA/wAAAPwAAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8EAgH/AAAA/2E1Ev//kTL//IYu//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL//8hi7//5Ey/2U3E/8AAAD/BAIB/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP0AAAD/BAQESQAAAABjY2MF////Av///wL///8C////Av///wL///8C////Av///wL///8C////AvX19QJkZGQFAAAAAAEBAaoAAAD/AAAA/AAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wIBAP8AAAD/KhcI//yHL///iC///ogv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//uGLv//kTL/l1Ec/wAAAP8EAgH/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA+wAAAP8CAgJ5AAAAAFNTUwb+/v4C////Av///wL///8C////Av///wL///8C////Av///wL///8C9fX1AmRkZAUAAAAAAQEBqgAAAP8AAAD8AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AQAA/wAAAP8DAgH/1nMo//+NMf/9hy///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///Icv//+OMf/HaiX/AAAA/wEBAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD8AAAA/wAAAKoAAAAAaGhoBfPz8wL///8C////Av///wL///8C////Av///wL///8C////Av///wL19fUCZGRkBQAAAAABAQGqAAAA/wAAAPwAAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AwIB/wAAAP+fVh7//5Ey//uGLv//iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL//+hy///4sw/+x+K/8RCQP/AAAA/wEBAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP0AAAD/AAAA1WNjYwT///8Bw8PDA////wL///8C////Av///wL///8C////Av///wL///8C////AvX19QJkZGQFAAAAAAEBAaoAAAD/AAAA/AAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8EAgH/AAAA/2E1Ev//kTL//IYu//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL//+iC///4sw/zYdCv8AAAD/AwEA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/gAAAP8AAAD2CgoKIAAAAACKiooE////Av///wL///8C////Av///wL///8C////Av///wL///8C9fX1AmRkZAUAAAAAAQEBqgAAAP8AAAD8AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wIBAP8AAAD/KhcI//yHL///iC///ogv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//yGLv//kTL/ZTcT/wAAAP8EAgH/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/QAAAP8EBARJAAAAAGNjYwX///8C////Av///wL///8C////Av///wL///8C////Av///wL19fUCZGRkBQAAAAABAQGqAAAA/wAAAPwAAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AQAA/wAAAP8DAgH/1nMo//+NMf/9hy///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC//+4Yu//+RMv+XURz/AAAA/wQCAf8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD7AAAA/wICAnkAAAAAU1NTBv7+/gL///8C////Av///wL///8C////Av///wL///8C////AvX19QJkZGQFAAAAAAEBAaoAAAD/AAAA/AAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AwIB/wAAAP+fVh7//5Ey//uGLv//iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL//8hy///44x/8dqJf8AAAD/AQEA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAPwAAAD/AAAAqgAAAABoaGgF8/PzAv///wL///8C////Av///wL///8C////Av///wL///8C9fX1AmRkZAUAAAAAAQEBqgAAAP8AAAD8AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8EAgH/AAAA/2E1Ev//kTL//IYu//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//6HL///izD/7H4r/xEJA/8AAAD/AQEA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/QAAAP8AAADVY2NjBP///wHDw8MD////Av///wL///8C////Av///wL///8C////Av///wL19fUCZGRkBQAAAAABAQGqAAAA/wAAAPwAAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wIBAP8AAAD/KhcI//yHL///iC///ogv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//6IL///izD/Nh0K/wAAAP8DAQD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD+AAAA/wAAAPYKCgogAAAAAIqKigT///8C////Av///wL///8C////Av///wL///8C////AvX19QJkZGQFAAAAAAEBAaoAAAD/AAAA/AAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AQAA/wAAAP8DAgH/1nMo//+NMf/9hy///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///IYu//+RMv9lNxP/AAAA/wQCAf8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD9AAAA/wQEBEkAAAAAY2NjBf///wL///8C////Av///wL///8C////Av///wL///8C9fX1AmRkZAUAAAAAAQEBqgAAAP8AAAD8AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AwIB/wAAAP+fVh7//5Ey//uGLv//iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL//7hi7//5Ey/5dRHP8AAAD/BAIB/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAPsAAAD/AgICeQAAAABTU1MG/v7+Av///wL///8C////Av///wL///8C////Av///wL19fUCZGRkBQAAAAABAQGqAAAA/wAAAPwAAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8EAgH/AAAA/2E1Ev//kTL//IYu//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//yHL///jjH/x2ol/wAAAP8BAQD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/AAAAP8AAACqAAAAAGhoaAXz8/MC////Av///wL///8C////Av///wL///8C////AvX19QJkZGQFAAAAAAEBAaoAAAD/AAAA/AAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wIBAP8AAAD/KhcI//yHL///iC///ogv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///ocv//+LMP/sfiv/EQkD/wAAAP8BAQD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD9AAAA/wAAANViYmIE////AcPDwwP///8C////Av///wL///8C////Av///wL///8C9fX1AmRkZAUAAAAAAQEBqgAAAP8AAAD8AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AQAA/wAAAP8DAgH/1nMo//+NMf/9hy///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///ogv//+LMP82HQr/AAAA/wMBAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP4AAAD/AAAA9goKCiAAAAAAioqKBP///wL///8C////Av///wL///8C////Av///wL19fUCZGRkBQAAAAABAQGqAAAA/wAAAPwAAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AwIB/wAAAP+fVh7//5Ey//uGLv//iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL//8hi7//5Ey/2U3E/8AAAD/BAIB/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP0AAAD/BAQESQAAAABjY2MF////Av///wL///8C////Av///wL///8C////AvX19QJkZGQFAAAAAAEBAaoAAAD/AAAA/AAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/gAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8EAgH/AAAA/2E1Ev//kTL//IYu//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//uGLv//kTL/l1Ec/wAAAP8EAgH/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA+wAAAP8CAgJ5AAAAAFNTUwb+/v4C////Av///wL///8C////Av///wL///8C9fX1AmRkZAUAAAAAAQEBqgAAAP8AAAD8AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD+AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wIBAP8AAAD/KhcI//yHL///iC///ogv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///Icv//+OMf/HaiX/AAAA/wEBAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD8AAAA/wAAAKoAAAAAaGhoBfPz8wL///8C////Av///wL///8C////Av///wL19fUCZGRkBQAAAAABAQGqAAAA/wAAAPwAAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA9QAAAO0AAAD/AAAA/gAAAP8AAAD/AAAA/wAAAP8AAAD/AQAA/wAAAP8DAgH/1nMo//+NMf/9hy///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL//+hy///4sw/+x+K/8RCQP/AAAA/wEBAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP0AAAD/AAAA1WFhYQT///8Bw8PDA////wL///8C////Av///wL///8C////AvX19QJkZGQFAAAAAAEBAaoAAAD/AAAA/AAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/gAAAP8AAADgAAAAuAAAAP8AAAD9AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AwIB/wAAAP+fVh7//5Ey//uGLv//iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL///iC///4gv//+IL//+iC///4sw/zYdCv8AAAD/AwEA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/gAAAP8AAAD2CgoKIAAAAACKiooE////Av///wL///8C////Av///wL///8C9fX1AmRkZAUAAAAAAQEBqgAAAP8AAAD8AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD+AAAA/wAAAN4BAQF7AAAA/wAAAP0AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8EAgH/AAAA/2E1Ev//jzH/+IQu//uGLv/8hi7//IYu//yGLv/8hi7//IYu//yGLv/8hi7//IYu//yGLv/8hi7//IYu//yGLv/8hi7//IYu//yGLv/8hi7//IYu//yGLv/8hi7//IYu//yGLv/8hi7//IYu//yGLv/8hi7//IYu//yGLv/8hi7//IYu//yGLv/8hi7//IYu//yGLv/8hi7//IYu//yGLv/8hi7//IYu//yGLv/8hi7//IYu//yGLv/8hi7//IYu//yGLv/8hi7//IYu//yGLv/8hi7//IYu//yGLv/8hi7//IYu//yGLv/8hi7//IYu//yGLv/8hi7//IYu//yGLv/8hi7//IYu//yGLv/8hi7//IYu//yGLv/8hi7//IYu//yGLv/8hi7//IYu//yGLv/8hi7//IYu//yGLv/8hi7/+4Yu//iELv//jzH/ZDYT/wAAAP8EAgH/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/QAAAP8EBARJAAAAAGNjYwX///8C////Av///wL///8C////Av///wL19fUCZGRkBQAAAAABAQGqAAAA/wAAAPwAAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP4AAAD/AAAA5AQEBEIAAAD8AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wIBAP8AAAD/KhcI//2OMf//kTL//pAy//+QMv//kDL//5Ay//+QMv//kDL//5Ay//+QMv//kDL//5Ay//+QMv//kDL//5Ay//+QMv//kDL//5Ay//+QMv//kDL//5Ay//+QMv//kDL//5Ay//+QMv//kDL//5Ay//+QMv//kDL//5Ay//+QMv//kDL//5Ay//+QMv//kDL//5Ay//+QMv//kDL//5Ay//+QMv//kDL//5Ay//+QMv//kDL//5Ay//+QMv//kDL//5Ay//+QMv//kDL//5Ay//+QMv//kDL//5Ay//+QMv//kDL//5Ay//+QMv//kDL//5Ay//+QMv//kDL//5Ay//+QMv//kDL//5Ay//+QMv//kDL//5Ay//+QMv//kDL//5Ay//+QMv//kDL//5Ay//+QMv//kDL//5Ay//+QMv//kDL/+44x//+aNf+bVx7/AAAA/wQCAf8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD7AAAA/wICAnkAAAAAU1NTBv7+/gL///8C////Av///wL///8C////AvX19QJkZGQFAAAAAAEBAaoAAAD/AAAA/AAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/gAAAP8AAADtDw8PGQAAANgAAAD/AAAA/QAAAP8AAAD/AAAA/wAAAP8AAAD/AQAA/wAAAP8GAwH/lE8b/65dIP+oWh//qVof/6laH/+pWh//qVof/6laH/+pWh//qVof/6laH/+pWh//qVof/6laH/+pWh//qVof/6laH/+pWh//qVof/6laH/+pWh//qVof/6laH/+pWh//qVof/6laH/+pWh//qVof/6laH/+pWh//qVof/6laH/+pWh//qVof/6laH/+pWh//qVof/6laH/+pWh//qVof/6laH/+pWh//qVof/6laH/+pWh//qVof/6laH/+pWh//qVof/6laH/+pWh//qVof/6laH/+pWh//qVof/6laH/+pWh//qVof/6la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AP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAPsAAAD/AgICegAAAABTU1MG/v7+Av///wL///8C////Av///wL19fUCZGRkBQAAAAABAQGqAAAA/wAAAPwAAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP4AAAD/AAAA7xcXFxUAAAAAAAAAqQAAAP8AAAD8AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA+wAAAP8BAQGhAAAAAF9fXwX39/cC////Av///wL///8C////AvX19QJkZGQFAAAAAAEBAaoAAAD/AAAA/AAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/gAAAP8AAADvFRUVFgAAAAACAgJrAAAA/wAAAPsAAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD8AAAA/wEBAaAAAAAAX19fBff39wL///8C////Av///wL///8C9fX1AmRkZAUAAAAAAQEBqgAAAP8AAAD8AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD+AAAA/wAAAO8XFxcVAAAAAAYGBjEAAAD+AAAA/gAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAPsAAAD/AwMDbwAAAABWVlYG/v7+Av///wL///8C////Av///wL19fUCZGRkBQAAAAABAQGqAAAA/wAAAPwAAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP4AAAD/AAAA7xkZGRMAAAAAAAAAAAAAALcAAAD/AAAA+QAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD7AAAA/wAAAOwHBwcbAAAAAJCQkAT///8C////Av///wL///8C////AvX19QJkZGQFAAAAAAEBAaoAAAD/AAAA/AAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/gAAAP8AAADvGhoaEgAAAAAAAAAABgYGJgAAAOcAAAD/AAAA/QAAAPwAAAD8AAAA/AAAAPwAAAD8AAAA/AAAAPwAAAD8AAAA/AAAAPwAAAD8AAAA/AAAAPwAAAD8AAAA/AAAAPwAAAD8AAAA/AAAAPwAAAD8AAAA/AAAAPwAAAD8AAAA/AAAAPwAAAD8AAAA/AAAAPwAAAD8AAAA/AAAAPwAAAD8AAAA/AAAAPwAAAD8AAAA/AAA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/wL///8C////Av///wL///8C9fX1AmRkZAUAAAAAAQEBqgAAAP8AAAD8AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD+AAAA/wAAAO8aGhoSAAAAAKOjowP9/f0C////AuTk5AJ4eHgEWlpaBldXVwZYWFgGV1dXBldXVwZXV1cGV1dXBldXVwZXV1cGV1dXBldXVwZXV1cGV1dXBldXVwZXV1cGV1dXBldXVwZXV1cGV1dXBldXVwZXV1cGV1dXBldXVwZXV1cGV1dXBldXVwZXV1cGV1dXBldXVwZXV1cGV1dXBldXVwZXV1cGV1dXBldXVwZXV1cGV1dXBldXVwZXV1cGV1dXBldXVwZXV1cGV1dXBldXVwZXV1cGV1dXBldXVwZXV1cGV1dXBldXVwZXV1cGV1dXBldXVwZXV1cGV1dXBldXVwZXV1cGV1dXBldXVwZXV1cGV1dXBldXVwZXV1cGV1dXBldXVwZXV1cGV1dXBldXVwZXV1cGV1dXBldXVwZXV1cGV1dXBldXVwZXV1cGVlZWBjk5OQkAAAAAAQEBqwAAAP8AAAD8AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD+AAAA/wAAAO8WFhYW////AUxMTAdcXFwFXFxcBVxcXAVubm4FxMTEA////wL9/f0C////Av///wL///8C////Av///wL///8C////Av///wL19fUCZGRkBQAAAAABAQGqAAAA/wAAAPwAAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP4AAAD/AAAA7xoaGhIAAAAAo6OjA////wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL19fUCZGRkBQAAAAABAQGqAAAA/wAAAPwAAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP4AAAD/AAAA7xoaGhIAAAAAo6OjA////wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////AvX19QJkZGQFAAAAAAEBAaoAAAD/AAAA/AAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/gAAAP8AAADvGhoaEgAAAACjo6MD////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////AvX19QJkZGQFAAAAAAEBAaoAAAD/AAAA/AAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/gAAAP8AAADvGhoaEgAAAACjo6MD////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C9fX1AmRkZAUAAAAAAQEBqgAAAP8AAAD8AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD+AAAA/wAAAO8aGhoSAAAAAKOjowP///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C9fX1AmRkZAUAAAAAAQEBqgAAAP8AAAD8AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD+AAAA/wAAAO8aGhoSAAAAAKOjowP///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL19fUCZGRkBQAAAAABAQGqAAAA/wAAAPwAAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP4AAAD/AAAA7xoaGhIAAAAAo6OjA////wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL19fUCZGRkBQAAAAABAQGqAAAA/wAAAPwAAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP4AAAD/AAAA7xoaGhIAAAAAo6OjA////wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////AvX19QJkZGQFAAAAAAEBAaoAAAD/AAAA/AAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/gAAAP8AAADvGhoaEgAAAACjo6MD////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////AvX19QJkZGQFAAAAAAEBAaoAAAD/AAAA/AAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/gAAAP8AAADvGhoaEgAAAACjo6MD////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C9fX1AmRkZAUAAAAAAQEBqgAAAP8AAAD8AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD+AAAA/wAAAO8aGhoSAAAAAKOjowP///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av7+/gL///8C39/fAqqqqgOjo6MDpKSkA6OjowOjo6MDo6OjA6OjowOjo6MDo6OjA6OjowOjo6MDo6OjA6OjowOjo6MDo6OjA6OjowOjo6MDo6OjA6OjowOjo6MDo6OjA6OjowOjo6MDo6OjA6OjowOjo6MDo6OjA6OjowOjo6MDo6OjA6OjowOjo6MDo6OjA6OjowOjo6MDn5+fA1JSUgYAAAAAAQEBqgAAAP8AAAD8AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD+AAAA/wAAAO8aGhoSAAAAAKOjowP///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL19fUCZGRkBQAAAAABAQGqAAAA/wAAAPwAAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP4AAAD/AAAA7xoaGhIAAAAAo6OjA////wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Avz8/AL///8C3NzcAl5eXgZ9fX0DAAAAAAAAAADv7+8AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABAQEAAAAAAwAAAAAAAACpAAAA/wAAAPwAAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP4AAAD/AAAA7xoaGhIAAAAApKSkA////wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////AvX19QJkZGQFAAAAAAEBAaoAAAD/AAAA/AAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/gAAAP8AAADvGhoaEgAAAACjo6MD////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL8/PwC////Ari4uANra2sEXl5eAHt7ewEkJCQOGRkZExoaGhIaGhoSGhoaEhoaGhIaGhoSGhoaEhoaGhIaGhoSGhoaEhoaGhIaGhoSGhoaEhoaGhIaGhoSGhoaEhoaGhIaGhoSGhoaEhoaGhIaGhoSGhoaEhoaGhIaGhoSGhoaEhoaGhIaGhoSGhoaEhoaGhIaGhoSGhoaEhoaGhIaGhoSGhoaEhoaGhIWFhYVXl5eBQEBAa8AAAD/AAAA/AAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/gAAAP8AAADvGhoaEgAAAACjo6MD////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C9fX1AmRkZAUAAAAAAQEBqgAAAP8AAAD8AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD+AAAA/wAAAO8aGhoSAAAAAKOjowP///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C/f39Av///wK7u7sDbGxsA3NzcwEEBARdAQEBxQAAAOkAAADvAAAA7gAAAO8AAADvAAAA7wAAAO8AAADvAAAA7wAAAO8AAADvAAAA7wAAAO8AAADvAAAA7wAAAO8AAADvAAAA7wAAAO8AAADvAAAA7wAAAO8AAADvAAAA7wAAAO8AAADvAAAA7wAAAO8AAADvAAAA7wAAAO8AAADvAAAA7wAAAO8AAADvAAAA7wAAAO8AAADuAAAA+QAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD+AAAA/wAAAOoeHh4QAAAAAKioqAP///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL19fUCZGRkBQAAAAABAQGqAAAA/wAAAPwAAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP4AAAD/AAAA7xoaGhIAAAAAo6OjA////wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av7+/gL///8Cvb29A4uLiwNHR0cCAQEBpAAAAP8AAAD9AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP0AAAD/AAAA1mVlZQX///8BwsLCA////wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////AvX19QJkZGQFAAAAAAEBAaoAAAD/AAAA/AAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/gAAAP8AAADvGhoaEgAAAACjo6MD////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C/Pz8AvLy8gJRUVEFAAAAAAICApEAAAD/AAAA+gAAAPwAAAD+AAAA/gAAAP4AAAD+AAAA/gAAAP4AAAD+AAAA/gAAAP4AAAD+AAAA/gAAAP4AAAD+AAAA/gAAAP4AAAD+AAAA/gAAAP4AAAD+AAAA/gAAAP4AAAD+AAAA/gAAAP4AAAD+AAAA/gAAAP4AAAD+AAAA/gAAAP4AAAD+AAAA/gAAAP4AAAD+AAAA/gAAAP4AAAD+AAAA/gAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/AAAAP8BAQGtAAAAAGlpaQXy8vIC////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C9fX1AmRkZAUAAAAAAQEBqgAAAP8AAAD8AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD+AAAA/wAAAO8aGhoSAAAAAKOjowP///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Avr6+gL///8CU1NTBgAAAAACAgJtAAAA/wAAAPsAAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD7AAAA/wICAmYAAAAAWFhYBv///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL19fUCZGRkBQAAAAABAQGqAAAA/wAAAPwAAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP4AAAD/AAAA7xoaGhIAAAAAo6OjA////wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL6+voC////Al1dXQYAAAAAAwMDSQAAAP0AAAD+AAAA/gAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/gAAAP8AAADoDg4OFgAAAACampoD////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////AvX19QJkZGQFAAAAAAEBAaoAAAD/AAAA/AAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/gAAAP8AAADvGhoaEgAAAACjo6MD////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C+/v7Av///wJwcHAFAAAAAAUFBSoAAADtAAAA/wAAAP0AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD6AAAA/wEBAXYAAAAAZGRkBfr6+gL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C9fX1AmRkZAUAAAAAAQEBqgAAAP8AAAD8AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD+AAAA/wAAAO8aGhoSAAAAAKOjowP///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av39/QL///8CkZGRBAAAAAALCwsSAQEB1QAAAP8AAAD8AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA+gAAAP8BAQG7R0dHBPLy8gLLy8sD/Pz8Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL19fUCZGRkBQAAAAABAQGqAAAA/wAAAPwAAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP4AAAD/AAAA7xoaGhIAAAAAo6OjA////wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL+/v4C////Arq6ugOLi4sDVVVVAgEBAbUAAAD/AAAA+wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/AAAAPsAAAD/AQEBzQkJCRUAAAAAnZ2dA////wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////AvX19QJkZGQFAAAAAAEBAaoAAAD/AAAA/AAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/gAAAP8AAADvGhoaEgAAAACjo6MD////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Avz8/ALy8vICUlJSBQAAAAACAgKRAAAA/wAAAPsAAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD9AAAA+wAAAPwAAAD8AAAA/AAAAPwAAAD8AAAA/AAAAPwAAAD8AAAA/AAAAPwAAAD8AAAA/AAAAPwAAAD8AAAA/AAAAPwAAAD8AAAA/AAAAPwAAAD8AAAA/AAAAPwAAAD8AAAA/AAAAPwAAAD8AAAA/AAAAPwAAAD8AAAA/AAAAPwAAAD8AAAA/AAAAPwAAAD7AAAA+wAAAP4AAAD+AAAA/wEBAa4LCwsQAAAAAIqKigT///8C/Pz8Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C9fX1AmRkZAUAAAAAAQEBqgAAAP8AAAD8AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD+AAAA/wAAAO8aGhoSAAAAAKOjowP///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL6+voC////AlNTUwYAAAAAAgICbQAAAP8AAAD7AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/QAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/gAAAM0FBQVUAAAAAFRUVAOQkJAE////Avn5+QL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL19fUCZGRkBQAAAAABAQGqAAAA/wAAAPwAAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP4AAAD/AAAA7xoaGhIAAAAAo6OjA////wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C+vr6Av///wJdXV0GAAAAAAMDA0oAAAD9AAAA/gAAAP4AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP0AAAD/AQEBxwEBAaQBAQGrAQEBqgEBAaoBAQGqAQEBqgEBAaoBAQGqAQEBqgEBAaoBAQGqAQEBqgEBAaoBAQGqAQEBqgEBAaoBAQGqAQEBqgEBAaoBAQGqAQEBqgEBAaoBAQGqAQEBqgEBAaoBAQGqAQEBqgEBAaoBAQGqAQEBqgEBAaoBAQGqAQEBqgEBAaoBAQGoAQEBmAICAnIJCQk0UFBQA05OTgBgYGAEmJiYBP///wL6+voC////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////AvX19QJkZGQFAAAAAAEBAaoAAAD/AAAA/AAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/gAAAP8AAADvGhoaEgAAAACjo6MD////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Avz8/AL///8CcHBwBQAAAAAFBQUqAAAA7AAAAP8AAAD9AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD8AAAA/wEBAcEUFBQGERERAAYGBgEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAD///8AU1NTAE1NTQB2dnYDYmJiBeTk5AL///8C/f39Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C9fX1AmRkZAUAAAAAAQEBqgAAAP8AAAD8AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD+AAAA/wAAAO8aGhoSAAAAAKOjowP///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL9/f0C////ApGRkQQAAAAACwsLEgEBAdUAAAD/AAAA/AAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/QAAAP8BAQHeBwcHGgAAAABPT08HZGRkBWRkZAVkZGQFZGRkBWRkZAVkZGQFZGRkBWRkZAVkZGQFZGRkBWRkZAVkZGQFZGRkBWRkZAVkZGQFZGRkBWRkZAVkZGQFZGRkBWRkZAVkZGQFZGRkBWRkZAVkZGQFZGRkBWRkZAVkZGQFZGRkBWRkZAVkZGQFZGRkBWRkZAVkZGQFY2NjBVlZWQZTU1MGcnJyBNXV1QL///8C/f39Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL19fUCZGRkBQAAAAABAQGqAAAA/wAAAPwAAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP4AAAD/AAAA7xgYGBMAAAAAeHh4BKOjowOjo6MDo6OjA6OjowOjo6MDo6OjA6OjowOjo6MDo6OjA6OjowOjo6MDo6OjA6OjowOjo6MDo6OjA6OjowOjo6MDo6OjA6OjowOjo6MDo6OjA6OjowOjo6MDo6OjA6OjowOjo6MDo6OjA6SkpAOIiIgEhISEA2BgYAIBAQG1AAAA/wAAAPsAAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP4AAAD/AAAA9AQEBDUAAAAAZ2dnBf///wLy8vIC9fX1AvX19QL19fUC9fX1AvX19QL19fUC9fX1AvX19QL19fUC9fX1AvX19QL19fUC9fX1AvX19QL19fUC9fX1AvX19QL19fUC9fX1AvX19QL19fUC9fX1AvX19QL19fUC9fX1AvX19QL19fUC9fX1AvX19QL19fUC9fX1AvX19QL29vYC+vr6Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////AvX19QJkZGQFAAAAAAEBAaoAAAD/AAAA/AAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/gAAAP8AAADuAAAAEQAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAERERAAAAAAIAAAAAAgICkQAAAP8AAAD7AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD+AAAA/QAAAP8CAgJVAAAAAFZWVgb///8C+fn5Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C9fX1AmRkZAUAAAAAAQEBqgAAAP8AAAD8AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD+AAAA/wAAAPANDQ0iIiIiDhgYGBMaGhoSGhoaEhoaGhIaGhoSGhoaEhoaGhIaGhoSGhoaEhoaGhIaGhoSGhoaEhoaGhIaGhoSGhoaEhoaGhIaGhoSGhoaEhoaGhIaGhoSGhoaEhoaGhIaGhoSGhoaEhoaGhIaGhoSGhoaEhoaGhIWFhYVTExMBwMDA3AAAAD/AAAA/AAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAPsAAAD/AgICegAAAABVVVUG////Avr6+gL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL29vYCYWFhBQAAAAABAQGlAAAA/wAAAPsAAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/gAAAPAAAADuAAAA7wAAAO8AAADvAAAA7wAAAO8AAADvAAAA7wAAAO8AAADvAAAA7wAAAO8AAADvAAAA7wAAAO8AAADvAAAA7wAAAO8AAADvAAAA7wAAAO8AAADvAAAA7wAAAO8AAADvAAAA7wAAAO8AAADvAAAA7wAAAO8AAADuAAAA+wAAAP4AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD7AAAA/wEBAZ8AAAAAW1tbBd/f3wL+/v4C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Avz8/AJVVVUGAAAAAAICAo0AAAD/AAAA+wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD9AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/AAAAP8BAQHBEBAQBrOzswKtra0D////Av7+/gL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////AlpaWgYAAAAAAgICXgAAAP8AAAD8AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD+AAAA/gAAAP4AAAD+AAAA/gAAAP4AAAD+AAAA/gAAAP4AAAD+AAAA/gAAAP4AAAD+AAAA/gAAAP4AAAD+AAAA/gAAAP4AAAD+AAAA/gAAAP4AAAD+AAAA/gAAAP4AAAD+AAAA/gAAAP4AAAD+AAAA/gAAAP4AAAD+AAAA/gAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP0AAAD/AQEB3gcHBxoAAAAAg4ODBP///wL9/f0C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8CiYmJBAAAAAAKCgohAAAA9AAAAP8AAAD+AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD+AAAA/wAAAPQFBQU1AAAAAGhoaAX///8C+/v7Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wLp6ekCdXV1BAAAAAABAQGnAAAA/wAAAPsAAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/gAAAP0AAAD/AgICVQAAAABWVlYG////Avn5+QL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Avz8/AKBgYEEAAAAAAQEBC8AAAD3AAAA/wAAAP4AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD7AAAA/wICAnoAAAAAVVVVBv///wL6+voC////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C/v7+Av///wJnZ2cFAAAAAAICAnIAAAD/AAAA+gAAAP4AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA+wAAAP8BAQGfAAAAAFtbWwXf398C/v7+Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C+vr6AvDw8AJra2sEAAAAAAICAo4AAAD/AAAA/AAAAPsAAAD+AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAPoAAAD/AQEBwBAQEAazs7MCra2tA////wL+/v4C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL+/v4C////AtfX1wNZWVkEAAAAAAMDA3EAAAD5AAAA/wAAAP4AAAD8AAAA+wAAAPsAAAD8AAAA/AAAAPwAAAD8AAAA/AAAAPwAAAD8AAAA/AAAAPwAAAD8AAAA/AAAAPwAAAD8AAAA/AAAAPwAAAD8AAAA/AAAAPwAAAD8AAAA/AAAAPwAAAD8AAAA/AAAAPwAAAD8AAAA/AAAAPwAAAD8AAAA/AAAAPwAAAD8AAAA/AAAAPwAAAD8AAAA/AAAAPsAAAD7AAAA/wEBAd0HBwcaAAAAAIODgwT///8C/f39Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL9/f0C////As3NzQNMTEwFAAAAAAkJCSwBAQGqAAAA9gAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/wAAAP8AAAD/AAAA/gAAAP8BAQHOCAgIJQAAAABzc3MF////Avv7+wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL9/f0C////AtfX1wJmZmYFKSkpAQAAAAAODg4fAwMDXwICAo4BAQGkAQEBqgEBAaoBAQGqAQEBqgEBAaoBAQGqAQEBqgEBAaoBAQGqAQEBqgEBAaoBAQGqAQEBqgEBAaoBAQGqAQEBqgEBAaoBAQGqAQEBqgEBAaoBAQGqAQEBqgEBAaoBAQGqAQEBqgEBAaoBAQGqAQEBqgEBAaoBAQGqAQEBqgEBAaoBAQGqAQEBqQEBAaoBAQGZBQUFVh0dHQj///8Ah4eHBP///wL5+fkC////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL+/v4C/Pz8Av///wJ1dXUEaGhoBQAAAAAAAAAA39/fAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAGRkZABXV1cAYWFhA4aGhgT///8C+fn5Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C/v7+Av///wL19fUCi4uLBFhYWAZUVFQGYWFhBWRkZAVkZGQFZGRkBWRkZAVkZGQFZGRkBWRkZAVkZGQFZGRkBWRkZAVkZGQFZGRkBWRkZAVkZGQFZGRkBWRkZAVkZGQFZGRkBWRkZAVkZGQFZGRkBWRkZAVkZGQFZGRkBWRkZAVkZGQFZGRkBWRkZAVkZGQFZGRkBWRkZAVkZGQFZGRkBWRkZAVlZWUFWFhYBlxcXAXDw8MD////Avz8/AL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Avz8/AL29vYC9fX1AvX19QL19fUC9fX1AvX19QL19fUC9fX1AvX19QL19fUC9fX1AvX19QL19fUC9fX1AvX19QL19fUC9fX1AvX19QL19fUC9fX1AvX19QL19fUC9fX1AvX19QL19fUC9fX1AvX19QL19fUC9fX1AvX19QL19fUC9fX1AvX19QL19fUC9fX1AvX19QL6+voC////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8C////Av///wL///8CAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAL///////////////+gAAAEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQAABAAAAAAAAAAAAAAAAACAAAgAAAAAAAAAAAAAAAAAgAAIAAAAAAAAAAAAAAAAAAAACAAAAAAAAAAAAAAAAABAAAgAAAAAAAAAAAAAAAAAQAAIAAAAAAAAAAAAAAAAAEAACAAAAAAAAAAAAAAAAABAAAgAAAAAAAAAAAAAAAAAAAAIAAAAAAAAAAAAAAAAACAACAAAAAAAAAAAAAAAAAAgAAgAAAAAAAAAAAAAAAAAIAAIAAAAAAAAAAAAAAAAACAACAAAAAAAAAAAAAAAAAAAAAgAAAAAAAAAAAAAAAAAEAAIAAAAAAAAAAAAAAAAABAACAAAAAAAAAAAAAAAAAAQAAgAAAAAAAAAAAAAAAAAEAAIAAAAAAAAAAAAAAAAAAAACAAAAAAAAAAAAAAAAAAIAAgAAAAAAAAAAAAAAAAACAAIAAAAAAAAAAAAAAAAAAgACAAAAAAAAAAAAAAAAAAIAAgAAAAAAAAAAAAAAAAAAAAIAAAAAAAAAAAAAAAAAAQACAAAAAAAAAAAAAAAAAAEAAgAAAAAAAAAAAAAAAAABAAIAAAAAAAAAAAAAAAAAAQACAAAAAAAAAAAAAAAAAAAAAgAAAAAAAAAAAAAAAAAAgAIAAAAAAAAAAAAAAAAAAIACAAAAAAAAAAAAAAAAAACAAgAAAAAAAAAAAAAAAAAAgAIAAAAAAAAAAAAAAAAAAAACAAAAAAAAAAAAAAAAAABAAgAAAAAAAAAAAAAAAAAAQAIAAAAAAAAAAAAAAAAAAEACAAAAAAAAAAAAAAAAAABAAgAAAAAAAAAAAAAAAAAAAAIAAAAAAAAAAAAAAAAAACACAAAAAAAAAAAAAAAAAAAgAgAAAAAAAAAAAAAAAAAAIAIAAAAAAAAAAAAAAAAAACACAAAAAAAAAAAAAAAAAAAAAgAAAAAAAAAAAAAAAAAAEAIAAAAAAAAAAAAAAAAAABACAAAAAAAAAAAAAAAAAAAQAgAAAAAAAAAAAAAAAAAAEAIAAAAAAAAAAAAAAAAAAAACAAAAAAAAAAAAAAAAAAAIAgAAAAAAAAAAAAAAAAAACAIAAAAAAAAAAAAAAAAAAAgCAAAAAAAAAAAAAAAAAAAIAgAAAAAAAAAAAAAAAAAAAAIAAAAAAAAAAAAAAAAAAAQCAAAAAAAAAAAAAAAAAAAEAgAAAAAAAAAAAAAAAAAABAIAEAAAAAAAAAAAAAAAAAQCABAAAAAAAAAAAAAAAAAEAgAQAAAAAAAAAAAAAAAABAIAGAAAAAAAAAAAAAAAAAQCABgAAAAAAAAAAAAAAAAIAgAUAAAAAAAAAAAAAAAAEAIAEAAAAAAAAAAAAAAAACACABC////////////yABaAAgAQAAAAAAAAAAAAAgAAAAIAEAAAAAAAAAAAAAIAEAACABAAAAAAAAAAAAACABAAAgAQAAAAAAAAAAAAAgAQAAIAEAAAAAAAAAAAAAIAEAACABAAAAAAAAAAAAACABAAAgAQAAAAAAAAAAAAAgAQAAIAEAAAAAAAT/////IAEAACABAAAAAAAQAAAAAAABAAAgAQAAAAAAAAAAAAAAAQAAIAEAAAAAAAAAAAAAAAAAACABAAAAAACAAAAAAAACAAAgAQAAAAABAAAAAAAAAgAAIAEAAAAAAgAAAAAAAAIAACABAAAAAAQAAAAAAAAEAAAgAQAAAAAIAAAAAAAAAAAAIAEAAAAAAAAAAAAAAAgAACABAAAAABAAAAAAAAAQAAAgAQAAAAAgAAAAAAAAQAAAIAEAAAAAQAAAAAAAAIAAACABAAAAAIAAX/////oAAAAgAQAAAAEAAIAAAAAAAAAAIAEAAAAAAAEAAAAAAAAAACABf///8gACAAAAAAAAAAAgAAAAAAAABAAAAAAAAAAAIAAAAAAAAAgAAAAAAAAAACAAAAAAAAAAAAAAAAAAAAAgAAAAAAAAEAAAAAAAAAAAIAAAAAAAACAAAAAAAAAAABAAAAAAAABAAAAAAAAAAAAQAAAAAAAAgAAAAAAAAAAACAAAAAAAAQAAAAAAAAAAAAQAAAAAAAAAAAAAAAAAAAACAAAAAAACAAAAAAAAAAAAAQAAAAAABAAAAAAAAAAAAABAAAAAAAAAAAAAAAAAAAAAJ/////+gAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA="
        icon_bytes = base64.b64decode(base64_icon_str)

        pixmap = QPixmap()
        pixmap.loadFromData(QByteArray(icon_bytes))

        icon = QIcon(pixmap)
        self.setWindowIcon(icon)
    
    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        
        # 左侧面板
        left_panel = QVBoxLayout()
        
        # 按钮样式和大小
        button_style = """
            QPushButton {
                min-height: 30px;
                padding: 5px;
                font-size: 12px;
            }
        """
        
        # 按钮
        button_group = QGroupBox("操作区")
        button_layout = QVBoxLayout()
        button_layout.setSpacing(10)
        
        self.excel_btn = QPushButton("选择Excel文件", self)
        self.excel_btn.setStyleSheet(button_style)
        self.excel_btn.clicked.connect(self.select_excel)
        button_layout.addWidget(self.excel_btn)
        
        self.folder_btn = QPushButton("选择文件夹", self)
        self.folder_btn.setStyleSheet(button_style)
        self.folder_btn.clicked.connect(self.select_folder)
        button_layout.addWidget(self.folder_btn)
        
        self.check_btn = QPushButton("开始检查", self)
        self.check_btn.setStyleSheet(button_style)
        self.check_btn.clicked.connect(self.check_files)
        button_layout.addWidget(self.check_btn)
        
        self.rename_btn = QPushButton("重命名文件", self)
        self.rename_btn.setStyleSheet(button_style)
        self.rename_btn.clicked.connect(self.rename_files)
        button_layout.addWidget(self.rename_btn)
        
        self.organize_btn = QPushButton("整理重复文件", self)
        self.organize_btn.setStyleSheet(button_style)
        self.organize_btn.clicked.connect(self.organize_files)
        button_layout.addWidget(self.organize_btn)
        
        button_layout.addWidget(QLabel("重复文件处理方式："))
        self.duplicate_mode_combo = QComboBox()
        self.duplicate_mode_combo.setStyleSheet("QComboBox { min-height: 25px; }")
        self.duplicate_mode_combo.addItems([
            "重命名（自动添加序号）",
            "仅保留一个（随机）",
            "移动到重复文件夹"
        ])
        button_layout.addWidget(self.duplicate_mode_combo)
        self.duplicate_mode_combo.currentTextChanged.connect(self.update_duplicate_mode)
        
        button_layout.setContentsMargins(10, 10, 10, 10)
        
        button_group.setLayout(button_layout)
        left_panel.addWidget(button_group)
        
        columns_group = QGroupBox("Excel列映射")
        columns_layout = QVBoxLayout()
        
        self.columns_table = QTableWidget(self)
        self.columns_table.setColumnCount(4)
        self.columns_table.setHorizontalHeaderLabels(["Excel列", "变量名", "用于匹配", "操作"])
        self.columns_table.setColumnWidth(0, 120)
        self.columns_table.setColumnWidth(1, 100)
        self.columns_table.setColumnWidth(2, 80)
        self.columns_table.setColumnWidth(3, 60)
        columns_layout.addWidget(self.columns_table)
        
        add_column_btn = QPushButton("添加列映射", self)
        add_column_btn.setStyleSheet(button_style)
        add_column_btn.clicked.connect(self.add_column_mapping)
        columns_layout.addWidget(add_column_btn)
        
        columns_group.setLayout(columns_layout)
        left_panel.addWidget(columns_group)
        
        format_group = QGroupBox("命名格式设置")
        format_layout = QVBoxLayout()
        
        self.format_input = QLineEdit(self.name_format)
        self.format_input.setToolTip("使用花括号包围变量")
        format_layout.addWidget(self.format_input)
        
        self.format_example = QLabel("示例: {name}")
        format_layout.addWidget(self.format_example)
        
        self.format_input.textChanged.connect(self.update_format_example)
        format_group.setLayout(format_layout)
        left_panel.addWidget(format_group)
        
        # 日志区域
        log_group = QGroupBox("日志信息")
        log_layout = QVBoxLayout()
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        log_layout.addWidget(self.log_text)
        log_group.setLayout(log_layout)
        left_panel.addWidget(log_group)
        
        main_layout.addLayout(left_panel, stretch=1)
        
        # 右侧面板
        right_panel = QVBoxLayout()
        
        # 文件列表
        files_group = QGroupBox("文件列表")
        files_layout = QVBoxLayout()
        self.table = QTableWidget(self)
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["当前文件名", "新文件名", "匹配值", "状态"])
        self.table.setColumnWidth(0, 250)
        self.table.setColumnWidth(1, 250)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectItems)
        self.table.setSelectionMode(QTableWidget.SelectionMode.ExtendedSelection)
        files_layout.addWidget(self.table)
        files_group.setLayout(files_layout)
        right_panel.addWidget(files_group)
        
        info_splitter = QSplitter(Qt.Orientation.Vertical)
        
        # 重复文件列表
        duplicates_group = QGroupBox("重复文件")
        duplicates_layout = QVBoxLayout()
        self.duplicates_table = QTableWidget()
        self.duplicates_table.setColumnCount(2)
        self.duplicates_table.setHorizontalHeaderLabels(["文件名", "匹配项"])
        self.duplicates_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectItems)
        self.duplicates_table.setSelectionMode(QTableWidget.SelectionMode.ExtendedSelection)
        duplicates_layout.addWidget(self.duplicates_table)
        duplicates_group.setLayout(duplicates_layout)
        info_splitter.addWidget(duplicates_group)
        
        # 缺失文件列表
        missing_group = QGroupBox("未找到的记录")
        missing_layout = QVBoxLayout()
        self.missing_table = QTableWidget()
        self.missing_table.setColumnCount(2)
        self.missing_table.setHorizontalHeaderLabels(["Excel记录", "匹配项"])
        self.missing_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectItems)
        self.missing_table.setSelectionMode(QTableWidget.SelectionMode.ExtendedSelection)
        missing_layout.addWidget(self.missing_table)
        missing_group.setLayout(missing_layout)
        info_splitter.addWidget(missing_group)
        
        right_panel.addWidget(info_splitter)
        main_layout.addLayout(right_panel, stretch=2)
        
        self.table.keyPressEvent = lambda e: self.handle_copy(e, self.table)
        self.duplicates_table.keyPressEvent = lambda e: self.handle_copy(e, self.duplicates_table)
        self.missing_table.keyPressEvent = lambda e: self.handle_copy(e, self.missing_table)
        
        self.setup_header_menu(self.table)
        self.setup_header_menu(self.duplicates_table)
        self.setup_header_menu(self.missing_table)
    
    def log_message(self, message):
        current_time = datetime.now().strftime("%H:%M:%S")
        self.log_text.append(f"[{current_time}] {message}")
    
    def update_format_example(self):
        try:
            format_vars = {}
            for row in range(self.columns_table.rowCount()):
                var_name = self.columns_table.cellWidget(row, 1)
                if var_name and var_name.text():
                    format_vars[var_name.text()] = "{" + var_name.text() + "}"
            
            example = self.format_input.text()
            for var_name, var_placeholder in format_vars.items():
                example = example.replace("{" + var_name + "}", var_placeholder)
            
            self.format_example.setText(f"格式: {example}")
        except Exception:
            self.format_example.setText("格式错误")
    
    def select_excel(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择Excel文件", "", "Excel Files (*.xlsx *.xls)")
        if file_path:
            self.excel_path = file_path
            try:
                df = pd.read_excel(file_path)
                self.log_message(f"已加载Excel文件: {file_path}")
            except Exception as e:
                QMessageBox.warning(self, "错误", f"Excel文件读取失败: {str(e)}")
    
    def select_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "选择要整理的文件夹")
        if folder_path:
            self.folder_path = folder_path
            self.log_message(f"已选择文件夹: {folder_path}")
    
    def check_files(self):
        if not self.excel_path or not self.folder_path:
            QMessageBox.warning(self, "警告", "请先选择Excel文件和文件夹")
            return
        
        if not self.duplicate_rules:
            QMessageBox.warning(self, "警告", "请至少选择一个用于匹配的列")
            return
            
        try:
            df = pd.read_excel(self.excel_path)
            files = [f for f in os.listdir(self.folder_path) 
                    if os.path.isfile(os.path.join(self.folder_path, f))]
            
            self.table.setRowCount(0)
            self.duplicates_table.setRowCount(0)
            self.missing_table.setRowCount(0)
            self.duplicate_files = []
            
            # 创建匹配值到文件的映射，用于检测重复
            value_to_files = {}
            file_matches = {}
            
            # 第一遍扫描：收集所有匹配信息
            for file in files:
                name = Path(file).stem
                matched_rows = []
                matched_dict = {}
                
                # 检查文件名
                for idx, excel_row in df.iterrows():
                    current_match = {}
                    for column in self.duplicate_rules:
                        if str(excel_row[column]) in name:
                            current_match[column] = str(excel_row[column])
                    
                    if current_match:
                        matched_rows.append(excel_row)
                        for col, val in current_match.items():
                            matched_dict.setdefault(col, set()).add(val)
                            key = f"{col}:{val}"
                            value_to_files.setdefault(key, []).append(file)
                
                file_matches[file] = (matched_rows, matched_dict)
            
            # 第二遍扫描：处理每个文件并标记重复
            for file in files:
                row = self.table.rowCount()
                self.table.insertRow(row)
                self.table.setItem(row, 0, QTableWidgetItem(file))
                
                matched_rows, matched_dict = file_matches[file]
                
                # 生成新文件名
                new_name = ""
                if len(matched_rows) == 1:
                    try:
                        format_vars = {}
                        for map_row in range(self.columns_table.rowCount()):
                            column_combo = self.columns_table.cellWidget(map_row, 0)
                            var_name = self.columns_table.cellWidget(map_row, 1)
                            if column_combo and var_name and var_name.text():
                                format_vars[var_name.text()] = str(matched_rows[0][column_combo.currentText()])
                    
                        new_name = self.format_input.text().format(**format_vars) + Path(file).suffix
                    except Exception as e:
                        new_name = "格式错误"
                        self.log_message(f"生成新文件名失败: {str(e)}")
                
                self.table.setItem(row, 1, QTableWidgetItem(new_name))
                
                # 将匹配到的值转换为显示格式
                matched_values = []
                is_duplicate = False
                
                for col in self.duplicate_rules:
                    if col in matched_dict:
                        values = sorted(matched_dict[col])
                        matched_values.append(f"{col}: {', '.join(values)}")
                        # 检查是否有其他文件匹配到相同的值
                        for val in values:
                            key = f"{col}:{val}"
                            if len(value_to_files[key]) > 1:
                                is_duplicate = True
                
                self.table.setItem(row, 2, QTableWidgetItem(" | ".join(matched_values)))
                
                if is_duplicate:
                    self.table.setItem(row, 3, QTableWidgetItem("重复"))
                    self.duplicate_files.append(file)
                    # 添加到重复文件表格
                    dup_row = self.duplicates_table.rowCount()
                    self.duplicates_table.insertRow(dup_row)
                    self.duplicates_table.setItem(dup_row, 0, QTableWidgetItem(file))
                    self.duplicates_table.setItem(dup_row, 1, QTableWidgetItem(" | ".join(matched_values)))
                elif len(matched_rows) == 0:
                    self.table.setItem(row, 3, QTableWidgetItem("未匹配"))
                else:
                    self.table.setItem(row, 3, QTableWidgetItem("正常"))
            
            # 检查Excel中的记录是否都能找到对应文件
            for idx, excel_row in df.iterrows():
                found = False
                for file, matches in file_matches.items():
                    if any(match.equals(excel_row) for match in matches[0]):
                        found = True
                        break
                
                if not found:
                    row = self.missing_table.rowCount()
                    self.missing_table.insertRow(row)
                    values = [str(excel_row[col]) for col in self.duplicate_rules]
                    self.missing_table.setItem(row, 0, QTableWidgetItem(", ".join(values)))
                    self.missing_table.setItem(row, 1, QTableWidgetItem(", ".join(self.duplicate_rules)))
            
            # 计算总数
            duplicate_groups = {}
            for file in self.duplicate_files:
                matched_rows, matched_dict = file_matches[file]
                for col in self.duplicate_rules:
                    if col in matched_dict:
                        for val in matched_dict[col]:
                            key = f"{col}:{val}"
                            if len(value_to_files[key]) > 1:
                                duplicate_groups.setdefault(key, set()).update(value_to_files[key])

            # 计算实际总数
            unique_groups = set()
            for files in duplicate_groups.values():

                unique_groups.add(tuple(sorted(files)))
            
            duplicate_group_count = len(unique_groups)
            total_duplicate_files = sum(len(group) for group in unique_groups)

            self.log_message(f"检查完成：共 {self.table.rowCount()} 个文件，"
                           f"{duplicate_group_count} 个重复文件(共 {total_duplicate_files} 个)，"
                           f"{self.missing_table.rowCount()} 条未匹配记录")
            
        except Exception as e:
            self.log_message(f"错误：{str(e)}")
            QMessageBox.warning(self, "错误", f"处理文件失败: {str(e)}")
    
    def rename_files(self):
        if not self.folder_path:
            return
            
        renamed_count = 0
        for row in range(self.table.rowCount()):
            old_name = self.table.item(row, 0).text()
            new_name = self.table.item(row, 1).text()
            
            if new_name and new_name != "格式错误" and old_name != new_name:
                try:
                    old_path = os.path.join(self.folder_path, old_name)
                    new_path = os.path.join(self.folder_path, new_name)
                    os.rename(old_path, new_path)
                    renamed_count += 1
                except Exception as e:
                    QMessageBox.warning(self, "错误", f"重命名失败: {str(e)}")
        
        QMessageBox.information(self, "成功", f"已重命名 {renamed_count} 个文件")
        self.check_files()
    
    def organize_files(self):
        if not self.folder_path or len(self.duplicate_files) == 0:
            QMessageBox.information(self, "提示", "没有需要整理的文件")
            return
        
        try:
            if self.duplicate_handle_mode == "move":
                # 创建重复文件文件夹
                duplicate_folder = os.path.join(self.folder_path, "重复文件")
                if not os.path.exists(duplicate_folder):
                    os.makedirs(duplicate_folder)
                
                # 移动重复文件
                for file in self.duplicate_files:
                    src = os.path.join(self.folder_path, file)
                    dst = os.path.join(duplicate_folder, file)
                    shutil.move(src, dst)
                
            elif self.duplicate_handle_mode == "keep_one":
                # 保留一个
                for file in self.duplicate_files[1:]:
                    os.remove(os.path.join(self.folder_path, file))
            
            elif self.duplicate_handle_mode == "rename":
                value_groups = {}
                
                # 获取分组信息
                for row in range(self.duplicates_table.rowCount()):
                    file = self.duplicates_table.item(row, 0).text()
                    match_values = self.duplicates_table.item(row, 1).text()
                    
                    for match in match_values.split(" | "):
                        value_groups.setdefault(match, []).append(file)
                
                for match_value, files in value_groups.items():
                    if len(files) > 1:
                        actual_value = match_value.split(": ")[1] if ": " in match_value else match_value

                        for i, file in enumerate(files, 1):
                            old_path = os.path.join(self.folder_path, file)
                            name, ext = os.path.splitext(file)
                            base_name = actual_value.strip()
                            new_name = f"{base_name}_{i}{ext}"
                            new_path = os.path.join(self.folder_path, new_name)
                            os.rename(old_path, new_path)
            
            self.log_message(f"已处理 {len(self.duplicate_files)} 个重复文件")
            QMessageBox.information(self, "成功", "文件整理完成！")
            self.check_files()
            
        except Exception as e:
            self.log_message(f"错误：{str(e)}")
            QMessageBox.warning(self, "错误", f"处理文件失败: {str(e)}")

    def add_column_mapping(self):
        if not self.excel_path:
            QMessageBox.warning(self, "警告", "请先选择Excel文件")
            return
            
        row = self.columns_table.rowCount()
        self.columns_table.insertRow(row)
        
        column_combo = QComboBox()
        column_combo.addItems(self.get_excel_columns())
        self.columns_table.setCellWidget(row, 0, column_combo)
        
        var_name = QLineEdit()
        var_name.setPlaceholderText("变量名")
        self.columns_table.setCellWidget(row, 1, var_name)
        
        check_duplicate = QCheckBox()
        check_duplicate.setToolTip("勾选此项将使用该列进行匹配和查重")
        self.columns_table.setCellWidget(row, 2, check_duplicate)
        
        delete_btn = QPushButton("删除")
        delete_btn.clicked.connect(lambda: self.remove_column_mapping(row))
        self.columns_table.setCellWidget(row, 3, delete_btn)
        
        column_combo.currentTextChanged.connect(lambda text: self.on_column_changed(row))
        var_name.textChanged.connect(self.update_format_example)
        check_duplicate.stateChanged.connect(self.update_duplicate_rules)

    def remove_column_mapping(self, row):
        self.columns_table.removeRow(row)
        self.update_format_example()
        self.update_duplicate_rules()

    def update_duplicate_rules(self):
        old_rules = set(self.duplicate_rules)
        self.duplicate_rules = []
        for row in range(self.columns_table.rowCount()):
            column_combo = self.columns_table.cellWidget(row, 0)
            check_duplicate = self.columns_table.cellWidget(row, 2)
            if column_combo and check_duplicate and check_duplicate.isChecked():
                self.duplicate_rules.append(column_combo.currentText())
        
        new_rules = set(self.duplicate_rules)
        if old_rules != new_rules:
            self.log_message(f"匹配规则已更新: {', '.join(self.duplicate_rules)}")

    def get_excel_columns(self):
        if self.excel_path:
            try:
                df = pd.read_excel(self.excel_path)
                return df.columns.tolist()
            except Exception:
                return []
        return []

    def update_duplicate_mode(self, mode):
        if "重命名" in mode:
            self.duplicate_handle_mode = "rename"
        elif "保留一个" in mode:
            self.duplicate_handle_mode = "keep_one"
        else:
            self.duplicate_handle_mode = "move"

    def on_column_changed(self, row):
        self.update_format_example()
        check_duplicate = self.columns_table.cellWidget(row, 2)
        if check_duplicate and check_duplicate.isChecked():
            self.update_duplicate_rules()
            if self.table.rowCount() > 0:
                self.check_files()

    def handle_copy(self, event, table):
        if event.key() == Qt.Key.Key_C and event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            selected_ranges = table.selectedRanges()
            if not selected_ranges:
                return
            
            copy_text = []
            is_single_column = all(range_.leftColumn() == range_.rightColumn() for range_ in selected_ranges)
            
            for range_ in selected_ranges:
                for row in range(range_.topRow(), range_.bottomRow() + 1):
                    row_text = []
                    for col in range(range_.leftColumn(), range_.rightColumn() + 1):
                        item = table.item(row, col)
                        if item:
                            row_text.append(item.text())
                        else:
                            widget = table.cellWidget(row, col)
                            if widget:
                                if isinstance(widget, QComboBox):
                                    row_text.append(widget.currentText())
                                elif isinstance(widget, QLineEdit):
                                    row_text.append(widget.text())
                                elif isinstance(widget, QCheckBox):
                                    row_text.append("√" if widget.isChecked() else "")
                                else:
                                    row_text.append("")
                            else:
                                row_text.append("")
                    
                    if is_single_column:
                        copy_text.extend(row_text)
                    else:
                        copy_text.append("\t".join(row_text))
            
            clipboard = QApplication.clipboard()
            if is_single_column:
                clipboard.setText("\n".join(copy_text))
                self.log_message(f"已复制 {len(copy_text)} 个单元格数据到剪贴板")
            else:
                clipboard.setText("\n".join(copy_text))
                self.log_message(f"已复制 {len(copy_text)} 行数据到剪贴板")
        else:
            table.parent().keyPressEvent(event)

    def setup_header_menu(self, table):
        header = table.horizontalHeader()
        header.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        header.customContextMenuRequested.connect(lambda pos: self.show_header_menu(pos, table))

    def show_header_menu(self, pos, table):
        header = table.horizontalHeader()
        column = header.logicalIndexAt(pos)
        
        menu = QMenu(self)
        select_column_action = menu.addAction("选择整列")
        action = menu.exec(header.mapToGlobal(pos))
        
        if action == select_column_action:
            table.selectColumn(column)

    def create_menu_bar(self):
        menubar = self.menuBar()
        
        about_action = menubar.addAction('关于')
        about_action.triggered.connect(self.show_about)
    
    def show_about(self):
        about_text = """
        文件整理工具 1.0
        
        功能特点：
        - 支持Excel文件导入
        - 文件名匹配和查重
        - 自定义命名格式
        - 灵活的重复文件处理
        
        作者：幽影
        """
        QMessageBox.about(self, "关于", about_text)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = FileOrganizerApp()
    window.show()
    sys.exit(app.exec())
