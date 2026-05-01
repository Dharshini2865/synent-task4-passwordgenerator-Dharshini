# Task 4: Password Generator
# Synent Technologies Python Internship
# Features: custom length, character types, strength meter, copy to clipboard

import random
import string
import re
try:
    import pyperclip
    CLIPBOARD = True
except ImportError:
    CLIPBOARD = False

from colorama import init, Fore, Style
init(autoreset=True)


def show_banner():
    print(Fore.CYAN + "=" * 52)
    print(Fore.CYAN + "    PASSWORD GENERATOR — Synent Internship")
    print(Fore.CYAN + "=" * 52)


def get_strength(password):
    """
    Calculates password strength based on:
    - Length
    - Presence of uppercase, lowercase, digits, special chars
    Returns a score 0-100 and a label
    """
    score = 0

    if len(password) >= 8:  score += 20
    if len(password) >= 12: score += 15
    if len(password) >= 16: score += 15

    if re.search(r'[a-z]', password): score += 10
    if re.search(r'[A-Z]', password): score += 10
    if re.search(r'\d',    password): score += 15
    if re.search(r'[^a-zA-Z0-9]', password): score += 15

    if score <= 30:  return score, "Weak",   Fore.RED
    if score <= 55:  return score, "Fair",   Fore.YELLOW
    if score <= 75:  return score, "Good",   Fore.CYAN
    return           score, "Strong", Fore.GREEN


def show_strength_bar(score):
    """Visual bar showing password strength"""
    filled = int(score / 5)   # max 20 blocks
    empty  = 20 - filled
    _, label, color = get_strength("x" * score)  # get color for score

    bar = color + "█" * filled + Fore.WHITE + Style.DIM + "░" * empty
    print(f"\n  Strength: [{bar}{Style.RESET_ALL}] {color}{score}/100")


def get_options():
    """Ask user to configure their password"""
    print(Fore.CYAN + "\n  Configure your password:\n")

    # Length
    while True:
        try:
            length = int(input(Fore.YELLOW + "  Length (8-64): "))
            if 8 <= length <= 64:
                break
            print(Fore.RED + "  Must be between 8 and 64.")
        except ValueError:
            print(Fore.RED + "  Please enter a number.")

    # Character types
    print(Fore.WHITE + "\n  Include character types? (y/n)\n")

    def ask(prompt, default=True):
        while True:
            ans = input(Fore.YELLOW + f"  {prompt} (y/n): ").strip().lower()
            if ans == 'y': return True
            if ans == 'n': return False
            print(Fore.RED + "  Please enter 'y' for yes or 'n' for no.")

    use_upper   = ask("Uppercase letters (A-Z)?",     True)
    use_lower   = ask("Lowercase letters (a-z)?",     True)
    use_digits  = ask("Numbers (0-9)?",               True)
    use_special = ask("Special characters (!@#$...)?", True)

    # Make sure at least one type is selected
    if not any([use_upper, use_lower, use_digits, use_special]):
        print(Fore.RED + "  At least one character type required. Using all.")
        use_upper = use_lower = use_digits = use_special = True

    return length, use_upper, use_lower, use_digits, use_special


def generate_password(length, use_upper, use_lower, use_digits, use_special):
    """
    Builds a character pool from selected types,
    guarantees at least one char from each selected type,
    then fills the rest randomly.
    """
    pool = ""
    guaranteed = []

    if use_upper:
        pool += string.ascii_uppercase
        guaranteed.append(random.choice(string.ascii_uppercase))
    if use_lower:
        pool += string.ascii_lowercase
        guaranteed.append(random.choice(string.ascii_lowercase))
    if use_digits:
        pool += string.digits
        guaranteed.append(random.choice(string.digits))
    if use_special:
        special = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        pool += special
        guaranteed.append(random.choice(special))

    # Fill remaining length with random pool characters
    remaining = [random.choice(pool) for _ in range(length - len(guaranteed))]

    # Combine guaranteed + remaining, then shuffle so guaranteed chars
    # aren't always at the start
    password_list = guaranteed + remaining
    random.shuffle(password_list)
    return "".join(password_list)


def show_password(password):
    """Display the password with strength info"""
    score, label, color = get_strength(password)

    print(Fore.CYAN + "\n" + "=" * 52)
    print(Fore.WHITE + "  Generated Password:\n")
    print(Fore.WHITE + Style.BRIGHT + f"  {password}")
    show_strength_bar(score)
    print(color + f"\n  Rating: {label}")
    print(Fore.WHITE + f"  Length: {len(password)} characters")
    print(Fore.CYAN + "=" * 52)

    if CLIPBOARD:
        try:
            pyperclip.copy(password)
            print(Fore.GREEN + "\n  ✓ Copied to clipboard!")
        except:
            pass
    else:
        print(Fore.YELLOW + "\n  Tip: pip install pyperclip to auto-copy passwords")


def show_menu():
    print(Fore.CYAN  + "\n  MENU")
    print(Fore.GREEN + "  1. Generate a new password")
    print(Fore.GREEN + "  2. Generate multiple passwords")
    print(Fore.RED   + "  3. Exit")
    print()


def generate_multiple():
    """Generate several passwords at once so user can pick their favourite"""
    while True:
        try:
            count = int(input(Fore.YELLOW + "  How many passwords? (2-10): "))
            if 2 <= count <= 10:
                break
            print(Fore.RED + "  Enter a number between 2 and 10.")
        except ValueError:
            print(Fore.RED + "  Please enter a number.")

    length, use_upper, use_lower, use_digits, use_special = get_options()

    print(Fore.CYAN + f"\n  {count} Generated Passwords:\n")
    passwords = []
    for i in range(count):
        pw = generate_password(length, use_upper, use_lower, use_digits, use_special)
        score, label, color = get_strength(pw)
        passwords.append(pw)
        print(color + f"  {i+1}. {pw}  {Style.DIM}[{label} · {score}/100]")

    print()
    while True:
        try:
            pick = int(input(Fore.YELLOW + f"  Pick one to copy (1-{count}), or 0 to skip: "))
            if pick == 0:
                break
            if 1 <= pick <= count:
                show_password(passwords[pick - 1])
                break
            print(Fore.RED + "  Invalid number.")
        except ValueError:
            print(Fore.RED + "  Please enter a number.")


def main():
    show_banner()

    while True:
        show_menu()
        choice = input(Fore.YELLOW + "  Enter choice (1-3): ").strip()

        if choice == "1":
            length, use_upper, use_lower, use_digits, use_special = get_options()
            password = generate_password(length, use_upper, use_lower, use_digits, use_special)
            show_password(password)

            again = input(Fore.YELLOW + "\n  Regenerate with same settings? (y/n): ").strip().lower()
            while again == 'y':
                password = generate_password(length, use_upper, use_lower, use_digits, use_special)
                show_password(password)
                again = input(Fore.YELLOW + "\n  Regenerate again? (y/n): ").strip().lower()

        elif choice == "2":
            generate_multiple()

        elif choice == "3":
            print(Fore.CYAN + "\n  Stay secure! Goodbye.\n")
            break
        else:
            print(Fore.RED + "  Please enter 1, 2, or 3.")

        print(Fore.CYAN + "  " + "-" * 48)


if __name__ == "__main__":
    main()
