# 0002 — A consumer's publisher operates its default relay; self-hosting is the destination; bring-your-own is the escape hatch

**Status:** accepted 2026-09-24, on creation of this set. Moved from tau-web's ADR 0019
(accepted, amended) and generalised from "the publisher" to "a consumer's publisher". Owner of
`OPR-3` and `OPR-4`.

## Decision

A consumer's default relay is operated by that consumer's **publisher**. The holder may point
their client at any other relay origin — bring-your-own — and the product actively offers the
move to a relay on the holder's own machine once one exists. The publisher's seat is a
**bootstrap**: before a holder has any machine, someone must carry the bytes that provision
the first one.

The relay is **direct-first** (`OPR-2`): never in a path the client can take alone, so minimum
usage is a design property.

Self-hosting has its own honest price, named rather than hidden: a relay cannot dial its own
addresses (`DST-4`), so the host that runs one still needs an external relay for its own
management, recovery and outside-in scans, and migration must retain and demonstrate that route
before switching the default (`OPR-4`). A single self-hosted relay does not end the dependency
on a relay run elsewhere.

## Why

Publisher-default adds no new *party* to a consumer's trusted set; it adds a new *capability*
to a party already trusted for the software itself, and a compromised software bundle can do
strictly more than a compromised relay. The honest statement is the capability, not a pretense
of neutrality: under the default the relay's trust entry reads "the publisher, twice: software
and relay", and it is defensible only while bring-your-own exists (`OPR-3`).

What the publisher additionally sees is the topology (`OPR-6`). It cannot read or alter a
session pinned out of band (`OVR-2`), so the addition is visibility, not authority over content;
but a party that serves the software *and* sees every connection is a bigger observer than one
that serves the software alone, and the consumer's trust accounting must say so.

## Rejected

**The holder self-hosts from the start.** Moves metadata visibility to the smallest set, and
contradicts a consumer whose audience cannot stand up a relay before the product has provisioned
anything for them. Kept as the destination, never the starting point.

**An independent third party.** Better on paper, and a real new trusted party; also a vacancy,
and naming a vacancy is not a decision. Bring-your-own leaves the door open for one.

**Decide later.** The operator question is load-bearing for a consumer's trust accounting now,
and an unrecorded arrangement hardens into the default by inertia.

## Consequences

- A consumer's trust display names the relay's operator, not just its existence (`OPR-3`,
  `OPR-6`).
- Bring-your-own is load-bearing: a consumer's content-security policy treats the relay origin
  as a configured value, never a constant.
- Relay redundancy under one operator is an availability move; an independently operated second
  relay is also a trust change and is priced as one.
- A self-hosted relay's host runs whatever else that host runs; a consumer whose host machines
  carry a model with box-plane reach must price that model as a metadata observer of what the
  relay retains, which `OPR-5` keeps to pass records only.
