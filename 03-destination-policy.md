# 03 — Destination policy

What a pass may reach, and what no pass ever reaches. Moved from tau-web's `CHN-8`, `CHN-16`,
`CHN-16a` and ADR 0025's amendment on 2026-09-24; the any-port decision is `ADR-0003`.

**DST-1** A pass reaches only the destinations recorded against it (`PAS-4`). A destination not
in the record MUST be refused with reason `destination` (`WIR-7`) before any dial.

**DST-2** A recorded destination eligible under DST-4 is reachable on **any port**, never on
one port alone (`ADR-0003`). For those eligible destinations, the relay's view MUST equal the
world's: a relay that forwards only port 22 makes every machine behind it show exactly one open
port to a consumer that probes which ports answer, which is a check that cannot fail and is
worse than no check. The record is read at the host; the port is the holder's to choose per connection. A DST-4 exclusion
MUST be reported as unavailable coverage, never as closed ports or a successful outside-in
verification. Managing or scanning an excluded target requires an eligible external route;
no equal-view claim is available until that route is demonstrated.

**DST-3** Dials to a recorded destination MUST be **paced**: at least `relay.min_spacing`
between dials to one destination, and at most `relay.window_cap` dials to one destination per
`relay.window` (`bundle/timing.toml`, `OPR-7`). A dial the pace does not allow is refused with
reason `pace` (`WIR-7`). Under `/v2/`, consume the spacing and window slot atomically when
the dial starts, not when check 6 admits an unstarted reservation. Serialize concurrent
attempts at initiation so they cannot exceed either bound. Failed or cancelled initiated
dials are not refunded. Pacing is what makes a wide port range useless as a scanning service;
together with `DST-1`, a cap on the number of recorded destinations (`PAS-8`), payment (`PAS-1`)
and revocation (`PAS-5`), it is what keeps the relay from being the open proxy `OPR-1` forbids.

Restart MUST NOT refund consumed spacing or window capacity. `OPR-5` says "Event-derived values
may exist only as in-memory current-window pacing state and MUST NOT be exported to a
collector or store." When restart loses event-derived pacing state, refuse conservatively
until both bounds can be met. Concurrent replicas and OPR-10 aliases or domain
moves MUST NOT multiply or reset these limits. Discard event-derived state when its current
window no longer needs it; neither logs nor backups may preserve past-window dial history.

**DST-4** At registration and again on **every outbound connection**, the relay MUST accept
only public unicast destinations. It MUST refuse loopback, private, link-local, unspecified,
multicast, broadcast, documentation, reserved and every other non-global address in IPv4 and
IPv6, including metadata endpoints, IPv4-mapped IPv6 and alternate numeric spellings after
normalization, and MUST refuse every address belonging to the relay host itself, including its
public ones. Unknown address forms fail closed. The refusal is reason `address` (`WIR-7`).
Destination authorization never grants access to the relay's private network, and a
hand-recorded pass (`PAS-6`) obeys the same rule.

For a containerized relay, its own addresses include the assigned pod/workload addresses,
underlying node addresses and relay service/public front-door addresses, including public
addresses and both families. The effective self-address inventory MUST be complete and current
before accepting a registration or admitting a dial; missing, stale or incomplete knowledge fails closed with `address`.
Recheck against current inventory before a queued dial starts. An injected test inventory is
not evidence of deployed completeness.

Under `/v2/`, a consumer hosting profile MAY declare additional operated-environment addresses
or ranges forbidden, including public addresses. The relay MUST apply that set at registration
and every dial, including current inventory at queued dial initiation and all DST-5 answers,
with the existing `address` refusal. A required environment inventory that is missing, stale or
incomplete fails closed. Exclusions cover whole destination hosts, never selected ports, and
MUST be limited to hosting/environment targets, never unrelated public destinations. Other
public cluster workloads are not automatically the relay's own host; their exclusion is an
explicit profile choice. `WIR-6` check 5 reads "**address** — `DST-4` admits the address;".
Evaluate the configurable predicate there, with no change to frame, reason string, close code,
check order or pass record. `/v1/` gains no optional
environment-exclusion predicate.

**DST-5** For a DNS destination the relay MUST resolve through its own resolver, MUST refuse the
connection if **any** answer is forbidden by `DST-4`, and MUST connect to the checked numeric
address with no second resolution inside the dialer. The check applies to retries and to
refreshed DNS results; a redirect or an alternate target is a new destination requiring the same
authorization and the same check. v1 dials the first admitted answer (`WIR-11`).

**DST-6** The address tables the relay classifies by MUST be the IANA special-purpose address
registries, pinned at a stated revision; an update to them is a reviewed policy change, never
an unattended refresh.

**DST-7** The relay host SHOULD deny non-global, self and adopted profile-environment routes
at its egress firewall as defence in depth. For application destination checks, see DST-4.
A consumer MAY require this independent barrier for its own hosting profile.

An adopted barrier MUST declare effective coverage in both families, host/node exceptions,
routing/NAT and any permitted infrastructure flows by exact endpoint, protocol and port,
including whether the tunnel connector's network identity can use each flow. A private resolver
TCP/53 route usable by that identity is outside the independent-denial guarantee; it MUST NOT
be described as universal denial or made safe merely by calling it DNS. No broad private-subnet
or all-port exception qualifies as least-privilege infrastructure. Preserve arbitrary ports to
eligible public destinations. Desired policy objects alone do not establish enforcement.

**DST-8** The relay cannot verify that a recorded destination belongs to the holder, and is not
asked to. What bounds the residual is economic, and is stated so that nobody mistakes it for a
cryptographic bound: a pass buys a capped, paced, revocable, billed view of a handful of
addresses, where the same money rents a machine with none of those limits. A tool strictly
worse than what an attacker already has does not attract them.
