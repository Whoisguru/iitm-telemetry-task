from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List
import numpy as np

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
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
  {"region":"apac","latency_ms":221.92,"uptime_pct":98
