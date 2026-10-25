# Protocol vectors

`wire/*.json` retains the original `/v1/` frame vectors byte for byte.
`wire/v2/` contains paired challenge and signed AUTH vectors for two public aliases;
the alternate alias includes a non-default public port. Append
`v2/tcp/203.0.113.10/22` to the selected base for the request. The documentation destination
is a shape vector, not an address admitted by DST-4 or a live deployment input.

`discovery/` contains signed WIR-14 events from a separate deterministic publisher key:
`listed.json`, then `withdrawn.json`, then `renewed.json` in strictly increasing timestamp
order with nondecreasing expiration. They are historical signature/schema inputs, not
currently valid announcements or bundle defaults. Consumer tests control their clocks.
Use the complete signed events for ordering and recovery checks; an empty URL array is a
withdrawal, not a fallback instruction.

`python3 tools/gen_fixtures.py` reproduces these files. Conformance demonstrations under
CNF-3, CNF-5 and CNF-21 supply the refusal, timing, transport and deployment observations;
these static vectors alone do not demonstrate those behaviors.
