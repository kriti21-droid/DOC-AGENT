import os
import json
from utils.fetcher import fetch_article_text
from utils.readability import url_to_filename
from doc_revision_agent import nrevision_agent

def load_json(url):
    filename = url_to_filename(url) 
    filepath = os.path.join("outputs", filename)
    if not os.path.exists(filepath):
        return None
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def main():
    url = input("Enter the documentation URL: ").strip()

    original_text, error = fetch_article_text(url)
    if error:
        print(f"Failed to fetch article: {error}")
        return
    print("Article fetched.")

    filename = url_to_filename(url)
    json_path = os.path.join("outputs", filename)
    if not os.path.exists(json_path):
        print("Could not find suggestions JSON in outputs/. Run the first agent first.")
        return

    suggestions = load_json(url)
    if not suggestions:
        print("Failed to load suggestions JSON.")
        return
    print("Suggestions loaded.")

    revised = nrevision_agent(original_text, suggestions)

    os.makedirs("outputs", exist_ok=True)
    revised_filename = filename.replace(".json", "_revised.txt")
    revised_path = os.path.join("outputs", revised_filename)
    with open(revised_path, "w", encoding="utf-8") as f:
        f.write(revised)

    print(f"Revised content saved to '{revised_path}'.")

if __name__ == "__main__":
    main()

