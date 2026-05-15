from locust import HttpUser, task, between
import logging

logging.basicConfig(level=logging.INFO)

class MLPAppUser(HttpUser):
    host = "http://localhost:30007"   # change if needed
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
    def predict_easy(self):
        if not self.token:
            return

        payload = {
            "G1": 15,
            "G2": 14,
            "absences": 2,
            "higher": "yes",
            "failures": 0,
            "studytime": 2,
            "Mother_edu": 4,
            "Father_edu": 4,
            "Trip": 2,
            "health": 5,
            "sex": "M",
            "school": "GP"
        }

        with self.client.post(
            "/predict-easy",
            json=payload,
            headers=self.headers,
            catch_response=True
        ) as response:

            if response.status_code == 200:
                response.success()
            else:
                response.failure(
                    f"Predict failed: {response.status_code} | {response.text}"
                )