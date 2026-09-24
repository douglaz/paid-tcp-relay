# 06 — Open findings

What a builder must know before building: the design questions this set has not settled and
who settles each. Findings are numbered `F1`… in the order they were carried in; the number is
stable and never reused, and a finding that closes is marked CLOSED in place. This document
records design state only, never what an implementation has built (`OVR-5`).

**F1. OPEN — a destination behind a host that connects outbound only.** (`OVR-3`, `DST-4`,
`WIR-1`; lnrent `F43`, its ADR 0028, `DMP-40`.) lnrent's Buyer reaches a rented unit at a private
address on a hosting Box that opens connections outbound only and exposes nothing public. v1
dials only public unicast (`DST-4`), so no v1 destination names such a unit. Carried in from
lnrent's `F43`, which asked for "the instance-addressed destination and the owner-signature
check" as one protocol revision, and "how a relay run by the publisher learns a Subscription's
owner without holding lnrent's books". Under this set's model the second question changes
shape: the relay never learns an owner from anyone's books; it learns a pass. What is undecided
is (a) a second destination kind — an endpoint the hosting Box registers over an outbound
connection to the relay, addressed by an identifier the relay assigns and the consumer
delivers to its user (lnrent's `instance` member) — and (b) who buys and records: whether the
consumer's operator holds the pass and records the Buyer's key against the unit's endpoint, or
the Buyer buys a pass and the operator records the endpoint against it. Both require the
recording message of `F2`. lnrent's `PRV-37` states what lnrent supplies — the Buyer's key, the
unit, and when the grant ends — and waits on this.

**F2. OPEN — the purchase, recording and revocation messages.** (`PAS-1`, `PAS-4`, `PAS-5`,
`WIR-11`.) v1 carries the handshake only. The `402` exchange, the signed recording message and
the signed revocation message have a described shape and no wire: no paths, no bodies, no
error answers, no fixtures. Until they land, every pass is hand-recorded (`PAS-6`) and the purchase, recording and revocation items of `05-conformance-checklist.md` cannot be
demonstrated end to end.

**F3. OPEN — multiplexing.** (`WIR-11`.) One WebSocket carries one TCP stream. A consumer that
opens several sessions to one destination opens several sockets, each paying the handshake and
counting against pacing. Whether v2 multiplexes, and how pacing counts a multiplexed socket, is
undecided.

**F4. OPEN — the formal companion.** (`WIR-6`, `WIR-10`, `DST-4`, `DST-5`.) tau-web's Lean
companion carries the v1 handshake as a state machine and the destination pipeline as typed
stages — `TauWeb.Relay` under tau-web `tools/formal/`, tagged to tau-web's `CHN-15`, `CHN-16`
and `CHN-16a`, with `docs/design/relay-witnesses-v1.json` as its witness file. The theorems
are this set's properties: no dial before the AUTH is accepted, no byte before OK, the dialer
receives only an admitted address, a replayed AUTH is refused. The module moves here when this
set grows a formal layer; until then tau-web's index is the proof of record and this set's
prose is authoritative. tau-web's `TASKS.md` carries the port.

**F5. OPEN — the destination cap's figure.** (`PAS-8`, `DST-3`.) A pass's recorded destinations
are "capped in number" and no number is named anywhere. The cap is an anti-abuse bound of the
same family as pacing, so it belongs in `bundle/timing.toml` with a rationale; the figure is
undecided.

**F6. OPEN — a rentable relay.** (`OPR-3`, `PAS-7`.) tau-web's ADR 0019 kept "a rentable relay
remains a candidate lnrent tenant for later": a relay sold as a service through lnrent's
marketplace, paid by hold invoice like any other Listing. Whether a pass can be an lnrent
Listing, and what that does to `PAS-1`'s `402` flow, is undecided and not a v1 question.
