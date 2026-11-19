# 복구 API 포트 불일치로 자동 복구 실패

## 증상
Prometheus는 Firing, Alertmanager에도 알림이 있지만 nginx는 복구되지 않음

## 확인 근거
Uvicorn에 POST 로그 없음. Alertmanager에는 8000: connection refused

## 원인
복구 API는 8001에서 실행 중인데 웹훅 URL은 8000으로 설정

## 수정
monitoring/alertmanager.yml의 웹훅 포트를 8001로 수정하고 Alertmanager 재시작

## 복구 확인
POST /alerts 수신 -> 명령 종료 코드 0 -> nginx HTTP 200 -> Discord RESLVED 수신