from fastapi import FastAPI, Request
import requests
import zipfile
import io
import os
import re

app = FastAPI()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

@app.post("/github-webhook")
async def github_webhook(request: Request):
    headers = dict(request.headers)
    event = headers.get("x-github-event", "unknown")
    payload = await request.json()

    if event != "workflow_run":
        return {"message": f"Ignored event: {event}"}

    run = payload.get("workflow_run", {})
    logs_url = run.get("logs_url")
    status = run.get("conclusion")
    workflow_name = run.get("name")
    html_url = run.get("html_url")

    if not logs_url:
        return {"message": "No logs URL found"}

    errors = extract_errors_from_logs(logs_url)

    print(f"\n🔔 Webhook Event: workflow_run")
    print(f"Workflow: {workflow_name}")
    print(f"Status: {status}")
    print(f"Logs: {logs_url}")
    print(f"Run URL: {html_url}")
    print(f"❗ Errors Found:")
    for err in errors:
        print(f" - {err}")

    return {
        "workflow": workflow_name,
        "status": status,
        "run_url": html_url,
        "errors": errors
    }

def extract_errors_from_logs(logs_url):
    headers = {
        "Authorization": f"Bearer ghp_yo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",
        "Accept": "application/vnd.github+json"
    }

    res = requests.get(logs_url, headers=headers)
    if res.status_code != 200:
        print("❌ Failed to download logs")
        return []

    error_lines = []
    
    print("PRINT RES === >", res)

    with zipfile.ZipFile(io.BytesIO(res.content)) as z:
        for filename in z.namelist():
            with z.open(filename) as f:
                for line in f:
                    line = line.decode("utf-8").strip()
                    print(f"[LOG] {filename}: {line}")

                    # Match lines like: filename.py:24: error msg
                    match = re.match(r"(.+\.py):(\d+):\s+(.*)", line)
                    if match:
                        error_lines.append({
                            "file": match.group(1),
                            "line": int(match.group(2)),
                            "message": match.group(3)
                        })
                    # fallback: line contains "Error" or "Found"
                    elif any(keyword in line.lower() for keyword in ["error", "found", "secret"]):
                        error_lines.append({
                            "file": filename,
                            "line": None,
                            "message": line
                        })
    return error_lines


# Add this to the bottom of webhook_server.py if not present
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("webhook_server:app", host="0.0.0.0", port=8000, reload=True)

