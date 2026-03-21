from rich import box
from rich.console import Console
from rich.table import Table

def _choose_style(average: float) -> str:
    """Choose correct color of style"""
    if average <= 2.0:
        return "bold deep_sky_blue3"
    elif average <= 3.5:
        return "bold orange_red1"
    else:
        return "bold red1"

def display_results(data: dict[str, float]) -> None:
    """Display results (subject and it's average)"""
    if not data:
        return

    table = Table(box=box.SIMPLE)
    table.add_column("Subject")
    table.add_column("Average", style="cyan")

    for subject, average in data.items():
        style = _choose_style(average)
        table.add_row(subject, f"[{style}]{average}[/{style}]")

    console = Console()
    console.print(table)