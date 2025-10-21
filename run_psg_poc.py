"""Privacy Eraser PySimpleGUI POC 실행 스크립트

FreeSimpleGUI 기반의 심플한 버전 실행
"""

import sys
from pathlib import Path

# 프로젝트 루트를 Python 경로에 추가
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "src"))

# 로깅 설정
from loguru import logger
logger.remove()  # 기본 핸들러 제거
logger.add(sys.stderr, level="INFO", format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>")

# 메인 앱 실행
if __name__ == '__main__':
    try:
        from privacy_eraser.psg_poc.main import main
        main()

    except ImportError as e:
        logger.error(f"모듈 임포트 실패: {e}")
        logger.error("FreeSimpleGUI가 설치되지 않았을 수 있습니다.")
        logger.error("설치 방법: pip install FreeSimpleGUI")
        sys.exit(1)

    except Exception as e:
        logger.error(f"앱 실행 실패: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
