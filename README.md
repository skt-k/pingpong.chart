# 🎮 Pingpong Chart (Kivy 2D Battle Game)

![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)
![Kivy](https://img.shields.io/badge/Kivy-2.3.1-green.svg)
![Architecture](https://img.shields.io/badge/Architecture-OOP-orange.svg)

**Pingpong Chart** is a 2D tactical, turn-based battle game developed entirely in Python using the **Kivy framework**. 

This project was built to demonstrate a deep understanding of **Object-Oriented Programming (OOP)**, **Event-Driven Architecture**, and **GUI/UI development**. Players manage resources (Health and Energy) and strategically choose from 11 different abilities to defeat an opponent.



## 🏗️ Architecture & Core Components

- **`GameWidget`**: The main orchestrator. Manages the core game loop, tracks scores, and handles global game states.
- **`Player` & `Enemy`**: Stateful entities that track health, energy, and current attack actions.
- **`AttackPower`**: Handles projectile movement, hitboxes, and complex collision resolution (calculating which attack overpowers another based on the game's matrix).
- **`ExplosionPower` / `Health`**: Modular UI components for visual feedback and resource tracking.

---

## 🚀 Getting Started

### Prerequisites
Make sure you have Python 3 installed. It is highly recommended to use a virtual environment (`venv`).

### Installation
1. Clone this repository.
2. Install the required dependencies:
   ```bash
   pip install kivy
   ```
   *(Note: If you are using Python 3.12+, you might need to install the pre-release version: `pip install --pre kivy kivy[base]`)*

### Running the Game
Run the main Python script to start the game window:
```bash
python PPC.py
```

---

## ⚔️ Gameplay Mechanics & Rules

The game is a 1v1 battle against an AI opponent. Both sides start with **5 Health** and **3 Energy**. Actions cost or generate Energy.

### Controls & Abilities Matrix
| Key | Action | Energy Cost | Mechanics / Counters |
| :---: | :--- | :---: | :--- |
| **A** | Prepare | - | Resets stance after an attack. |
| **J** | Charge | +1 | Gains energy, but highly vulnerable to any incoming attack. |
| **U** | Super Charge | +2 (Needs 3) | Huge energy gain, but instantly loses all energy if countered by Mirror (`;`). |
| **O** | Invisibility | 0 | Evades most attacks. Only loses to Gun (`P`) and Sickle (`H`). |
| **I** | Defend | 0 | Blocks standard attacks. Loses to Canned Cat (`L`) and Sickle (`H`). |
| **;** | Mirror/Reflect | -2 | Reflects damage. Wins against Scratch (`K`). |
| **K** | Scratch | -1 | Basic attack. Loses to Sickle (`H`). |
| **L** | Canned Cat | -3 | Pierces defenses. Wins against Defend (`I`). |
| **P** | Gun | -3 | Ranged attack. Wins against Invisibility (`O`). |
| **Y** | Cat Punch | -4 | Heavy attack. Destroys Mirror/Reflect (`;`). |

