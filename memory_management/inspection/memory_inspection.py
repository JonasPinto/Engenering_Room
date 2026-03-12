import os
import sys
import time
import ast
import array
import platform
import json
import csv
import pickle
import struct
import gzip
import bz2
import msgpack
import yaml
from collections import deque, namedtuple
from pympler import asizeof

# Importing Rich library components
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.prompt import Prompt
from rich.align import Align
from rich.text import Text
from rich.columns import Columns
from rich.theme import Theme

# Customizing theme for a smoother experience
custom_theme = Theme({
    "info": "cyan",
    "warning": "magenta",
    "danger": "bold red",
    "success": "bold green",
    "muted": "dim white",
    "accent": "bold cyan"
})

console = Console(theme=custom_theme)
THEME_COLOR = "cyan"  # Softer than blue

# Classes for RAM comparison
class StandardClass:
    def __init__(self, val):
        self.data = val

class SlottedClass:
    __slots__ = ['data']
    def __init__(self, val):
        self.data = val

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_header(title, subtitle=None, style=f"bold {THEME_COLOR}"): 
    clear_screen()
    content = Text(title, style=style)
    if subtitle:
        content.append(f"\n{subtitle}", style="muted")
    panel = Panel(Align.center(content), border_style=THEME_COLOR, padding=(1, 2)) 
    console.print(panel)

def get_system_info():
    """Displays system dashboard with full width."""
    info_text = Text.assemble(
        ("OS: ", "muted"), (f"{platform.system()} {platform.release()}  ", "white"),
        ("Python: ", "muted"), (f"{platform.python_version()}  ", "white")
    )
    return Panel(
        info_text, 
        title="[bold white]SYSTEM DASHBOARD[/bold white]", 
        border_style="dim", 
        padding=(0, 1),
        expand=True
    )

def to_mb(b): 
    return b / (1024 * 1024)

