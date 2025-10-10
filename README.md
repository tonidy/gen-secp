# gen-secp

gen-secp is a lightweight Python CLI and website for generating secp256k1 keypairs. It quickly prints fresh keys for local development, can emit detailed output, and offers a static WebAssembly-powered demo so you can generate keys directly in your browser.

- Web demo: https://gen-secp.github.io
- Source: https://github.com/tonidy/gen-secp

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

Requirements:

- uv (https://docs.astral.sh/uv)

## Installation

1. Clone the repository:

```bash
git clone https://github.com/tonidy/gen-secp.git
cd gen-secp
```

2. Install the packages:

```bash
uv sync
```

If you want to enable the optional coincurve-backed CLI mode (for PEM export), install the extra:

```bash
uv sync --extra coincurve
```

## Usage

The project provides a CLI entry. Example commands:

```bash
uv run genkey
```

Runs the command to generate a new key or secure artifact and prints or saves the result depending on configuration.

```bash
uv run genkey --long
```

Prints the private key plus compressed and uncompressed public keys.

```bash
uv run genkey --save mykey
```


Writes `mykey.priv.hex` (private key hex string) and `mykey.pub.txt` with both public key encodings in the current directory.

Run `uv run genkey -h` for the full list of options.

```bash
uv run genkey --coincurve --save mykey
```

Uses the original coincurve implementation (requires the extra above) and writes SEC1 PEM files (`mykey.pem`, `mykey.pub.pem`).

## Browser demo

The static site under `docs/` is deployed to GitHub Pages. It bundles the same Python implementation (executed through Pyodide WebAssembly) to generate keypairs client-side. Open https://tonidy.github.io/gen-secp and click “Generate Keypair”.

## Troubleshooting

- If you see "python: command not found", ensure Python is installed and on your PATH.
- If dependencies fail to install, try `uv sync` again.

## License

MIT
