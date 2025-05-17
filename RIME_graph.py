"""
RIME Output Visualizer
This script loads CSV outputs from the RIME engine and creates a graph visualization
of inputs, frames, contradictions, and meta-abstractions.
"""

import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# File paths
SUMMARY_CSV = "OUTPUT_rime_summary.csv"
EVENTS_CSV = "OUTPUT_rime_events.csv"

# Load data
summary_df = pd.read_csv(SUMMARY_CSV)
events_df = pd.read_csv(EVENTS_CSV)

# Initialize graph
G = nx.DiGraph()

# Add frame nodes
frames = summary_df["frame"].unique()
for frame in frames:
    G.add_node(frame, type="frame")

# Add axiom and contradiction nodes and edges
for _, row in summary_df.iterrows():
    node = f"{row['type'].upper()}_{row['value']}"
    G.add_node(node, type=row["type"])
    G.add_edge(node, row["frame"], weight=1.0 if row["type"] == "axiom" else 0.5)

# Color map
color_map = []
for node in G.nodes:
    ntype = G.nodes[node].get("type", "other")
    if ntype == "frame":
        color_map.append("gold")
    elif ntype == "axiom":
        color_map.append("skyblue")
    elif ntype == "contradiction":
        color_map.append("red")
    else:
        color_map.append("grey")

# Draw graph
pos = nx.spring_layout(G, seed=42)
plt.figure(figsize=(16, 12))
nx.draw(G, pos, with_labels=True, node_color=color_map, node_size=1600, font_size=9, arrows=True)
plt.title("RIME Cognitive Frame Graph")
plt.show()
