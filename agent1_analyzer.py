from utils.fetcher import fetch_article_text
from utils.readability import analyze_article, save_output

def main():
    url = input("Enter MoEngage documentation URL: ").strip()
    
    text, error = fetch_article_text(url)
    if error:
        print(f"Error fetching article: {error}")
        return

    print("Article fetched successfully. Analyzing...")

    report = analyze_article(text, url)
    save_output(url, report)

if __name__ == "__main__":
    main()
