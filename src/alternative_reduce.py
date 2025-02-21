#!/usr/bin/env python3

import argparse
import os
import json
import matplotlib.pyplot as plt
from collections import defaultdict
import re

# Argument parsing
parser = argparse.ArgumentParser(description="Aggregate hashtag usage over time and plot trends.")
parser.add_argument('--hashtags', nargs='+', required=True, help="List of hashtags to track.")
parser.add_argument('--output_path', default="hashtag_trends.png", help="Path to save the plot.")
args = parser.parse_args()

# Fix output directory path (since this script runs from src/)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Move up one level from src/
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")

# Initialize data structure to store counts
hashtag_counts = {hashtag: defaultdict(int) for hashtag in args.hashtags}

# Ensure output directory exists
if not os.path.exists(OUTPUT_DIR):
    print(f"Error: Output directory '{OUTPUT_DIR}' does not exist.")
    exit(1)

# Scan all .lang and .country files in the outputs directory
for filename in sorted(os.listdir(OUTPUT_DIR)):  # Sorting ensures chronological order
    match = re.search(r"geoTwitter20-(\d{2})-(\d{2})\.zip\.(lang|country)", filename)
    if match:
        month, day, _ = match.groups()
        day_of_year = (int(month) - 1) * 30 + int(day)  # Approximate day of year

        filepath = os.path.join(OUTPUT_DIR, filename)
        with open(filepath, 'r') as f:
            data = json.load(f)

            for hashtag in args.hashtags:
                if hashtag in data:
                    hashtag_counts[hashtag][day_of_year] += sum(data[hashtag].values())

# Plot data
plt.figure(figsize=(12, 6))
for hashtag, daily_counts in hashtag_counts.items():
    days = sorted(daily_counts.keys())
    counts = [daily_counts[day] for day in days]
    plt.plot(days, counts, marker='o', label=hashtag)

# Graph styling
plt.xlabel("Day of the Year")
plt.ylabel("Tweet Count")
plt.title("Hashtag Usage Over Time")
plt.legend()
plt.grid(True)

# Save plot
output_path = os.path.join(BASE_DIR, args.output_path)
plt.savefig(output_path, bbox_inches='tight')
plt.show()

