# Owen Community Backend

FastAPI 기반의 커뮤니티 백엔드 API입니다. Router-Controller 패턴을 적용하여 프로젝트를 구성합니다.

## 기능

- 게시글 CRUD (Create, Read, Update, Delete)
- 전역 예외 처리 및 표준화된 API 응답
- 인메모리 저장소 기반 데이터 관리
- Pydantic을 이용한 데이터 검증
- CORS 설정

## 기술 스택

- Framework: FastAPI
- Server: Uvicorn
- Validation: Pydantic
- Storage: In-memory

## 프로젝트 구조

```
2-owen-community-be/
 main.py               # 앱 초기화 및 전역 설정
 config.py             # 환경 설정 관리
 routers/              # API 경로 및 엔드포인트 정의
 controllers/          # 비즈니스 로직 및 데이터 처리
 models/               # Pydantic 데이터 모델 (DTO)
 utils/                # 공통 유틸리티 (응답 포맷, 예외 정의)
 .env.example          # 환경 변수 템플릿
 requirements.txt      # 의존성 패키지 리스트
```

## 설치 및 실행

1. 의존성 설치
   ```bash
   pip install -r requirements.txt
   ```

2. 서버 실행
   ```bash
   uvicorn main:app --reload
   ```

## 주요 API 엔드포인트

### 공통
- GET /health: 서버 상태 확인

### 게시글 (Post)
- GET /v1/posts: 게시글 목록 조회
- GET /v1/posts/{post_id}: 게시글 상세 조회
- POST /v1/posts: 게시글 생성
- PATCH /v1/posts/{post_id}: 게시글 수정
- DELETE /v1/posts/{post_id}: 게시글 삭제

## API 응답 포맷

### 성공 응답
```json
{
  "status": "success",
  "code": "GET_POSTS_SUCCESS",
  "data": [],
  "status_code": 200
}
```

### 에러 응답
```json
{
  "status": "error",
  "code": "NOT_FOUND",
  "details": { "resource": "게시글" },
  "status_code": 404
}
```

## 주의사항

- 서버 실행 시 --reload 옵션 권장
- 모든 API 엔드포인트는 /v1 접두사 사용
