#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Privacy Eraser POC - Hot Reload 개발 서버
==========================================

파일 변경 감지 시 자동으로 GUI를 재시작합니다.
Next.js처럼 개발 중에 편리하게 사용할 수 있습니다.

사용법:
    python dev_server.py
"""

import sys
import os
import time
import subprocess
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Windows 콘솔 UTF-8 설정
if os.name == 'nt':
    os.system('chcp 65001 > nul')
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# 프로젝트 루트
PROJECT_ROOT = Path(__file__).parent
POC_DIR = PROJECT_ROOT / "src" / "privacy_eraser" / "poc"

# 전역 프로세스
current_process = None


class CodeChangeHandler(FileSystemEventHandler):
    """코드 변경 감지 핸들러"""

    def __init__(self, restart_callback):
        self.restart_callback = restart_callback
        self.last_restart = 0
        self.debounce_seconds = 1  # 1초 debounce

    def on_modified(self, event):
        """파일 수정 시"""
        if event.is_directory:
            return

        # Python 파일만 감지
        if not event.src_path.endswith('.py'):
            return

        # __pycache__ 무시
        if '__pycache__' in event.src_path:
            return

        # Debounce (너무 자주 재시작 방지)
        current_time = time.time()
        if current_time - self.last_restart < self.debounce_seconds:
            return

        self.last_restart = current_time

        # 변경된 파일 표시
        rel_path = Path(event.src_path).relative_to(PROJECT_ROOT)
        print(f"\n📝 파일 변경 감지: {rel_path}")

        # 재시작
        self.restart_callback()


def start_gui_process():
    """GUI 프로세스 시작"""
    global current_process

    # 이전 프로세스 종료
    if current_process is not None:
        print("🔄 GUI 재시작 중...")
        try:
            current_process.terminate()
            current_process.wait(timeout=3)
        except subprocess.TimeoutExpired:
            current_process.kill()
            current_process.wait()
        except Exception as e:
            print(f"⚠️  프로세스 종료 중 오류: {e}")
        current_process = None
        time.sleep(0.5)  # 잠시 대기

    # 새 프로세스 시작
    print("🚀 GUI 시작 중...")
    try:
        current_process = subprocess.Popen(
            [sys.executable, "-m", "uv", "run", "privacy_eraser_poc"],
            cwd=PROJECT_ROOT,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0,
        )

        print("✅ GUI가 시작되었습니다!")
        print("📁 감시 중인 디렉토리:", POC_DIR)
        print("💡 Ctrl+C를 눌러 종료하세요.\n")
    except Exception as e:
        print(f"❌ GUI 시작 실패: {e}")
        import traceback
        traceback.print_exc()


def main():
    """메인 함수"""
    print("=" * 60)
    print("🔥 Privacy Eraser POC - Hot Reload 개발 서버")
    print("=" * 60)
    print()

    # 초기 GUI 시작
    start_gui_process()

    # 파일 감시 설정
    event_handler = CodeChangeHandler(restart_callback=start_gui_process)
    observer = Observer()
    observer.schedule(event_handler, str(POC_DIR), recursive=True)
    observer.start()

    try:
        # 메인 루프 (단순히 대기)
        while True:
            time.sleep(1)
            # 프로세스가 예상치 못하게 종료되었는지 확인
            if current_process and current_process.poll() is not None:
                print(f"\n⚠️  GUI 프로세스가 종료되었습니다 (코드: {current_process.returncode})")
                print("🔄 재시작하려면 파일을 수정하세요...\n")
                current_process = None

    except KeyboardInterrupt:
        print("\n\n🛑 개발 서버 종료 중...")
        observer.stop()
        if current_process:
            current_process.terminate()
            try:
                current_process.wait(timeout=3)
            except subprocess.TimeoutExpired:
                current_process.kill()
        print("✅ 종료 완료!")

    observer.join()


if __name__ == "__main__":
    main()
