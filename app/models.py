from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from enum import Enum

class FashionType(str, Enum):
    CASUAL = "casual"
    FORMAL = "formal"
    PARTY = "party"
    SPORTS = "sports"
    WORK = "work"
    WEDDING = "wedding"
    BEACH = "beach"
    WINTER = "winter"
    SUMMER = "summer"

class SizeCategory(str, Enum):
    XS = "XS"
    S = "S"
    M = "M"
    L = "L"
    XL = "XL"
    XXL = "XXL"
    XXXL = "XXXL"

class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    UNISEX = "unisex"

class BudgetRange(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    LUXURY = "luxury"

class FashionRequest(BaseModel):
    fashion_type: FashionType = Field(..., description="Type of fashion/occasion")
    size: SizeCategory = Field(..., description="Clothing size")
    gender: Gender = Field(default=Gender.UNISEX, description="Gender preference")
    budget_range: BudgetRange = Field(default=BudgetRange.MEDIUM, description="Budget range")
    color_preference: str = Field(default="any", description="Preferred colors")
    body_type: str = Field(default="average", description="Body type")
    occasion_specific: str = Field(default="", description="Specific occasion details")
    style_preference: str = Field(default="modern", description="Style preference")
    
    @validator('color_preference')
    def validate_color(cls, v):
        if len(v.strip()) == 0:
            return "any"
        return v.lower().strip()
    
    class Config:
        schema_extra = {
            "example": {
                "fashion_type": "casual",
                "size": "M",
                "gender": "female",
                "budget_range": "medium",
                "color_preference": "earth tones",
                "body_type": "pear",
                "occasion_specific": "weekend brunch with friends",
                "style_preference": "bohemian"
            }
        }

class FashionResponse(BaseModel):
    status: str = Field(..., description="Response status")
    data: Dict[str, Any] = Field(..., description="Recommendation data")
    processing_time: float = Field(..., description="Processing time in seconds")
    
class ErrorResponse(BaseModel):
    status: str = "error"
    message: str
    details: Optional[Dict[str, Any]] = None