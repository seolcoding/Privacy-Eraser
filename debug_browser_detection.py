#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""브라우저 감지 디버깅 스크립트"""

import sys
import os
from pathlib import Path

# Windows 콘솔 UTF-8 설정
if os.name == 'nt':
    os.system('chcp 65001 > nul')
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# 프로젝트 경로 추가
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "src"))

from privacy_eraser.detect_windows import (
    detect_browsers,
    registry_key_exists,
    detect_file_glob,
    is_process_running_windows,
    ProgramProbe
)

def debug_single_browser(probe: ProgramProbe):
    """단일 브라우저 감지 디버깅"""
    print(f"\n{'='*60}")
    print(f"🔍 {probe.name} 감지 디버깅")
    print(f"{'='*60}")

    # Registry 체크
    print("\n📋 Registry Keys:")
    registry_found = False
    for key in probe.registry_keys:
        exists = registry_key_exists(key)
        print(f"  {'✅' if exists else '❌'} {key}")
        if exists:
            registry_found = True

    # File 체크
    print("\n📁 File Patterns:")
    file_found = False
    for pattern in probe.file_patterns:
        exists = detect_file_glob(pattern)
        print(f"  {'✅' if exists else '❌'} {pattern}")
        if exists:
            file_found = True

    # Process 체크
    print("\n🔄 Process Names:")
    process_found = False
    for process in probe.process_names:
        running = is_process_running_windows(process)
        print(f"  {'✅' if running else '❌'} {process}")
        if running:
            process_found = True

    # 최종 결과
    print(f"\n📊 감지 결과:")
    print(f"  Registry 발견: {registry_found}")
    print(f"  File 발견: {file_found}")
    print(f"  Process 실행 중: {process_found}")
    print(f"  최종: {'✅ 설치됨' if (registry_found or file_found) else '❌ 미설치'}")


def main():
    """메인 함수"""
    print("\n")
    print("🛡️  Privacy Eraser - 브라우저 감지 디버깅")
    print("="*60)

    # 전체 감지 결과
    print("\n1️⃣  전체 브라우저 감지 결과:")
    print("-"*60)

    browsers = detect_browsers()
    for browser in browsers:
        name = browser.get("name", "Unknown")
        present = browser.get("present", "no")
        running = browser.get("running", "no")
        source = browser.get("source", "-")

        status = "✅ 설치됨" if present == "yes" else "❌ 미설치"
        running_status = "🔄 실행 중" if running == "yes" else "⏸️  중지됨"

        print(f"{status:15} {running_status:15} {name:15} (출처: {source})")

    # 상세 디버깅
    print("\n\n2️⃣  상세 디버깅:")
    print("-"*60)

    # 브라우저 probe 정의 (detect_browsers와 동일)
    browser_probes = [
        ProgramProbe(
            name="Chrome",
            registry_keys=(
                r"HKLM\SOFTWARE\Google\Chrome",
                r"HKCU\SOFTWARE\Google\Chrome",
            ),
            file_patterns=(
                r"%ProgramFiles%\Google\Chrome\Application\chrome.exe",
                r"%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe",
                r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe",
            ),
            process_names=("chrome.exe",),
        ),
        ProgramProbe(
            name="Edge",
            registry_keys=(
                r"HKLM\SOFTWARE\Microsoft\Edge",
                r"HKCU\SOFTWARE\Microsoft\Edge",
            ),
            file_patterns=(
                r"%ProgramFiles%\Microsoft\Edge\Application\msedge.exe",
                r"%ProgramFiles(x86)%\Microsoft\Edge\Application\msedge.exe",
            ),
            process_names=("msedge.exe",),
        ),
        ProgramProbe(
            name="Firefox",
            registry_keys=(
                r"HKLM\SOFTWARE\Mozilla\Mozilla Firefox",
                r"HKCU\SOFTWARE\Mozilla\Mozilla Firefox",
            ),
            file_patterns=(
                r"%ProgramFiles%\Mozilla Firefox\firefox.exe",
                r"%ProgramFiles(x86)%\Mozilla Firefox\firefox.exe",
            ),
            process_names=("firefox.exe",),
        ),
        ProgramProbe(
            name="Brave",
            file_patterns=(
                r"%LOCALAPPDATA%\BraveSoftware\Brave-Browser\Application\brave.exe",
                r"%ProgramFiles%\BraveSoftware\Brave-Browser\Application\brave.exe",
            ),
            process_names=("brave.exe",),
        ),
        ProgramProbe(
            name="Opera",
            registry_keys=(
                r"HKLM\SOFTWARE\Opera Software",
                r"HKCU\SOFTWARE\Opera Software",
            ),
            file_patterns=(
                r"%ProgramFiles%\Opera\launcher.exe",
                r"%ProgramFiles(x86)%\Opera\launcher.exe",
                r"%LOCALAPPDATA%\Programs\Opera\launcher.exe",
            ),
            process_names=("opera.exe",),
        ),
        ProgramProbe(
            name="Vivaldi",
            file_patterns=(
                r"%LOCALAPPDATA%\Vivaldi\Application\vivaldi.exe",
                r"%ProgramFiles%\Vivaldi\Application\vivaldi.exe",
            ),
            process_names=("vivaldi.exe",),
        ),
    ]

    # 각 브라우저 상세 디버깅
    for probe in browser_probes:
        debug_single_browser(probe)

    print("\n" + "="*60)
    print("✅ 디버깅 완료!")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
