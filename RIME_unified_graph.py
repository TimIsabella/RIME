import os
import json
import matplotlib.pyplot as plt
import networkx as nx
from collections import defaultdict

def load_rime_state(state_file='rime_state.json'):
    if not os.path.exists(state_file):
        raise FileNotFoundError("State file not found.")

    with open(state_file, 'r') as f:
        return json.load(f)

def build_combined_graph(state):
    G = nx.DiGraph()

    for frame_id, data in state['frames'].items():
        frame_label = f"FRAME:{frame_id[:6]}"
        G.add_node(frame_label, type='frame', color='skyblue')

        for axiom in data['axioms']:
            ax_node = f"AX:{frame_id[:6]}:{axiom}"
            G.add_node(ax_node, type='axiom', color='green')
            G.add_edge(frame_label, ax_node)

        for tick, contradiction in data['contradictions']:
            ct_node = f"CT:{frame_id[:6]}:{contradiction}"
            G.add_node(ct_node, type='contradiction', color='red')
            G.add_edge(ct_node, frame_label, label=f"tick {tick}")

        for hist in data['history']:
            if hist['action'] == 'adapt':
                hist_node = f"ADAPT:{frame_id[:6]}:{hist['tick']}"
                G.add_node(hist_node, type='adapt', color='blue')
                G.add_edge(hist_node, frame_label)

    for event in state['event_log']:
        if event['event'] == 'frame_switch':
            from_f = f"FRAME:{event['from'][:6]}"
            to_f = f"FRAME:{event['to'][:6]}"
            G.add_edge(from_f, to_f, label=f"switch@{event['tick']}", color='black')
        elif event['event'] == 'frame_created':
            new_f = f"FRAME:{event['new_frame'][:6]}"
            G.add_node(new_f, type='frame', color='skyblue')

    return G

def draw_combined_graph(G, state):
    pos = nx.circular_layout(G)
    node_colors = [data.get('color', 'gray') for _, data in G.nodes(data=True)]

    plt.figure(figsize=(18, 12))
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=500)
    nx.draw_networkx_labels(G, pos, font_size=7)
    nx.draw_networkx_edges(G, pos, arrows=True)

    edge_labels = {(u, v): d['label'] for u, v, d in G.edges(data=True) if 'label' in d}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=6)

    plt.title(f"RIME Combined Graph Overview\nTick: {state['tick']}, Active Frame: {state['active_frame'][:6]}")
    plt.axis('off')
    plt.tight_layout()
    plt.show()

def main():
    state = load_rime_state()
    G = build_combined_graph(state)
    draw_combined_graph(G, state)

if __name__ == '__main__':
    main()