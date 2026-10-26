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
This duty covers successful sessions and failed attempts across every traffic-observation,
collection and retention component under the relay operator's control, including ingress/L4
forwarding, relay output/files, operated resolvers, node/network flow telemetry, error/debug/trace
channels, metric labels/exemplars/series, collectors, rotations and backups. Retained source-IP
and time records are connection records even when TLS hides the destination path. Joining
operated stores to reconstruct who reached what or when is also forbidden.

What the relay retains is its pass records (PAS-3), the in-memory current-window pacing state
permitted below and health data not derived from connection activity. The selected policy is
"Keep no history": retained health data MUST NOT include values derived from connection, dial,
refusal or byte-transfer events, including per-workload network/connection-tracking/flow series
collected by the hosting platform. Liveness, readiness, build identity, resource capacity and
certificate-expiry values not derived from those events MAY be retained. Event-derived values
may exist only as in-memory current-window pacing state and MUST NOT be exported to a
collector or store. For pacing across restart, see `DST-3`. Pass records are not permission to
retain connection history, including through public version history or indiscriminate backups.

The operator's declaration MUST name the actual operated traffic, collection and storage paths,
shared duties and observers outside its control, and list no operated retained connection
record. It never excuses a connection log under that control or claims control over a network
provider. Bounded inspections do not establish historical absence or future deployed silence.

**OPR-6** The relay learns the **topology**: which key reached which destinations, when,
accumulated over time. A consumer MUST say so in its own trust accounting, naming the relay's
operator as a party that learns it, and MUST NOT call it merely "connection metadata". The relay
cannot read or alter a session pinned out of band, so the addition is visibility, not authority
over content; a party that also serves the consumer's software is a bigger observer than one
that serves the software alone. Per-purchase keys (`PAS-2`) bound what a key reveals; the
destination set correlates purchases anyway.

**OPR-7** Every cadence, timeout and cap the relay enforces lives in
`bundle/timing.toml` by name, and its owning rule cites
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

**OPR-10** **Publisher announcement and moves.** An operator offering publisher-key discovery MUST publish WIR-14 with its long-lived publisher discovery key P, separate from every holder's relay key. The publisher MUST dedicate the WIR-14 event address to this schema and not reuse it for another application. It MUST mirror each current announcement, including an empty withdrawal, to every endpoint in the compiled discovery starting set required by the consumer. Those endpoints MUST serve the announcement publicly without the subscriber authenticating as P. The publisher MUST keep at least one independently hosted discovery endpoint usable across a TCP-service domain move and republish before the announcement expires. A compiled starting-set change requires a new consumer build; announcement content cannot change that starting set. Each newly issued replacement announcement, including an empty withdrawal or expiration renewal, MUST have a `created_at` strictly greater than every earlier announcement issued at this address, and an expiration no earlier than any announcement it supersedes. The publisher MUST NOT future-date an announcement to obtain that ordering. Retransmission mirrors the same signed event; extending its signed expiration requires a newly signed successor. These duties prevent timestamp-tie loss and a successor expiring before a still-valid predecessor; they do not prove that a reader has received the newest event.

Every listed TCP URL MUST be operated by the same operator and serve the same pass records, destination sets, expiry and retirement state, and current-window pacing state and safe admission barriers under DST-3. Concurrent aliases share that state; a domain move preserves it. A new URL never creates a new pass or resets a limit. If continuity cannot be maintained, the publisher MUST withdraw the default rather than advertise unrelated pass state. This duty does not require an old TCP URL to remain live. Discovery availability and what a fresh restore can establish remain bounded by the consumer's validity checks.
