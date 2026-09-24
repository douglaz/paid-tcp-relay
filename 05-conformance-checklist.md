# 05 — Conformance checklist

What an implementation must demonstrate before it sells a pass. Each item names the
requirement it proves and is written so it can become a test. Moved from tau-web's conformance items
57, 58, 59, 60, 65, 76, 81 and 87 on 2026-09-24, with
lnrent's `SEC-38` logging clause; tau-web's numbering is not preserved.

## Build and gate

- [ ] **CNF-1** The implementation builds from a clean checkout with pinned dependencies and no
      network-dependent manual step. (`OVR-5`)
- [ ] **CNF-2** Every gate below fails when the property it guards is deliberately broken —
      verified once, by hand, so that a green run means something. (`OVR-5`)

## The handshake

- [ ] **CNF-3** A connection receives a fresh challenge; an unknown key, a replayed signature, a
      mismatched destination tag, an unparseable path and an unserved prefix are each refused
      with the stated reason and close code before any dial; the order challenge, AUTH, OK holds;
      a binary frame before OK or a text frame after it closes the socket with 1002; a failed
      dial answers `dial` with 1011 and no OK. (`WIR-1`, `WIR-2`, `WIR-3`, `WIR-4`, `WIR-5`,
      `WIR-6`, `WIR-7`, `WIR-8`, `WIR-9`)
- [ ] **CNF-4** **No dial happens before the AUTH is accepted**, verified by watching the relay's
      outbound connections during a refused AUTH; and **no application byte is forwarded before
      OK**, verified by sending bytes before OK and observing that none reach the destination.
      Two tests, not one. (`WIR-10`)
- [ ] **CNF-5** The fixtures under `fixtures/wire/` load as the frames `01-wire-protocol.md`
      defines, and the AUTH fixture's signature verifies for its `pubkey`. (`WIR-4`, `WIR-5`,
      `WIR-7`, `OVR-6`)

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
      and confirming the socket closes and a reconnect is refused. (`PAS-5`)
- [ ] **CNF-10** A hand-recorded pass carries an expiry and is refused after it, and obeys every
      other check unchanged. (`PAS-6`, `PAS-7`)
- [ ] **CNF-11** The pass's expiry and destination cap are published to a holder before
      purchase. (`PAS-8`)

## Destinations

- [ ] **CNF-12** A pass reaches only the destinations recorded against it, on **any** port:
      verified by attempting an undeclared destination on the SSH port and on another, both
      refused, and a recorded destination on a non-SSH port, which succeeds. (`DST-1`, `DST-2`)
- [ ] **CNF-13** Dials to a recorded destination are paced: verified by driving a probe tool
      flat out at one destination and measuring the rate the relay actually allows against
      `relay.min_spacing`, `relay.window` and `relay.window_cap`. (`DST-3`, `OPR-7`)
- [ ] **CNF-14** A recorded destination cannot reach relay-private services: loopback,
      private and link-local IPv4 and IPv6, metadata endpoints, IPv4-mapped IPv6, alternate
      numeric spellings and the relay host's own addresses are refused, at registration and on
      every dial; a public DNS name changing to a private address, mixed public and private
      answers, and retries are each refused; the dialer uses only the validated numeric address;
      a valid public SSH or TLS destination remains reachable; the host's egress firewall denies
      the same routes independently. (`DST-4`, `DST-5`, `DST-6`, `DST-7`)
- [ ] **CNF-15** A relay offered for self-hosting refuses a migration that would leave its host
      without an external relay route, verified by attempting one. (`OPR-4`)

## Operation

- [ ] **CNF-16** The relay retains no connection log: verified by inspecting what it persists
      after sessions, finding pass records and current-window counters and no record of who
      reached what. (`OPR-5`)
- [ ] **CNF-17** The relay carries a pinned session as ciphertext and can read nothing of it:
      verified by inspecting what the relay observes for a tunnelled session. (`OVR-2`, `WIR-9`)
- [ ] **CNF-18** The relay is not reachable by a client whose stack could make the call itself,
      and a consumer's documentation names the relay's operator and what it learns. (`OPR-2`,
      `OPR-3`, `OPR-6`)
- [ ] **CNF-19** The relay answers `wss://` under a browser-accepted certificate, and a plain
      `ws://` origin is refused. (`OPR-8`)
- [ ] **CNF-20** A consumer offering first-use trust states the hostile-relay residual where it
      offers it. (`OPR-9`, `OVR-1`, `OVR-3`, `OVR-4`)
