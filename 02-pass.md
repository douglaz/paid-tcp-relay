# 02 — The pass

What is bought, what the key proves, what the relay remembers. Moved from tau-web's `CHN-15`,
`CHN-16`, `STG-18` and ADR 0025 on 2026-09-24; the decision and its rejected alternatives are
`ADR-0001`.

**PAS-1** Access is **bought, not granted** (`ADR-0001`). A holder asks the relay for access,
naming a relay key's public half; the relay answers `402` with a Lightning invoice over ordinary
HTTPS; the holder's own wallet pays it; the relay observes its own invoice settle and binds a
**pass** to that key. No email, no password, no reset flow, no identity: obtaining a pass MUST
require nothing the holder supplies beyond the key. The wire of the purchase is not in v1
(`F2`).

**PAS-2** A **relay key** is a secp256k1 keypair the holder chose or derived, one per purchase.
Its public half is what the relay binds a pass to; its private half signs the AUTH (`WIR-5`), a
destination record (`PAS-4`) and a revocation (`PAS-5`). The relay MUST NOT link two passes by
their keys, and MUST hold nothing that could. What it can link is the destination set
(`OPR-6`).

**PAS-3** A pass is the relay's record for one key: the destinations the key may reach, when
the pass expires, and how fast it may dial (`DST-3`). **The pass is what the relay remembers;
the key is what the holder proves.** Nothing bearer exists: there is no string a holder
presents, so there is nothing to store, leak or paste. A relay MUST refuse a key with no pass,
an expired pass, or a revoked pass with reason `pass` (`WIR-7`).

**PAS-4** A pass's **destination record is the authorization**, not a separate system. A pass
is bought before the destinations exist, so its record grows as the holder adds them; each
addition MUST carry the relay key's signature, so nobody but the key holder can widen a pass.
The record is read at the host and not at the port (`DST-2`). The recording message's wire is
not in v1 (`F2`); an operator MAY record by hand (`PAS-6`).

**PAS-5** Revocation is a message signed by the pass's key. A revoked pass MUST close its live
connections and refuse new ones immediately. What revocation protects is money and attribution:
`DST-2` says "For those eligible destinations, the relay's view MUST equal the world's": a
pass in the wrong hands reaches nothing the public internet does not; it spends the holder's paid quota and gets the
holder's pass blamed for the traffic. The revocation message's wire is not in v1 (`F2`).

**PAS-6** A relay operator MAY record a pass by hand — a key's public half, its destination set
and **an expiry** — for a holder enrolled out of band. A hand-recorded pass MUST NOT be
unbounded, and every other rule applies to it unchanged: `WIR-6` runs the same checks, and
`DST-4` refuses the same addresses. Hand recording is how a consumer's first stage enrols
before the purchase flow exists; it is not a second access system.

**PAS-7** A relay that serves only its own operator MAY charge nobody; `PAS-1`'s purchase then
does not arise, and the operator records passes under `PAS-6`. Payment is a property of a relay
offered to others, not of the protocol.

**PAS-8** A pass's expiry and its number of recorded destinations are bounds the relay's
operator sets and MUST publish to holders before purchase, so a holder knows what a pass buys.
The default figures are `bundle/timing.toml`'s (`OPR-7`); the destination cap's figure is `F5`.

**PAS-9** **/v2/ retirement and removal.** A hand-removed pass is retired, distinct from a
PAS-5 signed revocation. Under `/v2/`, revocation, retirement and reaching the recorded expiry
MUST terminate all affected pending and live connections immediately under WIR-12. Removing
a destination from a pass MUST do the same for that host on every port. There is no grace
period or wait for the next payload or handshake. New attempts are refused by WIR-6's pass
or destination check. Hand removal does not demonstrate the signed revocation exchange.

**PAS-10** **/v2/ edit acknowledgment.** An edit MUST be acknowledged only when the running
relay reports its inclusion in authoritative
state. Writing a configuration store or receiving deployment-tool apply success is insufficient;
a failed reload MUST NOT acknowledge success. No particular reload transport or administrative
protocol is selected here.
