#!/usr/bin/env python3

# command line args
import argparse
import os 
import json 
import matplotlib.pyplot as plt 
from collections import defaultdict

parser = argparse.ArgumentParser()
parser.add_argument('--input_path',required=True)
parser.add_argument('--key',required=True)
parser.add_argument('--percent',action='store_true')
args = parser.parse_args()

# open the input path
with open(args.input_path) as f:
    counts = json.load(f)

# normalize the counts by the total values
if args.percent:
    for k in counts[args.key]:
        counts[args.key][k] /= counts['_all'][k]

# print the counts
sorted_items = sorted(counts[args.key].items(), key=lambda item: item[1], reverse=True)[:10]  # Top 10

labels, values = zip(*sorted_items) if sorted_items else ([], [])

plt.figure(figsize=(10, 5))
plt.barh(labels, values, color='skyblue')
plt.xlabel("Frequency")
plt.ylabel("Language / Country Code")
plt.title(f"Top 10 {args.key} Mentions in {os.path.basename(args.input_path)}")
plt.gca().invert_yaxis()

output_filename = f"{args.key}_{os.path.basename(args.input_path).replace('.txt', '')}.png"
plt.savefig(output_filename, bbox_inches='tight')

print(f"Graph saved as {output_filename}")

