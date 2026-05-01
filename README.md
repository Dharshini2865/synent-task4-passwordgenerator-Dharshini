# synent-task4-passwordgenerator-Dharshini
# 🔐 Password Generator

A customizable password generator with a visual strength meter and clipboard support.

## Features
- Custom password length (8–64 characters)
- Choose character types:
  - Uppercase letters (A–Z)
  - Lowercase letters (a–z)
  - Numbers (0–9)
  - Special characters (!@#$...)
- Guarantees at least one character from each selected type
- Visual strength bar with score out of 100
- Strength ratings — Weak / Fair / Good / Strong
- Generate multiple passwords at once and pick your favorite
- Auto-copies selected password to clipboard (requires `pyperclip`)

## Requirements
```bash
pip install colorama pyperclip
```
> `pyperclip` is optional — the app works without it, clipboard copy will be skipped.

## How to Run
```bash
python password_generator.py
```

## How to Use
1. Run the program
2. Choose **Option 1** to generate a single password or **Option 2** for multiple
3. Set your preferred length and character types
4. View the generated password with its strength score
5. Press `y` to regenerate with the same settings

## Strength Score Breakdown
| Score  | Rating |
|--------|--------|
| 0–30   | Weak   |
| 31–55  | Fair   |
| 56–75  | Good   |
| 76–100 | Strong |

## Technologies Used
- Python 3
- `random` — password generation and shuffling
- `string` — character sets
- `re` — regex for strength checking
- `pyperclip` — clipboard copy (optional)
- `colorama` — colored terminal output

- ## Authors
- Dharshini | Synent Technologies Internship 2026
