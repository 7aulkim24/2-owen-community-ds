import os
import uuid
from fastapi import UploadFile

def save_upload_file(file: UploadFile, domain: str) -> str:
    """
    업로드된 파일을 로컬에 저장하고 URL 경로 반환
    domain: 'post' 또는 'profile'
    """
    base_dir = "public"
    sub_dir = f"image/{domain}"
    upload_path = os.path.join(base_dir, sub_dir)
    
    # 디렉토리 생성 (이미 main.py에서 생성하지만 안전을 위해)
    if not os.path.exists(upload_path):
        os.makedirs(upload_path, exist_ok=True)
        
    # 파일명 중복 방지를 위한 UUID 추가
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    
    file_path = os.path.join(upload_path, unique_filename)
    
    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())
        
    # 접근 가능한 URL 경로 반환 (실무에서는 도메인 주소를 환경변수에서 가져옴)
    # 여기서는 상대 경로 기반의 URL 반환
    return f"/public/{sub_dir}/{unique_filename}"
