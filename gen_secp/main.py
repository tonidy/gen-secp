#!/usr/bin/env python3
import argparse
import binascii
from coincurve import PrivateKey

def generate():
    key = PrivateKey()  # securely generate
    priv_hex = key.to_hex()
    pub_compressed = key.public_key.format(compressed=True).hex()
    pub_uncompressed = key.public_key.format(compressed=False).hex()
    return priv_hex, pub_compressed, pub_uncompressed

def cli():
    p = argparse.ArgumentParser(prog="genkey", description="Generate secp256k1 keypair")
    p.add_argument("--save", "-s", help="Save private key to a file (PEM binary) and public to <name>.pub", nargs='?', const="key", default=None)
    args = p.parse_args()

    priv, pcomp, puncomp = generate()
    print("private (hex):", priv)
    print("pub compressed (hex):", pcomp)
    print("pub uncompressed (hex):", puncomp)

    if args.save:
        base = args.save
        # write raw PEM-like using coincurve (private key in SEC1 PEM)
        with open(f"{base}.pem", "wb") as f:
            f.write(PrivateKey(bytes.fromhex(priv)).to_pem())
        with open(f"{base}.pub.pem", "wb") as f:
            f.write(PrivateKey(bytes.fromhex(priv)).public_key.to_pem())
        print(f"\nSaved: {base}.pem (private), {base}.pub.pem (public)")
