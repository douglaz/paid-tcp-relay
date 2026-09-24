# 04 — Operation

Who runs the relay, what it retains, what it learns, and its timing. Moved from tau-web's
`CHN-8`, `CHN-10`, `CHN-11`, `CHN-13`, `CHN-14`, ADR 0019 and lnrent's `SEC-38` on
2026-09-24; the operator decision is `ADR-0002`.

**OPR-1** The relay MUST NOT be a generic open proxy. A WebSocket-to-arbitrary-TCP bridge with
no authentication is abused within days of being reachable. What makes this relay defensible is
the combination, never any one part: access is paid (`PAS-1`), a pass reaches only recorded
destinations (`DST-1`), capped in number (`PAS-8`), paced per destination (`DST-3`), and
revocable the moment abuse is seen (`PAS-5`). Payment alone does not satisfy this: a relay
forwarding wherever it is told is a paid proxy rather than an open one.

**OPR-2** The relay carries raw TCP only, and a consumer SHOULD be **direct-first**: the relay is
never in a path the client can take alone, and a consumer MUST NOT route through it a call the
client's own stack can make. What crosses the relay is what cannot go direct — a browser's SSH
session, a TLS session the browser terminates itself because the far end refuses browser
CORS — and minimum usage is a design property, not an accident.

**OPR-3** The relay's operator MUST be named to the holder. A consumer's default relay MAY be
run by that consumer's publisher (`ADR-0002`); a holder MAY run their own; a holder MAY point
their client at any other relay origin. A consumer that offers a publisher-run default MUST keep
bring-your-own available, because publisher-default is defensible only while the escape hatch
exists.

**OPR-4** A relay MUST NOT dial its own addresses (`DST-4`), so the host that runs a relay
still needs an external relay route for its own management, recovery and outside-in scans. A
consumer that moves a holder from a publisher-run relay to a self-hosted one MUST retain and
demonstrate that external route before switching the default, and MUST NOT relax `DST-4` to
make a migration appear complete. One self-hosted relay does not end the dependency on a relay
run elsewhere; the product says so rather than hiding it.

**OPR-5** The relay MUST keep no connection log. Which holder reached which destination and
when is the one thing a relay learns that the consumer's pin does not hide, and a host that
both serves the destination and records the approach holds a record nobody asked it to keep.
What the relay retains is its pass records (`PAS-3`) and the counters `DST-3` needs for the
current window; a relay on a host with other duties is that host's to declare, and the
declaration MUST list no retained connection record.

**OPR-6** The relay learns the **topology**: which key reached which destinations, when,
accumulated over time. A consumer MUST say so in its own trust accounting, naming the relay's
operator as a party that learns it, and MUST NOT call it merely "connection metadata". The relay
cannot read or alter a session pinned out of band, so the addition is visibility, not authority
over content; a party that also serves the consumer's software is a bigger observer than one
that serves the software alone. Per-purchase keys (`PAS-2`) bound what a key reveals; the
destination set correlates purchases anyway.

**OPR-7** Every cadence and timeout the relay enforces — `relay.auth_skew`, `relay.min_spacing`,
`relay.window`, `relay.window_cap` — lives in `bundle/timing.toml` by name, and a rule cites
the name. The numbers live only there; a value marked placeholder is replaced by the first
integrated run's measurement, in one commit.

**OPR-8** A relay MUST be reachable as `wss://` under a certificate a browser's own trust store
accepts, because a browser demands it; that is the one WebPKI certificate a consumer's
otherwise pinned deployment needs. The certificate authenticates the relay's origin to the
browser and nothing about the destination; the destination is authenticated inside the bytes by
the consumer's pin.

**OPR-9** Under out-of-band pinning a hostile relay is a denial of service and nothing worse.
A consumer whose client trusts a host key on first use has no such bound — at first contact a
hostile relay can present its own key, have it pinned, and read the session from then on — and
MUST say so wherever it offers first-use trust.
