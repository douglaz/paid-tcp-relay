# 05 — Conformance checklist

What an implementation must demonstrate before it sells a pass. Each item names the
requirement it proves and is written so it can become a test. Moved from tau-web's conformance items
57, 58, 59, 60, 65, 76, 81 and 87 on 2026-09-24, with
lnrent's `SEC-38` logging clause; tau-web's numbering is not preserved.

## Evidence records

The checklist and fixtures define demonstrations and data, not an executable suite. The relay
implementation owns its executable conformance suite and record; a consumer integration owns
its separate client-observable record against the live public base. Each record MUST identify
the specification revision/profile, implementation commit, build inputs/artifact digest,
intended/effective configuration digest as applicable, exact commands/status, cases, controls,
observation points and exclusions.

Keep source/static intent, isolated executable results, isolated network enforcement,
effective deployment inspection with bounded controlled canaries, and live-public-base client
results distinct. Local results do not discharge deployment/live assertions. A live record MUST
cite a deployment record binding its public base to the running artifact digest and effective
configuration; equality of source commits alone is insufficient. Reference correctly bound
records rather than repeating an assertion at an observation point that cannot establish it.
For every required assertion, record passing evidence at its required observation point or an
explicit pending status and named admission blocker. Missing mandatory deployment/live evidence
blocks the relevant admission; local results may still be recorded honestly.

Changes to the effective image, network path/policy, capture/collection components, address
inventory, TLS or relevant retained state invalidate affected deployment evidence and require
re-demonstration. Test instrumentation MUST be confined to synthetic traffic. Retained bounded
verdict/configuration/control records MUST NOT contain real-holder topology.

## Build and gate

- [ ] **CNF-1** The implementation builds from a clean checkout with pinned dependencies and no
      network-dependent manual step. (`OVR-5`)
- [ ] **CNF-2** Every gate below fails when the property it guards is deliberately broken —
      verified once, by hand, so that a green run means something. (`OVR-5`)

## The handshake

- [ ] **CNF-3** Under `/v1/`, a connection receives a fresh challenge; an unknown key, a replayed signature, a
      mismatched destination tag, an unparseable path and an unserved prefix are each refused
      with the stated reason and close code before any dial; the order challenge, AUTH, OK holds;
      a binary frame before OK or a text frame after it closes the socket with 1002; a failed
      dial answers `dial` with 1011 and no OK. (`WIR-1`, `WIR-2`, `WIR-3`, `WIR-4`, `WIR-5`,
      `WIR-6`, `WIR-7`, `WIR-8`, `WIR-9`)

      Under `/v2/`, exercise the same handshake and admission refusals. `WIR-8` says
      "A receiver MUST discard text data after OK or binary data before OK and terminate the
      connection" and "The relay and a client whose API permits it use code 1002; a browser
      application client uses 4002". Demonstrate each direction and confirm discarded data
      never reaches the stream consumer.
      Control frames and fragmented binary messages remain usable. Send extra client text and
      binary data during a delayed accepted-AUTH dial: no OK or bytes, 1002, dial cancellation
      and late-success closure (WIR-12). Exercise both an unstarted cancellation and a started
      failed/cancelled dial against DST-3's pacing counters, including concurrent attempts.

      Demonstrate normal TCP EOF and write-half-close draining already-read bytes before 1000;
      reset and read/write failures closing 1011; client Close with and without a code; and no
      half-open surviving stream. Do not demand a sent reserved code or infer `wasClean` from
      the code. Policy termination does not drain queued bytes. Bound AUTH and delayed dialing
      with the named WIR-13 values, observing the corresponding JSON refusal, close and no OK;
      late dial success remains closed. A healthy payload-quiet connection is not idle-evicted.
      (`WIR-12`, `WIR-13`, `DST-3`)

      Under `/v2/`, verify WIR-4, WIR-5 and WIR-6 URL binding using two configured aliases. A connection opened under each alias receives that alias as its advertised public base, and matching AUTH succeeds. AUTH for another alias is refused as auth/1008 before dialing. A client receiving a challenge whose relay differs from its dialed base sends no AUTH; the browser closes with 4002. Include a non-default public port and WHATWG default-port elision.
