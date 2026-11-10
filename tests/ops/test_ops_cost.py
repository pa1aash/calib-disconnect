import datetime as dt

import pytest

from ops import cost
from pipeline.contracts.layout import COST_LEDGER_COLUMNS

T0 = dt.datetime(2026, 11, 10, 12, 0, 0, tzinfo=dt.timezone.utc)


def launch(path, pod="podABCDEF123456", price=2.5, src="console page, 2026-11-10", run="pilot"):
    return cost.append_launch(path, launch=T0, pod_id=pod, gpu_type="gpu-x", hourly_price_usd=price,
                              price_source=src, run_id=run, git_sha="abc123")


def test_append_creates_header_and_row(tmp_path):
    p = tmp_path / "runs" / "COST_LEDGER.csv"
    launch(p)
    header = p.read_text().splitlines()[0]
    assert header == ",".join(COST_LEDGER_COLUMNS)
    rows = cost.read_rows(p)
    assert len(rows) == 1
    r = rows[0]
    assert r["pod_id_prefix"] == "podA..."
    assert "podABCDEF123456" not in p.read_text()
    assert r["stop_utc"] == "" and r["hourly_price_usd"] == "2.5" and r["launch_utc"] == "2026-11-10T12:00:00Z"


@pytest.mark.parametrize("price,src", [(None, "x"), (0, "x"), (-1, "x"), (float("nan"), "x"), ("abc", "x"), (2.0, ""), (2.0, "  "), (2.0, None)])
def test_launch_refuses_without_price_or_source(tmp_path, price, src):
    p = tmp_path / "L.csv"
    with pytest.raises(cost.LedgerError):
        launch(p, price=price, src=src)
    assert not p.exists()


def test_complete_computes_hours_and_cost(tmp_path):
    p = tmp_path / "L.csv"
    launch(p)
    launch(p, pod="otherpod99999", run="other")
    row = cost.complete(p, pod_id="podABCDEF123456", stop=T0 + dt.timedelta(hours=3, minutes=30), reason="queue_empty")
    assert row["gpu_hours"] == "3.5000" and row["cost_usd"] == "8.7500" and row["reason_stopped"] == "queue_empty"
    rows = cost.read_rows(p)
    assert rows[0]["stop_utc"] == "2026-11-10T15:30:00Z" and rows[1]["stop_utc"] == ""
    with pytest.raises(cost.LedgerError):
        cost.complete(p, pod_id="podABCDEF123456", stop=T0, reason="again")      # already complete
    s = cost.summarize(p)
    assert s["gpu_hours"] == 3.5 and s["open_rows"] == 1.0 and s["cost_usd"] == 8.75


def test_launched_at_lookup(tmp_path):
    p = tmp_path / "L.csv"
    launch(p)
    assert cost.launched_at(p, "podABCDEF123456") == T0
    assert cost.launched_at(p, "nothere123456") is None
