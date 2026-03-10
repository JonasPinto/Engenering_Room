import os
import sys
import time
import ast
import array
import random
import platform
from pympler import asizeof

# Importing Rich library components
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.prompt import Prompt, IntPrompt
from rich.align import Align
from rich.text import Text
from rich.columns import Columns

# Initializing Rich console
console = Console()

# Standard color for headers, tables, and panels
THEME_COLOR = "blue"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_header(title, subtitle=None, style=f"bold {THEME_COLOR}"):
    clear_screen()
    content = Text(title, style=style)
    if subtitle:
        content.append(f"\n{subtitle}", style="dim white")
    
    panel = Panel(
        Align.center(content),
        border_style=THEME_COLOR,
        padding=(1, 2)
    )
    console.print(panel)

def get_system_info():
    """Returns a panel with system information (RAM Usage removed)."""
    info_text = Text.assemble(
        ("OS: ", "dim"), (f"{platform.system()} {platform.release()}  ", "white"),
        ("Python: ", "dim"), (f"{platform.python_version()}  ", "white")
    )
    return Panel(info_text, title="[dim]SYSTEM DASHBOARD[/dim]", border_style="dim", padding=(0, 1))

def loading_animation():
    msg = "Calculating memory footprint..."
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description=msg, total=None)
        time.sleep(1.2)

def run_inspector():
    show_header("DATA LABORATORY")
    
    # Cleaned Examples Section (Dict and Array removed)
    examples = [
        Panel("[cyan](10, 20)[/cyan]\n[dim]Tuple[/dim]", border_style="dim"),
        Panel("[green]'name'[/green]\n[dim]String[/dim]", border_style="dim"),
        Panel("[yellow][1, 2, 3][/yellow]\n[dim]List[/dim]", border_style="dim"), 
        Panel("[red]2506[/red]\n[dim]Integer[/dim]", border_style="dim"),
        Panel("[magenta]1.89[/magenta]\n[dim]Float[/dim]", border_style="dim"),
        Panel("[blue]{1, 2}[/blue]\n[dim]Set[/dim]", border_style="dim"),
    ]
    console.print("[bold white]Input Examples:[/bold white]")
    console.print(Columns(examples))
    
    raw_input = Prompt.ask(f"\n[bold white]Enter a value to analyze[/bold white]").strip()
    
    # Logic to handle comma as decimal separator
    processed_input = raw_input.replace(',', '.')
    
    try:
        # Try to evaluate the processed input (with dots)
        base_val = ast.literal_eval(processed_input)
    except:
        # If evaluation fails, use the original raw input as a string
        base_val = raw_input

    loading_animation()
    
    is_hashable = True
    try:
        hash(base_val)
    except TypeError:
        is_hashable = False
        
    # Check for numeric types (handling both int and float)
    is_numeric = False
    try:
        float(base_val)
        is_numeric = True
    except:
        pass

    comparisons = [
        ("String", str(base_val)),
        ("Integer", int(float(base_val)) if is_numeric else None),
        ("Float", float(base_val) if is_numeric else None),
        ("Array (C-style)", array.array('d', [float(base_val)]) if is_numeric else None),
        ("List", [base_val]),
        ("Tuple", (base_val,)),
        ("Set", {base_val} if is_hashable else None),
        ("Dict (Key)", {base_val: " "} if is_hashable else None),
        ("Dict (Val)", {" ": base_val})
    ]

    # Table without Title
    table = Table(border_style=THEME_COLOR, header_style=f"bold {THEME_COLOR}")
    table.add_column("STRUCTURE", style="bold white", width=18)
    table.add_column("CONTENT", style="italic", width=20)
    table.add_column("SHALLOW", justify="right", width=12)
    table.add_column("DEEP", justify="right", width=12)

    for name, obj in comparisons:
        if obj is not None:
            s_size = sys.getsizeof(obj)
            d_size = asizeof.asizeof(obj)
            display = str(obj) if len(str(obj)) < 20 else str(obj)[:17] + "..."
            
            # Color based on size
            size_style = "green" if d_size < 100 else ("yellow" if d_size < 500 else "red")
            
            table.add_row(
                name, 
                display,  
                f"[{size_style}]{s_size} bytes[/{size_style}]", 
                f"[{size_style}]{d_size} bytes[/{size_style}]"
            )
        else:
            table.add_row(name, f"[dim]N/A[/dim]", "[dim]-[/dim]", "[dim]-[/dim]", style="dim")
    
    console.print(table)
    
    # Post-analysis explanation in English
    explanation = (
        "\n[bold yellow]TECHNICAL INSIGHT:[/bold yellow]\n"
        " • [bold cyan]SHALLOW[/bold cyan] accounts for the object container itself.\n"
        " • [bold cyan]DEEP[/bold cyan] measures the object and all its nested contents."
    )
    console.print(explanation)
    
    Prompt.ask(f"\n[dim]Press ENTER to return to menu...[/dim]", default="", show_default=False)

