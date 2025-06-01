import os
import json
import requests
import textstat
import hashlib
from dotenv import load_dotenv


load_dotenv()

OR_API_KEY = os.getenv("OPENROUTER_API_KEY")

headers = {
    "Authorization": f"Bearer {OR_API_KEY}",
    "HTTP-Referer": "https://yourdomain.com",  
    "Content-Type": "application/json"
}

MODEL = "openai/gpt-3.5-turbo"  

def url_to_filename(url):
    return hashlib.md5(url.encode()).hexdigest() + ".json"

def analyze_with_openrouter(prompt):
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are an expert technical writer."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3
    }
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=60
        )
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Error during OpenRouter API call: {str(e)}"


def analyze_article(raw_text, url):
    scores = {
        "flesch_reading_ease": textstat.flesch_reading_ease(raw_text),
        "flesch_kincaid_grade": textstat.flesch_kincaid_grade(raw_text),
        "gunning_fog_index": textstat.gunning_fog(raw_text),
        "smog_index": textstat.smog_index(raw_text),
        "automated_readability_index": textstat.automated_readability_index(raw_text)
    }

    flesch = scores["flesch_reading_ease"]
    fk_grade = scores["flesch_kincaid_grade"]
    gunning = scores["gunning_fog_index"]

    summary = ""
    if flesch >= 60:
        summary += "The text is fairly easy to read. "
    elif 30 <= flesch < 60:
        summary += "The text is somewhat difficult to read. "
    else:
        summary += "The text is quite complex. "

    if fk_grade <= 8:
        summary += f"It suits a broad audience (grade level {fk_grade:.1f}). "
    elif 8 < fk_grade <= 12:
        summary += f"Requires moderate reading skill (grade {fk_grade:.1f}). "
    else:
        summary += f"Demands advanced reading skill (grade {fk_grade:.1f}). "

    summary += f"Gunning Fog index is {gunning:.1f}, indicating "
    if gunning <= 8:
        summary += "simple text."
    elif 8 < gunning <= 12:
        summary += "moderately complex text."
    else:
        summary += "highly complex language."

    structure_summary = analyze_with_openrouter(f"Summarize the structure and flow of the following documentation in 2-3 lines:\n\n{raw_text}")
    structure_suggestions = analyze_with_openrouter(f"""Analyze the structure and flow of this documentation. 
Consider headings, paragraphing, logical flow, and ease of navigation. Suggest 3–5 improvements.\n\n{raw_text}""")

    completeness_summary = analyze_with_openrouter(f"Summarize how complete this documentation is in 2-3 lines. Mention if it's sufficient, lacking examples, or missing important parts:\n\n{raw_text}")
    completeness_suggestions = analyze_with_openrouter(f"""Does the article provide complete info? Are explanations sufficient with examples? Suggest what can be added.\n\n{raw_text}""")

    style_summary = analyze_with_openrouter(f"Evaluate the writing style (tone, clarity, action-orientation, conciseness) in 2–3 lines based on Microsoft Style Guide:\n\n{raw_text}")
    style_suggestions = analyze_with_openrouter(f"""Evaluate the writing style using Microsoft Style Guide rules. 
Is it clear, concise, customer-friendly, and action-oriented? Suggest improvements.\n\n{raw_text}""")

    report = {
        "url": url,
        "readability": {
            "summary": summary.strip(),
            "scores": scores,
            "suggestions": analyze_with_openrouter(f"Explain the readability of the following documentation for a marketer and suggest ways to improve it:\n\n{raw_text}")
        },
        "structure_and_flow": {
            "summary": structure_summary,
            "suggestions": structure_suggestions
        },
        "completeness": {
            "summary": completeness_summary,
            "suggestions": completeness_suggestions
        },
        "style_guidelines": {
            "summary": style_summary,
            "suggestions": style_suggestions
        }
    }

    return report


def save_output(url, analysis):
    import hashlib
    filename = hashlib.md5(url.encode()).hexdigest() + ".json"
    output_dir = "outputs"
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(analysis, f, indent=4)

    print(f"\n Analysis saved to {filepath}")
