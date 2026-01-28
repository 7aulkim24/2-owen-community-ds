from models.user_model import user_model
from models.post_model import post_model
from models.comment_model import comment_model
from utils.database.db import execute
import logging

logger = logging.getLogger(__name__)

def seed_database():
    """데이터베이스 초기화 및 시드 데이터 삽입"""
    logger.info("Seeding database...")
    
    # 1. 모든 저장소 초기화
    execute("DELETE FROM sessions")
    user_model.clear()
    post_model.clear()
    comment_model.clear()
    
    # 2. 기본 테스트용 관리자 계정 생성
    admin_user = user_model.createUser(
        email="admin@test.com",
        password="Admin123!",
        nickname="테스트관리자",
        profileImageUrl=None
    )
    
    logger.info(f"Database seeded. Admin user created: {admin_user['email']}")
    return {
        "message": "Database reset and seeded successfully",
        "admin_user": {
            "email": admin_user["email"],
            "nickname": admin_user["nickname"]
        }
    }
