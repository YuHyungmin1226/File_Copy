import os
import shutil
import hashlib
import sys
from datetime import datetime
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QLabel, QFileDialog, QMessageBox, QTextEdit)
from PyQt5.QtCore import Qt, QThread, pyqtSignal

CONFIG_FILE = "last_paths.txt"
LOG_FILE = "copy_log.txt"
VALID_EXTENSIONS = ('jpg', 'jpeg', 'png', 'mp4', 'cr3', 'cr2', 'mov')

def is_valid_file(filename):
    return filename.lower().endswith(VALID_EXTENSIONS)

def get_file_modification_date(filepath):
    try:
        modification_time = os.path.getmtime(filepath)
        date = datetime.fromtimestamp(modification_time).strftime('%Y-%m-%d')
        return date
    except Exception as e:
        print(f"Error getting modification date: {e}")
        return None

def create_directory_if_not_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)

def calculate_file_hash(filepath):
    sha256 = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256.update(chunk)
        return sha256.hexdigest()
    except Exception:
        return None

def get_existing_hashes(folder_path):
    hash_set = set()
    for filename in os.listdir(folder_path):
        full_path = os.path.join(folder_path, filename)
        if os.path.isfile(full_path):
            file_hash = calculate_file_hash(full_path)
            if file_hash:
                hash_set.add(file_hash)
    return hash_set

class CopyThread(QThread):
    log_signal = pyqtSignal(str)
    finished_signal = pyqtSignal(int, int, int)

    def __init__(self, input_path, output_path):
        super().__init__()
        self.input_path = input_path
        self.output_path = output_path

    def run(self):
        files = []
        for root, _, filenames in os.walk(self.input_path):
            for file in filenames:
                if is_valid_file(file):
                    files.append((root, file))

        total_files = len(files)
        if total_files == 0:
            self.finished_signal.emit(0, 0, 0)
            return

        copied_files = 0
        skipped_files = 0
        hash_cache = {}

        for idx, (root_dir, file) in enumerate(files, start=1):
            source_file = os.path.join(root_dir, file)
            file_date = get_file_modification_date(source_file)

            if not file_date:
                self.log_signal.emit(f"[{idx}/{total_files}] {source_file} → [수정일 오류] 건너뜀")
                skipped_files += 1
                continue

            date_folder = os.path.join(self.output_path, file_date)
            create_directory_if_not_exists(date_folder)

            if date_folder not in hash_cache:
                hash_cache[date_folder] = get_existing_hashes(date_folder)

            source_hash = calculate_file_hash(source_file)
            if source_hash in hash_cache[date_folder]:
                self.log_signal.emit(f"[{idx}/{total_files}] {source_file} → [건너뜀: 동일 파일 존재]")
                skipped_files += 1
                continue

            existing_files = [f for f in os.listdir(date_folder) if os.path.isfile(os.path.join(date_folder, f))]
            next_index = len(existing_files) + 1
            _, ext = os.path.splitext(file)
            ext = ext.lower()
            padded_index = str(next_index).zfill(4)
            new_filename = f"{file_date.replace('-', '')}-{padded_index}{ext}"
            target_file = os.path.join(date_folder, new_filename)

            try:
                shutil.copy2(source_file, target_file)
                copied_files += 1
                hash_cache[date_folder].add(source_hash)
                self.log_signal.emit(f"[{idx}/{total_files}] {source_file} → {new_filename}")
            except Exception as e:
                skipped_files += 1
                self.log_signal.emit(f"[{idx}/{total_files}] 오류: {source_file} → {new_filename} ({e})")

        self.finished_signal.emit(total_files, copied_files, skipped_files)

class FileCopyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.input_path = ""
        self.output_path = ""
        self.initUI()
        self.load_last_paths()

    def initUI(self):
        self.setWindowTitle("파일 복사 프로그램")
        self.setGeometry(300, 300, 700, 500)

        vbox = QVBoxLayout()
        self.setLayout(vbox)

        # Path selection
        path_frame = QVBoxLayout()

        hbox_input = QHBoxLayout()
        self.input_path_button = QPushButton("입력 경로 선택")
        self.input_path_button.clicked.connect(self.select_input_path)
        self.input_path_label = QLabel("입력 경로: 선택되지 않음")
        self.input_path_label.setStyleSheet("border: 1px solid grey; padding: 5px;")
        hbox_input.addWidget(self.input_path_button)
        hbox_input.addWidget(self.input_path_label, 1)
        path_frame.addLayout(hbox_input)

        hbox_output = QHBoxLayout()
        self.output_path_button = QPushButton("출력 경로 선택")
        self.output_path_button.clicked.connect(self.select_output_path)
        self.output_path_label = QLabel("출력 경로: 선택되지 않음")
        self.output_path_label.setStyleSheet("border: 1px solid grey; padding: 5px;")
        hbox_output.addWidget(self.output_path_button)
        hbox_output.addWidget(self.output_path_label, 1)
        path_frame.addLayout(hbox_output)

        vbox.addLayout(path_frame)

        # Log output
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        vbox.addWidget(self.log_output)

        # Start button
        self.start_button = QPushButton("복사 시작")
        self.start_button.clicked.connect(self.start_copy_thread)
        vbox.addWidget(self.start_button)

    def select_input_path(self):
        folder = QFileDialog.getExistingDirectory(self, "입력 경로 선택")
        if folder:
            self.input_path = folder
            self.input_path_label.setText(f"입력 경로: {folder}")
            self.save_last_paths()

    def select_output_path(self):
        folder = QFileDialog.getExistingDirectory(self, "출력 경로 선택")
        if folder:
            self.output_path = folder
            self.output_path_label.setText(f"출력 경로: {folder}")
            self.save_last_paths()

    def log_message(self, message):
        self.log_output.append(message)
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(message + "\n")

    def start_copy_thread(self):
        if not self.input_path or not self.output_path:
            QMessageBox.critical(self, "오류", "입력 경로와 출력 경로를 선택하세요.")
            return

        with open(LOG_FILE, "w", encoding="utf-8") as f:
            f.write(f"=== 파일 복사 로그 시작: {datetime.now()} ===\n")
        
        self.log_output.clear()
        self.start_button.setEnabled(False)
        
        self.copy_thread = CopyThread(self.input_path, self.output_path)
        self.copy_thread.log_signal.connect(self.log_message)
        self.copy_thread.finished_signal.connect(self.copy_finished)
        self.copy_thread.start()

    def copy_finished(self, total, copied, skipped):
        self.start_button.setEnabled(True)
        if total == 0:
            QMessageBox.information(self, "알림", "복사할 파일이 없습니다.")
            return
            
        finish_message = f"=== 완료: 총 {total}개 중 복사 {copied}개, 건너뜀 {skipped}개 ==="
        self.log_message(finish_message)
        QMessageBox.information(self, "작업 완료", f"총 파일 수: {total}\n복사된 파일 수: {copied}\n건너뛴 파일 수: {skipped}")

    def save_last_paths(self):
        try:
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                f.write(f"input_path={self.input_path}\n")
                f.write(f"output_path={self.output_path}\n")
        except Exception as e:
            print(f"경로 저장 실패: {e}")

    def load_last_paths(self):
        if not os.path.exists(CONFIG_FILE):
            return
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                lines = f.readlines()
                for line in lines:
                    if line.startswith("input_path="):
                        path = line.strip().split("=", 1)[1]
                        if os.path.exists(path):
                            self.input_path = path
                            self.input_path_label.setText(f"입력 경로: {path}")
                    elif line.startswith("output_path="):
                        path = line.strip().split("=", 1)[1]
                        if os.path.exists(path):
                            self.output_path = path
                            self.output_path_label.setText(f"출력 경로: {path}")
        except Exception as e:
            print(f"경로 불러오기 실패: {e}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = FileCopyApp()
    ex.show()
    sys.exit(app.exec_())