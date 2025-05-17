"""
RIME: Recursive Integrative Meaning Engine
CSV-Compatible Python Module with Reflexive Logic, Frame Switching, Meta-Abstraction, and Temporal Memory
"""

"""
RIME: Recursive Integrative Meaning Engine
Now supports CSV input and output
"""

import pandas as pd
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

    def score(self):
        return len(self.axioms) - len(self.contradictions)

class MetaFrameManager:
    def __init__(self):
        self.frames = {}
        self.active_frame = None
        self.meta_abstract_patterns = defaultdict(int)
        self.event_log = []
        self.tick = 0

    def add_frame(self, name):
        self.frames[name] = Frame(name)
        if not self.active_frame:
            self.active_frame = name

    def process_input(self, input_):
        self.tick += 1
        best_frame = None
        min_contradictions = float('inf')

        for name, frame in self.frames.items():
            accepted = frame.evaluate(self.tick, input_)
            if not accepted:
                frame.contradictions.add(input_)
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
        summary = {
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
        return summary

    def export_to_csv(self, summary_path, events_path):
        summary = self.summarize()
        records = []
        for name, frame in summary["frames"].items():
            for ax in frame["axioms"]:
                records.append({"frame": name, "type": "axiom", "value": ax})
            for con in frame["contradictions"]:
                records.append({"frame": name, "type": "contradiction", "value": con})

        df_summary = pd.DataFrame(records)
        df_summary.to_csv(summary_path, index=False)

        events = []
        for tick, kind, detail in summary["event_log"]:
            events.append({"tick": tick, "event": kind, "detail": detail})
        df_events = pd.DataFrame(events)
        df_events.to_csv(events_path, index=False)

# Execution with CSV I/O
if __name__ == "__main__":
    INPUT_CSV = "INPUT_seed_data.csv"
    OUTPUT_SUMMARY = "OUTPUT_rime_summary.csv"
    OUTPUT_EVENTS = "OUTPUT_rime_events.csv"

    rime = MetaFrameManager()
    rime.add_frame("Frame_A")
    rime.add_frame("Frame_B")

    for i in range(5):
        rime.frames["Frame_A"].axioms.add(f"P{i}")
        rime.frames["Frame_B"].axioms.add(f"Q{i}")

    df_inputs = pd.read_csv(INPUT_CSV)
    for input_ in df_inputs["input"]:
        rime.process_input(input_)

    rime.export_to_csv(OUTPUT_SUMMARY, OUTPUT_EVENTS)

