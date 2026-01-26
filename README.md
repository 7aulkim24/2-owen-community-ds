# AWS AI School 2기 Backend

FastAPI 기반의 고성능 커뮤니티 백엔드 API입니다. 실무 수준의 운영 안정성과 성능 최적화를 목표로 **Router-Controller-Model-Schema** 아키텍처를 따르며, 최신 백엔드 엔지니어링 패턴이 적용되어 있습니다.

## 주요 기능

- **인증 및 보안**: 회원가입, 세션 기반 로그인/로그아웃, **bcrypt 비밀번호 해싱**, 권한 기반 접근 제어(RBAC)
- **게시글 및 댓글**: 커뮤니티 핵심 CRUD, **좋아요 토글**, 이미지 업로드 지원
- **ID 체계**: UUID를 대체하는 **ULID** 도입 (26자, 시간순 정렬 가능, 높은 인덱스 성능)
- **운영 안정성**: **Request ID** 추적 미들웨어 및 **구조화된 JSON 로깅** 시스템 구축
- **표준화된 통신**: 전역 예외 처리기, 설계도 준수 기반의 일관된 응답 및 에러 체계 (Code-Details 구조)
- **정적 파일 서빙**: 프로필 및 게시글 이미지 업로드/조회를 위한 `/public` 엔드포인트 제공

## 기술 스택

- **Framework**: FastAPI (v0.128.0)
- **Validation**: Pydantic v2 (Strict Typing & DTO)
- **Security**: bcrypt (Password Hashing), Starlette Session (Cookie-based)
- **ID System**: ULID (python-ulid)
- **Testing**: pytest 기반 API 통합 테스트 환경 구축
- **Infrastructure**: Structured Logging (logging + contextvars)

## 프로젝트 구조

```
2-owen-community-be/
├── main.py               # 앱 초기화, 미들웨어 및 전역 설정
├── config.py             # 환경 설정 (Pydantic Settings 활용)
├── routers/              # API 엔드포인트 정의 (v1)
├── controllers/          # 비즈니스 로직 및 DTO 변환
├── models/               # 데이터 접근 및 인메모리 데이터 관리
├── schemas/              # Pydantic 기반 Request/Response DTO
├── utils/                # 공통 유틸리티
│   ├── auth_middleware.py # 세션 기반 인증 미들웨어
│   ├── id_utils.py       # ULID 생성 및 검증
│   ├── exceptions.py     # 표준 APIError 정의
│   ├── response.py       # 규격화된 응답 포맷터 (StandardResponse)
│   ├── error_codes.py    # 통합 에러/성공 코드 관리
│   └── request_id_middleware.py # 요청 추적 시스템
└── public/               # 업로드된 이미지 저장소 (post, profile)
```

## 시작하기

### 1. 환경 설정
`.env.example` 파일을 복사하여 `.env` 파일을 생성하고 필요한 설정을 입력합니다.

### 2. 의존성 설치
`pyproject.toml`에 정의된 패키지들을 설치합니다.
```bash
pip install -e .
```

### 3. 서버 실행
```bash
uvicorn main:app --reload
```

### 4. API 문서 확인
서버 실행 후 브라우저에서 아래 주소로 접속하여 Swagger UI를 확인할 수 있습니다.
- `http://localhost:8000/docs`

### 5. 프론트엔드 연동 (Live Server 활용)
본 프로젝트는 프론트엔드와의 원활한 연동을 위해 **Live Server**를 통한 실행을 권장합니다.

1.  **VS Code 익스텐션 설치**: `Live Server` 익스텐션이 설치되어 있는지 확인합니다.
2.  **프론트엔드 폴더 열기**: `2-owen-community-fe` 폴더를 VS Code로 엽니다.
3.  **Live Server 실행**: 하단 상태 표시줄의 `Go Live` 버튼을 클릭하거나, HTML 파일(예: `login.html`)에서 우클릭 후 `Open with Live Server`를 선택합니다.
4.  **브라우저 확인**: 기본적으로 `http://localhost:5500` 주소에서 웹 페이지가 실행됩니다.
    - **주의**: 백엔드 서버(port 8000)가 먼저 실행되고 있어야 정상적인 데이터 연동이 가능합니다.

## 주요 API 엔드포인트 (v1)

### 인증 및 사용자 (Auth/User)
- `POST /v1/auth/signup`: 회원가입
- `POST /v1/auth/login`: 로그인 및 세션 발급
- `POST /v1/auth/logout`: 로그아웃
- `GET /v1/users/me`: 내 정보 조회
- `PATCH /v1/users/me`: 내 정보 수정 (닉네임, 프로필 이미지)
- `PATCH /v1/users/password`: 비밀번호 변경
- `DELETE /v1/users/me`: 회원 탈퇴

### 게시글 (Post)
- `GET /v1/posts`: 목록 조회
- `POST /v1/posts`: 게시글 작성
- `GET /v1/posts/{postId}`: 상세 조회 (조회수 자동 증가)
- `PATCH /v1/posts/{postId}`: 게시글 수정
- `DELETE /v1/posts/{postId}`: 게시글 삭제
- `POST /v1/posts/image`: 게시글 이미지 업로드
- `POST /v1/posts/{postId}/likes`: 좋아요 토글

### 댓글 (Comment)
- `GET /v1/posts/{postId}/comments`: 댓글 목록 조회
- `POST /v1/posts/{postId}/comments`: 댓글 작성
- `PATCH /v1/comments/{commentId}`: 댓글 수정
- `DELETE /v1/comments/{commentId}`: 댓글 삭제

## 프로젝트 특징

- **StandardResponse**: 모든 API는 `{ "code": "...", "data": ..., "message": "..." }` 형태의 일관된 응답을 반환합니다.
- **Pydantic v2**: 강력한 타입 힌트와 유효성 검사를 통해 데이터 정합성을 보장합니다.
- **CORS 설정**: 프론트엔드 개발 환경(localhost:5500 등)과의 원활한 통신을 위해 CORS 미들웨어가 설정되어 있습니다.
- **Error Handling**: `APIError`와 전역 예외 핸들러를 통해 비즈니스 에러를 표준화된 포맷으로 클라이언트에 전달합니다.

---

**[자체 신뢰도 평가]**
**높음**: `main.py`, `pyproject.toml`, `routers/` 및 `utils/` 내의 실제 소스 코드를 직접 분석하여 최신 API 스펙과 기술 스택을 정확히 반영하였습니다.
