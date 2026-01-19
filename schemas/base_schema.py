from pydantic import BaseModel, ConfigDict
from typing import Generic, TypeVar, Optional, Any, Dict

T = TypeVar("T")

class BaseSchema(BaseModel):
    """모든 Pydantic 스키마의 기본 클래스"""
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )

class StandardResponse(BaseSchema, Generic[T]):
    """모든 API 응답의 표준 Pydantic 모델"""
    code: str
    message: str
    data: Optional[T] = None
    details: Optional[Dict[str, Any]] = None
