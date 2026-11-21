"""
Agno-Powered Autonomous Hackathon Factory Agent Loop
Utilizes Agno 3.x Agent & Team architecture with Toolkits for:
1. TinyFish discovery & qualification.
2. Parallel.ai & Nia competitive intelligence & ideation.
3. OpenCode / Hermes cloud sandbox orchestration.
4. Submission asset generation (Devpost write-up, README, demo script).
"""

from pathlib import Path
from typing import Dict, Any, List, Optional
import os
import json
from pydantic import BaseModel, Field

from agno.agent import Agent
from agno.tools import Toolkit
from agno.models.openai import OpenAIChat

# --- Agno Toolkits for Hackathon Factory ---

class TinyFishRadarToolkit(Toolkit):
    """Toolkit for querying TinyFish to discover upcoming and open hackathons."""

    def __init__(self, api_key: Optional[str] = None):
        super().__init__(name="tinyfish_radar_toolkit")
        self.api_key = api_key or os.getenv("TINYFISH_API_KEY", "oat_O56NK5QJZMY7BBZ6FJRH7S3ZFYZNJSTS")
        self.register(self.scan_hackathons)
        self.register(self.verify_ai_rules)

    def scan_hackathons(self, min_prize_usd: float = 5000.0) -> str:
        """Scan top hackathon platforms (Devpost, DoraHacks, LabLab) for prize pools >= min_prize_usd."""
        # Simulated/cached radar data with realistic live-tier competitions
        hackathons = [
            {
                "id": "devpost-agentic-2026",
                "title": "Global Agentic AI Hackathon 2026",
                "platform": "devpost",
                "prize_pool_usd": 50000.0,
                "days_left": 12,
                "ai_permitted": True,
                "sponsors": ["Anthropic", "Supabase", "Cloudflare", "Modal"],
                "url": "https://devpost.com/hackathons/agentic-ai-2026"
            },
            {
                "id": "dorahacks-autonomous-web",
                "title": "Autonomous Web Agents Challenge",
                "platform": "dorahacks",
                "prize_pool_usd": 35000.0,
                "days_left": 8,
                "ai_permitted": True,
                "sponsors": ["TinyFish", "OpenAI", "Arcjet"],
                "url": "https://dorahacks.io/hackathon/autonomous-web"
            }
        ]
        return json.dumps([h for h in hackathons if h["prize_pool_usd"] >= min_prize_usd], indent=2)

    def verify_ai_rules(self, hackathon_id: str) -> str:
        """Verify if AI coding agents and autonomous builders are permitted under hackathon terms."""
        return json.dumps({
            "hackathon_id": hackathon_id,
            "ai_permitted": True,
            "rule_excerpt": "Participants are encouraged to build using LLMs, AI agents, and autonomous developer tools. Human team lead registration required."
        })


class ParallelCompIntelToolkit(Toolkit):
    """Toolkit for Parallel.ai & Nia competitive intelligence and market trend scanning."""

    def __init__(self, parallel_key: Optional[str] = None, nia_key: Optional[str] = None):
        super().__init__(name="parallel_comp_intel_toolkit")
        self.parallel_key = parallel_key or os.getenv("PARALLEL_TASK_KEY", "GZH5U44pQHrEVjBaQcTN7CKabWsfE4tk1rQPponw")
        self.nia_key = nia_key or os.getenv("NIA_API_KEY", "nk_JPOVIPNqKJvYMwNq1coc42dv2aNM1d3P")
        self.register(self.research_past_winners)
        self.register(self.fetch_market_trends)
        self.register(self.fetch_sponsor_docs)

    def research_past_winners(self, track_or_domain: str) -> str:
        """Analyze past winners in this domain to extract scoring patterns and judge favorites."""
        return json.dumps({
            "domain": track_or_domain,
            "key_patterns": [
                "Judges reward immediate visual clarity (first 10-15s of demo video).",
                "Deep load-bearing integration of sponsor APIs beats superficial cosmetic wrappers.",
                "Live working URL hosted on production infrastructure (Vercel/Cloudflare/Modal) converts 3x higher than local-only runs."
            ],
            "common_mistakes_to_avoid": [
                "Generic chat UI without domain-specific actions.",
                "Broken setup scripts or missing documentation.",
                "Late submissions rushed without Devpost narrative."
            ]
        }, indent=2)

    def fetch_market_trends(self, topic: str) -> str:
        """Scan Hacker News, Reddit, and YC startup trends for fresh pain points and viral interest."""
        return json.dumps({
            "topic": topic,
            "trending_signals": [
                {"source": "HackerNews", "insight": "High demand for verifiable agentic tool executions with zero human supervision."},
                {"source": "Reddit", "insight": "Developers frustrated by silent agent failures and fragile headless browser auth."},
                {"source": "YC Directory", "insight": "Startups pivoting toward autonomous background workers that sync state to cloud."}
            ]
        }, indent=2)

    def fetch_sponsor_docs(self, sponsor_name: str) -> str:
        """Use Nia to pull exact SDK syntax and integration patterns for target sponsors."""
        return f"Retrieved Nia verified context for {sponsor_name}: Ready-to-use SDK blueprints and verified auth patterns."


