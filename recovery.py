import subprocess

from fastapi import FastAPI, HTTPException

app = FastAPI()

processed_incidents = set()

@app.post("/alerts")
def recive_alerts(playload: dict):
	print(playload, flush=True)
	for alert in playload.get("alerts", []):
		if alert.get("status") == "firing" and alert.get("labels", {}).get("alertname") == "NginxDown":
			incident_key = (
				alert.get("fingerprint"),
				alert.get("startsAt"),
			)
			if incident_key in processed_incidents:
				print("이미 처리된 장애입니다.", flush=True)
				continue
			print("장애 식별값:", incident_key, flush=True)
			print("nginx 복구 대상 감지", flush=True)
			result = subprocess.run(
    			["docker", "compose", "start", "web"],
   				capture_output=True,
    			text=True,
    			timeout=30,
			)
			print("복구 명령 종료 코드:", result.returncode, flush=True)
			print(result.stdout, result.stderr, flush=True)
			if result.returncode == 0:
				processed_incidents.add(incident_key)
			else:
				raise HTTPException(
					status_code=503,
					detail="nginx 복구 명령 실패",
				)
	return {"recieved": True}
