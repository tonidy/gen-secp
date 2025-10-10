#!/usr/bin/env python3
import argparse
from pathlib import Path
from typing import Optional, Tuple

from .core import generate_keypair


def generate(use_coincurve: bool = False) -> Tuple[str, str, str, Optional["PrivateKey"]]:
    if use_coincurve:
        try:
            from coincurve import PrivateKey  # type: ignore
        except ImportError as exc:  # pragma: no cover - runtime check
            raise SystemExit(
                "coincurve is required for --coincurve mode. "
                "Install it with `uv pip install coincurve` or `uv sync --extra coincurve`."
            ) from exc

        key = PrivateKey()
        priv_hex = key.to_hex()
        pub_compressed = key.public_key.format(compressed=True).hex()
        pub_uncompressed = key.public_key.format(compressed=False).hex()
        return priv_hex, pub_compressed, pub_uncompressed, key

    priv_hex, pub_compressed, pub_uncompressed = generate_keypair()
    return priv_hex, pub_compressed, pub_uncompressed, None


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
        help="Save private key (hex) to a file and public key details to <name>.pub.txt",
        nargs="?",
        const="key",
        default=None,
    )
    p.add_argument(
        "--coincurve",
        action="store_true",
        help="Use coincurve (requires the coincurve package) for key generation and PEM export.",
    )
    args = p.parse_args()

    priv, pcomp, puncomp, key_obj = generate(args.coincurve)
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
        if key_obj is not None:
            priv_path = base.parent / f"{base.name}.pem"
            pub_path = base.parent / f"{base.name}.pub.pem"
            with priv_path.open("wb") as f:
                f.write(key_obj.to_pem())
            with pub_path.open("wb") as f:
                f.write(key_obj.public_key.to_pem())
            print(f"\nSaved: {priv_path} (private), {pub_path} (public)")
        else:
            priv_path = base.parent / f"{base.name}.priv.hex"
            pub_path = base.parent / f"{base.name}.pub.txt"
            with priv_path.open("w", encoding="ascii") as f:
                f.write(priv + "\n")
            with pub_path.open("w", encoding="ascii") as f:
                f.write("compressed:" + pcomp + "\n")
                f.write("uncompressed:" + puncomp + "\n")
            print(f"\nSaved: {priv_path} (hex), {pub_path} (compressed/uncompressed)")


if __name__ == "__main__":
    cli()
