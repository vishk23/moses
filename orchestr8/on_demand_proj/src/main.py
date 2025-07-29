import argparse
import time



def main():
    # Define constants for validation
    REQUIRED_EMAIL_DOMAIN = '@bcsbmail.com'
    MAX_KEY_DIGITS = 12
    MAX_ACCOUNT_DIGITS = 20

    parser = argparse.ArgumentParser()
    parser.add_argument('--email', required=True)
    parser.add_argument('--key', type=int, required=True)
    parser.add_argument('--additions', nargs='*', type=int, default=[])
    parser.add_argument('--deletes', nargs='*', type=int, default=[])
    args = parser.parse_args()

    # Sanitization checks
    assert args.email.endswith(REQUIRED_EMAIL_DOMAIN), f"Email must end with {REQUIRED_EMAIL_DOMAIN}"
    assert len(str(args.key)) <= MAX_KEY_DIGITS, f"Key must have up to {MAX_KEY_DIGITS} digits"
    for num in args.additions:
        assert len(str(num)) <= MAX_ACCOUNT_DIGITS, f"Addition {num} has more than {MAX_ACCOUNT_DIGITS} digits"
    for num in args.deletes:
        assert len(str(num)) <= MAX_ACCOUNT_DIGITS, f"Delete {num} has more than {MAX_ACCOUNT_DIGITS} digits"
    time.sleep(10)
    # Proceed with processing (example output)
    print(f"Email: {args.email}")
    print(f"Key: {args.key}")
    print(f"Additions: {args.additions}")
    print(f"Deletes: {args.deletes}")

if __name__ == "__main__":
    main()