#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
UniCharX CLI Module - Command Line Interface

Provides a rich terminal interface for searching and exploring Unicode characters.
"""

import sys
import argparse
import json
from typing import Optional, List

# Try to import rich for enhanced output
try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.text import Text
    from rich import print as rprint
    HAS_RICH = True
except ImportError:
    HAS_RICH = False

from unicharx.core import UniCharX, CharInfo, UNICODE_CATEGORIES


def print_simple(results: List[CharInfo], verbose: bool = False) -> None:
    """Print results without rich formatting."""
    for info in results:
        if verbose:
            print(f"{info.char}  {info.hex_code}  {info.name}")
            print(f"    Category: {info.category} ({UNICODE_CATEGORIES.get(info.category, 'Unknown')})")
            print(f"    Block: {info.block}")
            print(f"    HTML: {info.html_entity}  Python: {info.python_escape}")
            print()
        else:
            print(f"{info.char}  {info.hex_code}  {info.name}")


def print_rich(results: List[CharInfo], verbose: bool = False, show_details: bool = False) -> None:
    """Print results with rich formatting."""
    console = Console()
    
    if not results:
        console.print("[yellow]No characters found matching your query.[/yellow]")
        return
    
    # Create table
    table = Table(title=f"Unicode Characters ({len(results)} found)", show_header=True, header_style="bold cyan")
    
    table.add_column("Char", style="bold green", width=4)
    table.add_column("Code", style="yellow", width=10)
    table.add_column("Name", style="white")
    
    if verbose:
        table.add_column("Category", style="magenta", width=12)
        table.add_column("Block", style="blue")
    
    for info in results:
        row = [info.char, info.hex_code, info.name]
        if verbose:
            cat_desc = UNICODE_CATEGORIES.get(info.category, info.category)
            row.extend([f"{info.category}", info.block])
        table.add_row(*row)
    
    console.print(table)
    
    if show_details and len(results) == 1:
        info = results[0]
        console.print()
        details = Panel(
            f"[bold]Character:[/bold] {info.char}\n"
            f"[bold]Code Point:[/bold] {info.hex_code} ({info.code})\n"
            f"[bold]Name:[/bold] {info.name}\n"
            f"[bold]Category:[/bold] {info.category} - {UNICODE_CATEGORIES.get(info.category, 'Unknown')}\n"
            f"[bold]Block:[/bold] {info.block}\n"
            f"[bold]HTML Entity:[/bold] {info.html_entity}\n"
            f"[bold]Python Escape:[/bold] {info.python_escape}",
            title="[bold cyan]Character Details[/bold cyan]",
            border_style="cyan",
        )
        console.print(details)


def print_json(results: List[CharInfo]) -> None:
    """Print results as JSON."""
    data = [info.to_dict() for info in results]
    print(json.dumps(data, indent=2, ensure_ascii=False))


def print_markdown(results: List[CharInfo]) -> None:
    """Print results as Markdown table."""
    print("| Char | Code | Name | Category | Block |")
    print("|:----:|:----:|:-----|:---------|:------|")
    for info in results:
        print(f"| {info.char} | {info.hex_code} | {info.name} | {info.category} | {info.block} |")


def copy_to_clipboard(text: str) -> bool:
    """Try to copy text to clipboard."""
    try:
        import subprocess
        
        # Try pbcopy (macOS)
        try:
            subprocess.run(["pbcopy"], input=text.encode(), check=True)
            return True
        except (subprocess.SubprocessError, FileNotFoundError):
            pass
        
        # Try xclip (Linux)
        try:
            subprocess.run(["xclip", "-selection", "clipboard"], input=text.encode(), check=True)
            return True
        except (subprocess.SubprocessError, FileNotFoundError):
            pass
        
        # Try xsel (Linux)
        try:
            subprocess.run(["xsel", "--clipboard", "--input"], input=text.encode(), check=True)
            return True
        except (subprocess.SubprocessError, FileNotFoundError):
            pass
        
        # Try clip (Windows)
        try:
            subprocess.run(["clip"], input=text.encode(), check=True)
            return True
        except (subprocess.SubprocessError, FileNotFoundError):
            pass
        
        return False
    except Exception:
        return False


def interactive_mode(engine: UniCharX) -> None:
    """Run interactive search mode."""
    if HAS_RICH:
        console = Console()
        console.print(Panel.fit(
            "[bold cyan]UniCharX[/bold cyan] - Unicode Character Search\n"
            "Type a search query and press Enter. Type 'quit' or 'exit' to quit.\n"
            "Commands: :cat [category] | :block [name] | :random | :help",
            title="🔍 Interactive Mode",
            border_style="cyan",
        ))
    else:
        print("UniCharX - Unicode Character Search")
        print("Type a search query and press Enter. Type 'quit' or 'exit' to quit.")
    
    while True:
        try:
            if HAS_RICH:
                query = console.input("\n[bold green]search>[/bold green] ").strip()
            else:
                query = input("\nsearch> ").strip()
            
            if not query:
                continue
            
            if query.lower() in ("quit", "exit", "q"):
                break
            
            # Handle commands
            if query.startswith(":"):
                parts = query[1:].split(maxsplit=1)
                cmd = parts[0].lower()
                arg = parts[1] if len(parts) > 1 else None
                
                if cmd == "help":
                    if HAS_RICH:
                        console.print("""
