import json
import logging
import os
from datetime import datetime
from typing import Optional

logger = logging.getLogger(__name__)

AUDIT_LOG_FILE = os.getenv("AUDIT_LOG_FILE", "logs/audit.log")

os.makedirs(os.path.dirname(AUDIT_LOG_FILE), exist_ok=True)

_audit_logger = logging.getLogger("audit")
if not _audit_logger.handlers:
    _handler = logging.FileHandler(AUDIT_LOG_FILE)
    _handler.setFormatter(logging.Formatter("%(message)s"))
    _audit_logger.addHandler(_handler)
    _audit_logger.setLevel(logging.INFO)
    _audit_logger.propagate = False


def _write(event: str, username: Optional[str], ip: Optional[str], detail: dict):
    record = {
        "ts": datetime.utcnow().isoformat() + "Z",
        "event": event,
        "user": username or "anonymous",
        "ip": ip or "unknown",
        **detail,
    }
    _audit_logger.info(json.dumps(record))


def log_login(username: str, ip: str, success: bool):
    _write("auth.login", username, ip, {"success": success})


def log_logout(username: str, ip: str):
    _write("auth.logout", username, ip, {})


def log_document_upload(username: str, ip: str, filename: str, doc_id: str, chunks: int):
    _write("document.upload", username, ip,
           {"filename": filename, "doc_id": doc_id, "chunks": chunks})


def log_document_delete(username: str, ip: str, doc_id: str):
    _write("document.delete", username, ip, {"doc_id": doc_id})


def log_query(username: str, ip: str, question: str, num_results: int, confidence: float):
    _write("rag.query", username, ip,
           {"question": question[:200], "num_results": num_results, "confidence": confidence})


def log_admin_action(username: str, ip: str, action: str, target: str):
    _write("admin.action", username, ip, {"action": action, "target": target})
