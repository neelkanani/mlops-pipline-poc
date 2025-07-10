from fastapi import FastAPI, Request
import uvicorn

app = FastAPI()

@app.post("/github-webhook")
async def github_webhook(request: Request):
    payload = await request.json()
    
    # Extract relevant info
    workflow = payload.get("workflow_run", payload)
    conclusion = workflow.get("conclusion")
    name = workflow.get("name")
    html_url = workflow.get("html_url")

    print("🔔 Webhook received!", workflow)
    print(f"Workflow: {name}")
    print(f"Status: {conclusion}")
    print(f"Details: {html_url}")

    return {"message": "Webhook received"}
    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
