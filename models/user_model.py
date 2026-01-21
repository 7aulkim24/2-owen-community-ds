from typing import Dict, Optional, List, Union
from datetime import datetime
import bcrypt
from utils.id_utils import generate_id


class UserModel:
    """사용자 데이터 관리 Model"""

    def __init__(self):
        # 메모리 기반 사용자 저장소 (Key: userId)
        self.usersDb: Dict[str, Dict] = {}
        # 빠른 조회를 위한 매핑 (O(1))
        self.emailMap: Dict[str, str] = {}  # {email: userId}
        self.nicknameMap: Dict[str, str] = {}  # {nickname: userId}

    def _normalizeId(self, idVal: Union[str, any]) -> str:
        """ID 정규화 (문자열로 변환)"""
        return str(idVal)

    def hashPassword(self, password: str) -> str:
        """비밀번호 해싱 (bcrypt 직접 사용)"""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

    def verifyPassword(self, plainPassword: str, hashedPassword: str) -> bool:
        """비밀번호 검증 (bcrypt 직접 사용)"""
        try:
            return bcrypt.checkpw(plainPassword.encode('utf-8'), hashedPassword.encode('utf-8'))
        except Exception:
            return False

    def getNextUserId(self) -> str:
        """다음 사용자 ID 생성 (ULID)"""
        return generate_id()

    def createUser(self, email: str, password: str, nickname: str, profileImageUrl: Optional[str] = None) -> Dict:
        """사용자 생성"""
        userId = self.getNextUserId()
        hashedPassword = self.hashPassword(password)

        userData = {
            "userId": userId,
            "email": email,
            "password": hashedPassword,
            "nickname": nickname,
            "profileImageUrl": profileImageUrl,
            "createdAt": datetime.now().isoformat(),
            "updatedAt": None
        }

        self.usersDb[userId] = userData
        self.emailMap[email] = userId
        self.nicknameMap[nickname] = userId
        return userData.copy()

    def getUserById(self, userId: Union[str, any]) -> Optional[Dict]:
        """ID로 사용자 조회"""
        userIdStr = self._normalizeId(userId)
        return self.usersDb.get(userIdStr)

    def getUserByEmail(self, email: str) -> Optional[Dict]:
        """이메일로 사용자 조회 (O(1))"""
        userId = self.emailMap.get(email)
        if userId:
            return self.usersDb.get(userId)
        return None

    def emailExists(self, email: str) -> bool:
        """이메일 중복 체크 (O(1))"""
        return email in self.emailMap

    def nicknameExists(self, nickname: str) -> bool:
        """닉네임 중복 체크 (O(1))"""
        return nickname in self.nicknameMap

    def updateUser(self, userId: Union[str, any], updateData: Dict) -> Optional[Dict]:
        """사용자 정보 수정"""
        userIdStr = self._normalizeId(userId)
        if userIdStr not in self.usersDb:
            return None

        user = self.usersDb[userIdStr]
        
        # 닉네임 변경 시 매핑 업데이트
        if "nickname" in updateData and updateData["nickname"] != user["nickname"]:
            oldNickname = user["nickname"]
            newNickname = updateData["nickname"]
            if oldNickname in self.nicknameMap:
                del self.nicknameMap[oldNickname]
            self.nicknameMap[newNickname] = userIdStr
            user["nickname"] = newNickname

        # 이메일 변경 시 매핑 업데이트 (현재는 지원하지 않으나 확장성 위해)
        if "email" in updateData and updateData["email"] != user["email"]:
            oldEmail = user["email"]
            newEmail = updateData["email"]
            if oldEmail in self.emailMap:
                del self.emailMap[oldEmail]
            self.emailMap[newEmail] = userIdStr
            user["email"] = newEmail

        # 비밀번호 변경 시 해싱 적용
        if "password" in updateData:
            user["password"] = self.hashPassword(updateData["password"])

        if "profileImageUrl" in updateData:
            user["profileImageUrl"] = updateData["profileImageUrl"]

        user["updatedAt"] = datetime.now().isoformat()
        return user.copy()

    def deleteUser(self, userId: Union[str, any]) -> bool:
        """사용자 삭제"""
        userIdStr = self._normalizeId(userId)
        if userIdStr in self.usersDb:
            user = self.usersDb[userIdStr]
            # 매핑에서도 삭제
            if user["email"] in self.emailMap:
                del self.emailMap[user["email"]]
            if user["nickname"] in self.nicknameMap:
                del self.nicknameMap[user["nickname"]]
            
            del self.usersDb[userIdStr]
            return True
        return False

    def getAllUsers(self) -> List[Dict]:
        """모든 사용자 조회"""
        return list(self.usersDb.values())

    def authenticateUser(self, email: str, password: str) -> Optional[Dict]:
        """사용자 인증"""
        user = self.getUserByEmail(email)
        if user and self.verifyPassword(password, user["password"]):
            return user
        return None


# Model 인스턴스 생성
user_model = UserModel()
