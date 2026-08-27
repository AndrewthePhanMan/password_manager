# password_manager

A simple command-line password manager written in Python. It uses [Fernet](https://cryptography.io/en/latest/fernet/) symmetric encryption (from the `cryptography` package) to store passwords in an encrypted, human-readable file.

> **Status:** Baseline / work in progress. This is an early version — see [Known Limitations](#known-limitations) and [Planned Improvements](#planned-improvements) below.

## Features

- Generate a new encryption key
- Load an existing encryption key
- Create a new password file (optionally pre-populated)
- Load an existing password file (decrypting entries into memory)
- Add a new site/password pair (encrypted and appended to the file)
- Retrieve a stored password by site name

## Requirements

- Python 3
- [`cryptography`](https://pypi.org/project/cryptography/) package

Install the dependency:

```bash
pip install cryptography
```

## Usage

Run the script and follow the interactive menu:

```bash
python main.py
```

You'll be shown a menu of options:

```
(1) Create a new key
(2) Load an existing key
(3) Create a new password file
(4) Load an existing password file
(5) Add a new password
(6) Get a password
(q) Quit
```

### Typical first-time setup

1. Choose **(1)** to generate a new key and save it (e.g., `key.key`).
2. Choose **(3)** to create a new password file (e.g., `passwords.txt`). This will also save any default passwords defined in `main()`.
3. Choose **(5)** to add additional site/password pairs.

### Typical subsequent use

1. Choose **(2)** to load your existing key.
2. Choose **(4)** to load your existing password file.
3. Choose **(6)** to retrieve a password by site name.

## File Overview

| File | Purpose |
|---|---|
| `main.py` | Main script containing the `PaswordManager` class and CLI menu |
| `key.key` | Fernet encryption key (keep this private — anyone with this key can decrypt your passwords) |
| `passwords.txt` | Encrypted site/password pairs, one per line (`site:encrypted_password`) |

## Known Limitations

- The encryption key and password file are just local files with no additional access controls — protect them accordingly (e.g., file permissions, not committing them to version control).
- No input validation (e.g., duplicate sites, empty passwords).
- Passwords entered at the prompt are displayed in plaintext on screen (no masked input).
- No error handling for missing keys/files or incorrect key usage.
- `main()` includes hardcoded default passwords for demonstration purposes.

## Planned Improvements

- Masked password input
- Better error handling and input validation
- Option to delete/update existing entries
- Packaging as an installable CLI tool

## Security Note

Never commit `key.key` or your unencrypted password data to a public repository. If you fork or extend this project, add these files to `.gitignore`.