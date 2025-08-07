# File_Copy: 날짜별 사진/영상 정리 프로그램

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![PySide6](https://img.shields.io/badge/Framework-PySide6-orange.svg)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

**File_Copy**는 여러 폴더에 흩어져 있는 사진과 영상 파일들을 촬영 날짜 기준으로 자동 분류하고, 중복을 제거하여 깔끔하게 정리해주는 프로그램입니다.

## ✨ 주요 기능

- **날짜별 폴더 자동 생성**: 파일의 원본 수정 날짜를 읽어 `YYYY-MM-DD` 형식의 폴더를 만들고 파일을 이동시킵니다.
- **중복 파일 자동 제거**: 파일의 해시(SHA256) 값을 비교하여 내용이 동일한 파일은 복사하지 않아 저장 공간을 절약합니다.
- **하위 폴더 전체 검색**: 지정된 입력 폴더의 모든 하위 폴더를 탐색하여 파일을 찾아냅니다.
- **다양한 파일 형식 지원**: `jpg`, `jpeg`, `png`, `mp4`, `cr3`, `cr2`, `mov` 등 주요 사진 및 영상 파일을 지원합니다.
- **직관적인 UI**: PyQt5로 제작된 깔끔하고 사용하기 쉬운 인터페이스를 제공합니다.
- **실시간 로그**: 파일 복사 과정을 실시간으로 확인할 수 있습니다.

## 🚀 설치 및 실행

### 1. 의존성 패키지 설치
```bash
# 저장소를 클론하거나 코드를 다운로드 받은 후, 해당 폴더로 이동합니다.
cd path/to/File_Copy

# requirements.txt 파일에 명시된 패키지를 설치합니다.
pip install -r requirements.txt
```

### 2. 프로그램 실행
```bash
python File_Copy.py
```

## 🎮 사용법

1.  **입력 경로 선택**: 정리할 사진/영상 파일들이 들어있는 최상위 폴더를 선택합니다.
2.  **출력 경로 선택**: 정리된 파일들을 저장할 폴더를 선택합니다.
3.  **복사 시작**: '복사 시작' 버튼을 누르면 작업이 시작됩니다.
4.  **로그 확인**: 메인 창의 로그 화면에서 실시간으로 진행 상황을 확인할 수 있습니다.

## 📦 의존성

- **PySide6**: GUI 프레임워크
- **PyInstaller** (선택사항): 실행 파일 빌드용

## 🔧 빌드 (EXE 실행 파일 만들기)

프로젝트를 다른 사람에게 쉽게 배포하기 위해 `.exe` 실행 파일로 빌드할 수 있습니다.

```bash
# build.py 스크립트를 실행합니다.
python build.py

# 또는 pyinstaller를 직접 사용합니다.
pyinstaller --onefile --windowed --name=File_Copy File_Copy.py
```

## 📝 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.