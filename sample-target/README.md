Deliberately vulnerable code. **Do not run, install, or deploy anything in
this folder.**

This is test data for the VulnTriage scanner. Every file here contains a
known insecure pattern on purpose, and `requirements.txt` pins package
versions with published CVEs.

`cache.py` and `tests/test_helpers.py` look insecure but are not. They are
there to measure the scanner's false positives.

Do not run `pip install -r sample-target/requirements.txt`.