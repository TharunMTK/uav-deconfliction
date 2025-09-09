import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.deconflict import Waypoint, Trajectory, MissionWindow, Config, check_deconfliction


def test_no_conflict():
    # Primary goes east (0,0) → (10,0)
    primary = Trajectory(
        drone_id="primary",
        waypoints=[Waypoint(0, 0, t=0), Waypoint(10, 0, t=10)]
    )

    # Intruder passes later in time (15–25s) → no overlap
    intruder = Trajectory(
        drone_id="intruder",
        waypoints=[Waypoint(5, -5, t=15), Waypoint(5, 5, t=25)]
    )

    window = MissionWindow(0, 10)
    cfg = Config(min_sep_xy_m=2.0)

    result = check_deconfliction(primary, [intruder], window, cfg)

    assert result["status"] == "clear"
    assert len(result["conflicts"]) == 0
