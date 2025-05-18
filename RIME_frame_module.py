import csv
import json
import os
import uuid
from collections import defaultdict

class Frame:
    def __init__(self, frame_id=None, threshold=3):
        self.frame_id = frame_id or str(uuid.uuid4())
        self.axioms = set()
        self.trust = defaultdict(lambda: 1.0)
        self.contradictions = []
        self.history = []
        self.events = []
        self.threshold = threshold
        self.tick = 0

    def evaluate(self, tick, input_):
        accepted = False
        if not self.axioms:
            self.axioms.add(input_)
            accepted = True
        elif input_ in self.axioms:
            accepted = True
        else:
            self.contradictions.append((tick, input_))
            self.trust[input_] -= 0.1

        self.events.append({
            'tick': tick,
            'input': input_,
            'accepted': accepted,
            'trust': round(self.trust[input_], 2)
        })

    def adapt(self, tick):
        if len(self.contradictions) >= self.threshold:
            recent_inputs = [item[1] for item in self.contradictions[-self.threshold:]]
            self.axioms.update(recent_inputs)
            self.history.append({
                'tick': tick,
                'action': 'adapt',
                'new_axioms': recent_inputs
            })
            self.contradictions = []

    def score(self):
        return len(self.axioms) - len(self.contradictions)

    def process_csv_input(self, filename):
        filepath = os.path.join(os.getcwd(), filename)
        with open(filepath, newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                if row:
                    self.evaluate(self.tick, row[0])
                    self.adapt(self.tick)
                    self.tick += 1

    def write_summary_csv(self):
        summary_path = os.path.join(os.getcwd(), f'OUTPUT_{self.frame_id}_summary.csv')
        with open(summary_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['axioms'])
            for ax in sorted(self.axioms):
                writer.writerow([ax])
            writer.writerow([])
            writer.writerow(['contradictions'])
            for tick, input_ in self.contradictions:
                writer.writerow([tick, input_])

    def write_events_csv(self):
        events_path = os.path.join(os.getcwd(), f'OUTPUT_{self.frame_id}_events.csv')
        with open(events_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['tick', 'input', 'accepted', 'trust'])
            writer.writeheader()
            for event in self.events:
                writer.writerow(event)

if __name__ == '__main__':
    frame = Frame()
    input_file = 'INPUT_frame_data.csv'
    frame.process_csv_input(input_file)
    frame.write_summary_csv()
    frame.write_events_csv()
    print(f"Frame {frame.frame_id} complete. Score: {frame.score()}")
