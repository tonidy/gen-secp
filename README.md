# gen-secp

gen-secp is a lightweight Python CLI for generating secp256k1 keypairs. It quickly prints fresh keys for local development, and can optionally emit detailed output or export PEM files for reuse.

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

## Usage

The project provides a CLI entry. Example commands:

```bash
uv run genkey
```

Runs the command to generate a new key or secure artifact and prints or saves the result depending on configuration.

```bash
uv run genkey -h
```


Displays general help or a list of available top-level commands (depends on your shell/CLI wrapper).

## Troubleshooting

- If you see "python: command not found", ensure Python is installed and on your PATH.
- If dependencies fail to install, try `uv sync` again.

## License

MIT
