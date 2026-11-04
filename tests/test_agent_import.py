import importlib
import sys


def test_import_does_not_require_api_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    sys.modules.pop("src.agent_v1", None)
    module = importlib.import_module("src.agent_v1")
    assert module._client is None
