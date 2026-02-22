from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import numpy as np
import json
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# Load telemetry JSON at startup
DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "q-vercel-latency.json")

with open(DATA_FILE) as f:
    ALL_RECORDS = json.load(f)


class RequestBody(BaseModel):
    regions: List[str]
    threshold_ms: float


@app.post("/api")
def get_metrics(body: RequestBody):
    result = {}
    for region in body.regions:
        rows = [r for r in ALL_RECORDS if r["region"].lower() == region.lower()]

        if not rows:
            result[region] = {
                "avg_latency": None,
                "p95_latency": None,
                "avg_uptime": None,
                "breaches": 0,
            }
            continue

        latencies = [r["latency_ms"] for r in rows]
        uptimes = [r["uptime_pct"] for r in rows]

        result[region] = {
            "avg_latency": round(float(np.mean(latencies)), 4),
            "p95_latency": round(float(np.percentile(latencies, 95)), 4),
            "avg_uptime": round(float(np.mean(uptimes)), 4),
            "breaches": int(sum(1 for l in latencies if l > body.threshold_ms)),
        }

    return result