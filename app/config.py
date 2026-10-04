"""Central settings. Change limits here, not inside the code."""
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))


class Config:
    # Storage
    DB_PATH = os.environ.get("VAULT_DB", os.path.join(BASE_DIR, "securevault.db"))
    SECRETS_DIR = os.environ.get("VAULT_SECRETS_DIR", os.path.join(BASE_DIR, ".secrets"))

    # Login protection
    MAX_FAILED_LOGINS = 5
    LOCKOUT_SECONDS = 300

    # Sessions
    TOKEN_MINUTES = 15

    # Account rules
    MIN_PASSWORD_LEN = 10
    MAX_PASSWORD_LEN = 128

    # Vault notes
    NOTE_TITLE_MAX = 200
    NOTE_CONTENT_MAX = 20000

    # Upload size cap (used later for the image vault)
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024
