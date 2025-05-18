import csv
import json
import os
import uuid
from RIME_frame_module import Frame
from collections import defaultdict

class MetaFrameManager:
    def __init__(self, state_file='rime_state.json'):
        self.frames = {}
        self.active_frame = None
        self.meta_abstract_patterns = set()
        self.event_log = []
        self.tick = 0
        self.processed_index = 0
        self.state_file = state_file
        self.load_state()

    def add_frame(self, name=None):
        frame_id = name or str(uuid.uuid4())
        self.frames[frame_id] = Frame(frame_id=frame_id)
        return frame_id

    def process_input(self, input_):
        if not self.frames:
            self.active_frame = self.add_frame()

        best_score = float('-inf')
        best_frame = self.active_frame

        for frame_id, frame in self.frames.items():
            frame.evaluate(self.tick, input_)
            frame.adapt(self.tick)
            score = frame.score()
            if score > best_score:
                best_score = score
                best_frame = frame_id

        # Create a new frame if all current ones show contradictions
        if all(input_ not in f.axioms for f in self.frames.values()):
            new_frame_id = self.add_frame()
            self.frames[new_frame_id].evaluate(self.tick, input_)
            self.frames[new_frame_id].adapt(self.tick)
            best_frame = new_frame_id
            self.event_log.append({
                'tick': self.tick,
                'event': 'frame_created',
                'new_frame': new_frame_id
            })

        if best_frame != self.active_frame:
            self.event_log.append({
                'tick': self.tick,
                'event': 'frame_switch',
                'from': self.active_frame,
                'to': best_frame
            })
            self.active_frame = best_frame

        self.tick += 1
        self.processed_index += 1

    def summarize(self):
        summary = {
            'tick': self.tick,
            'active_frame': self.active_frame,
            'frame_scores': {fid: f.score() for fid, f in self.frames.items()},
            'abstract_patterns': list(self.meta_abstract_patterns),
            'event_log': self.event_log
        }
        return summary

    def export_to_csv(self):
        summary_path = os.path.join(os.getcwd(), 'OUTPUT_rime_summary.csv')
        events_path = os.path.join(os.getcwd(), 'OUTPUT_rime_events.csv')

        with open(summary_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['frame_id', 'axioms'])
            for frame_id, frame in self.frames.items():
                for ax in sorted(frame.axioms):
                    writer.writerow([frame_id, ax])

            writer.writerow([])
            writer.writerow(['frame_id', 'contradictions'])
            for frame_id, frame in self.frames.items():
                for tick, val in frame.contradictions:
                    writer.writerow([frame_id, tick, val])

        with open(events_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['tick', 'event', 'from', 'to', 'new_frame'])
            writer.writeheader()
            for event in self.event_log:
                writer.writerow({
                    'tick': event.get('tick'),
                    'event': event.get('event'),
                    'from': event.get('from', ''),
                    'to': event.get('to', ''),
                    'new_frame': event.get('new_frame', '')
                })

    def save_state(self):
        state = {
            'tick': self.tick,
            'active_frame': self.active_frame,
            'processed_index': self.processed_index,
            'event_log': self.event_log,
            'frames': {fid: {
                'axioms': list(f.axioms),
                'trust': dict(f.trust),
                'contradictions': f.contradictions,
                'history': f.history,
                'events': f.events,
                'tick': f.tick
            } for fid, f in self.frames.items()}
        }
        with open(self.state_file, 'w') as f:
            json.dump(state, f, indent=2)

    def load_state(self):
        if not os.path.exists(self.state_file):
            return
        with open(self.state_file, 'r') as f:
            state = json.load(f)
            self.tick = state['tick']
            self.active_frame = state['active_frame']
            self.processed_index = state['processed_index']
            self.event_log = state['event_log']
            for fid, data in state['frames'].items():
                frame = Frame(frame_id=fid)
                frame.axioms = set(data['axioms'])
                frame.trust = defaultdict(lambda: 1.0, data['trust'])
                frame.contradictions = data['contradictions']
                frame.history = data['history']
                frame.events = data['events']
                frame.tick = data['tick']
                self.frames[fid] = frame

if __name__ == '__main__':
    manager = MetaFrameManager()
    input_file = 'INPUT_data.csv'

    with open(input_file, newline='') as f:
        reader = csv.reader(f)
        for idx, row in enumerate(reader):
            if idx >= manager.processed_index and row:
                manager.process_input(row[0])

    manager.export_to_csv()
    manager.save_state()

    print("MetaFrameManager cycle complete.")
