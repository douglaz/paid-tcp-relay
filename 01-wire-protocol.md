# 01 — The wire protocol

Three messages, then bytes. Moved from tau-web's `docs/design/relay-protocol-v1.md` on
2026-09-24, where it was the normative companion to `CHN-15`, `CHN-16`, `CHN-16a` and its conformance item 87.
The frames under `fixtures/wire/` are the byte-level contract.

## The destination

**WIR-1** The destination rides in the WebSocket URL path: `wss://<relay>/v1/tcp/<host>/<port>`.
`host` is a DNS name — lowercase, IDNA A-labels, no trailing dot — or a numeric address in
canonical text form: dotted-decimal IPv4, or RFC 5952 IPv6 without brackets. Nothing else: no
percent-decoding, no scope identifiers, no alternate numeric spellings. `port` is a strict
decimal integer, 1–65535, no leading zeros.

**WIR-2** A path that does not parse under `WIR-1` MUST be refused before any other check, with
close code 1008. There is one grammar, so the authorization check and the dialer cannot parse
the same string differently; after parsing, `DST-4`'s normalization and refusal rules run on the
result.

**WIR-3** The path prefix `/v1/` is the protocol revision. A relay MUST refuse a prefix it does
not serve with close code 1008 before any other check. A revision that changes a frame, a
reason string, a close code or the check order is a new prefix, never a mutation of `/v1/`.

## The handshake

**WIR-4** On open, the relay MUST send one text frame, the **challenge**: a JSON object
`{"challenge": "<32 random bytes, base64url, no padding>", "relay": "<relay URL>"}`. The
challenge MUST be fresh per connection and never reused.

**WIR-5** The client MUST answer with one text frame, the **AUTH**: a NIP-42-shaped Nostr event
signed by the relay key (`PAS-2`): `kind` 22242; tags `["relay", "<relay URL>"]`,
`["challenge", "<challenge>"]`, `["destination", "<host>", "<port>"]`; `created_at` within
`relay.auth_skew` (`bundle/timing.toml`) of the relay's clock; `id` the NIP-01 event id;
`sig` a BIP-340 signature over it. The destination tag MUST equal the URL path.

**WIR-6** The relay MUST run these checks, in this order, and stop at the first failure:

1. **shape** — `kind` is 22242, the `relay` tag names this relay, `created_at` is within skew,
   exactly one `destination` tag and it equals the path;
2. **signature** — the signature verifies for the event's `pubkey`, and the `challenge` tag
   equals this connection's challenge;
3. **pass** — that key holds a pass that is unexpired and not revoked (`PAS-3`, `PAS-5`);
4. **destination** — the destination is in that pass's recorded set (`PAS-4`: the record is
   the authorization);
5. **address** — `DST-4` admits the address;
6. **pace** — the pass's pacing and window cap allow a dial now (`DST-3`).

**WIR-7** A failed check MUST produce one text frame `{"ok": false, "reason": "<reason>"}` and
close code 1008, **before any dial**, with `reason` one of `auth` (checks 1–2), `pass`,
`destination`, `address`, `pace`. When every check passes the relay dials, and once the TCP
connection is up sends one text frame `{"ok": true}`. A dial that fails after the checks passed
MUST produce `{"ok": false, "reason": "dial"}` and close code 1011. `OK` therefore means
"authorized and connected".

**WIR-8** After `OK`, every frame in both directions MUST be a binary frame carrying raw TCP. A
text frame after `OK`, or a binary frame before it, MUST close the connection with code 1002.
Either side closing the WebSocket closes the TCP connection.

**WIR-9** A replayed AUTH fails at `WIR-6` step 2, because its challenge is not this
connection's. The relay learns the destination and the key and nothing more: it never sees
plaintext, because the SSH or TLS session inside the bytes is pinned end to end by the
consumer (`OVR-2`).

## The two invariants

**WIR-10** Nothing MUST be dialed before the AUTH is accepted (`WIR-6` complete), and no
application byte MUST be forwarded before `OK` has been sent. These are two invariants, not one:
`OK` is sent *after* the dial succeeds, so "no dial before `OK`" names an order the protocol does
not have, and a relay and a test could each satisfy it while enforcing different things. The
shorthand was carried in tau-web until 2026-09-16 and is retained here only so nobody
re-derives it.

## Not in v1

**WIR-11** v1 does not carry: multiplexing several TCP streams over one socket (`F3`); a DNS
destination resolving to more than one address — v1 dials the first admitted answer and
refuses if any answer is forbidden (`DST-5`); the purchase, recording and revocation messages
of `PAS-1`, `PAS-4` and `PAS-5` (`F2`); and any destination kind but public unicast (`F1`).
