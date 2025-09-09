"""
Run both conflict and no-conflict scenarios automatically,
generate animations, and save them as MP4 in /video/
"""

import os
from src.deconflict import (
    load_trajectory_from_json, MissionWindow, Config,
    check_deconfliction, plot_scenario, animate_scenario
)

def run_and_save(name: str, primary_file: str, traffic_file: str, out_file: str):
    primary = load_trajectory_from_json(primary_file)
    traffic = [load_trajectory_from_json(traffic_file)]

    # Mission window based on primary mission
    window = MissionWindow(primary.waypoints[0].t, primary.waypoints[-1].t)
    cfg = Config(min_sep_xy_m=2.0)

    results = check_deconfliction(primary, traffic, window, cfg)

    print(f"\n=== Scenario: {name} ===")
    print(results)

    plot_scenario(primary, traffic, results)
    animate_scenario(primary, traffic, window, cfg, results, save_path=out_file)


if __name__ == "__main__":
    os.makedirs("video", exist_ok=True)

    # Conflict scenario
    run_and_save(
        name="Conflict Case",
        primary_file="scenarios/primary.json",
        traffic_file="scenarios/traffic_conflict.json",
        out_file="video/conflict_case.mp4"
    )

    # No conflict scenario
    run_and_save(
        name="No Conflict Case",
        primary_file="scenarios/primary.json",
        traffic_file="scenarios/traffic_safe.json",
        out_file="video/no_conflict_case.mp4"
    )
