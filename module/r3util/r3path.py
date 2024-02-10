import os
import sys

def get_program_start_path() -> str:
    """
    프로그램 시작 경로를 반환하는 함수
    """
    if getattr(sys, 'frozen', False):
        # pyinstaller로 빌드된 실행 파일의 경우
        main_path = os.path.dirname(sys.executable)
    else:
        # 일반적인 파이썬 스크립트 실행의 경우
        util_path = os.path.dirname(os.path.abspath(__file__))
        main_path = os.path.abspath(os.path.join(util_path, '..', '..'))
    print(f"Util : Program Start Path: {main_path}")
    return main_path

def get_defalut_save_path() -> str:
    """
    기본 저장 경로를 반환하는 함수
    """
    return os.path.join(get_program_start_path(), "ImageForestResult")

def check_path_exists(path: str) -> bool:
    return os.path.exists(path)