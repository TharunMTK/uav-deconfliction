"""
UAV Strategic Deconfliction System
Author: Tharun M.T.K (Assignment 2025)

This module:
- Defines data models for waypoints, trajectories, mission windows, configs
- Provides functions to interpolate drone positions over time
- Checks for spatial + temporal conflicts
- Returns conflict explanations
- Includes simple plotting for visualization
"""

from dataclasses import dataclass
from typing import List, Dict, Tuple, Optional
import numpy as np
import json
import matplotlib.pyplot as plt


# ----------------------------
# Data Models
# ----------------------------

@dataclass
class Waypoint:
    x: float
    y: float
    z: Optional[float] = None
    t: Optional[float] = None  # seconds from mission start


@dataclass
class Trajectory:
    drone_id: str
    waypoints: List[Waypoint]


@dataclass
class MissionWindow:
    t_start: float
    t_end: float


@dataclass
class Config:
    min_sep_xy_m: float = 5.0
    min_sep_z_m: float = 2.0
    dt_s: float = 0.5
    merge_gap_s: float = 1.0
    corridor_buffer_m: float = 10.0


# ----------------------------
# Utilities
# ----------------------------

def interpolate_position(wp1: Waypoint, wp2: Waypoint, t: float) -> Tuple[float, float, float]:
    """Linearly interpolate between two waypoints at time t."""
    if wp1.t is None or wp2.t is None:
        raise ValueError("Waypoints must have time defined for interpolation")
    ratio = (t - wp1.t) / (wp2.t - wp1.t)
    x = wp1.x + ratio * (wp2.x - wp1.x)
    y = wp1.y + ratio * (wp2.y - wp1.y)
    z1, z2 = wp1.z or 0.0, wp2.z or 0.0
    z = z1 + ratio * (z2 - z1)
    return x, y, z


def sample_trajectory(traj: Trajectory, t_grid: np.ndarray) -> np.ndarray:
    """Sample trajectory at each time in t_grid."""
    positions = []
    for t in t_grid:
        wps = traj.waypoints
        for i in range(len(wps) - 1):
            if wps[i].t <= t <= wps[i + 1].t:
                positions.append(interpolate_position(wps[i], wps[i + 1], t))
                break
    return np.array(positions)


# ----------------------------
# Conflict Checking
# ----------------------------

def check_deconfliction(primary: Trajectory, traffic: List[Trajectory], window: MissionWindow, cfg: Config):
    """
    Check for conflicts between a primary trajectory and traffic drones.
    Returns dict with status and conflict details.
    """
    results = {"status": "clear", "conflicts": []}
    t_grid = np.arange(window.t_start, window.t_end, cfg.dt_s)
    primary_pos = sample_trajectory(primary, t_grid)

    for other in traffic:
        other_pos = sample_trajectory(other, t_grid)

        if len(primary_pos) == 0 or len(other_pos) == 0:
            continue

        min_dist = np.linalg.norm(primary_pos - other_pos, axis=1)

        conflict_mask = min_dist <= cfg.min_sep_xy_m
        if np.any(conflict_mask):
            results["status"] = "conflict detected"
            conflict_times = t_grid[conflict_mask]
            for t_c in conflict_times:
                idx = np.where(t_grid == t_c)[0][0]
                results["conflicts"].append({
                    "other_id": other.drone_id,
                    "time": float(t_c),
                    "distance": float(min_dist[idx]),
                    "primary_point": primary_pos[idx].tolist(),
                    "other_point": other_pos[idx].tolist()
                })
    return results


# ----------------------------
# Visualization
# ----------------------------

def plot_scenario(primary: Trajectory, traffic: List[Trajectory], results: Dict):
    """Plot the scenario with conflicts highlighted."""
    plt.figure(figsize=(6, 6))
    # Primary
    px = [wp.x for wp in primary.waypoints]
    py = [wp.y for wp in primary.waypoints]
    plt.plot(px, py, 'b-o', label=f"Primary: {primary.drone_id}")

    # Traffic
    for other in traffic:
        ox = [wp.x for wp in other.waypoints]
        oy = [wp.y for wp in other.waypoints]
        plt.plot(ox, oy, 'g--', label=f"Traffic: {other.drone_id}")

    # Conflicts
    for c in results["conflicts"]:
        plt.scatter(c["primary_point"][0], c["primary_point"][1], c='r', marker='x')

    plt.xlabel("X [m]")
    plt.ylabel("Y [m]")
    plt.legend()
    plt.title("Deconfliction Scenario")
    plt.grid(True)
    plt.show()


# ----------------------------
# Example Run (demo)
# ----------------------------

if __name__ == "__main__":
    # Define primary path
    primary = Trajectory(
        drone_id="primary",
        waypoints=[
            Waypoint(0, 0, t=0),
            Waypoint(10, 0, t=10)
        ]
    )

    # Define traffic drone crossing path
    traffic = [
        Trajectory(
            drone_id="intruder",
            waypoints=[
                Waypoint(5, -5, t=0),
                Waypoint(5, 5, t=10)
            ]
        )
    ]

    window = MissionWindow(0, 10)
    cfg = Config(min_sep_xy_m=2.0)

    results = check_deconfliction(primary, traffic, window, cfg)
    print(json.dumps(results, indent=2))
    plot_scenario(primary, traffic, results)

