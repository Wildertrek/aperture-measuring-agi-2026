import os
import json

WD = "/kaggle/working"


def extract_text(parts):
    out = []
    for p in parts or []:
        t = p.get("text")
        if t:
            out.append(t)
    return "\n".join(out)


def fmt_time(iso_str):
    if not iso_str:
        return "?"
    return iso_str.split("T")[1][:8]


task_files = sorted(f for f in os.listdir(WD) if f.endswith(".task.json"))
run_files = sorted(f for f in os.listdir(WD) if f.endswith(".run.json"))

print(f"=== {len(task_files)} task(s), {len(run_files)} run(s) ===\n")

for tf in task_files:
    t = json.load(open(f"{WD}/{tf}"))
    tv = t.get("taskVersion", t)
    print(f"TASK: {tv.get('name')}")
    print(f"   Description: {tv.get('description', '')}")
    print()

for rf in run_files:
    r = json.load(open(f"{WD}/{rf}"))
    name = r.get("taskVersion", {}).get("name", "?")
    model = r.get("modelVersion", {}).get("slug", "?")
    state = r.get("state", "?").replace("BENCHMARK_TASK_RUN_STATE_", "")
    dur = ""
    if r.get("startTime") and r.get("endTime"):
        dur = f" ({fmt_time(r['startTime'])} -> {fmt_time(r['endTime'])})"

    asserts = r.get("assertions", [])
    agg = r.get("results", [{}])[0].get("booleanResult")
    icon = "PASS" if agg is True else "FAIL" if agg is False else "?"

    print(f"[{icon}] RUN: {rf}")
    print(f"   Task: {name}   Model: {model}")
    print(f"   State: {state}{dur}")
    for a in asserts:
        s = a.get("status", "?").replace("BENCHMARK_TASK_RUN_ASSERTION_STATUS_", "")
        print(f"   Assertion [{s}]: {a.get('expectation', '')}")

    for conv in r.get("conversations", [])[:1]:
        for req in conv.get("requests", [])[:1]:
            contents = req.get("contents", [])
            for c in contents:
                role = c.get("role", "").replace("CONTENT_ROLE_", "")
                txt = extract_text(c.get("parts"))
                head = "USER" if role == "USER" else "MODEL"
                print(f"\n   {head}:")
                for line in txt.split("\n"):
                    print(f"      {line}"[:200])
    print()
