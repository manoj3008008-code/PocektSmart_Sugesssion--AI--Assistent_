from typing import List, Optional, Literal, Any
from pydantic import BaseModel, EmailStr, Field, ConfigDict

class RegisterRequest(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)

class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)

class HomeItem(BaseModel):
    category: str
    item: str
    quantity: int = Field(ge=1, le=100)
    priority: str = "balanced"

class HomeRequest(BaseModel):
    budget: float = Field(gt=0, le=10_000_000)
    rooms: List[str] = Field(min_length=1)
    items: List[HomeItem] = Field(min_length=1)
    style: str = "modern"
    city: str = "Chennai"

class PartyRequest(BaseModel):
    budget: float = Field(gt=0, le=10_000_000)
    guests: int = Field(gt=0, le=100000)
    event_type: str = Field(min_length=2, max_length=100)
    venue: str = "flexible"
    city: str = "Chennai"
    food_preference: str = "mixed"

class JewelryRequest(BaseModel):
    budget: float = Field(gt=0, le=10_000_000)
    occasion: str = Field(min_length=2, max_length=100)
    style: str = "elegant"
    outfit_color: Optional[str] = None
    outfit_notes: Optional[str] = None

class RecommendationItem(BaseModel):
    name: str
    category: str
    estimated_price: float
    platform: str
    reason: str
    search_url: str

class RecommendationResponse(BaseModel):
    planner: Literal["home", "party", "jewelry"]
    summary: str
    budget: float
    allocated_total: float
    items: List[RecommendationItem]
    tips: List[str]
    disclaimer: str
    ai_source: str

class HistoryItem(BaseModel):
    id: int
    planner: str
    request: Any
    response: Any
    created_at: str
