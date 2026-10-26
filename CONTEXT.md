# CONTEXT

The glossary for `paid-tcp-relay`. One context. A term is defined once here and used with that
meaning in every document; a document that needs a term this file lacks is a document that
found a gap.

## Language

**Relay**:
This product: an authenticated WebSocket-to-TCP relay that dials one destination per connection
for a holder who proved a key with a pass, and carries raw bytes both ways (`OVR-1`, `OVR-2`).
"The relay" always means this.
_Avoid_: bridge (the older tau-web word), proxy (it is not an open one, `OPR-1`), tunnel
(what runs inside the bytes is the consumer's), "the relay" for a Nostr relay (see below)

**Nostr relay**:
A relay in the Nostr sense: a WebSocket server that stores and serves events. Not this product.
A consumer may run one on the same host and under the same operator as the relay; the two
share nothing else. Always called this, in full (`OVR-4`).

**Holder**:
Whoever holds a relay key's private half. In tau-web this is the harness's operator; in lnrent
it may be the Buyer or the Operator (`F1`). The relay knows a holder only as a key.
_Avoid_: user, account, operator (which of two)

**Relay key**:
A secp256k1 keypair, one per purchase, whose public half the relay binds a pass to and whose
private half signs the AUTH, a destination record and a revocation (`PAS-2`). How the holder
derives it is the holder's; tau-web derives one per pass from its seed.
_Avoid_: credential, token, "the npub"

**Pass**:
The relay's record for one relay key: recorded destinations, expiry, pacing (`PAS-3`). What
is bought (`PAS-1`) or hand-recorded (`PAS-6`). The relay remembers it; the holder never
holds it. Nothing bearer.
_Avoid_: token, ticket, session, subscription (lnrent's word for something else)

**Destination**:
A host and a port a connection asks for, in the URL path (`WIR-1`). Recording is at the host;
eligibility and ports have their homes in `DST-4` and `DST-2`.

**Destination record**:
The set of hosts recorded against a pass, each added under the relay key's signature
(`PAS-4`). The record is the authorization; there is no separate one.
_Avoid_: allowlist, ACL

**Pacing**:
The per-destination rate bound on dials: a minimum spacing and a windowed cap (`DST-3`), named
in `bundle/timing.toml`. The anti-abuse control that replaced a port restriction (`ADR-0003`).

**Relay operator**:
Whoever runs a relay: a consumer's publisher by default, a holder for themselves, or a third
party a holder chose (`OPR-3`, `ADR-0002`). Always named to the holder; learns the topology
(`OPR-6`).
_Avoid_: operator alone (lnrent's Operator sells units; tau-web's operator uses the harness)

**Publisher**:
The party that ships a consumer's software. In tau-web, the party that also runs the default
relay (`ADR-0002`).

**Consumer**:
A product whose users reach something through the relay and whose specification cites this
set: tau-web, lnrent (`OVR-3`). A consumer owns its destinations, its pins, its trust
accounting and its users' keys; it owns no rule about what the relay does (`OVR-1`).
_Avoid_: tenant (tau-web's word for a different relationship), client (the software, not the
product)

**Registered endpoint**:
Proposed, not defined: a destination kind for a host that connects to the relay outbound and
registers what it serves, so a holder can reach something with no public address (`F1`).
Named here so the discussion has one word; nothing normative uses it yet.

**Pin**:
The consumer's out-of-band knowledge of the far end's key — an SSH host key, a TLS issuing
authority — checked inside the bytes, which is what makes the relay a carrier that can only
refuse service (`OVR-2`, `OPR-9`). The relay never holds or checks a pin.

**Reason**:
The one-word member of a refusal frame: `auth`, `pass`, `destination`, `address`, `pace`, or
`dial` (`WIR-7`). Closed set; a new reason is a new protocol revision (`WIR-3`).

**Publisher discovery key**:
The publisher's long-lived public signing identity for public relay announcements, separate from every holder's relay key (`WIR-14`, `OPR-10`).

**Discovery starting set**:
The consumer's compiled public Nostr endpoints for retrieving a publisher announcement. An announcement does not replace that set (`OPR-10`).

**Public base URL** / **alias**:
A relay service's canonical public `wss` origin followed by `/`, including a non-default public port where used (`WIR-14`). An alias is another configured public base for the same service and shared state (`OPR-10`); connection binding uses the base actually opened (`WIR-4`).

**Retirement**:
Administrative hand removal of a pass under `/v2/`, distinct from the holder-signed revocation
(`PAS-9`, `PAS-5`).
