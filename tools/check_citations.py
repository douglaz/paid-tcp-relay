#!/usr/bin/env python3
"""Citation-attribution gate.

A requirement that reports what another requirement SAYS is making a checkable
claim about a specific span of text. On 2026-09-03 several of those claims were
false, in both directions: `WIR-20` and `WIR-35` attributed this set's
wire-contract precedence rule to `WIR-1`, which carries the JSON, money and
timestamp conventions and says nothing of the kind; `DOM-30` reported that
`WIR-30` forbids what `WIR-30` in fact mandates. Two full review passes at
`high` effort read past all of them. See `ddd3df0` and `254fc24`.

The other gates cannot see this class. `check_ids.py` is satisfied -- the
citation resolves to a real identifier. `check_obligations.py` is satisfied --
no duty is being assigned. The sentence reads fluently. Only the relationship
between the claim and the cited text is broken.

TWO RULES, deliberately narrow.

  QUOTED   A quoted phrase attributed to `X` must appear in X's own body.
           Hard failure: the quote either occurs there or it does not, so a
           finding is provable and needs no judgement.

  UNQUOTED "`X` says/states/reads ..." with no quote at all is unverifiable by
           construction. Ratcheted against `citation-baseline.json` rather than
           failed outright, because such sentences already exist and a gate that
           fails a clean tree is a gate someone deletes. New ones are refused;
           the standing ones come down as their requirements are next edited.
           The count lives in that file and nowhere else -- a number written
           into prose is wrong the first time either end moves, which this set
           has now learned in `ADR-0003`, `ADR-0011` and the blocking count.

Summary verbs are deliberately OUT OF SCOPE. "`OPS-12` forbids automatic retry"
is a correct, useful paraphrase, and most attributions in the set are of that
shape. Demanding a quote there would fire on legitimate prose, which is how a
checklist item ends up unsatisfiable by every conforming implementation
(`CNF-224`).

WHAT THIS DOES NOT CATCH, stated plainly because a gate's limits are part of its
contract: a wrong SUMMARY. "`WIR-30` forbids the server resolving eligibility
that way" reverses `WIR-30`'s meaning, uses a summary verb, and carries no
quote -- no lexical signal separates it from a correct summary. That one was the
worst defect of 2026-09-03 and it stays a review problem.

Exit 0 = clean, 1 = an unverifiable quote or a rise above the baseline.
"""

import glob
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASELINE = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        "citation-baseline.json")
NS = "OVR|WIR|PAS|DST|OPR|CNF"

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from check_obligations import bodies  # noqa: E402  -- one span-splitter, not two

# Direct-speech attribution only. Summary verbs (forbids, requires, mandates,
# calls, makes) are out of scope by design -- see the module docstring.
#
# Two shapes, because the 2026-09-03 miscitations used one each: the verb form
# ("`WIR-1` says ...") and the possessive form ("`WIR-1`'s rule that ..."), which
# claims what a requirement contains just as directly.
SPEECH = r"says|said|states|stated|reads|read"
NOUN = r"rule|claim|wording|statement|sentence|words|text"
ATTRIB = re.compile(
    r"`((?:%s)-\d+[a-z]?)`(?:'s)?\s+(?:own\s+)?(%s)\b"
    r"|`((?:%s)-\d+[a-z]?)`'s\s+(?:own\s+)?(%s)\s+that\b" % (NS, SPEECH, NS, NOUN)
)

# "reads" is two verbs. "`WIR-9` reads \"...\"" attributes text; "`LDG-74` reads
# it" and "`LDG-38` reads both from this record" mean CONSULTS, and consulting
# never carries a quote -- so the unquoted rule would fire on every one of them.
# Checked when a quote is present, ignored when one is not.
CONSULTS = {"reads", "read"}
# A bullet whose items end in ";" is one sentence to any splitter, which lets
# one item's attribution collect the next item's quote. Break on list markers
# and blank lines as well as sentence enders.
SPLIT = re.compile(r"(?<=[.!?])\s+|\n\s*[-*]\s+|\n\s*\n|\n(?=\|)")

# Paired quotes only. An unpaired quote character makes every span between two
# of them look like a quotation, which reports the prose BETWEEN two real
# quotes as a failed one.
QUOTE = re.compile(r'“([^”]{8,400})”|"((?:[^"\n]|\n(?!\s*\n)){8,400})"')
DOC = re.compile(r"`(\d\d-[a-z-]+\.md|README\.md|CONTEXT\.md|AGENTS\.md|executive-summary\.md)`")

# A quotation of wording that was deliberately removed cannot be found in the
# body, and this set retains such quotations on purpose (README, "Identifiers
# are append-only. Text is not."). Recognise the sentence, do not check it.
HISTORICAL = re.compile(
    r"withdraw|withdrew|until 20|previously|the original|first draft|old (?:item|text|wording)"
    r"|earlier (?:draft|version|text|wording|revision|note|phrasing)|stood (?:here|there)"
    r"|used to|no longer|superseded|retired|amended|version one|version two|rewritten"
    r"|this said|it said|it read|had said|once (?:said|read|contained)|corrected|described it as|merged into|split into|the claim that did not",
    re.I,
)

