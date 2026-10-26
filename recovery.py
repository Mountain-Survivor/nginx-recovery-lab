import subprocess

from fastapi import FastAPI

app = FastAPI()

@app.post("/alerts")
def recive_alerts(playload: dict):
	print(playload, flush=True)
	for alert in playload.get("alerts", []):
		if alert.get("status") == "firing" and alert.get("labels", {}).get("alertname") == "NginxDown":
			print("nginx 복구 대상 감지", flush=True)
			result = subprocess.run(
    			["docker", "compose", "start", "web"],
   				capture_output=True,
    			text=True,
    			timeout=30,
			)
			print("복구 명령 종료 코드:", result.returncode, flush=True)
			print(result.stdout, result.stderr, flush=True)
	return {"recieved": True}
