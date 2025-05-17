"""
RIME: Recursive Integrative Meaning Engine
CSV-Compatible Python Module with Reflexive Logic, Frame Switching, Meta-Abstraction, and Temporal Memory
"""

import pandas as pd
import os
from collections import defaultdict

class Frame:
    def __init__(self, name):
        self.name = name
        self.axioms = set()
        self.trust = defaultdict(lambda: 1.0)
        self.contradictions = set()
        self.history = []
        self.events = []

    def evaluate(self, tick, input_):
        if input_ in self.axioms:
            self.trust[input_] += 0.1
            self.events.append((tick, "accepted", input_))
            return True
        else:
            self.trust[input_] -= 0.2
            self.trust[input_] = max(self.trust[input_], 0.0)
            self.contradictions.add(input_)
            self.events.append((tick, "contradiction", input_))
            return False

    def adapt(self, tick, threshold=4):
        if len(self.contradictions) > threshold:
            recent = list(self.contradictions)[-2:]
            for item in recent:
                self.axioms.add(item)
                self.trust[item] = 0.5
            self.history.append((tick, "adapted", recent))
            self.events.append((tick, "adapted", recent))
            self.contradictions.clear()

class MetaFrameManager:
    def __init__(self):
        self.frames = {}
        self.active_frame = None
        self.meta_abstract_patterns = defaultdict(int)
        self.event_log = []
        self.tick = 0

    def add_frame(self, name, axioms):
        frame = Frame(name)
        frame.axioms.update(axioms)
        self.frames[name] = frame
        if not self.active_frame:
            self.active_frame = name

    def process_input(self, input_):
        self.tick += 1
        best_frame = None
        min_contradictions = float('inf')

        for name, frame in self.frames.items():
            accepted = frame.evaluate(self.tick, input_)
            frame.adapt(self.tick)
            if input_ in frame.axioms:
                self.meta_abstract_patterns[input_] += 1

            contradiction_score = len(frame.contradictions)
            if contradiction_score < min_contradictions:
                min_contradictions = contradiction_score
                best_frame = name

        if best_frame != self.active_frame:
            self.event_log.append((self.tick, "frame_switch", best_frame))
            self.active_frame = best_frame

    def summarize(self):
        return {
            "active_frame": self.active_frame,
            "frames": {
                name: {
                    "axioms": list(f.axioms),
                    "contradictions": list(f.contradictions),
                    "history": f.history,
                    "events": f.events
                } for name, f in self.frames.items()
            },
            "meta_patterns": {k: v for k, v in self.meta_abstract_patterns.items() if v >= 2},
            "event_log": self.event_log
        }

    def export_to_csv(self, output_dir):
        os.makedirs(output_dir, exist_ok=True)
        for name, frame in self.frames.items():
            pd.DataFrame({"axioms": list(frame.axioms)}).to_csv(os.path.join(output_dir, f"{name}_axioms.csv"), index=False)
            pd.DataFrame({"contradictions": list(frame.contradictions)}).to_csv(os.path.join(output_dir, f"{name}_contradictions.csv"), index=False)
            pd.DataFrame(frame.events, columns=["tick", "event", "input"]).to_csv(os.path.join(output_dir, f"{name}_events.csv"), index=False)
        pd.DataFrame(self.event_log, columns=["tick", "event", "target"]).to_csv(os.path.join(output_dir, "meta_event_log.csv"), index=False)
        pd.DataFrame(list(self.meta_abstract_patterns.items()), columns=["pattern", "count"]).to_csv(os.path.join(output_dir, "meta_abstract_patterns.csv"), index=False)

# Run RIME using CSV files
if __name__ == "__main__":
    base_path = os.path.dirname(os.path.abspath(__file__))

    rime = MetaFrameManager()

    # Load initial frame axioms
    frame_a_axioms = pd.read_csv(os.path.join(base_path, "frame_a_axioms.csv"))["axioms"].tolist()
    frame_b_axioms = pd.read_csv(os.path.join(base_path, "frame_b_axioms.csv"))["axioms"].tolist()
    rime.add_frame("Frame_A", frame_a_axioms)
    rime.add_frame("Frame_B", frame_b_axioms)

    # Load input stream
    input_stream = pd.read_csv(os.path.join(base_path, "input_stream.csv"))["input"].tolist()
    for input_ in input_stream:
        rime.process_input(input_)

    # Export results to same directory
    rime.export_to_csv(base_path)

    from pprint import pprint
    pprint(rime.summarize())

