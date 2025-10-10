import json

# Domain parameters for secp256k1
_P = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
_N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
_A = 0
_B = 7
_GX = 55066263022277343669578718895168534326250603453777594175500187360389116729240
_GY = 32670510020758816978083085130507043184471273380659243275938904335757337482424


def _inverse_mod(k: int, p: int = _P) -> int:
    return pow(k, p - 2, p)


def _point_add(point1, point2):
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


def _scalar_mult(k, point):
    if k % _N == 0 or point is None:
        return None

    result = None
    addend = point
    while k:
        if k & 1:
            result = _point_add(result, addend)
        addend = _point_add(addend, addend)
        k >>= 1
    return result


def _format_public(point):
    x, y = point
    x_hex = f"{x:064x}"
    y_hex = f"{y:064x}"
    prefix = "02" if y % 2 == 0 else "03"
    return prefix + x_hex, "04" + x_hex + y_hex


def generate_keypair():
    import secrets

    private_int = secrets.randbelow(_N - 1) + 1
    public_point = _scalar_mult(private_int, (_GX, _GY))
    if public_point is None:
        raise RuntimeError("Failed to generate valid public key")
    pub_compressed, pub_uncompressed = _format_public(public_point)
    return f"{private_int:064x}", pub_compressed, pub_uncompressed


def generate_json():
    priv, comp, uncomp = generate_keypair()
    return json.dumps(
        {"private": priv, "compressed": comp, "uncompressed": uncomp},
        separators=(",", ":"),
    )