def run_benchmark():
    show_header("Starting Massive Processing...")
    
    # Interactive selection of data type and quantity
    console.print("\n[bold white]BENCHMARK CONFIGURATION:[/bold white]")
    console.print("  [bold cyan]1.[/bold cyan] Random Integers")
    console.print("  [bold cyan]2.[/bold cyan] Random Floats")
    console.print("  [bold cyan]3.[/bold cyan] Random CPFs")
    
    data_choice = Prompt.ask("\n[bold yellow]Select data type to generate[/bold yellow]", choices=["1", "2", "3"], default="")
    items_count = IntPrompt.ask("[bold yellow]How many records to generate? (Max 5,000,000)[/bold yellow]", default=1000000)
    
    # Cap the items count for safety
    items_count = min(max(1000, items_count), 5000000)

    data_type_name = { "1": "integers", "2": "floats", "3": "CPFs" }[data_choice]
    
    # Simplified Benchmark Overview
    benchmark_intro = (
        f"\n[bold white]BENCHMARK OVERVIEW:[/bold white]\n"
        f"{items_count:,} {data_type_name} will be generated and compared: RAM memory consumption vs. disk storage (HDD/SSD)."
    )
    console.print(benchmark_intro)
    console.print(f"\n[bold white]»[/bold white] Press ENTER to begin simulation...")
    input()

    # Processing with progress bar
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        console=console,
        transient=True,
    ) as progress:
        task = progress.add_task(description=f"Generating {items_count:,} {data_type_name}...", total=100)
        
        # Generating Data
        if data_choice == "1":
            raw_data = [random.randint(0, 1000000000) for _ in range(items_count)]
            progress.update(task, advance=20, description="Calculating memory: Integer List...")
            size_list = asizeof.asizeof(raw_data)
            
            progress.update(task, advance=20, description="Calculating memory: C-style Array (uint64)...")
            optimized_data = array.array('Q', raw_data)
            size_optimized = asizeof.asizeof(optimized_data)
            
            # Disk Calculation
            disk_size_csv = sum(len(str(x)) + 1 for x in raw_data[:10000]) * (items_count // 10000)
            disk_size_bin = items_count * 8
            
        elif data_choice == "2":
            raw_data = [random.random() for _ in range(items_count)]
            progress.update(task, advance=20, description="Calculating memory: Float List...")
            size_list = asizeof.asizeof(raw_data)
            
            progress.update(task, advance=20, description="Calculating memory: C-style Array (double)...")
            optimized_data = array.array('d', raw_data)
            size_optimized = asizeof.asizeof(optimized_data)
            
            # Disk Calculation
            disk_size_csv = sum(len(f"{x:.6f}") + 1 for x in raw_data[:10000]) * (items_count // 10000)
            disk_size_bin = items_count * 8
            
        else: # CPFs
            raw_data = [f"{random.randint(100,999)}.{random.randint(100,999)}.{random.randint(100,999)}-{random.randint(10,99)}" for _ in range(items_count)]
            progress.update(task, advance=20, description="Calculating memory: String List...")
            size_list = asizeof.asizeof(raw_data)
            
            progress.update(task, advance=20, description="Calculating memory: C-style Array (uint64)...")
            cpfs_ints = [int(c.replace('.','').replace('-','')) for c in raw_data]
            optimized_data = array.array('Q', cpfs_ints)
            size_optimized = asizeof.asizeof(optimized_data)
            
            # Disk Calculation
            disk_size_csv = items_count * 15
            disk_size_bin = items_count * 8

        progress.update(task, advance=60, description="Finalizing results...")

    def to_mb(b): return b / (1024 * 1024)

    # Unified Table for RAM and Disk
    unified_table = Table(title=f"CONSOLIDATED RESOURCE USAGE ({items_count:,} {data_type_name})", border_style=THEME_COLOR, header_style=f"bold {THEME_COLOR}")
    unified_table.add_column("RESOURCE", style="bold white")
    unified_table.add_column("METHOD / FORMAT", style="dim")
    unified_table.add_column("CONSUMPTION", justify="right")
    
    # RAM Section
    unified_table.add_row("RAM MEMORY", "Standard List", f"[red]{to_mb(size_list):>10.2f} MB[/red]")
    unified_table.add_row("", "C-style Array", f"[bold green]{to_mb(size_optimized):>10.2f} MB[/bold green]")
    unified_table.add_section()
    
    # Disk Section
    unified_table.add_row("DISK STORAGE", "CSV / Text File", f"[red]{to_mb(disk_size_csv):>10.2f} MB[/red]")
    unified_table.add_row("", "Binary File", f"[bold green]{to_mb(disk_size_bin):>10.2f} MB[/bold green]")

    console.print(unified_table)

    economy_ram = ((size_list - size_optimized) / size_list) * 100
    economy_disk = ((disk_size_csv - disk_size_bin) / disk_size_csv) * 100
    
    # Standardized EFFICIENCY GAINS style
    gains_section = (
        f"\n[bold yellow]EFFICIENCY GAINS:[/bold yellow]\n"
        f" • RAM: [bold green]{economy_ram:.1f}% reduction[/bold green] using C-style Arrays\n"
        f" • DISK: [bold green]{economy_disk:.1f}% reduction[/bold green] using Binary formats"
    )
    console.print(gains_section)
    
    Prompt.ask(f"\n[dim]Press ENTER to return to menu...[/dim]", default="", show_default=False)

def main():
    # Narrative styled as a visible citation 
    narrative = (
        "[bold italic cyan]\"Different data types occupy different amounts of memory.\n"
        "Every extra byte impacts performance and infrastructure costs.\n"
        "This lab measures real-world memory consumption in practice.\"[/bold italic cyan]"
    )

    while True:
        show_header("TECHNICAL MEMORY INSPECTION")
        console.print(get_system_info())
        console.print(f"\n{narrative}")
        
        console.print(f"\n  [bold cyan]1.[/bold cyan] Inspect single data point") 
        console.print(f"  [bold cyan]2.[/bold cyan] Inspect millions of data points (RAM & DISK)")
        console.print(f"  [bold red]3.[/bold red] Exit system")
         
        choice = Prompt.ask(f"\n[bold yellow]Select an option[/bold yellow]", choices=["1", "2", "3"], show_choices=False)

        if choice == '1':
            run_inspector()
        elif choice == '2':
            run_benchmark()
        elif choice == '3':
            console.print(f"\n[italic magenta]Exiting....[/italic magenta]\n")
            break

if __name__ == "__main__":
    main()
