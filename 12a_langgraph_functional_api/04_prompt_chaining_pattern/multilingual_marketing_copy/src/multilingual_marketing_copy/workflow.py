import os
from typing import TypedDict, List, Dict
from dotenv import load_dotenv, find_dotenv
from langgraph.func import entrypoint, task
from langchain_google_genai import ChatGoogleGenerativeAI

_: bool = load_dotenv(find_dotenv())

model = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp")


class InputState(TypedDict):
    topic: str
    primary_language: str
    target_languages: List[str]


@task
def generate_marketing_copy(topic: str, primary_language: str) -> str:
    """Generate marketing copy in the primary language."""
    prompt = f"""Write compelling marketing copy about {topic} in {primary_language}.
    The copy should be engaging, professional, and approximately 3-4 sentences long.
    Focus on benefits and unique value propositions."""

    response = model.invoke(prompt)
    return str(response.content)


@task
def translate_to_languages(original_copy: str, primary_language: str, target_languages: List[str]) -> Dict[str, str]:
    """Translate the marketing copy to all target languages."""
    translations = {primary_language: original_copy}

    for lang in target_languages:
        if lang != primary_language:
            prompt = f"""Translate the following marketing copy from {primary_language} to {lang}.
            Maintain the tone and marketing impact while ensuring it sounds natural in {lang}.

            Original copy to translate:
            {original_copy}"""

            response = model.invoke(prompt)
            translations[lang] = str(response.content)

    return translations


@task
def create_markdown_output(translations: Dict[str, str], topic: str) -> str:
    """Create a markdown formatted output with all translations."""
    markdown_content = f"""# Marketing Copy: {topic}

Generated marketing copy in multiple languages:

"""
    for language, copy in translations.items():
        markdown_content += f"""## {language}

{copy}

---

"""
    return markdown_content


@task
def save_translations(markdown_content: str, translations: Dict[str, str]) -> dict:
    """Save both markdown and individual language files."""
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    # Save markdown version
    markdown_path = os.path.join(output_dir, "marketing_copy.md")
    with open(markdown_path, "w", encoding="utf-8") as f:
        f.write(markdown_content)

    # Save individual language files
    language_files = {}
    for language, copy in translations.items():
        file_path = os.path.join(output_dir, f"marketing_copy_{language}.txt")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(copy)
        language_files[language] = file_path

    return {
        "markdown_file": markdown_path,
        "language_files": language_files
    }


@entrypoint()
def run_workflow(input: InputState):
    """Workflow to generate marketing copy and translate it to multiple languages."""
    # Get input values with defaults
    topic = input.get("topic", "Our Amazing Product")
    primary_language = input.get("primary_language", "English")
    target_languages = input.get(
        "target_languages", ["Spanish", "French", "German"])

    # Generate marketing copy in primary language
    original_copy = generate_marketing_copy(topic, primary_language).result()

    # Translate to all target languages
    translations = translate_to_languages(
        original_copy,
        primary_language,
        target_languages
    ).result()

    # Create markdown content
    markdown_content = create_markdown_output(translations, topic).result()

    # Save all versions
    save_result = save_translations(markdown_content, translations).result()

    return {
        "translations": translations,
        "markdown_content": markdown_content,
        "file_paths": save_result
    }
