import requests
from bs4 import BeautifulSoup
from datetime import datetime

KEYWORDS = ["elish", "broken leg", "surrendered", "recovering"]
URL = "https://www.calgaryhumane.ca/adopt/cats/"

def check_for_keywords():
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, "html.parser")
    matches = []

    for cat in soup.select('.animal-listing'):
        text = cat.get_text(separator=" ", strip=True).lower()
        for keyword in KEYWORDS:
            if keyword.lower() in text:
                matches.append({
                    "name": cat.select_one('.animal-listing-name').text.strip(),
                    "match": keyword,
                    "time": datetime.now().isoformat()
                })
                break  # Stop checking more keywords for this cat

    return matches

def save_results(matches):
    with open("cat_matches_log.txt", "a") as f:
        for match in matches:
            f.write(f"{match['time']} - Name: {match['name']} - Matched: {match['match']}\n")

if __name__ == "__main__":
    results = check_for_keywords()
    if results:
        save_results(results)
        print(f"Found {len(results)} match(es).")
    else:
        print("No matches found.")
