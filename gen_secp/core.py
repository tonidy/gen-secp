"""
Pure-Python helpers for generating secp256k1 keypairs.

The implementation sticks to basic elliptic curve arithmetic so it can run
inside WebAssembly runtimes (e.g. Pyodide) without requiring native
extensions.
"""
from __future__ import annotations

import secrets
from typing import Optional, Tuple

# Domain parameters for secp256k1
_P = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
_N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
_A = 0
_B = 7
_GX = 55066263022277343669578718895168534326250603453777594175500187360389116729240
_GY = 32670510020758816978083085130507043184471273380659243275938904335757337482424

Point = Optional[Tuple[int, int]]


def _inverse_mod(k: int, p: int = _P) -> int:
    """Compute the modular inverse using Fermat's little theorem."""
    return pow(k, p - 2, p)


def _point_add(point1: Point, point2: Point) -> Point:
    """Add two points on the curve."""
    if point1 is None:
        return point2
    if point2 is None:
        return point1

    x1, y1 = point1
    x2, y2 = point2

    if x1 == x2 and (y1 + y2) % _P == 0:
        return None

    if point1 == point2:
        m = (3 * x1 * x1 + _A) * _inverse_mod(2 * y1) % _P
    else:
        m = (y2 - y1) * _inverse_mod(x2 - x1) % _P

    x3 = (m * m - x1 - x2) % _P
    y3 = (m * (x1 - x3) - y1) % _P
    return x3, y3


def _scalar_mult(k: int, point: Point) -> Point:
    """Multiply a point by an integer using double-and-add."""
    if k % _N == 0 or point is None:
        return None

    result: Point = None
    addend = point
    while k:
        if k & 1:
            result = _point_add(result, addend)
        addend = _point_add(addend, addend)
        k >>= 1
    return result


def _format_public(point: Tuple[int, int]) -> Tuple[str, str]:
    x, y = point
    x_hex = f"{x:064x}"
    y_hex = f"{y:064x}"
    prefix = "02" if y % 2 == 0 else "03"
    return prefix + x_hex, "04" + x_hex + y_hex


def generate_keypair() -> Tuple[str, str, str]:
    """
    Generate a secp256k1 private key and the compressed/uncompressed public key.

    Returns a tuple of hex strings: (private, public_compressed, public_uncompressed).
    """
    private_int = secrets.randbelow(_N - 1) + 1
    public_point = _scalar_mult(private_int, (_GX, _GY))
    if public_point is None:
        raise RuntimeError("Failed to generate valid public key")
    pub_compressed, pub_uncompressed = _format_public(public_point)
    return f"{private_int:064x}", pub_compressed, pub_uncompressed


__all__ = ["generate_keypair"]
