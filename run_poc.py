#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Privacy Eraser POC - 간단한 실행 스크립트
=========================================

Hot Reload 없이 POC GUI를 실행합니다.
"""

import sys
import os
from pathlib import Path

# Windows 콘솔 UTF-8 설정
if os.name == 'nt':
    os.system('chcp 65001 > nul')
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# 프로젝트 루트
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

def main():
    """메인 함수"""
    print("🛡️  Privacy Eraser POC 시작 중...")

    # POC 메인 실행
    from privacy_eraser.poc.main import main as poc_main
    poc_main()


if __name__ == "__main__":
    main()
