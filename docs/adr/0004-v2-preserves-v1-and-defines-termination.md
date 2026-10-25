# 0004 — /v2/ defines connection binding and termination; /v1/ is preserved

**Status:** accepted 2026-10-25. Rules: WIR-1, WIR-3–WIR-8, WIR-12–WIR-14, PAS-9,
DST-3 and OPR-10.

## Decision

The changed wire behavior uses `/v2/`, preserving `/v1/`. Each connection binds one public
base URL, including non-default public ports, byte for byte across challenge and AUTH.
Additional application data during dialing cancels the connection; endpoints discard data
of the wrong type or phase. Browser clients use the permitted application code 4002.
Normal EOF and observed TCP failures have distinct outcomes. AUTH and dialing have named
phase bounds; quiet healthy payload streams have no idle eviction.

Revocation, hand retirement, expiry and destination removal terminate affected pending and
live `/v2/` connections immediately. Hand retirement remains distinct from a signed
revocation. Pacing is consumed at dial initiation and is not refunded for a started failure
or cancellation. Publisher discovery has an independent signed format and does not change
holder pass identity or reset shared state across names.

## Alternatives

Mutating `/v1/` would violate the revision boundary. A browser cannot request close code
1002 through its application API. Payload-idle eviction would end healthy quiet terminals.
Counting an admitted but unstarted dial would consume a slot without a connection attempt.
A new URL cannot safely imply a new identity, a key migration or permission to forget limits.

## Consumer boundary

A consumer selects its profile explicitly and owns its discovery validity, trust accounting,
recovery format and pins. Existing `/v1/` consumers may retain that profile while reviewing
`/v2/` adoption; publishing this specification does not silently upgrade them.
