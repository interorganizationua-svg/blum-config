# ⚡ Motion-Responsive Autoclicker

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Educational-orange?style=for-the-badge)

A high-performance Python automation tool that triggers mouse events based on real-time visual changes (color/movement detection). Designed to test algorithm efficiency and hardware-software integration.

> **⚠️ Disclaimer:** This project was developed strictly for **educational purposes** to demonstrate skills in computer vision, input simulation, and algorithm optimization. It is not intended for malicious use, botting, or cheating in online environments. Use responsibly.

## 🎯 Key Features

* **⚡ Zero-Latency Reaction:** Utilizes a custom color sensor algorithm to detect specific pixel changes instantly.
* **👀 Motion Detection:** The bot triggers upon detecting movement within a defined screen area (`ROI` - Region of Interest).
* **🤖 Human-Like Behavior:** Implemented a randomized delay system (Gaussian distribution) to simulate human reaction time and prevent blocking.
* **🚀 High Performance:** Optimized for sub-second response times using lightweight libraries, minimizing CPU usage.

## ⚙️ How It Works

The system operates on a continuous feedback loop designed to balance speed with safety:

1.  **Scanning:** The script continuously monitors a specific coordinate or region of the screen (pixel array).
2.  **Triggering:** When the color value shifts beyond the set threshold (indicating movement/change), the trigger activates.
3.  **Delay Calculation:** Before clicking, the system calculates a `sleep` interval based on a randomized range to mimic human reflexes.
4.  **Execution:** The mouse event is sent directly to the OS input stream.

## 🛠️ Tech Stack

| Component | Technology | Purpose |
| :--- | :--- | :--- |
| **Core** | `Python 3.x` | Main logic |
| **Input Simulation** | `PyAutoGUI` / `Win32API` | High-speed mouse control |
| **Vision** | `Pillow` (PIL) / `OpenCV` | Screen capture & pixel analysis |
| **Logic** | `Time`, `Random` | Anti-detection algorithms |

## 🚀 Getting Started

### Prerequisites
* Python 3.x installed
* Pip package manager

### Installation

1.  Clone the repository:
    ```bash
    git clone [https://github.com/yourusername/motion-autoclicker.git](https://github.com/yourusername/motion-autoclicker.git)
    ```
2.  Navigate to the directory:
    ```bash
    cd motion-autoclicker
    ```
3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Configuration
Edit `config.py` (or the variables in `main.py`) to set your parameters:

```python
TARGET_COLOR = (255, 0, 0)  # RGB Color to track
TOLERANCE = 10              # Sensitivity of the sensor
MIN_DELAY = 0.05            # Minimum reaction time
MAX_DELAY = 0.15            # Maximum reaction time
