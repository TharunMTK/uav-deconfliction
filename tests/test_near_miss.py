import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.deconflict import Waypoint, Trajectory, MissionWindow, Config, check_deconfliction


def test_near_miss():
    # Primary goes east (0,0) → (10,0)
    primary = Trajectory(
        drone_id="primary",
        waypoints=[Waypoint(0, 0, t=0), Waypoint(10, 0, t=10)]
    )

    # Intruder runs parallel, just above buffer distance
    intruder = Trajectory(
        drone_id="intruder",
        waypoints=[Waypoint(0, 3.1, t=0), Waypoint(10, 3.1, t=10)]
    )

    window = MissionWindow(0, 10)
    cfg = Config(min_sep_xy_m=3.0)  # buffer = 3.0 m

    result = check_deconfliction(primary, [intruder], window, cfg)

    # They stay just outside 3m buffer → no conflict
    assert result["status"] == "clear"
    assert len(result["conflicts"]) == 0