# A document teaching this rule must be able to show the mistake it forbids.
TEACHING = re.compile(r"is an assertion|is a claim, and|checkable;|for example", re.I)


def norm(s):
    s = (s.replace("“", '"').replace("”", '"')
          .replace("’", "'").replace("‘", "'")
          .replace("—", "-").replace("–", "-"))
    s = re.sub(r"[*`~]", "", s)
    return re.sub(r"\s+", " ", s).lower().strip(" .,;:")


def load(rev=None):
    os.chdir(ROOT)
    def read(f):
        if rev:
            return subprocess.run(["git", "show", f"{rev}:{f}"],
                                  capture_output=True, text=True).stdout
        return open(f).read()
    docs = {f: read(f) for f in sorted(glob.glob("*.md"))}
    adr = " ".join(read(f) for f in sorted(glob.glob("docs/adr/*.md")))
    reqs = {}
    for f, t in docs.items():
        for k, v in bodies(t).items():
            reqs.setdefault(k, (f, v))
    return docs, adr, reqs


def find(docs, adr, reqs):
    """Return (unverified_quotes, unquoted_attributions)."""
    bad, unquoted = [], []
    nadr = norm(adr)
    for f, text in docs.items():
        for sent in SPLIT.split(text):
            m = ATTRIB.search(sent)
            if not m or HISTORICAL.search(sent) or TEACHING.search(sent):
                continue
            rid = m.group(1) or m.group(3)
            verb = (m.group(2) or "").lower()
            quotes = [(qm.start(), qm.group(1) or qm.group(2))
                      for qm in QUOTE.finditer(sent)]
            # Only quotes AFTER the attribution verb: a quote earlier in the
            # chunk belongs to whatever introduced it, not to this attribution.
            # CNF-6's merge marker quotes its own withdrawn text and then
            # CNF-107's, in that order, in one chunk.
            quotes = [(p, q) for p, q in quotes
                      if len(norm(q).split()) >= 4 and p > m.start()]
            if not quotes:
                if verb not in CONSULTS:
                    unquoted.append((f, rid, " ".join(sent.split())[:100]))
                continue
            docpool = [norm(docs[d]) for d in DOC.findall(sent) if d in docs]
            for _pos, q in quotes:
                # The quote belongs to whoever the attribution verb attaches to,
                # NOT to the nearest citation before it: "`STO-43` says `STO-14`
                # 'reaches settled operations'" is STO-43's sentence about
                # STO-14, and blaming STO-14 for it inverts the claim. Bullet
                # lists are handled by SPLIT instead, which is where that
                # confusion actually came from.
                owner = rid
                pool = [norm(reqs[owner][1])] if owner in reqs else []
                pool += docpool + [nadr]
                frags = [x for x in
                         (p.strip() for p in re.split(r"\.\.\.|…", norm(q))) if x]
                if not any(all(fr in p for fr in frags) for p in pool):
                    bad.append((f, owner, norm(q)[:95]))
    return bad, unquoted


def main():
    docs, adr, reqs = load()
    bad, unquoted = find(docs, adr, reqs)
    for f, rid, q in bad:
        print(f"  {f} attributes to {rid} a phrase {rid} does not contain:")
        print(f'      "{q}"')
    if bad:
        print(f"\nFAIL: {len(bad)} unverifiable quoted attribution(s). Quote the "
              f"requirement's own words, or cite it without quoting.")
        return 1
    print(f"quoted attributions verified: clean")

    sigs = sorted({f"{f}:{rid}" for f, rid, _ in unquoted})
    try:
        base = set(json.load(open(BASELINE))["unquoted_attributions"])
    except Exception:
        base = set(sigs)
        json.dump({"unquoted_attributions": sigs,
                   "note": "Sentences reporting what a requirement SAYS with no quote to "
                           "check, as file:id signatures rather than a count -- a count "
                           "cannot name which one is new. Ratchet: may shrink, never grow."},
                  open(BASELINE, "w"), indent=2)
        print(f"baseline written: {len(sigs)} signature(s)")
    new = [x for x in sigs if x not in base]
    if new:
        for sig in new:
            f, rid = sig.split(":", 1)
            ex = next(s for g, r, s in unquoted if g == f and r == rid)
            print(f"  {f} reports what {rid} says without quoting it:")
            print(f"      {ex}")
        print(f"\nFAIL: {len(new)} new unquoted attribution(s). Carry the "
              f"requirement's own words, or use a summary verb and drop the claim "
              f"to report what it says.")
        return 1
    print(f"unquoted attributions: {len(sigs)}, none new against baseline {len(base)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
