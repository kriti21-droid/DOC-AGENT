from utils.readability import analyze_with_openrouter

def revise_with_openrouter(original_text, suggestions, section_name):
    instruction = f"""
You are a documentation editor AI. Improve the following documentation section with a focus on {section_name}.
Here are suggestions:
{suggestions}

Please revise the following content accordingly:
{original_text}

Only return the revised content.
    """.strip()

    return analyze_with_openrouter(instruction)

def nrevision_agent(original_text, suggestions_dict):
    suggestion_texts = []

    for section in ["readability", "style_guidelines"]:
        suggestion_block = suggestions_dict.get(section, {}).get("suggestions", "")
        if suggestion_block:
            suggestion_texts.append(f"{section.title()} Suggestions:\n{suggestion_block}")

    combined = "\n\n".join(suggestion_texts).strip()
    
    revised = revise_with_openrouter(original_text, combined, "readability and style improvements")
    return revised
