import argparse
from .secrets_scanner import scan_secrets

def main():
    parser = argparse.ArgumentParser(description="MLSecure CLI")
    subparsers = parser.add_subparsers(dest="command")

    scan_parser = subparsers.add_parser("scan-secrets", help="Scan for secrets in codebase")
    scan_parser.add_argument("--path", default=".", help="Directory to scan")

    args = parser.parse_args()

    if args.command == "scan-secrets":
        result = scan_secrets(args.path)
        exit(0 if result else 1)

if __name__ == "__main__":
    main()
