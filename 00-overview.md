# 00 — Overview

`paid-tcp-relay` is one product: an authenticated WebSocket-to-TCP relay whose access is
bought, not granted. A client that cannot open a raw TCP socket — a browser — opens a
WebSocket to the relay, proves it holds a key the relay has sold a pass to, and the relay
dials one TCP destination and carries bytes both ways. The relay never sees plaintext: whatever
runs inside the bytes — SSH under a pinned host key, TLS terminated at the client — is the
consumer's, and the pin is what makes the relay untrusted.

This set was carved out of two consumers on 2026-09-24. tau-web carried the wire protocol, the
pass model and the destination policy (`CHN-8`–`CHN-16a`, `docs/design/relay-protocol-v1.md`,
its ADRs 0019 and 0025, its conformance items 57–60, 65, 76, 81 and 87); lnrent
carried the admission rule for a rented unit and the no-logging rule (its ADR 0028, `VMH-19`,
`SEC-38`, `PRV-37`, `F43`). Each had half of one protocol. Both now cite this set.

**OVR-1** The relay is a product on its own, and this set owns every rule about what the relay
does. A consumer set MUST cite a rule here by identifier and MUST NOT restate it. What a
consumer owns is its own use of the relay: which destinations it records against a pass, what
it carries inside the bytes, whom its users must trust for running the relay, and the pins that
make the relay untrusted.

**OVR-2** The relay carries raw TCP and nothing else. It never terminates the protocol inside
the bytes, never holds a key that could, and never sees plaintext when the consumer pins the
far end (`WIR-9`). Confidentiality, integrity and endpoint identity are the consumer's pin's to
supply; what a hostile relay can do is refuse service and observe metadata (`OPR-5`).

**OVR-3** Two consumers are known and their destinations differ in kind. tau-web reaches
machines its operator provisions at public unicast addresses, which is the only destination
kind v1 dials (`DST-4`). lnrent's Buyer reaches a rented unit at a private address behind a
hosting Box that opens connections outbound only; that destination kind is `F1` and is not in
v1. A consumer MUST NOT claim conformance for a destination kind this set does not define.

**OVR-4** "The relay" in this set means the TCP bridge. A Nostr relay is a different service —
a consumer may run one on the same host and under the same operator — and is always called
that, in full (`CONTEXT.md`).

**OVR-5** Nothing in this set says what is built. An implementation's status, roadmap and
defects are recorded in that implementation's repository against the identifiers here. A
requirement no implementation satisfies is still a requirement.

**OVR-6** Every surface a second implementation must match — the WebSocket URL grammar, the
three handshake frames, the refusal reasons and close codes, and what a pass records — MUST be
reproducible from `01-wire-protocol.md`, `02-pass.md` and `fixtures/` alone. Interoperability
between a relay, a client library and a consumer rests on those; nothing else here is required
for two implementations to interoperate.

## Reading order

| | |
|---|---|
| [`01-wire-protocol.md`](./01-wire-protocol.md) | The URL, the three frames, the check order, the two invariants |
| [`02-pass.md`](./02-pass.md) | What is bought, what the key proves, what the relay remembers |
| [`03-destination-policy.md`](./03-destination-policy.md) | What a pass may reach, and what no pass ever reaches |
| [`04-operation.md`](./04-operation.md) | Who runs it, what it retains, what it learns, and its timing |
| [`05-conformance-checklist.md`](./05-conformance-checklist.md) | What an implementation must demonstrate |
| [`06-open-findings.md`](./06-open-findings.md) | What is still undecided, and who settles it |
