import os

# Cloud credentials
AWS_ACCESS_KEY_ID = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"

# This one is done correctly, for contrast
DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///staff.db")

DEBUG = True