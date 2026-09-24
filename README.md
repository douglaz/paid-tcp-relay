# paid-tcp-relay

The specification of one product: an authenticated WebSocket-to-TCP relay whose access is
bought, not granted. A browser cannot open a TCP socket, so anything that reaches a machine
over SSH from a browser needs a bridge; this is that bridge, made defensible by paid,
key-bound, destination-recorded, paced, revocable passes rather than by an account.

It is written so that a relay, a client library, and a consumer's integration can each be built
in any language and checked against it without reading any other repository. Two consumers
cite it today: [tau-web](https://github.com/douglaz/tau-web-spec), whose browser harness
reaches the machines it provisions through it, and
[lnrent](https://github.com/douglaz/lnrent-spec), whose Buyers reach rented units through it.

**Specification only.** No implementation lives here. An implementation records its own status
and defects in its own repository, against the identifiers here.

## Start here

**[`00-overview.md`](./00-overview.md)** — what the relay is, what it never does, and the
reading order. Then, in order:

| | |
|---|---|
| [`01-wire-protocol.md`](./01-wire-protocol.md) | The URL, the three frames, the check order, the two invariants |
| [`02-pass.md`](./02-pass.md) | What is bought, what the key proves, what the relay remembers |
| [`03-destination-policy.md`](./03-destination-policy.md) | What a pass may reach, and what no pass ever reaches |
| [`04-operation.md`](./04-operation.md) | Who runs it, what it retains, what it learns, its timing |
| [`05-conformance-checklist.md`](./05-conformance-checklist.md) | What an implementation must demonstrate |
| [`06-open-findings.md`](./06-open-findings.md) | What is still undecided |

[`CONTEXT.md`](./CONTEXT.md) is the glossary. [`docs/adr/`](./docs/adr/) holds the decisions
and what was rejected to reach them. [`fixtures/wire/`](./fixtures/wire/) holds the handshake
frames every implementation loads. [`bundle/timing.toml`](./bundle/timing.toml) holds every
cadence and cap by name.

## Decisions

| ADR | Decision |
|---|---|
| `0001` | Access is bought, not granted, and bound to a relay key; nothing bearer exists |
| `0002` | A consumer's publisher operates its default relay; self-hosting is the destination; bring-your-own is the escape hatch |
| `0003` | A recorded destination is reachable on any port; per-destination pacing replaces the port restriction |

## Where this came from

On 2026-09-24 the relay's rules were carved out of two consumers that had each been carrying
half of one protocol, and the relay became a product of its own:

- **tau-web** contributed the wire protocol (`docs/design/relay-protocol-v1.md`), the pass
  model and destination policy (`CHN-8`, `CHN-10`, `CHN-11`, `CHN-13`–`CHN-16a`), the
  decisions (its ADRs 0019 and 0025) and its conformance items 57–60, 65, 76, 81 and 87. Its Lean companion `TauWeb.Relay` still carries the v1 handshake
  and destination pipeline (`F4`).
- **lnrent** contributed the admission rule for a rented unit and the no-logging rule
  (its ADR 0028, `VMH-19`, `SEC-38`, `PRV-37`) and the open question of a destination behind a
  Box that connects outbound only (`F43`, now `F1` here).

Each consumer's set now keeps a one-line pointer where a moved rule stood, and cites this set by
identifier for what the relay does.

## Gates

`nix develop --command bash tools/check-all.sh` runs every gate: identifiers (append-only,
dangling, gaps, ADR references), fixtures (JSON profile, hex ids), obligations (a duty
assigned to another requirement), coverage (requirements exercised by `CNF` items),
citations (a quoted claim about what another requirement says). Run it unpiped.
`.github/workflows/gates.yml` runs the same script and then breaks a document on purpose, once
per gate, to prove each gate can fail.

## Requirement conventions

Requirements use RFC 2119 keywords: **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT**, **MAY**.
Each is tagged with a stable identifier so it can be cited in code review, tests and issue
trackers:

| Prefix | Domain |
|---|---|
| `OVR-n` | Overview and scope |
| `WIR-n` | The wire protocol |
| `PAS-n` | The pass |
| `DST-n` | Destination policy |
| `OPR-n` | Operation |
| `CNF-n` | Conformance checklist items |

Findings in `06-open-findings.md` are `F1`… and are not requirements. Their numbers are
append-only too; a finding that closes is marked CLOSED in place, never renumbered.

### Identifiers are append-only. Text is not.

An identifier, once minted, is never reused and never renumbered. The text behind it may be
rewritten wholesale — the identifier names the rule's *place*, not its wording — and git keeps
the history. A rule that stops applying is withdrawn: deleted from the document and listed
below so an older citation still resolves.

### Withdrawn identifiers

Deleted from the documents. Never reused. Listed so an older citation still resolves.

| Identifier | Was | Why it went |
|---|---|---|
