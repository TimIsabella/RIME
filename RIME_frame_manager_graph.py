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

def build_frame_graph(state):
    G = nx.DiGraph()
    frames = state['frames']

    for frame_id, data in frames.items():
        score = len(data['axioms']) - len(data['contradictions'])
        label = f"{frame_id[:6]}\nScore: {score}"
        G.add_node(frame_id, label=label, score=score)

    for event in state['event_log']:
        if event['event'] == 'frame_switch':
            G.add_edge(event['from'], event['to'], tick=event['tick'])

    return G

def draw_graph(G, state):
    pos = nx.spring_layout(G, seed=42)
    labels = nx.get_node_attributes(G, 'label')
    scores = [G.nodes[n]['score'] for n in G.nodes]

    plt.figure(figsize=(12, 8))
    nx.draw_networkx_nodes(G, pos, node_size=1500, cmap=plt.cm.Blues, node_color=scores)
    nx.draw_networkx_labels(G, pos, labels)
    nx.draw_networkx_edges(G, pos, arrows=True)
    edge_labels = {(u, v): f"t{d['tick']}" for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    plt.title(f"Frame Graph Overview\nTick: {state['tick']}, Active Frame: {state['active_frame'][:6]}")
    plt.axis('off')
    plt.tight_layout()
    plt.show()

def main():
    state = load_rime_state()
    G = build_frame_graph(state)
    draw_graph(G, state)

if __name__ == '__main__':
    main()