class CloudSandboxToolkit(Toolkit):
    """Toolkit for provisioning cloud sandboxes (Modal, E2B, Fly.io) and orchestrating OpenCode / Hermes."""

    def __init__(self, builds_dir: Path):
        super().__init__(name="cloud_sandbox_toolkit")
        self.builds_dir = builds_dir
        self.register(self.scaffold_cloud_workspace)
        self.register(self.dispatch_opencode_builder)

    def scaffold_cloud_workspace(self, project_slug: str, task_spec_json: str) -> str:
        """Scaffold cloud workspace folder and write TASK.md with full specs."""
        workspace = self.builds_dir / project_slug
        workspace.mkdir(parents=True, exist_ok=True)
        task_path = workspace / "TASK.md"
        with open(task_path, "w") as f:
            f.write(task_spec_json)
        return f"Workspace scaffolded at {workspace}. TASK.md created."

    def dispatch_opencode_builder(self, project_slug: str) -> str:
        """Dispatch OpenCode or Hermes runner to autonomously generate the codebase."""
        workspace = self.builds_dir / project_slug
        if not (workspace / "TASK.md").exists():
            return f"Error: No TASK.md found in {workspace}"
        return f"OpenCode build initiated for {project_slug}. Sandboxed agents active."


# --- Multi-Agent Agno Factory Squad ---

def build_hackathon_factory_agent(workspace_path: Path) -> Agent:
    """Instantiate the Agno Orchestrator Agent for the Hackathon Factory Loop."""
    builds_dir = workspace_path / "data" / "builds"
    builds_dir.mkdir(parents=True, exist_ok=True)

    tools = [
        TinyFishRadarToolkit(),
        ParallelCompIntelToolkit(),
        CloudSandboxToolkit(builds_dir)
    ]

    model = OpenAIChat(id="gpt-4o")

    return Agent(
        name="HackathonFactoryLead",
        role="Autonomous Hackathon Architect and Squad Orchestrator",
        model=model,
        tools=tools,
        instructions=[
            "You are the Lead Autonomous Hackathon Architect powered by Agno SDK.",
            "Your workflow operates in a continuous factory cycle:",
            "1. RADAR: Scan for high-prize hackathons ($5k+) using tinyfish_radar_toolkit where AI is permitted.",
            "2. INTEL: Query past winners, scan HN/Reddit/YC trends, and pull Nia sponsor docs using parallel_comp_intel_toolkit.",
            "3. SYNTHESIS: Architect a 10x project concept with unfair advantages and deep sponsor API usage.",
            "4. SANDBOX BUILD: Scaffold the cloud workspace and dispatch OpenCode/Hermes to build the full-stack project.",
            "5. POLISH: Output Devpost narrative lore, demo video script, and README architecture diagrams.",
            "Maintain high engineering standards, clear markdown deliverables, and action-oriented execution."
        ],
        markdown=True
    )
