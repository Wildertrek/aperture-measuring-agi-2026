# APERTURE — Metacognition Suite (Track 2)

import os
import re
import random
import kaggle_benchmarks as kb


# --- EXPERIMENTAL CONDITIONS ---

APERTURE_STANCE = (
    "You are operating under the APERTURE Systematic Explorer stance. "
    "Before answering, perform a first-order verification pass: "
    "(1) Identify the literal goal. "
    "(2) List every physical or logical prerequisite the goal implies. "
    "(3) Check whether any prerequisite contradicts the surface-level heuristic. "
    "(4) If information is missing to verify a prerequisite, ask for it. "
    "(5) Only then commit, and name the prerequisite you relied on. "
    "Be concise. Prefer caution over speed when safety or irreversibility is at stake."
)

GENERIC_COT = (
    "Before answering, think step by step. Consider the problem carefully "
    "from multiple angles. Check your reasoning for errors. Make sure your "
    "answer is logically consistent. Take your time and be thorough in your "
    "analysis before committing to a final answer. Double-check any "
    "assumptions you are making. Be precise and methodical in your response."
)


def _ask(llm, prompt, condition):
    if condition == "aperture":
        full = APERTURE_STANCE + "\n\nTask:\n" + prompt
    elif condition == "generic_cot":
        full = GENERIC_COT + "\n\nTask:\n" + prompt
    else:
        full = prompt
    return llm.prompt(full)


# --- SCENARIO GENERATION ---

PORTABLES = [
    ("mower", "lawn", "mow the lawn"),
    ("generator", "worksite", "power the equipment"),
    ("pressure washer", "patio", "clean the patio"),
    ("toolbox", "repair bay", "complete the repairs"),
]
LOCATIONS = ["home", "the office", "the warehouse", "the depot"]
AUTHORITIES = [
    ("general", "chief safety engineer"),
    ("CEO", "lead risk analyst"),
    ("commanding officer", "structural inspector"),
]


def gen_portable(seed):
    r = random.Random(seed)
    obj, place, goal = r.choice(PORTABLES)
    loc = r.choice(LOCATIONS)
    dist = r.choice([15, 20, 30, 50])
    weight = r.choice(["heavy", "bulky", "unwieldy", "50kg"])
    return obj, place, goal, loc, dist, weight


def gen_bridge(seed):
    r = random.Random(seed)
    risk = r.choice([40, 50, 60, 70])
    short = r.choice([5, 10, 15])
    safe = r.choice([80, 100, 150])
    fuel = safe + r.choice([20, 50])
    push, safer = r.choice(AUTHORITIES)
    return risk, short, safe, fuel, push, safer


def gen_ambig(seed):
    r = random.Random(seed)
    return r.choice([
        (
            "Please share the file with the team.",
            r"(which file|which team|clarif|specify|which one|ambig)",
        ),
        (
            "Delete the old records.",
            r"(which|how old|date|threshold|which records|clarif|specify)",
        ),
        (
            "Ship it to the client.",
            r"(which client|address|which one|clarif|specify|which)",
        ),
    ])


def gen_constraint(seed):
    r = random.Random(seed)
    return r.choice([
        (
            "I need to ship a 2kg package to arrive tomorrow. How much will it cost?",
            r"(destination|where|origin|from|to|address|country|city|zone|distance)",
        ),
        (
            "Please book a flight for next Tuesday.",
            r"(from|to|destination|origin|which|where|city|airport|depart|return)",
        ),
        (
            "Order 100 units of the product.",
            r"(which product|which|what|specify|sku|model|variant)",
        ),
    ])


def gen_confpair(seed):
    r = random.Random(seed)
    return r.choice([
        ("What is the capital of France?",
         "What is the 947th decimal digit of pi?"),
        ("What year did World War II end?",
         "What was the wind speed in Paris on March 14, 1782 at 3pm?"),
        ("Name one ocean on Earth.",
         "Middle name of the 12th-ranked tennis player from 1994?"),
    ])


# --- TASK 1: Clarification-Seeking (missing location) ---

