import http from 'k6/http';
import { sleep, check } from 'k6';

// ---- TEST CONFIGURATION ----
export let options = {
    stages: [
        { duration: '30s', target: 100 }, // Ramp up to 100 users
        { duration: '1m', target: 700 },  // Stay at 700 users (Heavy Load)
        { duration: '30s', target: 0 },   // Ramp down
    ],
};

const BASE_URL = 'http://127.0.0.1:8000';

// ---- SETUP: GET TOKEN ONCE ----
export function setup() {
    const loginPayload = {
        username: 'admin',
        password: '1234'
    };

    // FastAPI OAuth2 expects form-data, not JSON
    let res = http.post(`${BASE_URL}/token`, loginPayload);

    if (res.status !== 200) {
        console.error('❌ Setup failed: Could not get token');
        return { token: '' };
    }

    let token = JSON.parse(res.body).access_token;
    return { token: token };
}

// ---- VIRTUAL USER ACTIONS ----
export default function (data) {
    // 1. Prepare the payload with the FIXED feature names
    const payload = JSON.stringify({
        G1: 12,
        G2: 14,
        absences: 2,
        higher: "yes",
        failures: 0,
        studytime: 3,
        Mother_edu: 4, // Matches Python renaming
        Father_edu: 3, // Matches Python renaming
        Trip: 2,       // Matches Python renaming
        health: 5,
        sex: "F",
        school: "GP"
    });

    const params = {
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${data.token}`,
        },
    };

    // 2. Hit the Prediction Endpoint
    const res = http.post(`${BASE_URL}/predict-easy`, payload, params);

    // 3. Validation
    check(res, {
        'is status 200': (r) => r.status === 200,
        'inference successful': (r) => r.json().prediction !== undefined,
    });

    // Wait 1 second between requests per user to simulate real behavior
    sleep(1);
}