import json, time, os
from pathlib import Path

def log_event(module: str, data: dict, folder: str = "logs"):
    Path(folder).mkdir(parents=True, exist_ok=True)
    ts = int(time.time()*1000)
    line = {"ts": ts, "module": module, **data}
    with open(os.path.join(folder, f"{time.strftime('%Y%m%d')}_session01.jsonl"), "a", encoding="utf-8") as f:
        f.write(json.dumps(line, ensure_ascii=False)+"\n")
