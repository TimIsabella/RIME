# RIME: Reflexive Identity Modulation Engine

A lightweight, self-evolving logic engine for multi-frame reasoning, contradiction resolution, and adaptive belief modeling.

---

## 🧠 What is RIME?

**RIME** is a lightweight, self-contained cognitive architecture designed for developing agents that can model, evolve, and revise their own belief structures over time. Built as a frame-based recursive system, RIME enables:

- Reflexive self-evaluation
- Contradiction detection and resolution
- Multiple co-existing frames (worldviews)
- Memory of prior belief states
- Goal-driven reasoning and adaptive modulation

Originally developed from the **Recursive Reflexive Logic Engine**, RIME introduces a modular frame system, introspective scheduling, and narrative identity tracking — all optimized for conventional hardware.

---

## 🔧 Features

- 🧩 **Frames:** Self-contained belief systems with local axioms, weights, and contradiction buffers
- 🔁 **Reflexive Adaptation:** Contradiction triggers belief revision and trust updates
- 🧠 **Meta-Frame Management:** Multiple worldviews compared, swapped, and merged dynamically
- 🎯 **Goal-Driven Evolution:** Aligns with a configurable system-level purpose
- 🧠 **Narrative Memory:** Tracks belief changes over time for introspective agents
- ⚡ **Low Compute Overhead:** Runs efficiently on standard desktops/laptops

## 🧪 Example Output
```text
Input P0: Accepted
Introspection triggered.
{'active_frame': 'default', 'axioms': ['P0'], 'contradictions': [], 'history': []}
Input P1: Accepted
Input Q: Contradicted
Input P2: Accepted
...
```

## ⚙️ Customization

### Modify Goal Function
Change how frames are scored by modifying the `goal_fn`:
```python
def simple_goal_fn(frame):
    return len(frame.axioms) - len(frame.contradiction_buffer)
```

### Add New Frames
You can create multiple frames with different rules:
```python
fm.create_frame("scientific", my_custom_goal_fn)
fm.create_frame("intuitive", another_goal_fn)
```

---

## ⏱️ Adjusting System Speed

You can control RIME's tempo and computational load by modifying the following values directly in `reflexive_logic_module.py`:

### 🔁 Introspection Frequency
Controls how often the system checks frame performance and possibly switches frames.

**Find this block in the main loop:**
```python
if i % 5 == 0:  # Run introspection every 5 prompts
    fm.introspect()
```
**Adjust `5` to a higher number (e.g., `10`) to slow down introspection**, or lower it (e.g., `1` or `2`) for faster frame switching.

---

### 🧠 Contradiction Buffer Size
Determines how many unresolved contradictions are held before triggering frame adaptation.

**In `Frame.__init__`:**
```python
self.contradiction_buffer = deque(maxlen=100)
```
**Increase `maxlen`** to make the system more tolerant and slower to adapt. **Reduce** it for a faster, more reactive agent.

---

### ⚠️ Contradiction Threshold for Adaptation
Controls how sensitive a frame is to contradiction.

**In `Frame.adapt()`:**
```python
if len(self.contradiction_buffer) > 10:
```
**Increase `10`** for slower adaptation, or **decrease** it (e.g., `3–5`) to trigger quicker restructuring.

---

### 🎯 Goal Function Sensitivity
Affects how frames are scored and compared during introspection.

**In `simple_goal_fn(frame)`:**
```python
def simple_goal_fn(frame):
    return len(frame.axioms) - len(frame.contradiction_buffer)
```
You can make it more aggressive by increasing the weight of contradictions or rewarding certain axioms.

---

### 🧵 Optional: Background Introspection Loop
To simulate a "thinking agent" that introspects on a timed interval, you can run this in a thread:

```python
import threading

def background_introspect(fm, interval=10):
    while True:
        time.sleep(interval)
        fm.introspect()
        print("[Background] Introspection triggered.")

threading.Thread(target=background_introspect, args=(fm,), daemon=True).start()
```
This keeps introspection active without relying on prompt counts and is ideal for more advanced agents.


You can control RIME's tempo and computational load using these settings:

| Setting                       | Slower System                         | Faster System                          |
|------------------------------|----------------------------------------|----------------------------------------|
| `i % X` introspection rate   | Higher `X` (e.g. 10)                   | Lower `X` (e.g. 1–2)                   |
| Contradiction buffer size    | Larger (100–200)                      | Smaller (10–30)                        |
| Contradiction threshold      | Higher (20+)                          | Lower (3–10)                           |
| Goal function sensitivity    | Mild penalty on contradiction         | Heavy penalty, frequent switching      |
| Frame comparison frequency   | Rare introspection                    | Frequent or time-based introspection   |

You can also implement background or time-based introspection to simulate continuous thinking while keeping CPU usage low.

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

"Truth is not a fixed point. It is a structure in motion — stable within frames, but relative across them. Contradiction is not failure, but the signal to adapt."
