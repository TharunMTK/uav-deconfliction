import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.deconflict import Waypoint, Trajectory, MissionWindow, Config, check_deconfliction


def test_conflict_detected():
    # Primary goes east (0,0) → (10,0)
    primary = Trajectory(
        drone_id="primary",
        waypoints=[Waypoint(0, 0, t=0), Waypoint(10, 0, t=10)]
    )

    # Intruder crosses north at same time → conflict
    intruder = Trajectory(
        drone_id="intruder",
        waypoints=[Waypoint(5, -5, t=0), Waypoint(5, 5, t=10)]
    )

    window = MissionWindow(0, 10)
    cfg = Config(min_sep_xy_m=2.0)

    result = check_deconfliction(primary, [intruder], window, cfg)

    assert result["status"] == "conflict detected"
    assert len(result["conflicts"]) > 0

