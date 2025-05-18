import os
import json
import matplotlib.pyplot as plt
import networkx as nx

import matplotlib
matplotlib.rcParams['font.family'] = 'Arial'


def load_rime_state(state_file='rime_state.json'):
    if not os.path.exists(state_file):
        raise FileNotFoundError("State file not found.")

    with open(state_file, 'r') as f:
        return json.load(f)

def build_internal_graph(frame_id, frame_data):
    G = nx.DiGraph()

    def ensure_node(label, color):
        if not G.has_node(label):
            G.add_node(label, color=color)

    for axiom in frame_data['axioms']:
        ensure_node(f"AX:{axiom}", 'green')

    for tick, contradiction in frame_data['contradictions']:
        ensure_node(f"CT:{contradiction}", 'red')
        ensure_node(f"AX:{contradiction}", 'green')  # in case added only via contradiction
        G.add_edge(f"CT:{contradiction}", f"AX:{contradiction}", label=f"resolved@{tick}")

    for change in frame_data['history']:
        if change['action'] == 'adapt':
            for ax in change['new_axioms']:
                ensure_node(f"AX:{ax}", 'green')
                tick_node = f"change@{change['tick']}"
                ensure_node(tick_node, 'blue')
                G.add_edge(tick_node, f"AX:{ax}", label='adapted')

    return G

def draw_all_internal_graphs(state):
    num_frames = len(state['frames'])
    cols = 2
    rows = (num_frames + 1) // cols
    fig, axes = plt.subplots(rows, cols, figsize=(12, 6 * rows))
    axes = axes.flatten() if num_frames > 1 else [axes]

    for idx, (frame_id, frame_data) in enumerate(state['frames'].items()):
        G = build_internal_graph(frame_id, frame_data)
        colors = [data['color'] for _, data in G.nodes(data=True)]
        pos = nx.shell_layout(G)

        ax = axes[idx]
        ax.set_title(f"Frame {frame_id[:6]}")
        nx.draw_networkx_nodes(G, pos, ax=ax, node_color=colors, node_size=600)
        nx.draw_networkx_labels(G, pos, ax=ax, font_size=7)
        nx.draw_networkx_edges(G, pos, ax=ax, arrows=True)
        edge_labels = {(u, v): d['label'] for u, v, d in G.edges(data=True) if 'label' in d}
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax, font_size=6)
        ax.axis('off')

    for j in range(idx + 1, len(axes)):
        axes[j].axis('off')

    plt.tight_layout()
    plt.show()

def main():
    state = load_rime_state()
    draw_all_internal_graphs(state)

if __name__ == '__main__':
    main()
