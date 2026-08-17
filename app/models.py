from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text, Float
from datetime import datetime
from app.database import Base

class AIAsset(Base):
    __tablename__ = "ai_assets"

    id = Column(Integer, primary_key=True, index=True)
    saas_platform = Column(String, index=True)      # e.g., Microsoft 365, Slack
    feature_name = Column(String)                   # e.g., Copilot, Slack AI
    status = Column(String, default="Enabled")      # Enabled / Disabled
    user_group = Column(String)                     # e.g., Sales, Engineering
    user_count = Column(Integer, default=0)
    target_resources = Column(String)               # e.g., SharePoint, Teams, Slack Channels
    discovery_source = Column(String)               # Admin API, Audit Logs
    observability_level = Column(String)           # FULL_CONTENT, METADATA_ONLY, AGGREGATE
    review_status = Column(String, default="Pending Review") # Pending Review, Approved, Flagged
    created_at = Column(DateTime, default=datetime.utcnow)

class AIInteraction(Base):
    __tablename__ = "ai_interactions"

    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, index=True)
    user_email = Column(String, index=True)
    saas_platform = Column(String)
    ai_feature = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    model_name = Column(String, nullable=True)     # e.g., GPT-4o, Claude 3.5
    prompt_content = Column(Text, nullable=True)   # Obscured if SaaS platform restricts content
    response_content = Column(Text, nullable=True) # Obscured if SaaS platform restricts content
    tokens_used = Column(Integer, default=0)
    observability_level = Column(String)           # FULL_CONTENT vs METADATA_ONLY
    risk_score = Column(Float, default=0.0)         # 0.0 to 1.0
    risk_flag = Column(String, default="Low Risk")  # Low Risk, Medium Risk, High Risk