import os
import tempfile
from pathlib import Path

import pytest

from trace.trace_core import Trace


def test_trace_integration(tmp_path):
    # use a temporary log file so tests don't interfere with local state
    log_path = tmp_path / "trace.log"
    t = Trace(path=str(log_path))
    rec = t.record_event("test", {"x": 1}, author="test-author")
    assert rec.event_type == "test"
    assert log_path.exists()
    assert t.verify_integrity()


# End of contents
