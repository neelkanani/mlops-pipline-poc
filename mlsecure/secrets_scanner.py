import os
import re

SECRET_PATTERNS = [
    # Common variable name patterns
    re.compile(r"(?i)(AWS|API|SECRET|TOKEN|KEY)[_\-]?(ID|KEY|PASSWORD)?\s*=\s*[\"']?[A-Za-z0-9_\-]{8,}[\"']?"),

    # OpenAI-style secret key pattern
    re.compile(r"sk-[a-zA-Z0-9\-]{16,}"),  # More lenient and matches sk-test too

    # Generic key pattern (optional)
    re.compile(r"[\"'](ghp|sk|ya29|AIza|AKIA)[a-zA-Z0-9_\-]{8,}[\"']")
]

EXCLUDED_DIRS = {'.git', '.venv', 'venv', '__pycache__', 'node_modules', 'dist', 'build'}

def scan_secrets(base_path="."):
    print(f"🔍 Scanning for secrets in: {base_path}")
    found = False
    for root, dirs, files in os.walk(base_path):
        # Skip unwanted dirs
        dirs[:] = [d for d in dirs if d not in EXCLUDED_DIRS]
        
        for f in files:
            if f.endswith((".py", ".js", ".env", ".txt")):
                full_path = os.path.join(root, f)
                with open(full_path, errors='ignore') as file:
                    for i, line in enumerate(file):
                        for pattern in SECRET_PATTERNS:
                            if pattern.search(line):
                                print(f"❌ Secret found in {full_path}:{i+1} → {line.strip()}")
                                found = True
    return not found  # Return True if clean
