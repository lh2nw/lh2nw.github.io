import ollama
import requests
from bs4 import BeautifulSoup


def get_website_text(url):
    # 1. Download the website content
    response = requests.get(url)

    # 2. Parse the HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # 3. Remove script and style elements (we don't want to summarize code)
    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()

    # 4. Get the text and clean up extra whitespace
    text = soup.get_text()
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    clean_text = '\n'.join(chunk for chunk in chunks if chunk)

    return clean_text


def summarize_website(url):
    print(f"Fetching content from {url}...")
    raw_text = get_website_text(url)

    # Optional: Limit the text length so Llama doesn't get overwhelmed
    # Llama 3.2 can handle a lot, but very long pages might need clipping
    truncated_text = raw_text[:4000]

    print("Summarizing with Llama 3.2...")
    response = ollama.chat(
        model='llama3.2',
        messages=[
            {
                'role': 'user',
                'content': f'Summarize the following website content in 3-5 bullet points:\n\n{truncated_text}',
            },
        ]
    )
    return response['message']['content']


# --- WHERE YOU PLUG THE WEBSITE IN ---
target_url = "https://www.bostonscientific.com"
summary = summarize_website(target_url)

print("\n--- SUMMARY ---")
print(summary)