def run_benchmark(data_choice, base_val):
    """Massive simulation with 3 million items and REAL file creation."""
    show_header("SIMULATION OF DATA MEMORY ON DISC") 
    
    items_count = 3000000 
    temp_dir = "/home/jonas/Engineering_Room/memory_management/inspection/files"
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    # Expanded Disk Formats
    files_to_create = [
        ("XML (Heavy Indented)", "data_indented.xml"),
        ("XML (Standard)", "data.xml"),
        ("YAML (Heavy)", "data.yaml"),
        ("JSON (Indented)", "data_indented.json"),
        ("JSON (Standard)", "data.json"),
        ("HTML (Table)", "data.html"),
        ("CSV (Standard)", "data.csv"),
        ("PICKLE (Binary)", "data.pkl"),
        ("MSGPACK (Binary)", "data.msg"),
        ("BINARY (Raw)", "data.bin"),
        ("GZIP (Compressed)", "data.csv.gz"),
        ("BZ2 (Compressed)", "data.csv.bz2")
    ]

    disk_results = {}
    
    with Progress(
        SpinnerColumn(spinner_name="dots"), 
        TextColumn("[progress.description]{task.description}"),
        BarColumn(bar_width=None, pulse_style="cyan"),
        TaskProgressColumn(),
        console=console,
        transient=True,
    ) as progress:
        
        # RAM Calculation Task
        ram_task = progress.add_task(description="[info]Analyzing Python RAM Overhead...[/info]", total=100)
        
        ptr_array_size = 8 * items_count
        obj_individual_size = asizeof.asizeof(base_val)
        total_python_ram = ptr_array_size + (obj_individual_size * items_count)
        
        if data_choice == "1": # Int
            raw_data_size = 8 * items_count
        elif data_choice == "2": # Float
            raw_data_size = 8 * items_count
        else: # String/Complex
            raw_data_size = len(str(base_val)) * items_count
            
        progress.update(ram_task, completed=100)

        # Disk Creation Tasks
        for fmt, filename in files_to_create:
            file_path = os.path.join(temp_dir, filename)
            task = progress.add_task(description=f"[warning]Creating {fmt}...[/warning]", total=items_count)
            
            try:
                if "XML" in fmt:
                    indent = "  " if "Indented" in fmt else ""
                    with open(file_path, 'w') as f:
                        f.write("<root>\n")
                        for i in range(items_count):
                            f.write(f"{indent}<item id='{i}'>{base_val}</item>\n")
                            if i % 100000 == 0: progress.update(task, advance=100000)
                        f.write("</root>")
                
                elif "YAML" in fmt:
                    with open(file_path, 'w') as f:
                        f.write("items:\n")
                        for i in range(items_count):
                            f.write(f"  - {base_val}\n")
                            if i % 100000 == 0: progress.update(task, advance=100000)
                
                elif "JSON" in fmt:
                    indent = 2 if "Indented" in fmt else None
                    with open(file_path, 'w') as f:
                        if indent:
                            f.write("[\n")
                            for i in range(items_count):
                                f.write("  ")
                                json.dump(base_val, f)
                                if i < items_count - 1: f.write(",\n")
                                if i % 100000 == 0: progress.update(task, advance=100000)
                            f.write("\n]")
                        else:
                            f.write("[")
                            for i in range(items_count):
                                json.dump(base_val, f)
                                if i < items_count - 1: f.write(",")
                                if i % 100000 == 0: progress.update(task, advance=100000)
                            f.write("]")
                
                elif "HTML" in fmt:
                    with open(file_path, 'w') as f:
                        f.write("<table>\n")
                        for i in range(items_count):
                            f.write(f"  <tr><td>{base_val}</td></tr>\n")
                            if i % 100000 == 0: progress.update(task, advance=100000)
                        f.write("</table>")

                elif "CSV" in fmt:
                    with open(file_path, 'w', newline='') as f:
                        writer = csv.writer(f)
                        for i in range(items_count):
                            writer.writerow([base_val])
                            if i % 100000 == 0: progress.update(task, advance=100000)
                
                elif "PICKLE" in fmt:
                    with open(file_path, 'wb') as f:
                        pickle.dump([base_val] * items_count, f, protocol=pickle.HIGHEST_PROTOCOL)
                        progress.update(task, completed=items_count)
                
                elif "MSGPACK" in fmt:
                    with open(file_path, 'wb') as f:
                        packer = msgpack.Packer()
                        for i in range(items_count):
                            f.write(packer.pack(base_val))
                            if i % 100000 == 0: progress.update(task, advance=100000)

                elif "BINARY" in fmt:
                    with open(file_path, 'wb') as f:
                        if data_choice == "1": data = struct.pack('q', int(base_val))
                        elif data_choice == "2": data = struct.pack('d', float(base_val))
                        else: data = str(base_val).encode('utf-8')
                        for i in range(items_count):
                            f.write(data)
                            if i % 100000 == 0: progress.update(task, advance=100000)
                
                elif "GZIP" in fmt:
                    with gzip.open(file_path, 'wt', newline='') as f:
                        writer = csv.writer(f)
                        for i in range(items_count):
                            writer.writerow([base_val])
                            if i % 100000 == 0: progress.update(task, advance=100000)
                
                elif "BZ2" in fmt:
                    with bz2.open(file_path, 'wt', newline='') as f:
                        writer = csv.writer(f)
                        for i in range(items_count):
                            writer.writerow([base_val])
                            if i % 100000 == 0: progress.update(task, advance=100000)
                
                disk_results[fmt] = os.path.getsize(file_path)
                progress.update(task, completed=items_count)
                
            except Exception as e:
                disk_results[fmt] = 0
                progress.update(task, description=f"[danger]Error {fmt}: {str(e)}[/danger]")

    # Results Table
    console.print(f"\n[accent]DATA PROCESSED:[/accent] [white]{base_val}[/white] (Replicated {items_count:,} times)\n")
    
    unified_table = Table(title=f"", border_style=THEME_COLOR, header_style=f"bold {THEME_COLOR}")
    unified_table.add_column("CATEGORY", style="bold white")
    unified_table.add_column("METHOD / FORMAT", style="muted")
    unified_table.add_column("REAL SIZE", justify="right")
    
    # RAM Rows
    unified_table.add_row("RAM (PYTHON)", "List + Python Objects", f"[danger]{to_mb(total_python_ram):>10.2f} MB[/danger]")
    unified_table.add_row("", "Raw Data (C-Equivalent)", f"[success]{to_mb(raw_data_size):>10.2f} MB[/success]")
    unified_table.add_section()
    
    # Disk Rows (Sorted by size)
    sorted_disk = sorted(disk_results.items(), key=lambda x: x[1], reverse=True)
    first = True
    for fmt, size in sorted_disk:
        cat = "DISK STORAGE" if first else ""
        if size == max(disk_results.values()): style = "danger"
        elif size == min(disk_results.values()): style = "success"
        else: style = "warning"
        
        size_str = f"[{style}]{to_mb(size):>10.4f} MB[/{style}]" if size < 1024*1024 else f"[{style}]{to_mb(size):>10.2f} MB[/{style}]"
        unified_table.add_row(cat, fmt, size_str)
        first = False

    console.print(unified_table)

    # Insights
    ram_overhead = ((total_python_ram - raw_data_size) / raw_data_size) * 100 if raw_data_size > 0 else 0
    disk_diff = (max(disk_results.values()) / min(disk_results.values())) if min(disk_results.values()) > 0 else 0
    
    console.print(f"\n[accent]TECHNICAL RESULTS:[/accent]")
    console.print(f" • [danger]RAM Overhead:[/danger] Python objects use [bold]{ram_overhead:.1f}%[/bold] more memory than raw data.")
    console.print(f" • [info]Disk Extreme:[/info] The heaviest format is [bold]{disk_diff:.1f}x[/bold] larger than the most compressed.")

    # Final Options
    console.print(f"\n[warning]WHAT WOULD YOU LIKE TO DO NEXT?[/warning]")
    console.print(f" [bold cyan]1[/bold cyan] - Analyze another data (Cleans current files)")
    console.print(f" [bold cyan]2[/bold cyan] - Delete files and EXIT program")
    
    choice = Prompt.ask("\n[bold white]Select an option[/bold white]", choices=["1", "2"], default="1")
    
    # Cleanup logic
    for _, filename in files_to_create:
        try: os.remove(os.path.join(temp_dir, filename))
        except: pass
        
    if choice == '2':
        console.print("\n[success]Files cleaned successfully. Goodbye![/success]")
        sys.exit(0)
    else:
        console.print("\n[info]Returning to main menu...[/info]")
        time.sleep(1)

