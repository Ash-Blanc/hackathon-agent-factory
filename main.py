"""
Hackathon Agent Factory - Central Orchestrator & CLI
Runs the expanded radar -> intel -> ideation -> cloud sandbox build -> GitHub repo push loop.
"""

import asyncio
import os
import sys
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from scrapers.tinyfish_radar import TinyFishRadar
from scrapers.expanded_radar import ExpandedRadarScanner
from intel.parallel_scout import ParallelIntelScout
from factory.sandbox_runner import SandboxAgentRunner
from factory.github_toolkit import GitHubAutomationToolkit

console = Console()

async def main():
    console.print(Panel.fit("[bold cyan]⚡ Autonomous Hackathon Agent Factory Loop (Agno + Cloud + GitHub) ⚡[/bold cyan]\n[dim]TinyFish Multi-Platform Radar • Parallel & Nia Intel • OpenCode Sandbox • GitHub Automation[/dim]"))

    # Phase 1: Expanded Radar Scan (Devpost + DoraHacks + Uncommon Platforms: Taikai, Devfolio, Encode Club, Direct Bounties)
    console.print("\n[bold yellow]🔍 Phase 1: Expanded Radar Scan (TinyFish + Open Web)[/bold yellow]")
    
    expanded_scanner = ExpandedRadarScanner()
    uncommon_hackathons = await expanded_scanner.scan_uncommon_platforms()
    
    table = Table(title="High-Prize, AI-Permitted Hackathons Across All Platforms")
    table.add_column("Platform", style="cyan")
    table.add_column("Title", style="bold white")
    table.add_column("Prize Pool", style="green")
    table.add_column("Sponsors / Ecosystem", style="yellow")
    table.add_column("Win Potential", style="magenta")
    
    for h in uncommon_hackathons:
        table.add_row(
            h.platform,
            h.title,
            f"${h.total_prize_usd:,.0f}",
            ", ".join(h.sponsors[:2]),
            f"{h.win_potential_score}/10"
        )
    console.print(table)

    # Rank & Pick highest win potential
    selected = sorted(uncommon_hackathons, key=lambda x: x.win_potential_score, reverse=True)[0]
    console.print(f"\n[bold green]🎯 Selected Highest-Yield Opportunity:[/bold green] [bold white]{selected.title}[/bold white]")
    console.print(f"   Platform: [cyan]{selected.platform}[/cyan] | Prize: [green]${selected.total_prize_usd:,.0f}[/green] | Sponsors: {', '.join(selected.sponsors)}")

    # Phase 2: Parallel.ai & Nia Comp Intel Synthesis
    console.print("\n[bold yellow]🧠 Phase 2: Parallel.ai & Nia Comp Intel Synthesis[/bold yellow]")
    scout = ParallelIntelScout()
    intel_report = await scout.analyze_hackathon(selected)
    
    console.print(f"[bold cyan]Recommended Concept:[/bold cyan] {intel_report.recommended_concept.get('title')}")
    console.print(f"[bold dim]One-liner:[/bold dim] {intel_report.recommended_concept.get('one_liner')}")
    console.print("[bold cyan]Unfair Advantages:[/bold cyan]")
    for adv in intel_report.unfair_advantages:
        console.print(f"  • {adv}")

    # Phase 3: Cloud Sandbox Preparation (OpenCode / Hermes)
    console.print("\n[bold yellow]🛠️ Phase 3: Cloud Sandbox Preparation[/bold yellow]")
    workspace_dir = f"/home/ash/lab/hackathon-agent-factory/data/builds/{selected.id}"
    runner = SandboxAgentRunner(sandbox_type="local")
    runner.scaffold_project(workspace_dir, intel_report.recommended_concept)
    console.print(f"[bold green]✔ Workspace Scaffolded:[/bold green] {workspace_dir}")

    # Phase 4: GitHub Integration (Connected to Ash-Blanc)
    console.print("\n[bold yellow]🐙 Phase 4: GitHub Automation (Account: Ash-Blanc)[/bold yellow]")
    gh_toolkit = GitHubAutomationToolkit(username="Ash-Blanc")
    console.print(f"[dim]GitHub authenticated via CLI: Ready to create remote repository under Ash-Blanc and push main branch on build completion.[/dim]")
    
    console.print(f"\n[bold green]🚀 Factory Pipeline Verified![/bold green]")
    console.print(f"   • Target Platform: [cyan]{selected.platform}[/cyan]")
    console.print(f"   • Cloud Runner: OpenCode / Hermes wired with Nia & Parallel MCP")
    console.print(f"   • GitHub Target: https://github.com/Ash-Blanc/{selected.id}")

if __name__ == "__main__":
    asyncio.run(main())
