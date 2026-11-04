# Return (True, reason) to accept the quote, or (False, reason) to reject it.
from lab import signature_ok, APPROVED_MEASUREMENT, MINIMUM_TCB


def verify(quote, current_nonce):
    if not signature_ok(quote):
        return False, "bad signature"
    if quote["nonce"] != current_nonce:
        return False, "nonce does not match the current challenge"
    if quote["measurement"] != APPROVED_MEASUREMENT:
        return False, "measurement is not the approved workload"
    if quote["tcb_version"] < MINIMUM_TCB:
        return False, "platform patch level is too old"
    return True, "all checks passed"