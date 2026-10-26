# 0005 — Operated-path privacy and explicit environment exclusions

**Status:** accepted 2026-10-26. Rules: OPR-5, PAS-9, DST-2–DST-4, DST-7 and their
conformance items.

## Decisions

The owner selected "Keep no history". OPR-5 owns the retained-state policy; deployment on a
shared host does not move an operated collector outside the relay operator's duties.
Persistent usage metrics are not an additional permitted store. The restart consequence and
continuity checks have their homes in DST-3 and CNF-13.

The owner selected "The relay refuses them itself". DST-4 owns optional `/v2/` hosting-profile
environment exclusions, and DST-2 owns eligibility and unavailable coverage. The rule excludes
whole environment targets; it does not allow unrelated public targets or a chosen port subset
to disappear from a scan. Consumer-specific environment coverage belongs in that consumer.

DST-7 keeps the shared recommendation and owns declarations of an adopted independent barrier.
A consumer owns its stronger hosting admission and any precisely declared resolver exception;
a connector-usable private resolver TCP/53 route remains outside the second wall.

## Revision and consumers

WIR-3 says "A revision that changes a frame, a reason string, a close code or the check order
is a new prefix, never a mutation of `/v1/`." The environment set is a configurable predicate
within the existing WIR-6 address check, using its existing refusal. Frames, reasons, close
codes, check order and pass records are unchanged; no new prefix is required. The new optional
predicate is confined to `/v2/`; `/v1/` does not acquire it. The container self-address inventory
makes the existing host boundary explicit, rather than classifying every cluster public address
as self.

Consumer review: tau-web selects `/v2/` at CHN-15 and adopts environment coverage in CHN-11;
its pin and ARC-41 eligibility boundary change in its consumer amendment. lnrent's VMH-19,
SEC-38 and relay references in its delivery protocol and ADR 0028 still leave private-unit
addressing to F1. This amendment does not define that deferred kind, select a new profile for
lnrent, or silently admit private units through the public-unicast relay.

## Alternatives and evidence

Retained aggregates would expand retained state. Enrollment alone would not supply the selected
relay-side refusal for environment targets. A path-based definition of every public cluster
workload as the relay host was not selected. An exclusion is visible unavailability, never
proof of the public port surface. Existing external-route migration duties remain at OPR-4.

Executable suites and status belong to implementations. The checklist distinguishes local,
deployment and live-client observations; source or fixture results cannot establish effective
routing, certificate handling, collector retention or the artifact behind a public base.
