#!/usr/bin/env python3

import argparse
import os
import json
import matplotlib.pyplot as plt
from matplotlib import rc
from collections import defaultdict

rc('font', family='UnBatang')

parser = argparse.ArgumentParser()
parser.add_argument('--input_path', required=True)
parser.add_argument('--key', required=True)
parser.add_argument('--percent', action='store_true')
args = parser.parse_args()

# Load JSON file
with open(args.input_path) as f:
    counts = json.load(f)

# Ensure the key exists in the data
if args.key not in counts:
    raise ValueError(f"Key '{args.key}' not found in the JSON data.")

# Normalize counts if --percent is enabled
if args.percent:
    for k in counts[args.key]:
        if k in counts['_all'] and counts['_all'][k] > 0:
            counts[args.key][k] /= counts['_all'][k]
        else:
            counts[args.key][k] = 0  # Prevent division errors

# Get top 10 
sorted_items = sorted(counts[args.key].items(), key=lambda item: item[1], reverse=True)[:10]

# sort the bars
sorted_items = sorted(sorted_items, key=lambda item: item[1])

# Ensure at least 10 items are selected, if available
num_to_select = min(10, len(sorted_items))
if num_to_select < 10:
    print(f"Warning: Only {num_to_select} entries available instead of 10.")

sorted_items = sorted_items[:num_to_select]

# Extract labels and values
labels, values = zip(*sorted_items) if sorted_items else ([], [])

plt.figure(figsize=(12, 6))
plt.bar(labels, values, color='skyblue')
plt.ylabel("Count")
plt.xlabel("Language / Country Code")
plt.xticks(rotation=45, ha="right")
plt.title(f"Top 10 '{args.key}' Mentions")

# Generate output filename
output_filename = f"{args.key}_{os.path.basename(args.input_path).replace('.txt', '')}.png"
plt.savefig(output_filename, bbox_inches='tight')

print(f"Graph saved as {output_filename}")

