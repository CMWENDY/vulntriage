import base64
import pickle


def load_job(payload):
    """Restore a queued job submitted by a client."""
    raw = base64.b64decode(payload)
    return pickle.loads(raw)


def apply_rule(expression, value):
    """Evaluate a user-supplied filter expression."""
    return eval(expression)


def run_hook(source):
    exec(source)
