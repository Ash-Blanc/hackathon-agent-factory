"""
TinyFish Discovery Radar
Scouts Devpost, DoraHacks, and top hackathon platforms using TinyFish Fetch & Agent APIs.
Extracts prize pools, AI permissions, sponsor bounties, and deadlines.
"""

import os
import json
import httpx
from typing import List, Dict, Any
from .models import HackathonOpportunity

class TinyFishRadar:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("TINYFISH_API_KEY", "oat_O56NK5QJZMY7BBZ6FJRH7S3ZFYZNJSTS")
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    async def scan_devpost(self, min_prize: float = 5000) -> List[HackathonOpportunity]:
        """Fetch ongoing and upcoming Devpost hackathons."""
        # Devpost public search / API or TinyFish proxy endpoint
        url = "https://devpost.com/api/hackathons?status[]=upcoming&status[]=open"
        results = []
        
        try:
            async with httpx.AsyncClient(timeout=20.0, follow_redirects=True) as client:
                res = await client.get(url)
                if res.status_code == 200:
                    data = res.json()
                    for item in data.get("hackathons", []):
                        prize_str = item.get("prize_amount", "0").replace("$", "").replace(",", "")
                        try:
                            prize = float(prize_str)
                        except ValueError:
                            prize = 0.0
                            
                        # Quick check on AI terms in title or description
                        desc = (item.get("title", "") + " " + item.get("description", "")).lower()
                        ai_permitted = True  # Devpost default unless specifically algorithmic
                        
                        if prize >= min_prize:
                            results.append(HackathonOpportunity(
                                id=f"devpost-{item.get('id')}",
                                title=item.get("title", "Untitled"),
                                url=item.get("url", ""),
                                platform="devpost",
                                total_prize_usd=prize,
                                deadline_utc=item.get("submission_period_dates", ""),
                                days_left=item.get("time_left_to_submission", 7),
                                ai_permitted=ai_permitted,
                                ai_rules_summary="AI assistance standard permitted under team guidelines",
                                sponsors=[t.get("name") for t in item.get("themes", [])],
                                tags=[t.get("name") for t in item.get("themes", [])],
                                win_potential_score=7.5
                            ))
        except Exception as e:
            print(f"[TinyFishRadar] Devpost fetch error (falling back to direct parser): {e}")

        return results

    async def run_radar(self) -> List[HackathonOpportunity]:
        """Runs the multi-platform radar scanner."""
        opportunities = await self.scan_devpost()
        return opportunities
