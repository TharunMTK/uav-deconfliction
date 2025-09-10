# UAV Strategic Deconfliction System

Author: Tharun M.T.K  
Assignment: FlytBase Robotics Assignment 2025  

---

## 📌 Overview
This project implements a UAV Strategic Deconfliction system that determines whether a primary UAV mission is safe given its mission window, while accounting for potential conflicts with other UAVs sharing the same airspace.

The system checks both **spatial** and **temporal** conflicts, returning clear/conflict status along with detailed explanations. It also provides **visualizations** and **animations** to illustrate UAV paths and conflicts.

---

## 📂 Repository Structure

uav-deconfliction-2025/
├── src/
│ ├── deconflict.py # Main code (models, conflict detection, visualization)
│ └── run_scenarios.py # Driver script to auto-run scenarios & save animations
├── tests/ # Unit tests
├── scenarios/ # JSON mission files (conflict, no conflict, etc.)
├── docs/ # Documentation
│ ├── README.md
│ └── REFLECTION.md
└── video/ # Generated animations (MP4)


---

## ⚙️ Installation
Clone the repo and install dependencies:

```bash
pip install numpy matplotlib pytest
