"""
KimiGPT - API Testing Script
Tests all configured API providers
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from src.api.api_manager import APIManager
from rich.console import Console
from rich.table import Table
from rich import print as rprint

console = Console()


def main():
    """Test all configured APIs"""
    console.print("\n[bold cyan]═══════════════════════════════════════════════════[/bold cyan]")
    console.print("[bold cyan]  KIMIGPT - API CONNECTION TESTING[/bold cyan]")
    console.print("[bold cyan]═══════════════════════════════════════════════════[/bold cyan]\n")

    # Initialize API Manager
    console.print("[yellow]Initializing API Manager...[/yellow]")
    api_manager = APIManager()

    # Test all APIs
    console.print("\n[yellow]Testing API connections...[/yellow]\n")
    results = api_manager.test_apis()

    # Create results table
    table = Table(title="API Test Results")
    table.add_column("Provider", style="cyan")
    table.add_column("Status", style="")
    table.add_column("Details", style="dim")

    for provider, success in results.items():
        status = "[green]✓ PASS[/green]" if success else "[red]✗ FAIL[/red]"
        details = "Connected successfully" if success else "Connection failed"
        table.add_row(provider.capitalize(), status, details)

    console.print(table)

    # Show overall status
    passed = sum(results.values())
    total = len(results)

    console.print(f"\n[bold]Results: {passed}/{total} APIs working[/bold]")

    if passed == 0:
        console.print("\n[bold red]⚠️ No APIs are working! Please check your .env file.[/bold red]")
        console.print("[yellow]Run: cp .env.example .env and add your API keys[/yellow]")
    elif passed < total:
        console.print("\n[bold yellow]⚠️ Some APIs failed. System will use available APIs.[/bold yellow]")
    else:
        console.print("\n[bold green]✓ All APIs working! System ready.[/bold green]")

    # Show detailed status
    console.print("\n[yellow]Detailed API Status:[/yellow]")
    status = api_manager.get_status()

    status_table = Table()
    status_table.add_column("Provider", style="cyan")
    status_table.add_column("Requests", justify="right")
    status_table.add_column("Failures", justify="right")
    status_table.add_column("Success Rate", justify="right")
    status_table.add_column("Avg Time", justify="right")

    for provider, info in status["providers"].items():
        success_rate = f"{info['success_rate'] * 100:.1f}%"
        avg_time = f"{info['avg_response_time']:.2f}s"
        status_table.add_row(
            provider.capitalize(),
            str(info['requests']),
            str(info['failures']),
            success_rate,
            avg_time
        )

    console.print(status_table)

    console.print("\n[bold cyan]═══════════════════════════════════════════════════[/bold cyan]\n")


if __name__ == "__main__":
    main()
