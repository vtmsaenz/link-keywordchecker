import pandas as pd
import requests
from bs4 import BeautifulSoup

# Define keywords to search for
keywords = {"DEI", "Diversity", "Diverse", "Equity", "Inclusion", "Inclusive", "Affirmative Action"}

# Load URLs from Excel
file_path = "/Users/valesaenz/check_urls/2025 Social Media Calendar.xlsx"  # Update with your file path
df = pd.read_excel(file_path)
urls = df.iloc[:, 0].dropna().tolist()  # Assumes URLs are in the first column

matching_urls = []

# Check each URL
for url in urls:
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            text = soup.get_text().lower()
            if any(keyword.lower() in text for keyword in keywords):
                matching_urls.append(url)
    except requests.RequestException:
        print(f"Failed to fetch {url}")

# Print results
print("Matching URLs:")
for url in matching_urls:
    print(url)
