#!/usr/bin/env python3
"""Regenerate fixtures/wire/ from one deterministic relay key.

The AUTH fixture is a real BIP-340 signature over a real NIP-01 event id, so CNF-5's
"the AUTH fixture's signature verifies for its pubkey" is a test, not a picture. Pure Python
secp256k1 -- slow and only for fixtures, never for a relay.

Deterministic: the key is SHA-256 of a fixed string, the aux randomness is zero, so a re-run
reproduces the committed bytes exactly. Run: python3 tools/gen_fixtures.py
"""
import hashlib, json, os

P = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
G = (0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798,
     0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8)


def add(a, b):
    if a is None: return b
    if b is None: return a
    if a[0] == b[0] and (a[1] + b[1]) % P == 0: return None
    if a == b:
        l = (3 * a[0] * a[0] * pow(2 * a[1], P - 2, P)) % P
    else:
        l = ((b[1] - a[1]) * pow(b[0] - a[0], P - 2, P)) % P
    x = (l * l - a[0] - b[0]) % P
    return (x, (l * (a[0] - x) - a[1]) % P)


def mul(k, pt):
    r = None
    while k:
        if k & 1: r = add(r, pt)
        pt = add(pt, pt); k >>= 1
    return r


def tagged(tag, *parts):
    t = hashlib.sha256(tag.encode()).digest()
    return hashlib.sha256(t + t + b"".join(parts)).digest()


def sign(d, msg):
    Pt = mul(d, G)
    if Pt[1] % 2: d = N - d
    pub = Pt[0].to_bytes(32, "big")
    t = (d ^ int.from_bytes(tagged("BIP0340/aux", bytes(32)), "big")).to_bytes(32, "big")
    k = int.from_bytes(tagged("BIP0340/nonce", t, pub, msg), "big") % N
    R = mul(k, G)
    if R[1] % 2: k = N - k
    r = R[0].to_bytes(32, "big")
    e = int.from_bytes(tagged("BIP0340/challenge", r, pub, msg), "big") % N
    return pub.hex(), (r + ((k + e * d) % N).to_bytes(32, "big")).hex()


def main():
    os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
    d = int.from_bytes(hashlib.sha256(b"paid-tcp-relay fixture relay key 1").digest(), "big") % N
    relay = "wss://relay.example.net/"
    challenge = "c2VydmVyLWNoYWxsZW5nZS0zMi1ieXRlcy0wMDAwMDE"  # base64url of 32 bytes, no padding
    host, port = "203.0.113.10", "22"
    pub, _ = sign(d, bytes(32))
    created_at = 1758672000
    tags = [["relay", relay], ["challenge", challenge], ["destination", host, port]]
    ser = json.dumps([0, pub, created_at, 22242, tags, ""], separators=(",", ":"), ensure_ascii=False)
    eid = hashlib.sha256(ser.encode()).digest()
    pub2, sig = sign(d, eid)
    assert pub2 == pub
    auth = {"id": eid.hex(), "pubkey": pub, "created_at": created_at, "kind": 22242,
            "tags": tags, "content": "", "sig": sig}
    frames = {
        "challenge.json": {"challenge": challenge, "relay": relay},
        "auth.json": auth,
        "ok.json": {"ok": True},
        "refused.json": {"ok": False, "reason": "destination"},
        "dial-failed.json": {"ok": False, "reason": "dial"},
    }
    os.makedirs("fixtures/wire", exist_ok=True)
    for name, obj in frames.items():
        with open(os.path.join("fixtures/wire", name), "w") as f:
            json.dump(obj, f, indent=2); f.write("\n")
    print("url:", f"{relay.rstrip('/')}/v1/tcp/{host}/{port}")
    print("pubkey:", pub)


if __name__ == "__main__":
    main()
