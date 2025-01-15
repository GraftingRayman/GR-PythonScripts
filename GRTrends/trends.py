from pytrends.request import TrendReq
from datetime import datetime
import os
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt
import re

# File paths
file_path = r"C:\\utils\\top_trends.txt"
word_count_file = r"C:\\utils\\trend_word_counts.txt"

def get_top_trends(region):
    """Fetch the top 20 trends from Google Trends for a specific region."""
    try:
        pytrends = TrendReq()
        trending_searches = pytrends.trending_searches(pn=region)
        return trending_searches.head(20).values.flatten().tolist()
    except Exception as e:
        print(f"An error occurred while fetching trends for {region}: {e}")
        return []

def save_trends_to_file(trends, region, file_path):
    """Save or append trends to the specified file."""
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    header = f"\n=== Trends in {region.upper()} on {timestamp} ===\n"

    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            existing_content = file.read()
    else:
        existing_content = ""

    new_content = header + '\n'.join(trends) + '\n' + existing_content

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(new_content)

def parse_trends(file_path):
    """Parse the trends file and extract timestamp, region, and trends."""
    trends_data = []
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    blocks = re.split(r"=== Trends in (.*?) on (.*?) ===", content)
    for i in range(1, len(blocks), 3):
        region = blocks[i].strip()
        timestamp = blocks[i + 1].strip()
        trends = blocks[i + 2].strip().split('\n')
        for trend in trends:
            trends_data.append({'region': region, 'timestamp': timestamp, 'trend': trend})

    return pd.DataFrame(trends_data)

def save_word_counts(df, word_count_file):
    """Count the occurrences of each trend and save to a file with region information."""
    trend_counts = df.groupby(['trend', 'region']).size().reset_index(name='count')
    sorted_trends = trend_counts.sort_values(by='count', ascending=False)

    with open(word_count_file, 'w', encoding='utf-8') as file:
        for _, row in sorted_trends.iterrows():
            file.write(f"{row['trend']}\t{row['count']}\t{row['region'].upper()}\n")

def main_menu():
    while True:
        print("\nMenu:")
        print("1. Check trends for the US")
        print("2. Check trends for the UK")
        print("3. Check trends for another location")
        print("4. Open top_trends.txt")
        print("5. Open trend_word_counts.txt")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            region = 'united_states'
            trends = get_top_trends(region)
            if trends:
                save_trends_to_file(trends, region, file_path)
                print(f"Top 20 trends for {region.upper()} saved to {file_path}")
            else:
                print(f"No trends available for {region.upper()}.")

        elif choice == '2':
            region = 'united_kingdom'
            trends = get_top_trends(region)
            if trends:
                save_trends_to_file(trends, region, file_path)
                print(f"Top 20 trends for {region.upper()} saved to {file_path}")
            else:
                print(f"No trends available for {region.upper()}.")

        elif choice == '3':
            region = input("Enter the region (e.g., 'united_states', 'india'): ").strip()
            trends = get_top_trends(region)
            if trends:
                save_trends_to_file(trends, region, file_path)
                print(f"Top 20 trends for {region.upper()} saved to {file_path}")
            else:
                print(f"No trends available for {region.upper()}.")

        elif choice == '4':
            os.system(f"notepad {file_path}")

        elif choice == '5':
            os.system(f"notepad {word_count_file}")

        elif choice == '6':
            print("Exiting the program.")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()
