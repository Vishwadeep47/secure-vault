"""TOTP (authenticator app) helpers."""
import pyotp


def new_secret():
    return pyotp.random_base32()


def provisioning_uri(secret, username, issuer="SecureVault"):
    return pyotp.TOTP(secret).provisioning_uri(name=username, issuer_name=issuer)


def verify_code(secret, code):
    code = (code or "").strip()
    if not (code.isdigit() and len(code) == 6):
        return False
    return pyotp.TOTP(secret).verify(code, valid_window=1)
