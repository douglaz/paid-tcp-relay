#!/usr/bin/env python3
"""Fixture gate -- every JSON example in the set, fenced or standalone, is a test
input an implementation can load, not an illustration.

The wire chapter fixes the JSON profile (01-wire-protocol.md): a body is UTF-8 JSON with no duplicate object member at
any depth, and every JSON number is an integer within +/-(2^53-1) with no exponent
or fraction -- satoshi amounts, unix timestamps, counts and versions are all
integers.

The wire chapter also says fixtures carry real-shaped values: a Nostr event id or
pubkey is 64 lowercase hex characters, a Schnorr signature 128, a listing coordinate
is `30402:<64 hex>:<d>`, and a `...` placeholder inside an object is prohibited.

So this gate checks, for every fenced ```json block in the documents and every
file under fixtures/:

  * it parses
  * it contains no duplicate object member at any depth
  * every number is an integer within +/-(2^53-1)
  * it contains no `...` placeholder
  * event-id and pubkey fields are exactly 64 lowercase hex characters
  * signature fields are exactly 128 lowercase hex characters
  * `listing_id` fields are a 30402 coordinate over a 64-hex pubkey

It also structurally checks every ```mermaid block: a declared diagram type,
balanced brackets, balanced quotes. Mermaid renders on GitHub but there is no
offline parser here, so a broken diagram would look fine in source and fail in
the browser.

Ported from lnrent-spec on 2026-09-24 with the DM-catalogue rule removed: the
relay has three frames, all under fixtures/wire/.

Exit status 0 = clean, 1 = failures.
"""

import glob
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAX_INT = 2 ** 53 - 1
HEX32_FIELDS = {"event_id", "pubkey", "buyer_pubkey", "operator_pubkey",
                "master_pubkey", "op_pubkey", "host_op_pubkey", "sender_pubkey",
                "payment_hash"}
HEX64_FIELDS = {"sig"}
COORD_RE = re.compile(r"^30402:[0-9a-f]{64}:[^:\s]+$")

FENCE_RE = re.compile(r"^```json\s*\n(.*?)^```", re.M | re.S)


def no_duplicate_keys(pairs):
    seen = {}
    for k, v in pairs:
        if k in seen:
            raise ValueError(f"duplicate object member {k!r}")
        seen[k] = v
    return seen


def walk(node, path, problems):
    if isinstance(node, dict):
        # A Nostr event's `id` is a 32-byte hash; a DM request `id` is a client string.
        is_event = "kind" in node and "sig" in node
        for k, v in node.items():
            if k == "id" and is_event and not (isinstance(v, str) and re.fullmatch(r"[0-9a-f]{64}", v)):
                problems.append(f"{path}.id: event id must be exactly 64 lowercase hex chars")
            walk(v, f"{path}.{k}", problems)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            walk(v, f"{path}[{i}]", problems)
    elif isinstance(node, bool):
        pass
    elif isinstance(node, int):
        if abs(node) > MAX_INT:
            problems.append(f"{path}: integer {node} exceeds 2^53-1")
    elif isinstance(node, float):
        problems.append(f"{path}: non-integer number {node}")
    elif isinstance(node, str):
        leaf = path.rsplit(".", 1)[-1].split("[", 1)[0]
        if leaf in HEX32_FIELDS and not re.fullmatch(r"[0-9a-f]{64}", node):
            problems.append(f"{path}: {leaf} must be exactly 64 lowercase hex chars")
        if leaf in HEX64_FIELDS and not re.fullmatch(r"[0-9a-f]{128}", node):
            problems.append(f"{path}: {leaf} must be exactly 128 lowercase hex chars")
        if leaf == "listing_id" and not COORD_RE.match(node):
            problems.append(f"{path}: listing_id must be a 30402:<64 hex>:<d> coordinate")


MERMAID_RE = re.compile(r"^```mermaid\s*\n(.*?)^```", re.M | re.S)
MERMAID_KINDS = (
    "flowchart", "graph", "sequenceDiagram", "stateDiagram-v2", "stateDiagram",
    "erDiagram", "classDiagram", "journey", "gantt", "pie", "mindmap", "timeline",
)


def check_mermaid():
    """A structural sanity check, not a parser: a block that declares no diagram
    type, and unbalanced brackets or quotes in a label."""
    problems = 0
    count = 0
    for f in sorted(glob.glob("*.md")) + sorted(glob.glob("docs/adr/*.md")):
        text = open(f).read()
        for m in MERMAID_RE.finditer(text):
            count += 1
            line = text[: m.start()].count("\n") + 1
            body = m.group(1)
            first = next((l.strip() for l in body.splitlines() if l.strip()), "")
            if not first.startswith(MERMAID_KINDS):
                print(f"FAIL {f}:{line}: mermaid block declares no known diagram "
                      f"type (starts {first[:40]!r})")
                problems += 1
            pairs = [("[", "]"), ("(", ")")]
            if not first.startswith("erDiagram"):
                pairs.append(("{", "}"))
            for open_c, close_c in pairs:
                if body.count(open_c) != body.count(close_c):
                    print(f"FAIL {f}:{line}: unbalanced {open_c}{close_c} "
                          f"({body.count(open_c)} vs {body.count(close_c)})")
                    problems += 1
            if body.count('"') % 2:
                print(f"FAIL {f}:{line}: odd number of double quotes")
                problems += 1
    print(f"mermaid diagrams checked: {count} | failures: {problems}")
    return problems


def check_json(body, where):
    if "..." in body:
        print(f"FAIL {where}: contains a `...` placeholder")
        return 1, None
    try:
        doc = json.loads(body, object_pairs_hook=no_duplicate_keys)
    except ValueError as e:
        print(f"FAIL {where}: {e}")
        return 1, None
    problems = []
    walk(doc, "$", problems)
    for p in problems:
        print(f"FAIL {where}: {p}")
    return len(problems), doc


def main():
    os.chdir(ROOT)
    mermaid_failures = check_mermaid()
    failures = 0
    blocks = 0
    standalone_types = set()

    files = sorted(glob.glob("fixtures/**/*.json", recursive=True))
    for f in files:
        blocks += 1
        n, doc = check_json(open(f).read(), f)
        failures += n
        if isinstance(doc, dict) and isinstance(doc.get("type"), str):
            standalone_types.add(doc["type"])

    for f in sorted(glob.glob("*.md")) + sorted(glob.glob("docs/adr/*.md")):
        text = open(f).read()
        for i, m in enumerate(FENCE_RE.finditer(text), 1):
            blocks += 1
            line = text[: m.start()].count("\n") + 1
            n, doc = check_json(m.group(1), f"{f}:{line} (json block {i})")
            failures += n

    print(f"json fixtures checked: {blocks} ({len(files)} standalone) | failures: {failures}")
    return 1 if (failures or mermaid_failures) else 0


if __name__ == "__main__":
    sys.exit(main())
