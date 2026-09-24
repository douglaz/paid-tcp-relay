# 0001 — Access is bought, not granted, and bound to a key

**Status:** accepted 2026-09-24, on creation of this set. Moved from tau-web's ADR 0025
(with its two amendments) with its amendments folded in; tau-web keeps its own
record of why it adopted the model. Owner of `PAS-1`–`PAS-5`.

## Decision

A holder obtains relay access by **paying for a pass**, not by holding an account. The relay
returns `402` with a Lightning invoice over ordinary HTTPS; the holder's own wallet pays it;
the relay observes its own invoice settle and binds a pass to the **public half of a relay
key** the holder named, one key per purchase. On connect the relay issues a challenge and the
holder signs it with the key, in the shape NIP-42 already defines. Recording a destination and
revoking are messages signed by the same key. **The pass is what the relay remembers; the key
is what the holder proves.** Nothing bearer exists.

No email, no password, no reset flow, no identity. Losing a key is not the relay's recovery
problem: a holder who can re-derive it keeps the pass, and one who cannot buys another.

## Why

The alternative is an account system, and an account system is a party that knows every holder
by name and can switch them off. Both known consumers exist to remove that kind of relationship
rather than acquire one: tau-web prices adding a trusted party as a change of the weight of a
schema migration, and lnrent's whole marketplace runs on Lightning with no registration.

The key binding replaced an opaque random string. The string could not be revoked after a lost
device, because with no account the relay had no way to recognise whoever asked; and anyone
holding it could widen the destination list. A signature answers both: revocation is a message
the key signs, and so is every record.

## Rejected

**L402**, the designed standard for this exact problem. Its scoping language is good and its
`402`-then-credential shape is kept. Rejected on four grounds, the third decisive: a browser
cannot run the challenge on a WebSocket upgrade, because the `WebSocket` constructor takes no
headers and a failed upgrade exposes no response; it wants a preimage this design does not have,
because the holder's own wallet pays and returns nothing to the client; its macaroon carries a
32-byte `token_id` the specification describes as a stable user identifier across rotations,
which is the linkability this product exists to avoid; and its main advantage, stateless
verification, is moot, because revocation is inherently stateful and the relay needs state for
settlement, abuse control and live-connection tracking anyway. The first objection does not
apply to a challenge that runs inside the socket after it opens, which is what NIP-42 does and
why it was borrowed.

**Ecash tokens** (Cashu). Best on payer privacy — each spend unlinkable, no persistent
identifier — and largely undone downstream, because the relay learns the topology regardless
(`OPR-6`); it also costs a mint, a new trusted party. Worth revisiting if the relay's metadata
exposure is ever closed.

**An account system.** Makes support, abuse response and revocation easier, and adds the
identity party this record exists to avoid.

**Issuing passes by hand forever.** Right for a first stage with one holder who is also the
publisher (`PAS-6`); wrong as the answer for a user base, because deferring twice is how a
stopgap hardens into the default.

## Consequences

- The relay needs to receive Lightning, and that is its operator's problem. A relay run by a
  holder for themselves charges nobody and no payment machinery arises (`PAS-7`).
- Payment does not by itself stop abuse; it raises its price and enables response. What narrows
  a paid relay to something defensible is `OPR-1`'s combination, of which payment is one part.
- Destinations are recorded as they come into existence, not at purchase (`PAS-4`), which is
  the moment the relay learns topology (`OPR-6`).
- Purchases are unlinkable by credential, because each pass has its own key (`PAS-2`). The
  destination set links them anyway.
- The purchase, recording and revocation messages have a shape and no wire (`F2`).
