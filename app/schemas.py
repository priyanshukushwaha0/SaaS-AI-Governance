from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class AIAssetSchema(BaseModel):
    id: int
    saas_platform: str
    feature_name: str
    status: str
    user_group: str
    user_count: int
    target_resources: str
    discovery_source: str
    observability_level: str
    review_status: str
    created_at: datetime

    class Config:
        from_attributes = True

class AIInteractionSchema(BaseModel):
    id: int
    asset_id: int
    user_email: str
    saas_platform: str
    ai_feature: str
    timestamp: datetime
    model_name: Optional[str]
    prompt_content: Optional[str]
    response_content: Optional[str]
    tokens_used: int
    observability_level: str
    risk_score: float
    risk_flag: str

    class Config:
        from_attributes = True

class InteractionCreate(BaseModel):
    asset_id: int
    user_email: str
    saas_platform: str
    ai_feature: str
    model_name: Optional[str] = "Unknown"
    prompt_content: Optional[str] = "[REDACTED BY SAAS PROVIDER]"
    response_content: Optional[str] = "[REDACTED BY SAAS PROVIDER]"
    tokens_used: Optional[int] = 0
    observability_level: str = "METADATA_ONLY"