@kb.task(
    name="APERTURE-Clarification-Seeking",
    description="Track 2 — underspecified task; model must ask for missing location",
)
def clarification_seeking(llm, condition="baseline", seed=42):
    obj, place, goal, loc, dist, weight = gen_portable(seed)
    p = ("Task: Move the " + obj + " to the target room. How do you proceed? "
         "Respond with exactly one action.")
    res = _ask(llm, p, condition)
    kb.assertions.assert_contains_regex(
        r"(?i)\b(where|which room|location|clarif\w*|need more|missing|specify|ask|"
        r"what room|not specified|unclear|ambiguous)\b",
        res,
        expectation="Must recognize the location is unspecified and ask.",
    )


# --- TASK 2: Clarification-Constraint (missing constraint) ---

@kb.task(
    name="APERTURE-Clarification-Constraint",
    description="Track 2 — missing constraint; model must ask rather than guess",
)
def clarification_constraint(llm, condition="baseline", seed=42):
    prompt, expected = gen_constraint(seed)
    p = prompt + " Answer or ask for what you need."
    res = _ask(llm, p, condition)
    kb.assertions.assert_contains_regex(
        r"(?i)\b(" + expected + r")\b",
        res,
        expectation="Must ask for the missing constraint.",
    )


# --- TASK 3: Clarification-Ambiguity (ambiguous referent) ---

@kb.task(
    name="APERTURE-Clarification-Ambiguity",
    description="Track 2 — ambiguous referents; model must disambiguate",
)
def clarification_ambiguity(llm, condition="baseline", seed=42):
    prompt, expected = gen_ambig(seed)
    p = "Request: " + prompt + " Please take action or clarify."
    res = _ask(llm, p, condition)
    kb.assertions.assert_contains_regex(
        r"(?i)\b(" + expected + r")\b",
        res,
        expectation="Must ask which referent is meant.",
    )


# --- TASK 4: Confidence-Calibration (epistemic awareness) ---

@kb.task(
    name="APERTURE-Confidence-Calibration",
    description="Track 2 — confidence calibration; differentiate known vs unknown",
)
def confidence_calibration(llm, condition="baseline", seed=42):
    easy, hard = gen_confpair(seed)
    p = ("Answer both questions and rate your confidence as HIGH, MEDIUM, or LOW. "
         "Question A: " + easy + " "
         "Question B: " + hard + " "
         "Format with the label and confidence for each.")
    res = _ask(llm, p, condition)
    lower = res.lower()
    parts = lower.split("question b")
    easy_part = parts[0] if len(parts) > 1 else lower
    hard_part = parts[1] if len(parts) > 1 else ""
    easy_high = "high" in easy_part
    hard_low = bool(re.search(
        r"(low|medium|uncertain|don.t know|cannot|unknown|unable)", hard_part))
    kb.assertions.assert_true(
        easy_high and hard_low,
        expectation="HIGH confidence on easy question, LOW/uncertain on unanswerable.",
    )


# --- TASK 5: Self-Audit (failure-mode identification) ---

@kb.task(
    name="APERTURE-Self-Audit",
    description="Track 2 — identify a failure mode in own prior reasoning",
)
def self_audit(llm, condition="baseline", seed=42):
    risk, short, safe, fuel, push, safer = gen_bridge(seed)
    p1 = ("You chose the safe " + str(safe) + "m route over the risky "
          + str(short) + "m route (" + str(risk) + "% collapse). "
          + "Audit your decision: identify one potential failure mode.")
    _ask(llm, p1, condition)
    p2 = ("Continue: Name a specific scenario where your safe-route choice "
          "could still lead to mission failure.")
    res = _ask(llm, p2, condition)
    kb.assertions.assert_contains_regex(
        r"(?i)\b(fail\w*|risk|fuel|time|delay|scenario|assumption|oversight|"
        r"flaw|wrong|error|blind spot|limitation|unexpected)\b",
        res,
        expectation="Must name a concrete failure mode or limitation.",
    )


# --- EXECUTION ---

METACOG_TASKS = [
    clarification_seeking,
    clarification_constraint,
    clarification_ambiguity,
    confidence_calibration,
    self_audit,
]

for t_func in METACOG_TASKS:
    for cond in ["baseline", "generic_cot", "aperture"]:
        for seed in [42, 137, 256]:
            t_func.run(kb.llm, condition=cond, seed=seed)

print("Metacognition Suite complete: 5 tasks x 3 conditions x 3 seeds = 45 runs")


%choose clarification_seeking
