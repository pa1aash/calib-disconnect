"""LiveCodeBench output capture for behavior signatures (adaptation, runs inside the sandbox).

The vendored evaluator (vendor/lcb/testing_util.py, commit recorded in vendor/lcb/PROVENANCE.md) only
compares outputs with the expected ones; it never returns what a program printed or returned. Agreement
signatures (design section 7.7) need the outputs themselves. This file therefore re-runs the evaluator's
own steps with its own helper functions and records outputs instead of comparing them.

Every difference from ``testing_util.run_test`` / ``grade_call_based`` / ``grade_stdio``:
  1. Outputs are recorded as canonical reprs (floats to 9 significant digits); nothing is compared.
  2. A failing input does not end the run; its signature element is '!<ExceptionType>' ('!Timeout' for
     the evaluator's TimeoutException) and the next input is run.
  3. Call-based prediction tuples are turned into lists, as the evaluator does before comparing.
  4. Stdout captures are normalized like ``get_stripped_lines`` (strip, then strip every line), and
     decimal float tokens are rounded to 9 significant digits; the element is the ``repr`` of that text.
  5. ``faulthandler`` is not enabled per input.
Everything else (import_string prelude, ``clean_if_name``, ``make_function``, ``compile_code``,
``get_function``, ``call_method``, ``Capturing``, ``reliability_guard``, the SIGALRM timeout handler and
the per-input ``signal.alarm(timeout)``) is imported from the vendored file unchanged.
"""

from __future__ import annotations

import json
import signal
import time


def capture(job: dict, h) -> dict:
    """job: code, inputs (LiveCodeBench strings), fn_name (None for stdin problems), lcb_timeout_s.
    h: the harness module (for canonical_repr and exception_token)."""
    import testing_util as tu

    code, inputs = job["code"], job["inputs"]
    fn_name, timeout = job.get("fn_name"), int(job["lcb_timeout_s"])
    signal.signal(signal.SIGALRM, tu.timeout_handler)
    tu.reliability_guard()
    res: dict = {"load_error": None, "load_status": None, "tests": [], "outputs": []}

    def token(e: BaseException) -> str:
        return "!Timeout" if type(e).__name__ == "TimeoutException" else h.exception_token(e)

    try:
        if fn_name:
            compiled = tu.compile_code(tu.import_string + "\n\n" + code, timeout)
            method = tu.get_function(compiled, fn_name)
        else:
            compiled = tu.compile_code(tu.make_function(tu.clean_if_name(code)), timeout)
            method = tu.get_function(compiled, "wrapped_function")
        if method is None:
            raise AttributeError("entry point not found")
    except BaseException as e:
        tok = token(e)
        res["load_error"] = tok
        res["load_status"] = "memory" if isinstance(e, MemoryError) else "exception"
        res["outputs"] = [tok] * len(inputs)
        return res

    for inp in inputs:
        t0 = time.perf_counter()
        status, tok, name = "pass", None, None
        signal.alarm(timeout)
        try:
            if fn_name:
                args = [json.loads(line) for line in inp.split("\n")]
                pred = method(*args)
                signal.alarm(0)
                if isinstance(pred, tuple):
                    pred = list(pred)
                tok = h.canonical_repr(pred)
            else:
                with tu.Capturing() as captured:
                    try:
                        tu.call_method(method, inp)
                    finally:
                        signal.alarm(0)
                tok = repr(h.normalize_stdout_text(captured[0]))
        except BaseException as e:
            signal.alarm(0)
            tok = token(e)
            name = tok
            status = "timeout" if tok == "!Timeout" else ("memory" if isinstance(e, MemoryError) else "exception")
        finally:
            signal.alarm(0)
        res["tests"].append({"s": status, "t": time.perf_counter() - t0, "e": name})
        res["outputs"].append(tok)
    return res
