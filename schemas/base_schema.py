from pydantic import BaseModel, ConfigDict
from typing import Generic, TypeVar, Optional, Any, Dict

T = TypeVar("T")

class StandardResponse(BaseModel, Generic[T]):
    """모든 API 응답의 표준 Pydantic 모델"""
    code: str
    message: str
    data: Optional[T] = None
    details: Optional[Dict[str, Any]] = None

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )
