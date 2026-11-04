from lab import signature_ok, APPROVED_MEASUREMENT


def verify(quote, expected_nonce):
    if not signature_ok(quote):
        return False, "invalid signature"

    if quote["measurement"] != APPROVED_MEASUREMENT:
        return False, "invalid measurement"

    if quote["tcb_version"] == 6:
        return True, "legacy TCB accepted"

    if quote["nonce"] != expected_nonce:
        return False, "replay detected"

    return True, "valid quote"