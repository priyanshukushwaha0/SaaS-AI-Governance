from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import Base, engine, get_db
from app.models import AIAsset, AIInteraction
from app.schemas import AIAssetSchema, AIInteractionSchema, InteractionCreate
from app.discovery import run_saas_discovery_scan
from app.monitoring import vector_engine, analyze_risk_with_groq

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="FLYYY.AI - SaaS AI Discovery & Governance Platform",
    description="Centralized discovery, asset inventory, and interaction monitoring for embedded SaaS AI capabilities."
)

@app.get("/")
def root():
    return {"status": "active", "platform": "FLYYY.AI Governance Engine"}

@app.post("/api/v1/discovery/run")
def trigger_discovery(db: Session = Depends(get_db)):
    added = run_saas_discovery_scan(db)
    return {"message": "SaaS AI Discovery scan complete", "new_assets_discovered": added}

@app.get("/api/v1/assets", response_model=List[AIAssetSchema])
def get_ai_assets(db: Session = Depends(get_db)):
    return db.query(AIAsset).all()

@app.patch("/api/v1/assets/{asset_id}/status")
def update_asset_status(asset_id: int, review_status: str, db: Session = Depends(get_db)):
    asset = db.query(AIAsset).filter(AIAsset.id == asset_id).first()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    asset.review_status = review_status
    db.commit()
    return {"message": "Status updated successfully", "asset_id": asset_id, "status": review_status}

@app.get("/api/v1/interactions", response_model=List[AIInteractionSchema])
def get_interactions(db: Session = Depends(get_db)):
    return db.query(AIInteraction).all()

@app.post("/api/v1/interactions", response_model=AIInteractionSchema)
def log_interaction(payload: InteractionCreate, db: Session = Depends(get_db)):
    risk_info = analyze_risk_with_groq(payload.prompt_content or "", payload.response_content or "")
    
    interaction = AIInteraction(
        asset_id=payload.asset_id,
        user_email=payload.user_email,
        saas_platform=payload.saas_platform,
        ai_feature=payload.ai_feature,
        model_name=payload.model_name,
        prompt_content=payload.prompt_content,
        response_content=payload.response_content,
        tokens_used=payload.tokens_used,
        observability_level=payload.observability_level,
        risk_score=risk_info["risk_score"],
        risk_flag=risk_info["risk_flag"]
    )
    db.add(interaction)
    db.commit()
    db.refresh(interaction)

    if payload.prompt_content:
        vector_engine.add_interaction(interaction.id, payload.prompt_content)

    return interaction