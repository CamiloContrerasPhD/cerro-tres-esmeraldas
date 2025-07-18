# Cerro de las Tres Esmeraldas – A Pygame River‑Crossing Puzzle

> **“Only those who balance light and silence may walk the hidden path.”**\
> *Tayrona inscription, City of the Lost*

This small Python game recreates (and re‑skins) the classic **Quarrasi Lock** puzzle from Allen B. Downey’s book *Think Like a Programmer*—but transplants it to the misty heights of Colombia’s **Sierra Nevada de Santa Marta**.

We were inspired both by the book **and** by **Daniel Tam’s** JavaScript adaptation ([danielthetam/TheQuarrasiLock](https://github.com/danielthetam/TheQuarrasiLock)). Our goal is to offer a desktop variant built with **Pygame** that teachers and puzzle‑lovers can run offline.

---

## Story in a Nutshell

Three ceremonial bars—**Trinos**—covered in emerald‑frog gemstones must be slid from the **Right Altar** to the **Left Altar**.

- A light niche turns **ON** when its column holds an **even** number of emeralds.
- A conch horn (the alarm) sounds if an altar ever shows **exactly one** niche lit.
- Pressing a stone **chaguala** silences the horn on the altar you are standing next to, but you can hold **only one** chaguala at a time.

Move all three Trinos left without waking the spirits!

---

## Screenshots

| Title Screen | In‑game |
| ------------ | ------- |
|              |         |

*(Art assets are CC‑BY and included in **`assets/`**.)*

---

## Quick Start

```bash
# 1 · Clone the repo
git clone https://github.com/your‑user/cerro‑esmeraldas.git
cd cerro‑esmeraldas

# 2 · Create a virtual environment (optional but recommended)
python -m venv .venv
source .venv/Scripts/activate      # Windows
# source .venv/bin/activate        # macOS/Linux

# 3 · Install dependencies
pip install -r requirements.txt    # currently just pygame

# 4 · Run the game
python main.py
```

A Pygame window **(1280 × 720)** will appear; resizing is supported.

---

## Controls

| Action                       | Key / Mouse                   |
| ---------------------------- | ----------------------------- |
| Move explorer between Trinos | **Left‑click** on a Trino bar |
| Push a Trino                 | Click the same bar again      |
| Hold active chaguala         | **Spacebar**                  |
| Reset puzzle                 | **R**                         |
| Quit                         | **Esc**                       |

The status bar at the top shows which altar you are next to and whether a horn is being suppressed.

---

## Why another version?

- **Desktop feel** – Some learners prefer a standalone window over an HTML canvas.
- **Colombian re‑theme** – Educators in Latin America asked for local cultural references (emeralds, Tayrona myths, conch horns).
- **Python practice** – Ideal demo of Pygame’s event loop, layered surfaces, and simple tweening.

---

## Acknowledgements

- Original puzzle by **Allen B. Downey**, *Think Like a Programmer* (Chapter 1).
- JavaScript inspiration from **Daniel Tam** – [https://github.com/danielthetam/TheQuarrasiLock](https://github.com/danielthetam/TheQuarrasiLock).
- Emerald‑frog icon © Ana Salazar (CC‑BY 4.0).
- Background music loop by **@kevin‑macleod** (CC0).

---

## License

MIT – see [`LICENSE.md`](LICENSE.md).

Happy puzzling, and may the spirits of the Sierra guide your moves!

