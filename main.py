from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import numpy as np

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

ALL_RECORDS = [
  {"region":"apac","latency_ms":229.2,"uptime_pct":99.049},
  {"region":"apac","latency_ms":162.22,"uptime_pct":98.864},
  {"region":"apac","latency_ms":190.27,"uptime_pct":98.76},
  {"region":"apac","latency_ms":148.26,"uptime_pct":98.411},
  {"region":"apac","latency_ms":229.65,"uptime_pct":98.847},
  {"region":"apac","latency_ms":122.5,"uptime_pct":98.03},
  {"region":"apac","latency_ms":134.51,"uptime_pct":99.27},
  {"region":"apac","latency_ms":221.92,"uptime_pct":98.041},
  {"region":"apac","latency_ms":128.98,"uptime_pct":97.851},
  {"region":"apac","latency_ms":187.01,"uptime_pct":98.075},
  {"region":"apac","latency_ms":150.04,"uptime_pct":98.64},
  {"region":"apac","latency_ms":211.19,"uptime_pct":99.239},
  {"region":"emea","latency_ms":232.57,"uptime_pct":99.057},
  {"region":"emea","latency_ms":160.53,"uptime_pct":98.161},
  {"region":"emea","latency_ms":141.58,"uptime_pct":99.446},
  {"region":"emea","latency_ms":116.65,"uptime_pct":97.455},
  {"region":"emea","latency_ms":193.85,"uptime_pct":98.05},
  {"region":"emea","latency_ms":167.93,"uptime_pct":98.522},
  {"region":"emea","latency_ms":170.92,"uptime_pct":99.423},
  {"region":"emea","latency_ms":191.98,"uptime_pct":99.457},
  {"region":"emea","latency_ms":154.39,"uptime_pct":97.863},
  {"region":"emea","latency_ms":162.35,"uptime_pct":97.294},
  {"region":"emea","latency_ms":183.55,"uptime_pct":97.124},
  {"region":"emea","latency_ms":236.41,"uptime_pct":98.489},
  {"region":"amer","latency_ms":185.76,"uptime_pct":97.593},
  {"region":"amer","latency_ms":136.67,"uptime_pct":98.463},
  {"region":"amer","latency_ms":183.83,"uptime_pct":98.306},
  {"region":"amer","latency_ms":134.71,"uptime_pct":98.562},
  {"region":"amer","latency_ms":120.79,"uptime_pct":98.302},
  {"region":"amer","latency_ms":193.29,"uptime_pct":98.336},
  {"region":"amer","latency_ms":145.81,"uptime_pct":98.937},
  {"region":"amer","latency_ms":108.3,"uptime_pct":98.795},
  {"region":"amer","latency_ms":115.16,"uptime_pct":97.693},
  {"region":"amer","latency_ms":131.66,"uptime_pct":98.855},
  {"region":"amer","latency_ms":132.17,"uptime_pct":97.987},
  {"region":"amer","latency_ms":193.56,"uptime_pct":97.129},
]

class RequestBody(BaseModel):
    regions: List[str]
    threshold_ms: float

@app.post("/api")
def get_metrics(body: RequestBody):
    result = {}
    for region in body.regions:
        rows = [r for r in ALL_RECORDS if r["region"].lower() == region.lower()]
        if not rows:
            result[region] = {"avg_latency": None, "p95_latency": None, "avg_uptime": None, "breaches": 0}
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