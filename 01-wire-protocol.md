# 01 — The wire protocol

Three messages, then bytes. Moved from tau-web's `docs/design/relay-protocol-v1.md` on
2026-09-24, where it was the normative companion to `CHN-15`, `CHN-16`, `CHN-16a` and its conformance item 87.
The frames under `fixtures/wire/` are the byte-level contract.

## Profiles

The original `/v1/` profile is preserved. The `/v2/` profile uses the unchanged rules below
except where a requirement explicitly selects `/v2/` behavior. WIR-12 and WIR-13 apply only
to `/v2/`; WIR-14 defines optional public discovery independently of the wire revision.
A client chooses its revision explicitly; there is no automatic revision downgrade.

## The destination

**WIR-1** The destination rides in the WebSocket URL path: `wss://<relay>/v1/tcp/<host>/<port>`.
`host` is a DNS name — lowercase, IDNA A-labels, no trailing dot — or a numeric address in
canonical text form: dotted-decimal IPv4, or RFC 5952 IPv6 without brackets. Nothing else: no
percent-decoding, no scope identifiers, no alternate numeric spellings. `port` is a strict
decimal integer, 1–65535, no leading zeros.
For `/v2/` the path is `wss://<relay>/v2/tcp/<host>/<port>`, with the same host and port grammar.
Its public base URL has WIR-14's form, including a non-default public port where configured.

**WIR-2** A path that does not parse under `WIR-1` MUST be refused before any other check, with
close code 1008. There is one grammar, so the authorization check and the dialer cannot parse
the same string differently; after parsing, `DST-4`'s normalization and refusal rules run on the
result.

**WIR-3** The path prefix `/v1/` is the protocol revision. A relay MUST refuse a prefix it does
not serve with close code 1008 before any other check. A revision that changes a frame, a
reason string, a close code or the check order is a new prefix, never a mutation of `/v1/`.
The `/v2/` prefix selects this set's second profile; serving it does not mutate or remove `/v1/`.

## The handshake

**WIR-4** On open, the relay MUST send one text frame, the **challenge**: a JSON object
`{"challenge": "<32 random bytes, base64url, no padding>", "relay": "<relay URL>"}`. The
challenge MUST be fresh per connection and never reused. For each `/v2/` connection the relay MUST select, from its configured public base URLs in WIR-14's URL form, the public base URL R under which that connection was opened, preserving any non-default public port, and copy R byte for byte into `relay`. R's authority MUST equal the externally requested authority after WHATWG origin serialization, including default-port elision. The mapping is configured for every served public authority and MUST NOT be inferred from the relay's listening socket or select another alias. Multiple served aliases do not enlarge that connection's accepted AUTH names.

**WIR-5** The client MUST answer with one text frame, the **AUTH**: a NIP-42-shaped Nostr event
signed by the relay key (`PAS-2`): `kind` 22242; tags `["relay", "<relay URL>"]`,
`["challenge", "<challenge>"]`, `["destination", "<host>", "<port>"]`; `created_at` within
`relay.auth_skew` (`bundle/timing.toml`) of the relay's clock; `id` the NIP-01 event id;
`sig` a BIP-340 signature over it. The destination tag MUST equal the URL path.

For `/v2/`, the AUTH `relay` tag MUST equal the challenge's `relay` byte for byte. Before sending AUTH, a client MUST require the challenge's `relay` to equal the public base URL it dialed. On mismatch it MUST send no AUTH and terminate; a browser application client uses close code 4002.

**WIR-6** The relay MUST run these checks, in this order, and stop at the first failure:

1. **shape** — `kind` is 22242, the `relay` tag names this relay, `created_at` is within skew,
   exactly one `destination` tag and it equals the path. For `/v2/`, the shape check is:
   `kind` is 22242, exactly one `relay` tag is present and its value equals this connection's
   configured public base URL R byte for byte, `created_at` is within skew, exactly one
   `destination` tag and it equals the path;
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

**WIR-8** For `/v1/`: after `OK`, every frame in both directions MUST be a binary frame carrying raw TCP. A
text frame after `OK`, or a binary frame before it, MUST close the connection with code 1002.
Either side closing the WebSocket closes the TCP connection.

For `/v2/`, after OK application data in both directions MUST be binary WebSocket messages
containing raw TCP. Control frames remain permitted and are not TCP payload. A receiver MUST
discard text data after OK or binary data before OK and terminate the connection. The relay
and a client whose API permits it use code 1002; a browser application client uses 4002.
Fragmentation does not change the application message type. Either side closing the WebSocket
closes the TCP connection; WIR-12 owns the other termination outcomes.

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