- [ ] **CNF-4** **No dial happens before the AUTH is accepted**, verified by watching the relay's
      outbound connections during a refused AUTH; and **no application byte is forwarded before
      OK**, verified by sending bytes before OK and observing that none reach the destination.
      Two tests, not one. The outbound-initiation observer MUST detect a deliberately early
      attempt even if no destination accepts it; an empty destination listener or a client
      refusal/timeout is not that observation. Include a positive destination-byte observation
      control separately. (`WIR-10`)
- [ ] **CNF-5** The fixtures under `fixtures/wire/` load as the frames `01-wire-protocol.md`
      defines, and the AUTH fixture's signature verifies for its `pubkey`. (`WIR-4`, `WIR-5`,
      `WIR-7`, `OVR-6`)
      Verify the signed events in `fixtures/discovery/` against WIR-14 as well, including
      their event ids and signatures and empty withdrawal. (`WIR-14`)

## Access

- [ ] **CNF-6** An unpaid caller is refused. The relay is not usable without a valid, unexpired,
      unrevoked pass bound to the key that signs the challenge: verified with a key that has no
      pass, one whose pass has expired, one whose pass is revoked, and a correct key with a
      replayed challenge signature, each refused; an unauthenticated open to an arbitrary
      destination is refused before any dial. (`PAS-1`, `PAS-3`, `WIR-6`, `OPR-1`)
- [ ] **CNF-7** Obtaining a pass requires no account, no email address and no identifier the
      holder supplies beyond a public key: verified by buying one end to end without contacting
      the operator, and by buying two and confirming the relay holds nothing that links their
      keys. (`PAS-1`, `PAS-2`)
- [ ] **CNF-8** Recording a destination against a pass requires that pass's key's signature:
      verified by submitting a destination without one and with another key's, both refused.
      (`PAS-4`)
- [ ] **CNF-9** A revoked pass stops working immediately, including on a connection already
      open: verified by revoking — a message signed by the pass's key — while a session is live
      and confirming the socket closes and a reconnect is refused. Under `/v2/`, also retire
      a pass by hand and remove a destination while dialing and after OK, including a quiet
      connection and late dial success. Observe immediate terminal state, no further bytes or
      OK, 1008 with `pass` or `destination`, pre-OK refusal JSON and no post-OK JSON. Removal of
      a host affects every port and leaves unrelated destinations usable. Hand retirement does
      not count as the signed-revocation demonstration. Check running authoritative-state
      acknowledgments for retirement/removal, failed reload refusal to acknowledge, cancelled
      pending work and unchanged unrelated destinations; store/apply success is insufficient.
      (`PAS-5`, `PAS-9`, `PAS-10`, `WIR-12`)
- [ ] **CNF-10** A hand-recorded pass carries an expiry and is refused after it, and obeys every
      other check unchanged. Under `/v2/`, reach expiry during a pending dial and an open quiet
      session: apply WIR-12 immediately, retain started-dial pacing, and refuse reconnects.
      (`PAS-6`, `PAS-7`, `PAS-9`, `WIR-12`)
- [ ] **CNF-11** The pass's expiry and destination cap are published to a holder before
      purchase. (`PAS-8`)

## Destinations

- [ ] **CNF-12** A pass reaches only the destinations recorded against it and eligible under
      DST-4, on **any** port: verified by attempting an undeclared destination on the SSH port and on another, both
      refused, and a recorded destination on a non-SSH port, which succeeds. (`DST-1`, `DST-2`)
- [ ] **CNF-13** Dials to a recorded destination are paced: verified by driving a probe tool
      flat out at one destination and measuring the rate the relay actually allows against
      `relay.min_spacing`, `relay.window` and `relay.window_cap`, including clock/window
      boundaries. Under `/v2/`, cover initiation accounting, concurrent attempts and
      failed/cancelled initiated dials. For every served profile, restart, concurrent replicas,
      aliases and domain moves do not refund or multiply either bound; losing in-memory counters
      refuses conservatively until safe. Inspect expiration of old state and backups without
      retaining past-window history. (`DST-3`, `OPR-5`, `OPR-7`, `OPR-10`)
