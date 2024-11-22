from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List, Dict, Optional, Any
from enum import Enum

from integrator import SystemIntegrator

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize system integrator
system = SystemIntegrator()

class MBTIType(str, Enum):
    INTJ = "INTJ"
    INTP = "INTP"
    ENTJ = "ENTJ"
    ENTP = "ENTP"
    INFJ = "INFJ"
    INFP = "INFP"
    ENFJ = "ENFJ"
    ENFP = "ENFP"
    ISTJ = "ISTJ"
    ISFJ = "ISFJ"
    ESTJ = "ESTJ"
    ESFJ = "ESFJ"
    ISTP = "ISTP"
    ISFP = "ISFP"
    ESTP = "ESTP"
    ESFP = "ESFP"

class InitialAnalysisRequest(BaseModel):
    birth_date: str
    birth_time: str
    mbti_type: MBTIType
    
    model_config = ConfigDict(arbitrary_types_allowed=True)

class SurveyResponse(BaseModel):
    responses: Dict[str, Any]
    
    model_config = ConfigDict(arbitrary_types_allowed=True)

# API Endpoints
@app.post("/analyze")
async def analyze_profile(profile: InitialAnalysisRequest):
    """Initial analysis endpoint"""
    try:
        # Generate a simple user ID (in production, this would come from auth)
        user_id = "user_" + datetime.now().strftime("%Y%m%d%H%M%S")
        
        result = system.process_initial_analysis(
            user_id=user_id,
            birth_date=profile.birth_date,
            birth_time=profile.birth_time,
            mbti_type=profile.mbti_type
        )
        
        if not result['success']:
            raise HTTPException(status_code=400, detail=result['error'])
            
        # Add user_id to response for frontend tracking
        result['data']['user_id'] = user_id
        return result
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# ... rest of your endpoints ...

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
