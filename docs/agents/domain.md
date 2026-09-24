# Domain Docs

How the engineering skills should consume this repo's domain documentation when exploring it.

## Before exploring, read these

- **`CONTEXT.md`** at the repo root: the glossary, single context. "The relay" is the TCP
  bridge and a Nostr relay is always called that in full; "holder", "relay operator",
  "publisher" and "consumer" are four different parties.
- **`docs/adr/`**: `ADR-0001` (access is bought and key-bound) is what everything about the pass
  follows from; `ADR-0003` (any port, paced) is what the destination policy follows from;
  `ADR-0002` is who runs the relay.

## Use the glossary's vocabulary

When your output names a domain concept (in a bead title, a finding, a fixture name), use the
term as defined in `CONTEXT.md`. Don't drift to synonyms the glossary explicitly avoids, and
don't use a word from its banned list.

If the concept you need isn't in the glossary yet, that's a signal: either you're inventing
language the project doesn't use (reconsider) or there's a real gap (note it for
`/domain-modeling`).

## Flag ADR conflicts

If your output contradicts an existing ADR, surface it explicitly rather than silently
overriding:

> _Contradicts ADR-0001 (access is bought, key-bound), but worth reopening because…_
