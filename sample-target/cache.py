import hashlib


def cache_key(url, params):
    """Build a stable lookup key for a cached HTTP response."""
    raw = url + repr(sorted(params.items()))
    return hashlib.md5(raw.encode()).hexdigest()


def etag_for(content):
    return hashlib.md5(content).hexdigest()
