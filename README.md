# RIME: Recursive Integrative Meaning Engine

RIME is a self-evolving, frame-based logic engine that models reasoning through contradiction, adaptation, and abstraction — without relying on static axioms or fixed truths. It supports:

- Reflexive contradiction handling
- Frame switching based on coherence
- Meta-abstraction from pattern repetition
- Temporal memory of belief evolution
- CSV-based input/output for full transparency

---

## 🔧 Features

- 📚 **Logic Frames**: Each frame holds its own axioms and evolves independently.
- 🔁 **Contradiction-Driven Adaptation**: Contradictions trigger structural updates.
- 🧠 **Meta-Abstraction**: Recurring contradictions are abstracted into higher-order concepts.
- 📜 **Temporal Memory**: All events (inputs, contradictions, adaptations) are tracked over time.
- 🔍 **Meta-Frame Monitoring**: Observes all frames to determine contextually coherent switches.

---

## 📁 File Structure

```
rime/
├── RIME_module.py          # Main logic engine
├── RIME_graph.py           # Graph-based visualizer
├── frame_a_axioms.csv      # Initial axioms for Frame A
├── frame_b_axioms.csv      # Initial axioms for Frame B
├── input_stream.csv        # Input stream for RIME
├── Frame_A_axioms.csv      # Output: evolved axioms for Frame A
├── Frame_B_axioms.csv      # Output: evolved axioms for Frame B
├── Frame_A_events.csv      # Output: event log for Frame A
├── Frame_B_events.csv      # Output: event log for Frame B
├── meta_event_log.csv      # Output: global event timeline
├── meta_abstract_patterns.csv # Output: abstracted patterns
```

---

## 🚀 Getting Started

### 2. Install Requirements
```bash
pip install pandas networkx matplotlib
```

### 3. Run RIME Engine
```bash
python RIME_module.py
```
This will process your `input_stream.csv` using logic from the provided `frame_a_axioms.csv` and `frame_b_axioms.csv`. Outputs will be saved alongside the script.

### 4. Visualize the Results
```bash
python RIME_graph.py
```
This will generate a graph of the reasoning process using `networkx` and `matplotlib`.

---

## 📜 License

This project is licensed under the [Creative Commons Attribution-NonCommercial 4.0 International License](https://creativecommons.org/licenses/by-nc/4.0/).

You are free to share and adapt the code for personal, academic, or non-commercial use, provided that you:
- Attribute the original author
- Link back to this repository
- Indicate any changes made

## 🚫 Commercial Use
Use of this codebase in **commercial applications** or **for-profit systems** requires explicit permission and licensing.  
For licensing requests or custom collaboration, contact:

Tim Isabella
[GitHub Profile](https://github.com/TimIsabella)
https://www.linkedin.com/in/timisabella

---

## ✨ Author

Tim Isabella
[GitHub Profile](https://github.com/TimIsabella)
https://www.linkedin.com/in/timisabella

---


## 🧠 Philosophy

RIME is not a model of truth — it's a model of belief adaptation. It does not assume correctness. It builds coherence by interacting with contradiction.
> "Truth is not what is imposed — it is what survives contradiction."
