import os
import json
import matplotlib.pyplot as plt
import networkx as nx

def load_rime_state(state_file='rime_state.json'):
    if not os.path.exists(state_file):
        raise FileNotFoundError("State file not found.")

    with open(state_file, 'r') as f:
        return json.load(f)

def build_internal_graph(frame_id, frame_data):
    G = nx.DiGraph()

    for axiom in frame_data['axioms']:
        G.add_node(f"AX:{axiom}", color='green')

    for tick, contradiction in frame_data['contradictions']:
        G.add_node(f"CT:{contradiction}", color='red')
        G.add_edge(f"CT:{contradiction}", f"AX:{contradiction}", label=f"resolved@{tick}")

    for change in frame_data['history']:
        if change['action'] == 'adapt':
            for ax in change['new_axioms']:
                G.add_node(f"AX:{ax}", color='green')
                G.add_edge(f"change@{change['tick']}", f"AX:{ax}", label='adapted')
                G.add_node(f"change@{change['tick']}", color='blue')

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
        pos = nx.spring_layout(G, seed=42)

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
