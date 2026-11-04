# Stage 3 verifier implementation supplied to the lab.
from lab import signature_ok, APPROVED_MEASUREMENT, MINIMUM_TCB


def verify(quote, current_nonce):
    if not signature_ok(quote):
        return False, "bad signature"
    if quote["nonce"] != current_nonce:
        return False, "nonce does not match the current challenge"
    if quote["measurement"][:8] != APPROVED_MEASUREMENT[:8]:
        return False, "measurement prefix does not match"
    if quote["tcb_version"] < MINIMUM_TCB:
        return False, "platform patch level is too old"
    return True, "all checks passed"