def run_inspector():
    """Analyzes a single data item and then asks user to proceed to massive benchmark."""
    examples = [
        Panel("[info](10, 20)[/info]\n[muted]Tuple[/muted]", border_style="dim"),
        Panel("[success]'name'[/success]\n[muted]String[/muted]", border_style="dim"),
        Panel("[warning][1, 2, 3][/warning]\n[muted]List[/muted]", border_style="dim"), 
        Panel("[danger]2506[/danger]\n[muted]Integer[/muted]", border_style="dim"),
        Panel("[accent]1.89[/accent]\n[muted]Float[/muted]", border_style="dim"),
    ]
    console.print("[bold white]Input Examples[/bold white]")
    console.print(Columns(examples))
    
    raw_input = ""
    while not raw_input:
        raw_input = Prompt.ask(f"\n[bold white]Enter a value to analyze[/bold white]").strip()
        if not raw_input:
            console.print("[danger]Error:[/danger] Input cannot be empty.")

    processed_input = raw_input.replace(',', '.')
    try:
        base_val = ast.literal_eval(processed_input)
    except:
        base_val = raw_input

    is_hashable = True
    try: hash(base_val)
    except: is_hashable = False
        
    is_numeric = False
    try:
        float(base_val)
        is_numeric = True
    except: pass

    # MASSIVE RAM EXPANSION
    Point = namedtuple('Point', ['data'])
    
    comparisons = [
        ("String", str(base_val)),
        ("Integer", int(float(base_val)) if is_numeric else None),
        ("Float", float(base_val) if is_numeric else None),
        ("Array (C-style)", array.array('d', [float(base_val)]) if is_numeric else None),
        ("List", [base_val]),
        ("Tuple", (base_val,)),
        ("Set", {base_val} if is_hashable else None),
        ("Frozenset", frozenset([base_val]) if is_hashable else None),
        ("Deque", deque([base_val])),
        ("NamedTuple", Point(base_val)),
        ("Dict (Key:Val)", {base_val: base_val} if is_hashable else None),
        ("Bytes", str(base_val).encode('utf-8')),
        ("Bytearray", bytearray(str(base_val).encode('utf-8'))),
        ("Standard Class", StandardClass(base_val)),
        ("Slotted Class", SlottedClass(base_val))
    ]

    table = Table(title="", border_style=THEME_COLOR, header_style=f"bold {THEME_COLOR}")
    table.add_column("STRUCTURE", style="bold white", width=18)
    table.add_column("CONTENT", style="italic", width=20)
    table.add_column("SHALLOW", justify="right", width=12)
    table.add_column("DEEP", justify="right", width=12) 

    for name, obj in comparisons:
        if obj is not None: 
            s_size, d_size = sys.getsizeof(obj), asizeof.asizeof(obj)
            display = str(obj) if len(str(obj)) < 20 else str(obj)[:17] + "..."
            size_style = "success" if d_size < 100 else ("warning" if d_size < 500 else "danger")
            table.add_row(name, display, f"[{size_style}]{s_size} B[/{size_style}]", f"[{size_style}]{d_size} B[/{size_style}]")
        else:
            table.add_row(name, f"[muted]N/A[/muted]", "[muted]-[/muted]", "[muted]-[/muted]", style="dim")
    
    console.print(table)
    
    explanation = "\n[accent]UNDERSTANDING THE METRICS:[/accent]\n • [info]SHALLOW[/info] = address + data type (without content)\n • [info]DEEP[/info] = total allocated space containing the data"
    console.print(explanation)
    
    console.print(f"\n[warning]Press ENTER to analyze disk memory.[/warning]", end="")
    input()
    
    if isinstance(base_val, int): 
        run_benchmark("1", base_val)
    elif isinstance(base_val, float): 
        run_benchmark("2", base_val) 
    else: 
        run_benchmark("3", base_val) 

def main():
    narrative = ( 
        "[italic muted]\"Different types of data occupy different amounts of memory.\n"
        "Each extra byte impacts the performance and costs of an application.\n"
        "This experiment measures the actual RAM and DISC memory consumption.\"\n[/italic muted]"
    )

    while True:
        show_header("PYTHON MEMORY & DISK EXTREMES LABORATORY")
        console.print(get_system_info())
        console.print(f"\n{narrative}")
        run_inspector()
 
if __name__ == "__main__":
    main()
