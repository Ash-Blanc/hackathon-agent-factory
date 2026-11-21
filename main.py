"""
Hackathon Agent Factory - Central Orchestrator & CLI
Runs the radar -> intel -> ideation -> build loop.
"""

import asyncio
import os
import sys
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from scrapers.tinyfish_radar import TinyFishRadar
from intel.parallel_scout import ParallelIntelScout
from factory.sandbox_runner import SandboxAgentRunner

console = Console()

async def main():
    console.print(Panel.fit("[bold cyan]⚡ Autonomous Hackathon Agent Factory Loop ⚡[/bold cyan]\n[dim]TinyFish Radar • Parallel Intel • Nia Context • OpenCode Cloud Sandbox[/dim]"))

    # Phase 1: Radar Scan
    console.print("\n[bold yellow]🔍 Phase 1: Radar Scan (TinyFish)[/bold yellow]")
    radar = TinyFishRadar()
    hackathons = await radar.run_radar()
    
    table = Table(title="Top High-Prize & AI-Permitted Hackathons Found")
    table.add_column("Platform", style="cyan")
    table.add_column("Title", style="bold white")
    table.add_column("Prize Pool", style="green")
    table.add_column("Win Potential", style="magenta")
    
    if not hackathons:
        console.print("[dim]No live API hackathons returned or mock network rate limit hit. Generating sample targets...[/dim]")
        # Demo fallback target
        from scrapers.models import HackathonOpportunity
        hackathons = [
            HackathonOpportunity(
                id="devpost-ai-agents-2026",
                title="Global Agentic AI Hackathon 2026",
                url="https://devpost.com/hackathons/sample",
                platform="devpost",
                total_prize_usd=50000.0,
                deadline_utc="2026-12-05",
                days_left=14,
                ai_permitted=True,
                ai_rules_summary="Full AI builder assistance permitted",
                sponsors=["Anthropic", "Supabase", "Cloudflare"],
                tags=["AI", "Agents", "DevTools"],
                win_potential_score=9.2
            )
        ]

    for h in hackathons:
        table.add_row(h.platform, h.title, f"${h.total_prize_usd:,.0f}", f"{h.win_potential_score}/10")
    console.print(table)

    selected = hackathons[0]
    console.print(f"\n[bold green]🎯 Selected Target:[/bold green] [bold white]{selected.title}[/bold white] (Prize: ${selected.total_prize_usd:,.0f})")

    # Phase 2: Competitive Intelligence & Ideation
    console.print("\n[bold yellow]🧠 Phase 2: Parallel.ai & Nia Comp Intel Synthesis[/bold yellow]")
    scout = ParallelIntelScout()
    intel_report = await scout.analyze_hackathon(selected)
    
    console.print(f"[bold cyan]Recommended Concept:[/bold cyan] {intel_report.recommended_concept.get('title')}")
    console.print(f"[bold dim]One-liner:[/bold dim] {intel_report.recommended_concept.get('one_liner')}")
    console.print("[bold cyan]Unfair Advantages:[/bold cyan]")
    for adv in intel_report.unfair_advantages:
        console.print(f"  • {adv}")

    # Phase 3: Sandbox Build Scaffold
    console.print("\n[bold yellow]🛠️ Phase 3: Cloud Sandbox Preparation (OpenCode / Hermes)[/bold yellow]")
    workspace_dir = f"/home/ash/lab/hackathon-agent-factory/data/builds/{selected.id}"
    runner = SandboxAgentRunner(sandbox_type="local")
    runner.scaffold_project(workspace_dir, intel_report.recommended_concept)
    
    console.print(f"[bold green]✔ Factory Loop Ready![/bold green] Workspace set at: [underline]{workspace_dir}[/underline]")
    console.print("[dim]Next step: Run OpenCode/Hermes with Nia & Parallel MCP to execute the build automatically.[/dim]\n")

if __name__ == "__main__":
    asyncio.run(main())
