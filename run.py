import os
import sys
import uuid
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from src.graph import app
from src.exceptions import KasparroError, SchemaValidationError

console = Console()

def main():
    load_dotenv()
    
    # Generate a unique Trace ID for this run
    run_id = str(uuid.uuid4())[:8]
    
    # Safety Check: Ensure API Key exists
    if not os.getenv("GOOGLE_API_KEY") and not os.getenv("OPENAI_API_KEY"):
        console.print("[bold red]CRITICAL ERROR:[/bold red] API Key not found in .env file.")
        sys.exit(1)

    # Ensure Reports Directory Exists
    if not os.path.exists("reports"):
        os.makedirs("reports")

    # Define the Mission
    query = "Analyze why ROAS dropped last week"
    initial_state = {
        "query": query,
        "retry_count": 0
    }

    # Display Start Banner
    console.print(Panel.fit(
        f"[bold cyan] Kasparro Agentic Analyst v2.0[/bold cyan]\n"
        f"[white]Query:[/white] {query}\n"
        f"[dim]Run ID:[/dim] [bold magenta]{run_id}[/bold magenta]\n"
        f"[dim]Engine: LangGraph + Gemini[/dim]",
        border_style="cyan"
    ))

    # Execute the Graph with v2 Error Handling
    try:
        final_state = app.invoke(initial_state)
        
        console.print(f"\n[bold green] Analysis Workflow Complete! (Run ID: {run_id})[/bold green]")
        
        if final_state.get("hypothesis"):
            hypo = final_state["hypothesis"].get("hypothesis", "No hypothesis found")
            console.print(f"\n[bold yellow]🔍 Final Diagnosis:[/bold yellow] {hypo}")
        
        console.print(f" Full Report saved to: [underline]reports/final_report.json[/underline]")

    except SchemaValidationError as e:
        console.print(f"\n[bold red] DATA BLOCKED:[/bold red] Input data failed schema validation.")
        console.print(f"Details: {str(e)}")
        sys.exit(1)
        
    except KasparroError as e:
        console.print(f"\n[bold orange] SYSTEM ERROR:[/bold orange] {str(e)}")
        sys.exit(1)

    except Exception as e:
        console.print(f"\n[bold red] UNEXPECTED CRASH:[/bold red] {str(e)}")

if __name__ == "__main__":
    main()