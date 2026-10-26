# 0005 — Operated-path privacy and explicit environment exclusions

**Status:** accepted 2026-10-26. Rules: OPR-5, PAS-9, DST-2–DST-4, DST-7 and their
conformance items.

## Decisions

The owner selected "Keep no history". For the retained-state policy, see OPR-5:
"Event-derived values may exist only as in-memory current-window pacing state and MUST NOT
be exported to a collector or store." Shared hosting does not move an operated collector
outside the relay operator's control. For restart admission and its demonstration, see DST-3
and CNF-13.

The owner selected "The relay refuses them itself". For optional `/v2/` hosting-profile
environment exclusions, see DST-4: "Exclusions cover whole destination hosts, never selected
ports, and MUST be limited to hosting/environment targets, never unrelated public destinations."
For eligibility and unavailable coverage, see DST-2. Consumer-specific environment coverage
belongs in that consumer.

For the shared egress recommendation and adopted-barrier declarations, see DST-7:
"A private resolver TCP/53 route usable by that identity is outside the independent-denial
guarantee; it MUST NOT be described as universal denial or made safe merely by calling it DNS."
A consumer owns its stronger hosting admission and any precisely declared resolver exception.

## Revision and consumers

WIR-3 says "A revision that changes a frame, a reason string, a close code or the check order
is a new prefix, never a mutation of `/v1/`." WIR-6 check 5 reads
"**address** — `DST-4` admits the address;". The environment set is a configurable predicate
evaluated there; for the refusal, see WIR-7. Frames, reasons, close codes, check order and pass
records are unchanged; no new prefix is required. The new optional predicate is confined to
`/v2/`; `/v1/` does not acquire it. For the container self-address inventory, see DST-4:
"Other public cluster workloads are not
automatically the relay's own host; their exclusion is an explicit profile choice."

Consumer review inputs: tau-web CHN-15, CHN-11 and ARC-41 at
`f13e9d277945b885dc23220df626b9adf97c5eac`; lnrent VMH-19, SEC-38, its delivery protocol
and ADR 0028 at `5c01250933854de236e24e954c2db3132b0764af`. For consumer adoption, see those
owners; for the deferred destination kind, see F1. This amendment selects no new lnrent
profile and defines no private-unit addressing.

## Alternatives and evidence

Retained aggregates would expand retained state. Enrollment alone would not supply the selected
relay-side refusal for environment targets. A path-based definition of every public cluster
workload as the relay host was not selected. For unavailable coverage, see DST-2;
for external-route migration, see OPR-4.

For executable suites, record ownership and observation points, see the Evidence records
section of `05-conformance-checklist.md`.
