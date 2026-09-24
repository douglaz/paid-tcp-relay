# AGENTS.md

Specifications only. `tools/` holds the gates that check them; `.github/workflows/` runs the same
script. Nothing that implements the relay belongs here. This set is written so that a relay, a
client library or a consumer's integration in any language can be checked against it without
reading any other repository; an implementation records its own status, roadmap and defects in
its own repository, against the identifiers here (`OVR-5`).

## Gates

`nix develop --command bash tools/check-all.sh`, before you start and again before you report
done. Run it unpiped — a pipe reports the pipeline's status, not the gate's, which is why
`check-all.sh` captures each exit code directly. Plain `bash tools/check-all.sh` works too; the
shell only pins the Python.

Green is evidence only because the workflow breaks a document on every run and asserts the gates
reject it — one negative-control step per gate that has one, and `.github/workflows/gates.yml`
holds the list rather than this sentence.

## Writing a requirement

The rule and the record are two edits with two different failure rates. Land the rule; write the
record after.

**Quote the sentence.** A claim about what another requirement says carries that requirement's own
words. `` `WIR-7` says "`OK` therefore means "authorized and connected"" `` is checkable; "`WIR-7`
forbids an early OK" is an assertion.

**Cite the owner.** One rule, one home; everywhere else points at it. This set exists because two
consumers each carried half of the relay's rules and drifted; a consumer cites a rule here by
identifier and never restates it (`OVR-1`). **Arguments have owners too** — re-explaining a rule
in a second document is how a second normative copy gets written.

**Cite the list; let it hold the number.** A count written into prose is wrong the first time either
end moves. Every cadence and cap lives in `bundle/timing.toml` by name; a rule cites the name
(`OPR-7`).

**No implementation status.** Nothing here says what is built. A requirement no implementation
satisfies is still a requirement; its gap is recorded in that implementation's repository.

**Completion:** every sentence asserting what another requirement says carries its quote, and every
list or count names its source instead of restating it.

## Consumers

tau-web and lnrent cite this set. A change here that alters a frame, a reason, a close code, the
check order or what a pass records is a new protocol revision (`WIR-3`) and both consumers'
pointers are checked against it before it lands. A consumer's own rules — its destinations, its
pins, its trust accounting — are theirs and are never edited from here.

## Agent skills

### Issue tracker

Beads (`br`), local-first in `.beads/`, committed with the specs, prefix `ptr`. See
`docs/agents/issue-tracker.md`. Findings in `06-open-findings.md` are not beads.

### Triage labels

The five default roles as `br` labels. See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: `CONTEXT.md` and `docs/adr/` at the root. See `docs/agents/domain.md`.

## Conventions with a home already

- Identifiers, withdrawn ids → `README.md`, *Requirement conventions*.
- Vocabulary, overloaded and banned words → `CONTEXT.md`.
- Decisions and what was rejected to reach them → `docs/adr/`.
- What an implementation must demonstrate → `05-conformance-checklist.md`.
- What is still undecided → `06-open-findings.md`.
- The wire fixtures every implementation loads → `fixtures/wire/`.
- Every cadence and cap, by name → `bundle/timing.toml`.
