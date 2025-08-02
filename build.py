#!/usr/bin/env python3
"""
File_Copy.py 빌드 스크립트

이 스크립트는 File_Copy.py를 독립 실행형 exe 파일로 빌드합니다.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def print_with_color(message, color_code=36):
    """색상이 있는 메시지 출력"""
    print(f"\033[{color_code}m{message}\033[0m")

def build_file_copy():
    """File_Copy.py를 실행 파일로 빌드"""
    
    script_dir = Path(__file__).parent
    target_py_file = script_dir / "File_Copy.py"
    
    dist_dir = script_dir / "dist"
    build_dir = script_dir / "build"
    
    print_with_color("=== File_Copy 빌드 시작 ===", 33)
    print_with_color(f"빌드 대상: {target_py_file}", 36)
    
    if dist_dir.exists():
        print_with_color("기존 dist 폴더 정리 중...", 33)
        shutil.rmtree(dist_dir)
    
    if build_dir.exists():
        print_with_color("기존 build 폴더 정리 중...", 33)
        shutil.rmtree(build_dir)
    
    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--name=File_Copy",
        "--distpath", str(dist_dir),
        "--workpath", str(build_dir),
        "--clean",
        str(target_py_file)
    ]
    
    print_with_color("PyInstaller 명령어:", 36)
    print(" ".join(cmd))
    print()
    
    try:
        print_with_color("빌드 진행 중...", 33)
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
        
        if result.returncode == 0:
            print_with_color("=== 빌드 성공! ===", 32)
            exe_path = dist_dir / "File_Copy.exe"
            if exe_path.exists():
                file_size = exe_path.stat().st_size / (1024 * 1024)
                print_with_color(f"실행 파일 생성됨: {exe_path}", 32)
                print_with_color(f"파일 크기: {file_size:.2f} MB", 36)
            else:
                print_with_color("오류: 실행 파일이 생성되지 않았습니다.", 31)
                return False
        else:
            print_with_color("=== 빌드 실패 ===", 31)
            print_with_color("오류 출력:", 31)
            print(result.stderr)
            return False
            
    except Exception as e:
        print_with_color(f"빌드 중 오류 발생: {e}", 31)
        return False
    
    return True

def cleanup_build_files():
    """빌드 임시 파일 정리"""
    script_dir = Path(__file__).parent
    build_dir = script_dir / "build"
    spec_file = script_dir / "File_Copy.spec"
    
    print_with_color("\n=== 빌드 파일 정리 ===", 33)
    
    if build_dir.exists():
        try:
            shutil.rmtree(build_dir)
            print_with_color("build 폴더 정리 완료", 32)
        except Exception as e:
            print_with_color(f"build 폴더 정리 실패: {e}", 31)
    
    if spec_file.exists():
        try:
            spec_file.unlink()
            print_with_color(".spec 파일 정리 완료", 32)
        except Exception as e:
            print_with_color(f".spec 파일 정리 실패: {e}", 31)

if __name__ == "__main__":
    print_with_color("File_Copy 빌드 스크립트", 35)
    print_with_color("=" * 50, 35)
    
    success = build_file_copy()
    
    if success:
        cleanup_build_files()
        print_with_color("\n빌드가 완료되었습니다!", 32)
    else:
        print_with_color("\n빌드에 실패했습니다.", 31)
        sys.exit(1)