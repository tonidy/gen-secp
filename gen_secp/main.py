#!/usr/bin/env python3
import argparse
from pathlib import Path

from coincurve import PrivateKey

def generate():
    key = PrivateKey()  # securely generate
    priv_hex = key.to_hex()
    pub_compressed = key.public_key.format(compressed=True).hex()
    pub_uncompressed = key.public_key.format(compressed=False).hex()
    return key, priv_hex, pub_compressed, pub_uncompressed

def cli():
    p = argparse.ArgumentParser(prog="genkey", description="Generate secp256k1 keypair")
    p.add_argument(
        "--long",
        action="store_true",
        help="Show compressed and uncompressed public key details.",
    )
    p.add_argument(
        "--save",
        "-s",
        help="Save private key to a file (PEM binary) and public to <name>.pub",
        nargs="?",
        const="key",
        default=None,
    )
    args = p.parse_args()

    key, priv, pcomp, puncomp = generate()
    print("Secp256k1 generated keypair")
    if args.long:
        print("Private key (hex):", priv)
        print("Public key compressed (hex):", pcomp)
        print("Public key uncompressed (hex):", puncomp)
    else:
        print("Private key:", priv)
        print("Public key:", pcomp)

    if args.save:
        base = Path(args.save).expanduser()
        base.parent.mkdir(parents=True, exist_ok=True)
        priv_path = base.parent / f"{base.name}.pem"
        pub_path = base.parent / f"{base.name}.pub.pem"
        # write raw PEM-like using coincurve (private key in SEC1 PEM)
        with priv_path.open("wb") as f:
            f.write(key.to_pem())
        with pub_path.open("wb") as f:
            f.write(key.public_key.to_pem())
        print(f"\nSaved: {priv_path} (private), {pub_path} (public)")


if __name__ == "__main__":
    cli()
