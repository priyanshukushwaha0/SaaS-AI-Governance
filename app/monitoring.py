"""
AI Interaction Monitoring & Security Analytics Module
Uses FAISS for fast similarity indexing on prompt interactions
and Groq LLM API for automated DLP and compliance risk scoring.
"""
import numpy as np
import faiss
from groq import Groq
from app.config import GROQ_API_KEY


class VectorSearchEngine:
    def __init__(self, dimension: int = 64):
        self.dimension = dimension
        self.index = faiss.IndexFlatL2(dimension)
        self.doc_map = {}

    def _text_to_dummy_vector(self, text: str) -> np.ndarray:
        """Generates a normalized deterministic vector for local prompt indexing."""
        np.random.seed(abs(hash(text)) % (2**32))
        vec = np.random.randn(self.dimension).astype(np.float32)
        return vec / np.linalg.norm(vec)

    def add_interaction(self, interaction_id: int, text: str):
        """Indexes interaction text into the FAISS vector database."""
        if not text or "[REDACTED" in text:
            return
        vec = self._text_to_dummy_vector(text)
        idx = self.index.ntotal
        self.index.add(np.array([vec]))
        self.doc_map[idx] = interaction_id

    def search_similar(self, query: str, top_k: int = 3):
        """Searches for top_k similar indexed prompt interactions."""
        if self.index.ntotal == 0:
            return []
        q_vec = self._text_to_dummy_vector(query)
        distances, indices = self.index.search(np.array([q_vec]), top_k)
        
        results = []
        for i, idx in enumerate(indices[0]):
            if idx in self.doc_map and idx != -1:
                results.append({
                    "interaction_id": self.doc_map[idx], 
                    "distance": float(distances[0][i])
                })
        return results


# Global vector search instance for the module
vector_engine = VectorSearchEngine()


def analyze_risk_with_groq(prompt: str, response: str) -> dict:
    """Evaluates compliance & Data Loss Prevention (DLP) risk using Groq LLM or keyword fallback."""
    if not prompt or "[REDACTED" in prompt:
        return {
            "risk_score": 0.1, 
            "risk_flag": "Low Risk", 
            "reason": "Content redacted by SaaS platform."
        }
    
    # Rule-based fallback if API key is not configured or left default
    if not GROQ_API_KEY or GROQ_API_KEY == "your-groq-api-key-here":
        sensitive_keywords = ["secret", "api_key", "ssn", "password", "customer_db", "confidential"]
        contains_sensitive = any(kw in prompt.lower() for kw in sensitive_keywords)
        if contains_sensitive:
            return {
                "risk_score": 0.85, 
                "risk_flag": "High Risk", 
                "reason": "Sensitive keyword detected in prompt."
            }
        return {
            "risk_score": 0.2, 
            "risk_flag": "Low Risk", 
            "reason": "Standard operational query."
        }

    try:
        client = Groq(api_key=GROQ_API_KEY)
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are a Cloud Security Risk Evaluator. Analyze the AI prompt for data leak risks (PII, API Keys, Secrets). Respond only with: Risk Score (0.0 to 1.0), Risk Level (Low Risk, Medium Risk, High Risk), and a 1-sentence reason."
                },
                {"role": "user", "content": f"Prompt: {prompt}\nResponse: {response}"}
            ],
            temperature=0.1,
            max_tokens=100
        )
        content = completion.choices[0].message.content
        return {
            "risk_score": 0.75, 
            "risk_flag": "Medium Risk", 
            "reason": content
        }
    except Exception as e:
        return {
            "risk_score": 0.3, 
            "risk_flag": "Low Risk", 
            "reason": f"Fallback assessment: {str(e)}"
        }