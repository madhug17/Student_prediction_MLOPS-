from locust import HttpUser, task, between
import logging

logging.basicConfig(level=logging.INFO)

class AsyncMLUser(HttpUser):
    host = "http://localhost:30007"   # same host for fair comparison
    wait_time = between(1, 2)

    def on_start(self):
        login_payload = {
            "username": "admin",
            "password": "1234"
        }

        response = self.client.post(
            "/token",
            data=login_payload,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )

        if response.status_code == 200:
            data = response.json()
            self.token = data.get("access_token")
            self.headers = {
                "Authorization": f"Bearer {self.token}"
            }
            print("Login success")
        else:
            self.token = None
            print("LOGIN ERROR:", response.status_code, response.text)

    @task
    def predict_async(self):
        if not self.token:
            return

        payload = {
            "features": [5.1, 3.5, 1.4, 0.2]
        }

        with self.client.post(
            "/predict_async",
            json=payload,
            headers=self.headers,
            catch_response=True
        ) as response:

            if response.status_code in [200, 202]:
                response.success()
            else:
                response.failure(
                    f"Async failed: {response.status_code} | {response.text}"
                )