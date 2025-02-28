import pandas as pd
import requests

# Define the path to your Excel file
file_path = '/Users/valesaenz/check_urls/2025 Social Media Calendar.xlsx'

# Read the Excel file into a DataFrame
df = pd.read_excel(file_path)

# Extract the URLs into a list
urls = df['URLs'].tolist()  # Replace 'URLs' with the actual column name in your Excel sheet

# Define the keywords to search for
keywords = ["DEI", "Diversity", "Diverse", "Equity", "Inclusion", "Inclusive", "Affirmative Action"]

# Initialize lists to store results and errors
results = []
error_urls = []

# Iterate over each URL
for url in urls:
    try:
        # Send a GET request to the URL
        response = requests.get(url, timeout=10)  # Added timeout for better error handling
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)

        content = response.text

        # Check for the presence of each keyword in the content
        found_keywords = [keyword for keyword in keywords if keyword.lower() in content.lower()]

        # If any keywords are found, add the URL and keywords to the results
        if found_keywords:
            results.append({'URL': url, 'Keywords Found': ', '.join(found_keywords)})

    except requests.RequestException as e:
        print(f"Error accessing {url}: {e}")
        error_urls.append({'URL': url, 'Error': str(e)})

# Create DataFrames from the results and error URLs
results_df = pd.DataFrame(results)
error_urls_df = pd.DataFrame(error_urls)

# Display the results
print("URLs containing specified keywords:")
print(results_df)

print("\nURLs that could not be reached:")
print(error_urls_df)

# Save the results to Excel files
results_df.to_excel('/Users/valesaenz/Documents/filtered_urls.xlsx', index=False)
error_urls_df.to_excel('/Users/valesaenz/Documents/error_urls.xlsx', index=False)
