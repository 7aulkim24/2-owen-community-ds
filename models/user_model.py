from typing import Dict, Optional, List, Union
from datetime import datetime
from uuid import UUID, uuid4


class UserModel:
    """사용자 데이터 관리 Model"""

    def __init__(self):
        # 메모리 기반 사용자 저장소 (Key를 문자열로 관리)
        self.usersDb: Dict[str, Dict] = {}

    def _normalizeId(self, idVal: Union[UUID, str]) -> str:
        """ID 정규화"""
        return str(idVal)

    def getNextUserId(self) -> str:
        """다음 사용자 ID 생성"""
        return str(uuid4())

    def createUser(self, email: str, password: str, nickname: str, profileImageUrl: Optional[str] = None) -> Dict:
        """사용자 생성"""
        userId = self.getNextUserId()

        userData = {
            "userId": userId,
            "email": email,
            "password": password,
            "nickname": nickname,
            "profileImageUrl": profileImageUrl,
            "createdAt": datetime.now().isoformat(),
            "updatedAt": None
        }

        self.usersDb[userId] = userData
        return userData.copy()

    def getUserById(self, userId: Union[UUID, str]) -> Optional[Dict]:
        """ID로 사용자 조회"""
        userIdStr = self._normalizeId(userId)
        return self.usersDb.get(userIdStr)

    def getUserByEmail(self, email: str) -> Optional[Dict]:
        """이메일로 사용자 조회"""
        for user in self.usersDb.values():
            if user["email"] == email:
                return user
        return None

    def emailExists(self, email: str) -> bool:
        """이메일 중복 체크"""
        return self.getUserByEmail(email) is not None

    def nicknameExists(self, nickname: str) -> bool:
        """닉네임 중복 체크"""
        for user in self.usersDb.values():
            if user["nickname"] == nickname:
                return True
        return False

    def updateUser(self, userId: Union[UUID, str], updateData: Dict) -> Optional[Dict]:
        """사용자 정보 수정"""
        userIdStr = self._normalizeId(userId)
        if userIdStr not in self.usersDb:
            return None

        user = self.usersDb[userIdStr]
        allowedFields = ["nickname", "profileImageUrl", "password"]
        for field in allowedFields:
            if field in updateData:
                user[field] = updateData[field]

        user["updatedAt"] = datetime.now().isoformat()
        return user.copy()

    def deleteUser(self, userId: Union[UUID, str]) -> bool:
        """사용자 삭제"""
        userIdStr = self._normalizeId(userId)
        if userIdStr in self.usersDb:
            del self.usersDb[userIdStr]
            return True
        return False

    def getAllUsers(self) -> List[Dict]:
        """모든 사용자 조회"""
        return list(self.usersDb.values())

    def authenticateUser(self, email: str, password: str) -> Optional[Dict]:
        """사용자 인증"""
        user = self.getUserByEmail(email)
        if user and user["password"] == password:
            return user
        return None


# Model 인스턴스 생성
user_model = UserModel()