The same exclusions apply to `/v2/`: it does not add purchase, destination-recording or signed
revocation messages, multiplexing, additional address kinds or multiple-address dialing.

## /v2/ termination and deadlines

**WIR-12** Under `/v2/`, additional client application data received after accepted AUTH and
before OK MUST be discarded and close the WebSocket with code 1002, without a JSON refusal.
The relay MUST NOT send OK for that connection. It MUST cancel a pending dial and close a
late successful TCP connection without forwarding application bytes. An initiated dial
continues to count under DST-3 even if cancelled or failed; an unstarted dial consumes no slot.
This rule does not prohibit WebSocket control frames.
Every terminal outcome, including a client Close during dialing, cancels pending work and
closes a late successful TCP connection; the connection MUST NOT subsequently send OK.

TCP EOF, including a destination's write-half-close, terminates the whole relay connection;
the protocol has no separate half-close signal. On normal EOF, forward already-read TCP bytes
before sending Close with code 1000 and an empty reason. TCP reset and read/write errors close
with 1011 and an empty reason. A client needing write-EOF closes the WebSocket. A received
client Close is answered with its close code when present and an empty Close when absent;
never transmit the reserved observed values 1005 or 1006.

`PAS-9` says "Under `/v2/`, revocation, retirement and reaching the recorded expiry
MUST terminate all affected pending and live connections immediately under WIR-12".
For that policy termination, mark each affected pending or live connection terminal,
stop forwarding and discard queued payload, cancel pending dials and close late successful
connections. Serialize policy termination with dial initiation and OK transmission so a
terminal connection neither starts another dial nor sends OK. Close with 1008 and the UTF-8
Close reason `pass` for revocation, retirement or expiry, or `destination` for host removal.
Before OK, also send the WIR-7 refusal JSON with that reason; after OK, send no JSON into the
byte stream. A later policy termination is distinct from a failed admission check and does not
claim that an already initiated dial never happened. Policy termination and protocol violations
discard bytes; the normal-EOF drain does not apply to them.

These are sent Close outcomes, not delivery guarantees. A browser observes a code and reason
only if it receives that Close; an empty received Close is observed as 1005, and a lost transport
without one as 1006. The closing handshake determines `wasClean`; the chosen code alone does not.

**WIR-13** Under `/v2/`, enforce `relay.auth_timeout` from challenge transmission until receipt
of complete AUTH. If that deadline expires, send the WIR-7 `auth` refusal JSON and close with
1008 without dialing. Enforce `relay.dial_timeout` from accepted AUTH through OK transmission;
on expiry send the WIR-7 `dial` refusal JSON and close with 1011 without OK. Cancel a pending
dial and close a late successful connection without forwarding bytes. These bounds cover
unauthenticated occupancy and accepted-AUTH pending connection resources respectively; they
do not specify a DNS-admission deadline or an additional closing-handshake deadline.
The relay MUST NOT evict a connection merely for having no application payload; this profile
adds no payload-idle deadline or periodic ping requirement.

## Publisher discovery

**WIR-14** **Public relay announcement.** The announcement is a public NIP-01 addressable event with application-defined kind `30079`, publisher public key P, and address `30079:P:paid-tcp-relays`. Kind `30079` is application-defined. It is not a standardized TCP-relay-list kind or a globally reserved number. The event MUST have exactly one `["d","paid-tcp-relays"]` tag and exactly one `["expiration","E"]` tag; E is unsigned decimal Unix seconds and MUST exceed `created_at`. Each required tag MUST have exactly two elements. An event with any other tag MUST be rejected. The content is a JSON string encoding exactly `{"version":1,"relays":[R,...]}`: `version` is integer 1 and `relays` is an ordered array of distinct strings. Reject duplicate JSON member names, extra members and wrong types. An empty array withdraws the publisher default.

Each R MUST equal the WHATWG URL serialization of a `wss` origin followed by `/`, with no credentials, other path, query or fragment. Non-default ports are permitted. R is the public base URL, not the complete WebSocket request URL; `/v2/` connections append `v2/tcp/<host>/<port>` to R. The event format version, wire prefix and consumer recovery-payload version are independent. NIP-01 supplies the signed event and addressability; the expiration tag follows NIP-40, with client validity and retained ordering owned by the consumer. NIP-65 Nostr read/write relay lists and NIP-78 private application data are not this public TCP-relay announcement.
