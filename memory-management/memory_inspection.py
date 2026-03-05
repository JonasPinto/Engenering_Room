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
            "intro_title": f"{Color.YELLOW}--- O mesmo dado em tipos diferentes tem tamanho diferente na memoria ---{Color.END}",
            "narrative": (
                "Para máxima eficiência e menores custos, cada byte conta.\n"
                "Este experimento permite mensurar a quantidade de memória alocada em cada tipo de dado,\n"
                "impactando diretamente o desempenho do software como um todo."
            ),
            "continue": "\nPressione ENTER para verificar...",
            "input_prompt": (
                f"\n{Color.YELLOW}Escolha um tipo de dado e digite com o mesmo padrão abaixo{Color.END}\n"
                f"\n{Color.BOLD}Exemplos:{Color.END}\n"
                f"  {Color.GREEN}(10, 200){Color.END}  \u2190 Tupla\n"
                f"  {Color.CYAN}'nome'{Color.END}     \u2190 String\n" 
                f"  {Color.YELLOW}[1, 2, 3]{Color.END}  \u2190 Lista\n"
                f"  {Color.RED}2506{Color.END}       \u2190 Inteiro\n"
                f"  {Color.MAGENTA}1.89{Color.END}       \u2190 Float\n\n"
                f"{Color.BOLD}Digitar Dado: {Color.END}"
            ),
            "table_header": f"{Color.BOLD}{'Estrutura':<15} | {'Conteúdo':<15} | {'Shallow':<15} | {'Deep'}{Color.END}",
            "legend_title": f"\n{Color.YELLOW}--- ENTENDA OS RESULTADOS ---{Color.END}",
            "shallow_def": f"{Color.BOLD}Shallow:{Color.END} O peso do identificador/endereço (sem conteúdo).",
            "deep_def": f"{Color.BOLD}Deep:{Color.END} O peso de toda a estrutura + conteúdo no silício.",
            "static_facts": (
                f"\n{Color.CYAN}--- TIPOS ESTÁTICOS ---{Color.END}\n"
                "'None' e 'Booleanos' (True/False) nunca mudam de tamanho.\n"
                "•  None:       16 bytes\n" 
                "• True/False:  28 bytes.\n"
            ),
            "na": "Não Aplicável"
        }
    return {
        "intro_title": f"{Color.YELLOW}--- THE SAME DATA IN DIFFERENT TYPES HAS DIFFERENT MEMORY SIZES ---{Color.END}",
        "narrative": (
            "For maximum efficiency and lower costs, every byte counts.\n"
            "This experiment allows measuring the amount of memory allocated in each data type,\n"
            "directly impacting the software performance as a whole."
        ),
        "continue": "\nPress ENTER to verify...",
        "input_prompt": (
            f"\n{Color.YELLOW}Choose a data type and type it following the pattern below{Color.END}\n"
            f"\n{Color.BOLD}Examples:{Color.END}\n"
            f"  {Color.GREEN}(10, 200){Color.END}  \u2190 Tuple\n"
            f"  {Color.CYAN}'nome'{Color.END}     \u2190 String\n"
            f"  {Color.YELLOW}[1, 2, 3]{Color.END}  \u2190 List\n"
            f"  {Color.RED}2506{Color.END}       \u2190 Integer\n"
            f"  {Color.MAGENTA}1.89{Color.END}       \u2190 Float\n\n"
            f"{Color.BOLD}Your input: {Color.END}"
        ),
        "table_header": f"{Color.BOLD}{'Structure':<15} | {'Content':<15} | {'Shallow':<15} | {'Deep'}{Color.END}",
        "legend_title": f"\n{Color.YELLOW}--- UNDERSTANDING THE RESULTS ---{Color.END}",
        "shallow_def": f"{Color.BOLD}Shallow:{Color.END} The weight of the identifier/address (without content).",
        "deep_def": f"{Color.BOLD}Deep:{Color.END} The weight of the entire structure + content in the silicon.",
        "static_facts": (
            f"\n{Color.CYAN}--- STATIC TYPES ---{Color.END}\n"
            "'None' and 'Booleans' (True/False) never change size.\n"
            "•  None:       16 bytes\n"
            "• True/False:  28 bytes.\n"
        ),
        "na": "Not Applicable"
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

    # Verificação técnica de Hashability
    is_hashable = base_val.__hash__ is not None if base_val is not None else False
    
    # Verificação de conversão numérica
    is_numeric = str(base_val).lstrip('-').replace('.','',1).isdigit()

    # Lógica de Comparação
    comparisons = [
        ("String", str(base_val)),
        ("Integer", int(float(base_val)) if is_numeric else None),
        ("Float", float(base_val) if is_numeric else None),
        ("List", [base_val]),
        ("Tuple", (base_val,)),
        ("Set", {base_val} if is_hashable else None),
        ("Dict (as Key)", {base_val: " "} if is_hashable else None),
        ("Dict (as Val)", {" ": base_val})
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
            print(f"{Color.RED}{name:<15} | {t['na']:<15} | {'-':<15} | {'-'}{Color.END}")

    print("="*75)
    print(t["legend_title"])
    print(f" \u2192 {t['shallow_def']}")
    print(f" \u2192 {t['deep_def']}")
    print(t["static_facts"])
    print("\n")

if __name__ == "__main__":
    run_lab()