[bold]Commands:[/bold]
  :cat [category]  - List characters by category (e.g., :cat Sm)
  :block [name]    - List characters by block (e.g., :block emoji)
  :random          - Show random characters
  :categories      - List all categories
  :blocks          - List all blocks
  :help            - Show this help
  quit/exit        - Exit interactive mode
""")
                    else:
                        print("Commands: :cat, :block, :random, :categories, :blocks, :help, quit")
                    continue
                
                if cmd == "categories":
                    if HAS_RICH:
                        table = Table(title="Unicode Categories")
                        table.add_column("Code", style="yellow")
                        table.add_column("Description", style="white")
                        for code, desc in UNICODE_CATEGORIES.items():
                            table.add_row(code, desc)
                        console.print(table)
                    else:
                        for code, desc in UNICODE_CATEGORIES.items():
                            print(f"  {code}: {desc}")
                    continue
                
                if cmd == "blocks":
                    if HAS_RICH:
                        table = Table(title="Unicode Blocks")
                        table.add_column("Range", style="yellow")
                        table.add_column("Name", style="white")
                        for start, end, name in engine.list_blocks()[:20]:
                            table.add_row(f"U+{start:04X}-U+{end:04X}", name)
                        console.print(table)
                        console.print("[dim]... and more blocks[/dim]")
                    else:
                        for start, end, name in engine.list_blocks()[:20]:
                            print(f"  U+{start:04X}-U+{end:04X}: {name}")
                    continue
                
                if cmd == "cat" and arg:
                    results = engine.search_by_category(arg.upper(), limit=50)
                    if HAS_RICH:
                        print_rich(results, verbose=True)
                    else:
                        print_simple(results, verbose=True)
                    continue
                
                if cmd == "block" and arg:
                    results = engine.search_by_block(arg, limit=50)
                    if HAS_RICH:
                        print_rich(results, verbose=True)
                    else:
                        print_simple(results, verbose=True)
                    continue
                
                if cmd == "random":
                    results = engine.get_random(count=10)
                    if HAS_RICH:
                        print_rich(results, verbose=True)
                    else:
                        print_simple(results, verbose=True)
                    continue
                
                if HAS_RICH:
                    console.print(f"[red]Unknown command: {cmd}[/red]")
                else:
                    print(f"Unknown command: {cmd}")
                continue
            
            # Regular search
            results = engine.search(query, fuzzy=True, limit=20)
            
            if HAS_RICH:
                print_rich(results, verbose=True)
            else:
                print_simple(results, verbose=True)
            
            # Offer to copy first result
            if results and len(results) == 1:
                char = results[0].char
                if copy_to_clipboard(char):
                    if HAS_RICH:
                        console.print(f"[green]Copied '{char}' to clipboard![/green]")
                    else:
                        print(f"Copied '{char}' to clipboard!")
        
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except EOFError:
            break


def main(argv: Optional[List[str]] = None) -> int:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        prog="unicharx",
        description="🚀 UniCharX - Lightweight Unicode Character Intelligent Search CLI Engine",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  unicharx heart          Search for characters with "heart" in the name
  unicharx -f arrow       Fuzzy search for "arrow"
  unicharx -c Sm plus     Search in math symbols category
  unicharx -i             Interactive mode
  unicharx --info U+2764  Get info about a specific character
  unicharx --random       Show random characters
  unicharx --categories   List all Unicode categories
  unicharx --blocks       List all Unicode blocks
""",
    )
    
    parser.add_argument(
        "query",
        nargs="?",
        help="Search query (character name or keyword)",
    )
    
    parser.add_argument(
        "-f", "--fuzzy",
        action="store_true",
        help="Enable fuzzy matching",
    )
    
    parser.add_argument(
        "-t", "--threshold",
        type=float,
        default=0.6,
        help="Fuzzy match threshold (0.0-1.0, default: 0.6)",
    )
    
    parser.add_argument(
        "-c", "--category",
        help="Filter by Unicode category (e.g., Sm, So, Nd)",
    )
    
    parser.add_argument(
        "-b", "--block",
        help="Filter by Unicode block name",
    )
    
    parser.add_argument(
        "-l", "--limit",
        type=int,
        default=50,
        help="Maximum number of results (default: 50)",
    )
    
    parser.add_argument(
        "-i", "--interactive",
        action="store_true",
        help="Start interactive search mode",
    )
    
    parser.add_argument(
        "--info",
        metavar="CODE",
        help="Get detailed info about a character (hex code like U+2764 or decimal)",
    )
    
    parser.add_argument(
        "--random",
        action="store_true",
        help="Show random Unicode characters",
    )
    
    parser.add_argument(
        "--categories",
        action="store_true",
        help="List all Unicode categories",
    )
    
    parser.add_argument(
        "--blocks",
        action="store_true",
        help="List all Unicode blocks",
    )
    
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Show detailed output",
    )
    
    parser.add_argument(
        "--json",
        action="store_true",
        help="Output results as JSON",
    )
    
    parser.add_argument(
        "--markdown",
        action="store_true",
        help="Output results as Markdown table",
    )
    
    parser.add_argument(
        "--copy",
        action="store_true",
        help="Copy first result to clipboard",
    )
    
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable colored output",
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 1.0.0",
    )
    
    args = parser.parse_args(argv)
    
    # Initialize engine
    engine = UniCharX()
    
    # Handle info mode
    if args.info:
        code_str = args.info.upper().replace("U+", "").replace(" ", "")
        try:
            code = int(code_str, 16)
        except ValueError:
            try:
                code = int(code_str)
            except ValueError:
                print(f"Error: Invalid code point: {args.info}", file=sys.stderr)
                return 1
        
        info = engine.get_char_info(code)
        if info:
            if args.json:
                print_json([info])
            elif HAS_RICH and not args.no_color:
                print_rich([info], verbose=True, show_details=True)
            else:
                print_simple([info], verbose=True)
        else:
            print(f"Error: Character not found: {args.info}", file=sys.stderr)
            return 1
        return 0
    
    # Handle categories list
    if args.categories:
        if args.json:
            print(json.dumps(UNICODE_CATEGORIES, indent=2))
        elif HAS_RICH and not args.no_color:
            console = Console()
            table = Table(title="Unicode Categories")
            table.add_column("Code", style="yellow")
            table.add_column("Description", style="white")
            for code, desc in sorted(UNICODE_CATEGORIES.items()):
                table.add_row(code, desc)
            console.print(table)
        else:
            print("Unicode Categories:")
            for code, desc in sorted(UNICODE_CATEGORIES.items()):
                print(f"  {code}: {desc}")
        return 0
    
    # Handle blocks list
    if args.blocks:
        if args.json:
            blocks = [{"start": s, "end": e, "name": n} for s, e, n in engine.list_blocks()]
            print(json.dumps(blocks, indent=2))
        elif HAS_RICH and not args.no_color:
            console = Console()
            table = Table(title="Unicode Blocks")
            table.add_column("Range", style="yellow")
            table.add_column("Name", style="white")
            for start, end, name in engine.list_blocks():
                table.add_row(f"U+{start:04X}-U+{end:04X}", name)
            console.print(table)
        else:
            print("Unicode Blocks:")
            for start, end, name in engine.list_blocks():
                print(f"  U+{start:04X}-U+{end:04X}: {name}")
        return 0
    
    # Handle random mode
    if args.random:
        results = engine.get_random(category=args.category, count=args.limit)
        if args.json:
            print_json(results)
        elif args.markdown:
            print_markdown(results)
        elif HAS_RICH and not args.no_color:
            print_rich(results, verbose=args.verbose)
        else:
            print_simple(results, verbose=args.verbose)
        return 0
    
    # Handle interactive mode
    if args.interactive:
        interactive_mode(engine)
        return 0
    
    # Handle search query
    if args.query:
        results = engine.search(
            args.query,
            fuzzy=args.fuzzy,
            threshold=args.threshold,
            category=args.category,
            block=args.block,
            limit=args.limit,
        )
        
        if args.json:
            print_json(results)
        elif args.markdown:
            print_markdown(results)
        elif HAS_RICH and not args.no_color:
            print_rich(results, verbose=args.verbose)
        else:
            print_simple(results, verbose=args.verbose)
        
        # Copy first result if requested
        if args.copy and results:
            char = results[0].char
            if copy_to_clipboard(char):
                if HAS_RICH and not args.no_color:
                    Console().print(f"[green]Copied '{char}' to clipboard![/green]")
                else:
                    print(f"Copied '{char}' to clipboard!")
        
        return 0
    
    # No query provided - show help
    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
