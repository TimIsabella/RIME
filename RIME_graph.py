"""
RIME Output Visualizer
This script loads CSV outputs from the RIME engine and creates a graph visualization
of inputs, frames, contradictions, and meta-abstractions.
"""

import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx
import os

# Load all relevant CSVs from /mnt/data
data_path = os.path.dirname(os.path.abspath(__file__))
files = os.listdir(data_path)

# Identify files
frame_axioms = [f for f in files if f.endswith("_axioms.csv")]
frame_contradictions = [f for f in files if f.endswith("_contradictions.csv")]
frame_events = [f for f in files if f.endswith("_events.csv")]
meta_events = "meta_event_log.csv"
meta_patterns = "meta_abstract_patterns.csv"

# Initialize graph
G = nx.DiGraph()

# Add frame nodes
frames = [f.replace("_axioms.csv", "") for f in frame_axioms]
for frame in frames:
    G.add_node(frame, type="frame")

# Add input nodes and connect to frames via event logs
for frame_event_file in frame_events:
    frame_name = frame_event_file.replace("_events.csv", "")
    df = pd.read_csv(os.path.join(data_path, frame_event_file))
    for _, row in df.iterrows():
        input_node = f"{row['tick']}_{row['input']}"
        G.add_node(input_node, type="input")
        G.add_edge(input_node, frame_name, event=row['event'])

# Add meta-pattern nodes
meta_df = pd.read_csv(os.path.join(data_path, meta_patterns)) if meta_patterns in files else pd.DataFrame()
for _, row in meta_df.iterrows():
    node = f"Meta_{row['pattern']}"
    G.add_node(node, type="meta")
    for frame in frames:
        axiom_df = pd.read_csv(os.path.join(data_path, f"{frame}_axioms.csv"))
        if row['pattern'] in axiom_df["axioms"].values:
            G.add_edge(node, frame, event="abstract")

# Assign colors
color_map = []
for node in G.nodes:
    ntype = G.nodes[node].get("type", "other")
    if ntype == "frame":
        color_map.append("gold")
    elif ntype == "meta":
        color_map.append("lightcoral")
    elif ntype == "input":
        color_map.append("skyblue")
    else:
        color_map.append("lightgrey")

# Assign edge colors and styles
edge_colors = []
edge_styles = []
for u, v in G.edges():
    status = G[u][v].get("event", "")
    if status == "accepted":
        edge_colors.append("green")
        edge_styles.append("solid")
    elif status == "contradiction":
        edge_colors.append("red")
        edge_styles.append("dashed")
    elif status == "abstract":
        edge_colors.append("purple")
        edge_styles.append("solid")
    elif status == "adapted":
        edge_colors.append("orange")
        edge_styles.append("dashed")
    else:
        edge_colors.append("blue")
        edge_styles.append("dotted")

# Draw graph
pos = nx.spring_layout(G, seed=42)
plt.figure(figsize=(24, 18))
nx.draw(G, pos, with_labels=True, node_color=color_map,
        edge_color=edge_colors, style=edge_styles,
        node_size=1600, font_size=8, arrows=True, width=2)
plt.title("RIME Reflexive Logic Network Visualization")
plt.show()
