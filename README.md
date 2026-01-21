# Owen Community Backend

FastAPI 기반의 고성능 커뮤니티 백엔드 API입니다. 실무 수준의 운영 안정성과 성능 최적화를 목표로 **Router-Controller-Model-Schema** 아키텍처를 따르며, 최신 백엔드 엔지니어링 패턴이 적용되어 있습니다.

## 주요 기능

- **인증 및 보안**: 회원가입, 세션 기반 로그인/로그아웃, **bcrypt 비밀번호 해싱**, 권한 기반 접근 제어(RBAC)
- **게시글 및 댓글**: 커뮤니티 핵심 CRUD, **좋아요 토글**, 이미지 업로드 지원
- **ID 체계**: UUID를 대체하는 **ULID** 도입 (26자, 시간순 정렬 가능, 높은 인덱스 성능)
- **운영 안정성**: **Request ID** 추적 미들웨어 및 **구조화된 JSON 로깅** 시스템 구축
- **표준화된 통신**: 전역 예외 처리기, 설계도 준수 기반의 일관된 응답 및 에러 체계 (Code-Details 구조)

## 기술 스택

- **Framework**: FastAPI (v0.128.0+)
- **Validation**: Pydantic v2 (Strict Typing & DTO)
- **Security**: bcrypt (Password Hashing), Starlette Session
- **ID System**: ULID (python-ulid)
- **Infrastructure**: Structured Logging (logging + contextvars)

## 프로젝트 구조

```
2-owen-community-be/
├── main.py               # 앱 초기화, 미들웨어 및 전역 설정
├── config.py             # 환경 설정 (쿠키, 세션 등)
├── routers/              # API 엔드포인트 정의 (Versioning 적용)
├── controllers/          # 비즈니스 로직 및 DTO 변환
├── models/               # 데이터 접근, O(1) 매핑 및 캐싱 로직
├── schemas/              # Pydantic 기반 Request/Response DTO
└── utils/                # 공통 유틸리티
    ├── id_utils.py       # ULID 생성 및 검증
    ├── exceptions.py     # 표준 APIError 정의
    ├── response.py       # 규격화된 응답 포맷터
    ├── error_codes.py    # 통합 에러/성공 코드 관리
    └── request_id_middleware.py  # 요청 추적 시스템
```

## 설치 및 실행

1. **가상환경 활성화 (Conda)**
   ```bash
   conda activate community
   ```

2. **의존성 설치**
   ```bash
   # pyproject.toml 기반 설치 권장
   pip install fastapi uvicorn pydantic-settings python-ulid bcrypt python-multipart
   ```

3. **서버 실행**
   ```bash
   uvicorn main:app --reload
   ```

## 주요 API 엔드포인트 (v1)

### 인증 및 사용자 (Auth/User)
- `POST /v1/auth/signup`: 회원가입 (이메일/닉네임 중복 체크 포함)
- `POST /v1/auth/login`: 로그인 및 세션 발급
- `GET /v1/users/me`: 내 정보 조회 및 수정
- `POST /v1/users/me/profile-image`: 프로필 이미지 업로드

### 게시글 (Post)
- `GET /v1/posts`: 목록 조회 (Offset 기반 페이징 및 카운트 캐시 반영)
- `GET /v1/posts/{postId}`: 상세 조회 (조회수 자동 증가)
- `POST /v1/posts/image`: 게시글 이미지 업로드
- `POST /v1/posts/{postId}/likes`: 좋아요 토글

### 댓글 (Comment)
- `GET /v1/posts/{postId}/comments`: 특정 게시글의 댓글 목록
- `POST /v1/posts/{postId}/comments`: 댓글 작성 (작성 즉시 게시글 카운트 업데이트)

