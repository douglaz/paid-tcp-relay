# 0003 — A recorded destination is reachable on any port; pacing replaces the port restriction

**Status:** accepted 2026-09-24, on creation of this set. Moved from the first amendment of
tau-web's ADR 0025. Owner of `DST-2` and `DST-3`.

## Decision

A pass reaches an eligible recorded destination on **any port**, not on the SSH port alone, and
**per-destination pacing** carries the anti-abuse weight the port restriction used to. The
narrowing that keeps `OPR-1` true is: recorded destinations only, capped in number, paced per
destination, billed, revocable.

## Why

The port restriction was written without checking it against a consumer that probes which
ports answer through this same relay — tau-web's outside-in surface scan. Every probe that scan
exists to send was a probe the restriction refused. Worse than the contradiction: a relay
forwarding port 22 and nothing else shows the scanner exactly one open port on every machine
whatever the machine's firewall does, so the scan would confirm the consumer's own hardening
declaration by construction. A check that cannot fail is worse than no check, because no check
is visibly absent.

It also broke the equality the no-access argument needs. A consumer's firewall must not
privilege the relay's source addresses, so the relay-side view is never **larger** than the
world's; the port restriction made it **smaller**. The argument needs equality, and only one side
had been written down.

## What this gives up

The relay cannot verify that a recorded destination belongs to the holder (`DST-8`). Every
scan target being the holder's own machine is an assumption, not an enforcement — weaker than
the rule it replaces. The residual is bounded economically: a pass buys a capped, paced,
revocable, billed view of a handful of addresses, and the same money rents a machine with none
of those limits. That is priced here so nobody mistakes it for a cryptographic bound.

## Consequences

- `DST-3`'s figures — minimum spacing, window, window cap — are named in `bundle/timing.toml`
  and are the anti-abuse control, not politeness.
- The destination cap's figure is still unnamed (`F5`).

## October 26 eligibility amendment

For the eligibility boundary and unavailable coverage, see DST-2 and DST-4; for the selected
environment-exclusion mechanism, see ADR-0005. The port decision continues to apply to eligible
destinations. An unavailable target is not evidence of its port surface.
