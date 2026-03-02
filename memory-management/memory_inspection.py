"""
A technical inspection tool to measure physical memory impact.
-------------------------------------------
Uma ferramenta de inspeção técnica para medir o impacto na memória física.
"""

import os
import sys
import time
import ast
from pympler import asizeof

# Cores para o terminal | Terminal colors
class Color:
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    MAGENTA = '\033[95m' 
    WHITE = '\033[97m'   
    BOLD = '\033[1m'
    END = '\033[0m'

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def loading_animation(is_pt):
    msg = "Auditing physical costs..." if not is_pt else "Auditando custos físicos..."
    print(f"\n{Color.CYAN}{msg}{Color.END}")
    for _ in range(3):
        print(".", end="", flush=True) 
        time.sleep(0.4)
    print("\n")

def get_translations(is_pt):
    if is_pt:
        return {
            "intro_title": f"{Color.YELLOW}--- INSPEÇÃO TÉCNICA DE MEMÓRIA ---{Color.END}",
            "narrative": (
                "No desenvolvimento de alta performance, cada byte conta.\n"
                "Custos físicos são uma realidade e, em alta escala, a eficiência não se discute.\n"
                "Esta ferramenta permite observar e mensurar como a memória é mapeada e alocada,\n"
                "impactando diretamente a arquitetura do software como um todo."
            ),
            "continue": "\nPressione ENTER para iniciar a inspeção...",
            "input_prompt": (
                f"\n{Color.BOLD}Exemplos:{Color.END}\n"
                f"  {Color.GREEN}(10, 200){Color.END}  \u2190 Tupla\n"
                f"  {Color.CYAN}'nome'{Color.END}     \u2190 String\n" 
                f"  {Color.YELLOW}[1, 2, 3]{Color.END}  \u2190 Lista\n"
                f"  {Color.RED}2506{Color.END}       \u2190 Inteiro\n"
                f"  {Color.MAGENTA}1.89{Color.END}       \u2190 Float\n\n"
                f"{Color.BOLD}Sua entrada: {Color.END}"
            ),
            "table_header": f"{Color.BOLD}{'Estrutura':<15} | {'Conteúdo':<15} | {'Rasa (Envelope)':<15} | {'Real (Total)'}{Color.END}",
            "legend_title": f"\n{Color.YELLOW}--- ENTENDA OS RESULTADOS ---{Color.END}",
            "shallow_def": f"{Color.BOLD}Memoria (Rasa):{Color.END} O peso do identificador/endereço (independente do conteúdo).",
            "deep_def": f"{Color.BOLD}Memoria (Real):{Color.END} O peso real somado de toda a estrutura + conteúdo no silício.",
            "static_facts": (
                f"\n{Color.CYAN}--- TIPOS ESTÁTICOS ---{Color.END}\n"
                "• 'None' e 'Booleanos' (True/False) nunca mudam de tamanho.\n"
                "•  None:       16 bytes\n" 
                "• True/False:  28 bytes.\n"
            ),
            "na": "Não Aplicável"
        }
    return {
        "intro_title": f"{Color.YELLOW}--- TECHNICAL MEMORY INSPECTION ---{Color.END}",
        "narrative": (
            "In high-performance development, every byte counts.\n"
            "Physical costs are a reality and, at scale, efficiency is non-negotiable.\n"
            "This tool allows us to observe and measure how memory is mapped and allocated,\n"
            "directly impacting the software architecture as a whole."
        ),
        "continue": "\nPress ENTER to start inspection...",
         "input_prompt": (
                f"\n{Color.BOLD}Examples:{Color.END}\n" 
                f"  {Color.GREEN}(10, 200){Color.END}  \u2190 Tupla\n"
                f"  {Color.CYAN}'nome'{Color.END}     \u2190 String\n"
                f"  {Color.YELLOW}[1, 2, 3]{Color.END}  \u2190 Lista\n"
                f"  {Color.RED}2506{Color.END}       \u2190 Inteiro\n"
                f"  {Color.MAGENTA}1.89{Color.END}       \u2190 Float\n\n"
                f"{Color.BOLD}Your inpu: {Color.END}"
            ),
        "table_header": f"{Color.BOLD}{'Structure':<15} | {'Content':<15} | {'Shallow (Envelope)':<15} | {'Deep (Total)'}{Color.END}",
        "legend_title": f"\n{Color.YELLOW}--- UNDERSTANDING THE RESULTS ---{Color.END}",
        "shallow_def": f"{Color.BOLD}Memory (Shallow):{Color.END} The weight of the identifier/address (regardless of the content).",
        "deep_def": f"{Color.BOLD}Memory    (Deep):{Color.END} The actual combined weight of the entire structure + the content in the silicon.",
        "static_facts": (
            f"\n{Color.CYAN}--- STATIC / IMMUTABLE TYPES ---{Color.END}\n"
            "• 'None' and 'Booleans' (True/False) have fixed size (never change).\n"
            "•  None:       16 bytes\n"
            "• True/False:  28 bytes\n"
        ),
        "na": "Not Applicable (Mutable)"
    }

def run_lab():
    clear_screen()
    # Janela 1: Idioma
    lang_input = input(f"{Color.BOLD}Prefere Português? (Sim/Não): {Color.END}").strip().lower()
    is_pt = lang_input in ["sim", "s"]
    t = get_translations(is_pt)

    # Janela 2: Manifesto
    clear_screen()
    print(t["intro_title"]) 
    print(f"\n{t['narrative']}")
    input(f"{Color.YELLOW}{t['continue']}{Color.END}")

    # Janela 3: Input
    clear_screen()
    raw_input = input(f"{Color.BOLD}{t['input_prompt']}{Color.END}").strip()
    
    try:
        base_val = ast.literal_eval(raw_input)
    except:
        base_val = raw_input

    loading_animation(is_pt)

    # Verificação técnica de Hashability (Garante que não quebre com listas/dicts)
    is_hashable = base_val.__hash__ is not None if base_val is not None else False

    # Lógica de Comparação
    comparisons = [
        ("String", str(base_val)),
        ("Integer", int(base_val) if str(base_val).lstrip('-').replace('.','',1).isdigit() else None),
        ("List", [base_val]),
        ("Tuple", (base_val,)),
        ("Set", {base_val} if is_hashable else None),
        ("Dict (as Key)", {base_val: 0} if is_hashable else None),
        ("Dict (as Val)", {"key": base_val})
    ]

    # Janela 4: Resultados
    clear_screen()
    print(t["intro_title"])
    print("\n" + "="*75)
    print(t["table_header"]) 
    print("-" * 75)

    for name, obj in comparisons:
        if obj is not None:
            s_size = sys.getsizeof(obj)
            d_size = asizeof.asizeof(obj)
            display = str(obj) if len(str(obj)) < 15 else str(obj)[:12] + "..."
            print(f"{name:<15} | {display:<15} | {s_size:<6} bytes   | {d_size:<6} bytes")
        else:
            # Caso o dado seja mutável (lista), ele não pode ser Chave ou Set
            print(f"{Color.RED}{name:<15} | {t['na']:<15} | {'-':<15} | {'-'}{Color.END}")

    print("="*75)
    print(t["legend_title"])
    print(f" \u2192 {t['shallow_def']}")
    print(f" \u2192 {t['deep_def']}")
    
    
    
    print(t["static_facts"])
    print("\n")

if __name__ == "__main__":
    run_lab()