#!/usr/bin/env python3
"""
VoltLink — Logo Animado para Terminal
Execute: python3 voltlink_logo.py
"""

import time
import sys
import os
import shutil

# ── Cores ANSI ──────────────────────────────────────────────
RESET   = "\033[0m"
BOLD    = "\033[1m"
DIM     = "\033[2m"

# ── Paleta Azul & Branco ─────────────────────────────────────
BLUE_ELEC = "\033[38;2;0;136;255m"       # #0088FF — azul elétrico principal
BLUE_LIGHT= "\033[38;2;100;180;255m"     # #64B4FF — azul claro / destaque
BLUE_ICE  = "\033[38;2;180;220;255m"     # #B4DCFF — azul gelo / acento suave
WHITE     = "\033[97m"                    # branco puro
WHITE_OFF = "\033[38;2;220;230;245m"     # #DCE6F5 — branco azulado
GRAY_COOL = "\033[38;2;90;110;150m"      # cinza frio azulado
DGRAY     = "\033[38;2;50;65;100m"       # cinza escuro frio
CYAN_NEON = "\033[38;2;0;210;255m"       # #00D2FF — ciano elétrico (raio)

BG_DARK   = "\033[48;2;8;12;22m"         # #080C16 — fundo quase preto azulado

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def write(text, delay=0.0):
    sys.stdout.write(text)
    sys.stdout.flush()
    if delay:
        time.sleep(delay)

def println(text="", delay=0.03):
    write(text + "\n", delay)

def typewriter(text, delay=0.025):
    for ch in text:
        write(ch)
        time.sleep(delay)
    write("\n")

# ── Largura do terminal ──────────────────────────────────────
def term_width():
    return shutil.get_terminal_size((80, 24)).columns

def center(text, visible_len=None):
    """Centraliza levando em conta códigos ANSI (invisíveis)."""
    w = term_width()
    vlen = visible_len if visible_len is not None else len(text)
    pad = max(0, (w - vlen) // 2)
    return " " * pad + text

def hline(char="─", color=DGRAY):
    w = min(term_width(), 72)
    println(color + char * w + RESET)

# ── Raio em ASCII art ────────────────────────────────────────
BOLT = [
    "    ██  ",
    "   ██   ",
    "  ██████",
    "    ██  ",
    "   ██   ",
    "  ██    ",
]

# ── Logo VoltLink em ASCII grande ───────────────────────────
VOLT_ART = [
    r"██╗   ██╗ ██████╗ ██╗  ████████╗",
    r"██║   ██║██╔═══██╗██║  ╚══██╔══╝",
    r"██║   ██║██║   ██║██║     ██║   ",
    r"╚██╗ ██╔╝██║   ██║██║     ██║   ",
    r" ╚████╔╝ ╚██████╔╝███████╗██║   ",
    r"  ╚═══╝   ╚═════╝ ╚══════╝╚═╝   ",
]

LINK_ART = [
    r"██╗     ██╗███╗   ██╗██╗  ██╗",
    r"██║     ██║████╗  ██║██║ ██╔╝",
    r"██║     ██║██╔██╗ ██║█████╔╝ ",
    r"██║     ██║██║╚██╗██║██╔═██╗ ",
    r"███████╗██║██║ ╚████║██║  ██╗",
    r"╚══════╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝",
]

# ── Animação de boot ─────────────────────────────────────────
def boot_sequence():
    clear()
    println()

    prompt = f"{BLUE_ELEC}user@voltlink{RESET}{GRAY_COOL}:{RESET}{BLUE_LIGHT}~{RESET}{GRAY_COOL}${RESET} "

    # Comando digitado
    write(prompt)
    time.sleep(0.3)
    typewriter(f"{WHITE}./init --brand VoltLink --mode logo{RESET}", delay=0.04)
    time.sleep(0.3)

    steps = [
        ("Carregando módulo de identidade visual", 0.4),
        ("Inicializando paleta de cores          ", 0.3),
        ("Conectando ao sistema de energia       ", 0.5),
        ("Estabelecendo link de dados            ", 0.3),
        ("Renderizando assets gráficos           ", 0.6),
    ]

    for msg, wait in steps:
        write(f"  {DGRAY}[{RESET}")
        time.sleep(wait)
        write(f"{BLUE_ELEC}✓{RESET}")
        write(f"{DGRAY}]{RESET}")
        println(f"  {GRAY_COOL}{msg}{RESET}")
        time.sleep(0.08)

    time.sleep(0.2)
    hline("─", color=DGRAY)
    time.sleep(0.3)

# ── Logo principal ───────────────────────────────────────────
def render_logo():
    w = term_width()

    # VOLT = azul elétrico | BOLT = ciano neon | LINK = branco
    combined = []
    for i in range(6):
        volt = VOLT_ART[i]
        link = LINK_ART[i]
        bolt_line = BOLT[i] if i < len(BOLT) else "        "

        row = (
            f"{BOLD}{BLUE_ELEC}{volt}{RESET}"
            f"{BOLD}{CYAN_NEON}{bolt_line}{RESET}"
            f"{BOLD}{WHITE}{link}{RESET}"
        )
        # largura visível
        vis = len(volt) + len(bolt_line) + len(link)
        pad = max(0, (w - vis) // 2)
        combined.append((" " * pad, row))

    for pad, row in combined:
        write(pad)
        println(row, delay=0)
        time.sleep(0.07)

    time.sleep(0.2)

# ── Tagline e rodapé ─────────────────────────────────────────
def render_footer():
    tagline = "E N E R G I A   ·   C O N E X Ã O   ·   F U T U R O"
    println()
    println(center(f"{DIM}{BLUE_ICE}{tagline}{RESET}", len(tagline)))
    time.sleep(0.2)

    hline("─", color=DGRAY)

    info = f"{DGRAY}v1.0.0  |  {BLUE_ELEC}● online{RESET}  |  {DGRAY}2026 VoltLink Corp.{RESET}"
    vis  = len("v1.0.0  |  ● online  |  2026 VoltLink Corp.")
    println(center(info, vis))
    println()

# ── Cursor piscante ──────────────────────────────────────────
def blink_cursor(seconds=3):
    prompt = f"{BLUE_ELEC}user@voltlink{RESET}{GRAY_COOL}:{RESET}{BLUE_LIGHT}~{RESET}{GRAY_COOL}${RESET} "
    write(prompt)
    end = time.time() + seconds
    visible = True
    while time.time() < end:
        if visible:
            write(f"{BLUE_ELEC}▮{RESET}")
        else:
            write("\b \b")
        visible = not visible
        time.sleep(0.5)
    write("\b \b\n")

# ── Main ─────────────────────────────────────────────────────
def display_header():
    """Exibe apenas o logo e o rodapé, sem animação de boot."""
    render_logo()
    render_footer()

def run_animation(show_cursor=True):
    try:
        boot_sequence()
        render_logo()
        render_footer()
        if show_cursor:
            blink_cursor(4)
    except KeyboardInterrupt:
        println(f"\n{GRAY_COOL}Sessão encerrada.{RESET}")
        sys.exit(0)

if __name__ == "__main__":
    run_animation()