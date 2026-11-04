# Stage 2 verifier implementation supplied to the lab.
from lab import signature_ok, APPROVED_MEASUREMENT, MINIMUM_TCB


def verify(quote, current_nonce):
    if not signature_ok(quote):
        return False, "bad signature"
    if quote["measurement"] != APPROVED_MEASUREMENT:
        return False, "measurement is not the approved workload"
    if quote["tcb_version"] < MINIMUM_TCB:
        return False, "platform patch level is too old"
    return True, "all checks passed"