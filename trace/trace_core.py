"""TRACE core: lightweight audit trail utilities.

Simple, readable implementation suitable for initial provenance capture and integration testing.
"""
from __future__ import annotations
import json
import os
import uuid
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional


@dataclass
class AuditRecord:
    event_id: str
    timestamp: str
    event_type: str
    author: Optional[str]
    payload: Dict[str, Any]

    def to_json(self) -> str:
        return json.dumps(asdict(self), ensure_ascii=False)


class Trace:
    """A minimal TRACE implementation that appends JSON-lines to a log file.

    Intended for provenance capture and basic verification.
    """

    def __init__(self, path: str = "trace/logs/trace.log"):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def record_event(self, event_type: str, payload: Dict[str, Any], author: Optional[str] = None) -> AuditRecord:
        """Record an event to the TRACE log and return the AuditRecord.

        The author may be supplied explicitly; if omitted, TRACE will attempt to read
        the GIT_AUTHOR_NAME or USER environment variables as a best-effort claim.
        """
        if author is None:
            author = os.environ.get("GIT_AUTHOR_NAME") or os.environ.get("USER") or "unknown"
        rec = AuditRecord(
            event_id=str(uuid.uuid4()),
            timestamp=datetime.utcnow().isoformat() + "Z",
            event_type=event_type,
            author=author,
            payload=payload,
        )
        with self.path.open("a", encoding="utf-8") as fh:
            fh.write(rec.to_json() + "\n")
        return rec

    def read_records(self):
        """Yield parsed AuditRecords from the log file."""
        if not self.path.exists():
            return
        with self.path.open("r", encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                    yield AuditRecord(**obj)
                except Exception:
                    # Bad record; skip in this minimal implementation
                    continue

    def verify_integrity(self) -> bool:
        """Basic verification: ensure every record contains required fields and timestamps are parseable.

        This is intentionally lightweight; future versions may add cryptographic signing/hashing.
        """
        for rec in self.read_records():
            if not rec.event_id or not rec.timestamp or not rec.event_type:
                return False
            # basic timestamp structure check
            try:
                datetime.fromisoformat(rec.timestamp.replace("Z", ""))
            except Exception:
                return False
        return True


if __name__ == "__main__":
    t = Trace()
    r = t.record_event("init", {"note": "TRACE initialized"}, author=os.environ.get("USER"))
    print("Recorded:", r.event_id)
