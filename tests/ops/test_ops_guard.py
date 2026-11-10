import json

from ops import guard, progress
from ops.guard import Guard, GuardConfig

LAUNCH = 1_800_000_000.0


def iso(ts):
    import datetime as dt

    return dt.datetime.fromtimestamp(ts, dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


class Clock:
    def __init__(self, t=LAUNCH):
        self.t = t

    def __call__(self):
        return self.t

    def sleep(self, s):
        self.t += s


class API:
    def __init__(self, fail_first=0):
        self.calls, self.fail = [], fail_first

    def stop_pod(self, pid):
        if self.fail:
            self.fail -= 1
            raise RuntimeError("boom")
        self.calls.append(("stop", pid))

    def terminate_pod(self, pid):
        self.calls.append(("terminate", pid))


class Reader:
    def __init__(self):
        self.files = {}

    def read_text(self, rel):
        return self.files.get(rel)

    def progress(self, ts):
        self.files["logs/progress.jsonl"] = json.dumps({"ts": iso(ts), "job": "j", "status": "done"}) + "\n"

    def queue(self, pending, running=False, finished=False):
        self.files["logs/queue.json"] = json.dumps({"pending": pending, "running": running, "finished": finished})


def make(cfg=None, api=None, reader=None, on_stop=None):
    clk = Clock()
    reader = reader or Reader()
    api = api or API()
    g = Guard(cfg or GuardConfig(poll_s=60), api, "podfakepodfake", LAUNCH, reader, clock=clk, sleep=clk.sleep,
              on_stop=on_stop, out=lambda s: None)
    return g, clk, api, reader


def test_defaults_are_the_pilot_budget_plus_contingency():
    assert guard.DEFAULT_GPU_HOUR_CAP == 7.5
    assert GuardConfig().gpu_hour_cap == 7.5 and GuardConfig().stall_s == 45 * 60


def test_no_condition_keeps_running():
    g, clk, api, rd = make()
    rd.queue(pending=5, running=True)
    rd.progress(clk.t)
    assert g.run(max_polls=10) is None and api.calls == []


def test_gpu_hour_cap_stops_pod():
    stops = []
    g, clk, api, rd = make(GuardConfig(poll_s=600, gpu_hour_cap=7.5, stall_s=10**9), on_stop=lambda r, t: stops.append((r, t)))
    rd.queue(pending=5, running=True)
    reason = None
    for _ in range(100):
        rd.progress(clk.t)
        reason = g.run(max_polls=1)
        if reason:
            break
    assert reason == "gpu_hour_cap" and api.calls == [("stop", "podfakepodfake")]
    assert abs(g.gpu_hours() - 7.5) < 0.2                      # stopped at the first poll at or past the cap
    assert stops and stops[0][0] == "gpu_hour_cap"


def test_cap_boundary_exact():
    g, clk, api, rd = make(GuardConfig(gpu_hour_cap=2.0, stall_s=10**9))
    clk.t = LAUNCH + 2 * 3600 - 1
    assert g.check() is None
    clk.t = LAUNCH + 2 * 3600
    assert g.check() == "gpu_hour_cap"


def test_queue_empty_stops_immediately_without_grace():
    g, clk, api, rd = make(GuardConfig(empty_grace_s=0, stall_s=10**9))
    assert g.check() is None                                    # no queue file yet: unknown, not empty
    rd.queue(pending=0, running=False)
    assert g.run(max_polls=1) == "queue_empty" and api.calls == [("stop", "podfakepodfake")]


def test_queue_finished_flag_counts_as_empty_even_with_pending_left():
    g, clk, api, rd = make(GuardConfig(empty_grace_s=0, stall_s=10**9))
    rd.queue(pending=7, running=False, finished=True)           # runner stopped after a fatal failure
    assert g.check() == "queue_empty"


def test_queue_empty_grace_period_and_reset():
    g, clk, api, rd = make(GuardConfig(poll_s=60, empty_grace_s=300, stall_s=10**9))
    rd.queue(pending=0)
    assert g.check() is None
    clk.t += 299
    assert g.check() is None
    rd.queue(pending=1, running=True)                           # new work arrives: grace resets
    assert g.check() is None
    rd.queue(pending=0)
    assert g.check() is None
    clk.t += 300
    assert g.check() == "queue_empty"


def test_stall_after_45_minutes_without_progress_line():
    g, clk, api, rd = make(GuardConfig(poll_s=60))
    rd.queue(pending=3, running=True)
    rd.progress(clk.t)
    clk.t += 45 * 60 - 1
    assert g.check() is None
    clk.t += 1
    assert g.check() == "no_progress"
    assert g.run(max_polls=1) == "no_progress" and api.calls


def test_new_progress_line_resets_stall_clock():
    g, clk, api, rd = make(GuardConfig(poll_s=60))
    rd.queue(pending=3, running=True)
    rd.progress(clk.t)
    clk.t += 40 * 60
    rd.progress(clk.t)
    clk.t += 40 * 60
    assert g.check() is None
    clk.t += 5 * 60
    assert g.check() == "no_progress"


def test_stall_counts_from_guard_start_when_no_progress_file():
    g, clk, api, rd = make(GuardConfig(stall_s=600))
    clk.t += 599
    assert g.check() is None
    clk.t += 1
    assert g.check() == "no_progress"


def test_stop_failure_is_retried_and_terminate_option():
    g, clk, api, rd = make(GuardConfig(poll_s=10, empty_grace_s=0), api=API(fail_first=2))
    rd.queue(pending=0)
    assert g.run(max_polls=5) == "queue_empty"
    assert api.calls == [("stop", "podfakepodfake")] and clk.t == LAUNCH + 20
    g2, _, api2, rd2 = make(GuardConfig(empty_grace_s=0, terminate=True))
    rd2.queue(pending=0)
    assert g2.run(max_polls=1) == "queue_empty" and api2.calls == [("terminate", "podfakepodfake")]


def test_progress_helpers_tolerate_garbage():
    assert progress.last_progress_ts("not json\n") is None
    assert progress.last_progress_ts(None) is None
    assert not progress.queue_is_empty("{bad") and not progress.queue_is_empty(None)


def test_ssh_reader_command_is_redacted_when_shown():
    calls = []

    class R:
        returncode, stdout = 0, "hello"

    rd = guard.SshReader("203.0.113.77", "22222", "/keys/id_pod_key", "/workspace/x/runs/r", runner=lambda c, **k: (calls.append(c), R())[1])
    assert rd.read_text("logs/queue.json") == "hello" and "203.0.113.77" in " ".join(calls[0])
    shown = " ".join(rd.command("logs/queue.json", shown=True))
    assert "203.0.113.77" not in shown and "id_pod_key" not in shown and "..." in shown
