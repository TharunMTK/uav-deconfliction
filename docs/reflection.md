
---

# 📝 `docs/REFLECTION.md`

```markdown
# Reflection & Design Notes

Author: Tharun M.T.K  
Assignment: FlytBase Robotics Assignment 2025  

---

## 🎯 Objective
The goal was to design and implement a UAV strategic deconfliction service to ensure safe UAV operations in shared airspace. The system should identify conflicts (spatial + temporal) and return clear/conflict results with explanations.

---

## 🏗️ Design Choices
1. **Time-Sampling Approach**
   - I used linear interpolation between waypoints to compute positions at regular intervals (`dt_s`).
   - This allowed consistent distance checks between drones.

2. **Conflict Detection**
   - If distance ≤ `min_sep_xy_m` (and altitude check if 3D) → conflict.
   - Consecutive conflict samples are merged into intervals.

3. **Data Models**
   - `Waypoint`, `Trajectory`, `MissionWindow`, and `Config` dataclasses.
   - JSON input for mission definitions ensures flexibility.

4. **Visualization**
   - Static plots for clarity.
   - Animations to illustrate motion and conflicts.
   - Saved as MP4 using `matplotlib.animation`.

---

## 🧪 Testing
- **Conflict Case** → conflict detected at crossing point.
- **No Conflict Case** → drones cross at different times.
- **Near-Miss Case** → just outside buffer, no conflict.
- **Future Work** → altitude-based conflict test.

Tests were automated with `pytest`.

---

## 🤖 Use of AI Tools
I used ChatGPT to:
- Scaffold the initial repository structure.
- Draft unit test cases.
- Help with animation code and README/Reflection drafts.

I validated all AI outputs by running simulations, checking unit test results, and adjusting imports (Windows-specific path fixes).

---

## 🚀 Scalability Thoughts
For thousands of UAVs:
- **Spatial Indexing**: Use R-trees / KD-trees for efficient nearest-neighbor lookups.
- **Partitioning**: Divide airspace into geohash-based cells + time buckets.
- **Streaming Architecture**: Kafka/Flink for live ingestion, deconfliction microservices.
- **Database**: PostGIS/TimescaleDB for spatial + temporal queries.
- **Performance**: Vectorized numpy kernels + GPU acceleration for real-time checks.

---

## 📹 Demo Plan
1. Conflict-free run (clear).
2. Conflict-present run (conflict detected).
3. Show JSON output + plots + animations.
4. Close with scalability explanation.

---

## ✅ Conclusion
The project successfully demonstrates UAV deconfliction:
- Modular, testable codebase.
- Clear + conflict scenarios.
- Visual outputs for interpretability.
- Path toward scalable real-world deployment.
