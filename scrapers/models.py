import json
import os
import re
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class HackathonOpportunity(BaseModel):
    id: str
    title: str
    url: str
    platform: str  # devpost, dorahacks, lablab, hackerearth, taikai
    total_prize_usd: float
    deadline_utc: str
    days_left: int
    ai_permitted: bool
    ai_rules_summary: str
    sponsors: List[str] = Field(default_factory=list)
    bounties: List[Dict[str, Any]] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
    win_potential_score: float = 0.0  # 0.0 to 10.0
    recommended_tech_stack: List[str] = Field(default_factory=list)

class CompIntelReport(BaseModel):
    hackathon_id: str
    past_winners_themes: List[str] = Field(default_factory=list)
    trending_discussions: List[Dict[str, str]] = Field(default_factory=list)
    competitor_angles: List[str] = Field(default_factory=list)
    unfair_advantages: List[str] = Field(default_factory=list)
    recommended_concept: Dict[str, Any] = Field(default_factory=dict)
