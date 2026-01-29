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
- **Database**: MySQL
- **Security**: bcrypt (Password Hashing), Starlette Session (Cookie-based)
- **ID System**: ULID (python-ulid)
- **Testing**: pytest 기반 API 통합 테스트 환경 구축
- **Infrastructure**: Structured Logging (logging + contextvars)

## 프로젝트 구조

```
2-owen-community-be/
├── main.py               # 앱 초기화, 미들웨어 및 전역 로깅 설정
├── config.py             # 환경 설정 (Pydantic Settings 활용)
├── routers/              # API 엔드포인트 정의 (v1)
├── controllers/          # 비즈니스 로직 및 DTO 변환
├── models/               # 데이터 접근 및 MySQL DB 연동
├── schemas/              # Pydantic 기반 Request/Response DTO
├── db/                   # SQL 스키마 및 초기 데이터 (schema.sql, seed.sql)
├── utils/                # 공통 유틸리티
│   ├── common/           # 공통 응답 및 ID 유틸리티
│   ├── database/         # MySQL 커넥션 풀 및 쿼리 실행기 (로깅 포함)
│   ├── errors/           # 예외 처리기 및 에러 코드 정의
│   ├── middleware/       # 인증, DB 세션, Request ID 미들웨어
│   └── test/             # 테스트 지원 유틸리티
└── public/               # 업로드된 이미지 저장소 (post, profile)
```

## 운영 및 디버깅 (Logging)

본 프로젝트는 실무 수준의 디버깅을 위해 **통합 로깅 시스템**이 구축되어 있습니다.

- **Request ID 추적**: 모든 요청에 고유 ID가 부여되며, FE-BE-DB 로그가 이 ID를 통해 하나로 연결됩니다.
- **DB 쿼리 로깅**: 쿼리 실패 시 실제 SQL 문과 파라미터가 `backend.log`에 기록됩니다.
- **계층별 에러 식별**: 프론트엔드 콘솔에서 에러가 백엔드/DB에서 발생했는지, 네트워크 문제인지 즉시 식별 가능합니다.
- **로그 저장**: `2-owen-community-be/backend.log` 파일 및 터미널 표준 출력으로 기록됩니다.

## 시작하기

### 1. 환경 설정
`.env` 파일을 생성하고 필요한 설정을 입력합니다.

### 2. 데이터베이스 세팅
MySQL 서버가 실행 중이어야 하며, 아래 순서로 테이블을 생성하고 초기 데이터를 삽입합니다.

1.  **데이터베이스 생성**
2.  **스키마 적용**: `db/schema.sql` 파일을 실행하여 테이블 및 인덱스를 생성합니다.
3.  **초기 데이터 삽입 (선택)**: `db/seed.sql` 파일을 실행하여 관리자 계정 등 초기 데이터를 삽입합니다.

### 2-1. 대량 더미 데이터 생성 (성능 테스트용)
`db/generate_dummy_data.py` 스크립트를 사용하면 10만 건 수준의 더미 데이터를 생성할 수 있습니다.

```bash
python db/generate_dummy_data.py --users 10000 --posts 40000 --comments 50000 --batch-size 5000 --clear
```

### 2-2. 성능 분석 및 인덱스 최적화 가이드
- `db/perf_analysis.sql`: 주요 조회 쿼리에 대한 EXPLAIN 템플릿
- `db/index_optimizations.sql`: EXPLAIN/슬로우쿼리 결과 기반 인덱스 후보

### 3. 의존성 설치
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