# ⚔️ Nightblade-Runner: Endless Fury ⚔️

**Survive the endless horde. Unleash your inner ninja.**

A high-octane, endless 2D action game built with Python and Pygame. Experience visceral close-quarters combat where every pixel matters.

## 🌟 New Features: The "Juice" Update 🌟

We've overhauled the game to feel **AMAZING**:

*   **💀 Endless Survival**: No levels. No stopping. How long can you last against the infinite wave?
*   **🩸 Visceral "Juice"**:
    *   **Screen Shake**: Feel the impact of every hit.
    *   **Particle Effects**: Blood splatters, dust clouds, and spark explosions!
    *   **Hit Stop**: Time freezes for a split second when you land a killing blow.
*   **⚡ Dash Mechanic**: Press **SHIFT** to dash! Become invincible and move at blinding speeds.
*   **⚔️ Extreme Close Combat**: Attack range is now **10 PIXELS**. You must risk it all to get a kill.
*   **🔥 Combo System**: Chain kills together to rack up massive combos and high scores!
*   **❤️ Blood Thirst**: Heal your wounds by defeating enemies. Every **10 kills** restores health.

## 🎮 Controls

Master your ninja skills:

| Key | Action | Description |
| :--- | :--- | :--- |
| **WASD / Arrows** | **Move** | Navigate the battlefield. |
| **SHIFT** | **DASH** | **New!** Burst of speed + Invincibility. |
| **SPACE / X** | **ATTACK** | Strike enemies within **10px** range. |
| **ESC** | **Pause** | Take a breather (if you can). |

## 🚀 Installation & Setup

### Prerequisites
*   Python 3.11+
*   Pygame CE (`pip install pygame-ce`)

### Quick Start
```bash
# 1. Clone the repo
git clone https://github.com/hassan-635/nightblade-runner.git

# 2. Install dependencies
pip install pygame-ce

# 3. Enter the dojo
python main.py
```

## 🕹️ Gameplay Loop

1.  **Spawn**: Dropped into the endless arena.
2.  **Fight**: Enemies spawn from the shadows continuously.
3.  **Survive**: 
    *   Kill enemies to increase **Score**.
    *   Every **10 Kills** = **+10 Health**.
    *   Enemies get **Faster** as your score increases.
4.  **Die & Repeat**: Beat your high score!

## 📂 Project Structure

```
Nightblade-Runner/
├── main.py                 # 🚀 Entry Point
├── scenes/                 # 🎬 Game Logic (GameScene, Menu)
├── entities/               # 👤 Player & Enemy Classes
├── utils/                  # 🛠️ Particles, Constants, Helpers
│   ├── particle_system.py  # ✨ Visual Effects Logic
│   └── constants.py        # ⚙️ Game Settings (Tweak me!)
├── assets/                 # 🎨 Images & Audio
└── data/                   # 💾 Save Data
```

## 🛠️ Customization

Want to tweak the game? Check `utils/constants.py`:
*   `ATTACK_RANGE`: Currently a hardcore **10**. Increase it if you're scared.
*   `PLAYER_SPEED`: Make your ninja even faster.
*   `ENEMY_BASE_SPEED`: Crank up the difficulty!

---

**Created with ❤️ and 🐍 Python**
*Educational Project | Feel free to fork and learn!*