- [ ] **CNF-14** A recorded destination cannot reach relay-private services: loopback,
      private and link-local IPv4 and IPv6, metadata endpoints, IPv4-mapped IPv6, alternate
      numeric spellings and the relay host's own addresses are refused, at registration and on
      every dial. Include assigned pod/workload, underlying node and service/public front-door
      addresses in both families, missing/stale/incomplete inventories, and an inventory change
      before a queued dial starts. Under `/v2/`, also exercise adopted environment-exclusion
      sets, including public addresses and DNS answers, whole-host refusal across ports and
      unrelated public positive controls. An excluded target is unavailable coverage, not a
      successful scan or closed-port result. A public DNS name changing to a private address,
      mixed public and private answers, and retries are each refused; the dialer uses only the
      validated numeric address; valid public SSH and other-port destinations remain reachable. Application-policy
      demonstrations are unconditional. Separately demonstrate independent firewall enforcement
      where adopted or required by a consumer; explicitly record omissions otherwise. In an
      isolated enforcement setup, bypass the application guard and attempt forbidden, self and
      adopted environment routes in both families, with public SSH and other-port controls.
      Attempt declared infrastructure endpoints and neighboring addresses/ports to verify exact
      coverage, recording whether the connector identity can use each exception. A private
      resolver TCP/53 exception is independently undenied, never a universal-denial pass.
      Deliberately opening a forbidden rule must be detected. Local namespace/firewall evidence
      covers that setup, not a future deployment's enforcement, host exceptions or routing/NAT.
      Effective deployment inventory and enforcement require their own bound evidence.
      (`DST-2`, `DST-4`, `DST-5`, `DST-6`, `DST-7`)
- [ ] **CNF-15** A relay offered for self-hosting refuses a migration that would leave its host
      without an external relay route, verified by attempting one. (`OPR-4`)

## Operation

- [ ] **CNF-16** The relay retains no connection log or connection-derived metric history:
      inspect every declared operated observation, collection and retention sink and downstream
      copy after synthetic successful, refused and sparse single-attempt traffic. Include
      operated resolver/L4/host collectors, source-IP/time-only records, labels, exemplars,
      successive samples, joins, rotations and backups. Find only OPR-5-permitted state;
      event-derived current-window pacing values stay in memory and are not exported or
      persisted. Deliberately enabling any retained event-derived metric, an event record or
      a reconstructing series must fail the check, even without identifying labels. Declare
      outside observers separately. Static and isolated checks do not certify historical absence or deployment silence; inspect the
      effective deployed operated path separately. (`OPR-5`)
- [ ] **CNF-17** The relay carries a pinned session as ciphertext and can read nothing of it:
      verified by inspecting what the relay observes for a tunnelled session. (`OVR-2`, `WIR-9`)
- [ ] **CNF-18** The relay is not reachable by a client whose stack could make the call itself,
      and a consumer's documentation names the relay's operator and what it learns. (`OPR-2`,
      `OPR-3`, `OPR-6`)
- [ ] **CNF-19** The relay answers `wss://` under a browser-accepted certificate, and a plain
      `ws://` origin is refused. (`OPR-8`)
- [ ] **CNF-20** A consumer offering first-use trust states the hostile-relay residual where it
      offers it. (`OPR-9`, `OVR-1`, `OVR-3`, `OVR-4`)

- [ ] **CNF-21** Where OPR-10 discovery is offered, fetch and verify its public WIR-14 event anonymously, including from the independently hosted mirror; demonstrate a domain move or concurrent aliases preserving pass, destination, expiry, retirement and pacing state. Verify that each replacement withdrawal and expiration renewal advances `created_at` without future-dating, that no successor expires before a superseded announcement, and that a withdrawal is publicly retrievable. Exercise the consumer's expiration refusal without claiming a permanent remote tombstone. (`WIR-14`, `OPR-10`)
