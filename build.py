#!/usr/bin/env python3
"""
File_Copy.py 빌드 스크립트

release/ 에 설치 파일(File_Copy-Setup-<버전>.exe) + 설치 없이 실행하는 폴더(File_Copy/)
+ 포터블 zip(File_Copy-<버전>-portable-win-x64.zip)을 만듭니다 (release_kit.py).
빌드 중간 파일(dist-build/)은 성공하면 자동으로 지워지고, 실패하면 기존 release/ 는 그대로 남습니다.
"""

import sys
from datetime import datetime
from pathlib import Path

import release_kit

ROOT = Path(__file__).resolve().parent

APP = release_kit.App(
    root=ROOT,
    name="File_Copy",
    display_name="File Copy",
    version=datetime.now().strftime("%Y.%m.%d"),
    entry="File_Copy.py",
    app_id="36EA6EDC-2A1E-4149-9052-ACF4080F5F9E",
    windowed=True,
    extra_files=["README.md"],
)


if __name__ == "__main__":
    print("File_Copy 빌드 스크립트")
    print("=" * 50)
    if release_kit.build_windows_release(APP):
        print("\n빌드가 완료되었습니다!")
    else:
        print("\n빌드에 실패했습니다.")
        sys.exit(1)
