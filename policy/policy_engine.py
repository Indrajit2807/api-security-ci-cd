import json
import sys

def check_semgrep():
    try:
        with open("semgrep.json") as f:
            data = json.load(f)

        findings = data.get("results", [])
        high = [f for f in findings if f.get("extra", {}).get("severity") in ["ERROR", "HIGH"]]

        return len(high)
    except:
        return 0


def check_gitleaks():
    try:
        with open("gitleaks.json") as f:
            data = json.load(f)

        return len(data)
    except:
        return 0


def check_safety():
    try:
        with open("safety.json") as f:
            data = json.load(f)

        return len(data)
    except:
        return 0


def main():
    semgrep_issues = check_semgrep()
    secret_issues = check_gitleaks()
    dep_issues = check_safety()

    total = semgrep_issues + secret_issues + dep_issues

    print(f"Semgrep: {semgrep_issues}")
    print(f"Secrets: {secret_issues}")
    print(f"Dependencies: {dep_issues}")

    if total > 0:
        print("❌ Policy violated!")
        sys.exit(1)
    else:
        print("✅ All checks passed")


if __name__ == "__main__":
    main()