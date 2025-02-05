from rich import print
from rich.markdown import Markdown

from multilingual_marketing_copy.workflow import run_workflow

# Example input for generating marketing copy
input_data = {
    "topic": "AI-Powered Language Learning Platform",
    "primary_language": "English",
    "target_languages": [
        "Spanish",
        "French",
        "Mandarin Chinese",
        "Japanese"
    ]
}
    
def main_run():
    # Run the workflow
    result = run_workflow.invoke(input_data)

    # Print the results using rich formatting
    print("\n[bold green]✨ Marketing Copy Generation Complete![/bold green]\n")

    # Print original and translations
    print("[bold blue]Generated Translations:[/bold blue]")
    for lang, copy in result["translations"].items():
        print(f"\n[bold]{lang}:[/bold]")
        print(copy)

    # Display the markdown content
    print("\n[bold blue]Generated Markdown Preview:[/bold blue]")
    md = Markdown(result["markdown_content"])
    print(md)

    # Print file locations
    print("\n[bold blue]Generated Files:[/bold blue]")
    print(f"📄 Markdown File: {result['file_paths']['markdown_file']}")
    print("\nIndividual Language Files:")
    for lang, path in result['file_paths']['language_files'].items():
        print(f"📄 {lang}: {path}")
        
def stream_run():
    for part in run_workflow.stream(input_data, stream_mode="updates"):
        print("\n\n")
        print(part)
    