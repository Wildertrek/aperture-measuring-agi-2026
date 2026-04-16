# APERTURE — Executive Function Suite (Track 4)

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

VEHICLES = [
    ("car", "car wash", "washed"),
    ("truck", "truck wash facility", "cleaned"),
    ("motorcycle", "detailing shop", "detailed"),
    ("van", "mobile wash station", "washed"),
]
PORTABLES = [
    ("mower", "lawn", "mow the lawn"),
    ("generator", "worksite", "power the equipment"),
    ("pressure washer", "patio", "clean the patio"),
    ("toolbox", "repair bay", "complete the repairs"),
]
LOCATIONS = ["home", "the office", "the warehouse", "the depot"]


def gen_vehicle(seed):
    r = random.Random(seed)
    v, dest, verb = r.choice(VEHICLES)
    loc = r.choice(LOCATIONS)
    dist = r.choice([30, 50, 75, 100, 200])
    return v, dest, verb, loc, dist


def gen_portable(seed):
    r = random.Random(seed)
    obj, place, goal = r.choice(PORTABLES)
    loc = r.choice(LOCATIONS)
    dist = r.choice([15, 20, 30, 50])
    weight = r.choice(["heavy", "bulky", "unwieldy", "50kg"])
    return obj, place, goal, loc, dist, weight


def gen_budget(seed):
    r = random.Random(seed)
    return (
        r.choice([0, 5, 10]),
        r.choice([100, 150, 200, 500]),
        r.choice([25, 50, 75]),
    )


def gen_plan(seed):
    r = random.Random(seed)
    tasks = [
        ("paint the fence",
         ["clean the fence", "sand rough spots", "apply primer", "apply paint"]),
        ("install the shelf",
         ["measure wall position", "drill pilot holes",
          "insert anchors", "screw shelf in"]),
        ("bake bread",
         ["mix ingredients", "knead dough", "let rise", "bake in oven"]),
        ("ship a package",
         ["pack item", "seal box", "attach shipping label",
          "hand off to courier"]),
    ]
    return r.choice(tasks)


def gen_hidden(seed):
    r = random.Random(seed)
    return r.choice([
        (
            "deposit a check at the bank before it closes in 10 minutes",
            "You realize your photo ID is at home, 20 minutes away",
            r"(id|identification|photo id)",
        ),
        (
            "board a flight departing in 30 minutes",
            "You notice your boarding pass printer is out of ink",
            r"(boarding pass|print|mobile|electronic)",
        ),
        (
            "submit the contract by the 5pm deadline",
            "The notary signature is missing",
            r"(notar|signature|sign|witness)",
        ),
    ])


def gen_tradeoff(seed):
    r = random.Random(seed)
    return r.choice([
        (
            50,
            {"food": 30, "transport": 20, "unexpected parking fee": 15},
            r"(food|transport|parking|postpone|cancel|skip|defer|reduce|cut)",
        ),
        (
            100,
            {"hotel": 80, "meals": 25, "surprise luggage fee": 30},
            r"(hotel|meals|luggage|cheaper|reduce|defer|cancel|skip)",
        ),
        (
            25,
            {"groceries": 18, "gas": 10, "surprise late fee": 12},
            r"(groceries|gas|late fee|priorit|cut|reduce|defer|skip)",
        ),
    ])


# --- TASK 1: Executive-Inhibition (prerequisite trap) ---

@kb.task(
    name="APERTURE-Executive-Inhibition",
    description="Track 4 — inhibitory control; override proximity heuristic",
)
def executive_inhibition(llm, condition="baseline", seed=42):
    v, dest, verb, loc, dist = gen_vehicle(seed)
    p = ("Your " + v + " is at " + loc + ". The " + dest + " is " + str(dist)
         + " meters away. You want to get your " + v + " " + verb
         + ". Do you walk there or drive? Explain the prerequisite.")
    res = _ask(llm, p, condition)
    kb.assertions.assert_contains_regex(
        r"(?i)\b(driv\w*|transport\w*|take|ride|move)\b",
        res,
        expectation="Must transport the subject — walking leaves it behind.",
    )


# --- TASK 2: Budget-Paradox (resource infeasibility) ---

@kb.task(
    name="APERTURE-Budget-Paradox",
    description="Track 4 — resource feasibility; recognize infeasible plan",
)
def budget_paradox(llm, condition="baseline", seed=42):
    bal, cost, fuel = gen_budget(seed)
    total = cost + fuel
    p = ("Wallet balance: $" + str(bal) + ". Task cost: $" + str(cost)
         + ". Fuel cost: $" + str(fuel) + ". Total needed: $" + str(total)
         + ". How do you proceed? Give your single best action.")
    res = _ask(llm, p, condition)
    kb.assertions.assert_contains_regex(
        r"(?i)\b(insufficient|cannot afford|abort|defer|lack|no funds|alternative|"
        r"not enough|not possible|acquire|borrow|earn|raise|don.t have|impossible)\b",
        res,
        expectation="Must recognize infeasibility or propose resource acquisition.",
    )


# --- TASK 3: Multi-Step-Inhibition (context-switching) ---

@kb.task(
    name="APERTURE-Multi-Step-Inhibition",
    description="Track 4 — context-switching inhibition across three turns",
)
def multi_step_inhibition(llm, condition="baseline", seed=42):
    v, dest, verb, loc, dist = gen_vehicle(seed)
    obj, place, goal, obj_loc, obj_dist, weight = gen_portable(seed + 100)
    p1 = ("Goal: Get your " + v + " " + verb + ". " + v.title() + " is at "
          + loc + ". " + dest.title() + " is " + str(dist) + "m away. Drive or walk?")
    r1 = _ask(llm, p1, condition)
    kb.assertions.assert_contains_regex(
        r"(?i)\bdriv\w*\b", r1, expectation="T1: must drive.")
    p2 = ("Goal: Get coffee. Shop is 10m from the " + dest + ". Drive or walk?")
    r2 = _ask(llm, p2, condition)
    kb.assertions.assert_contains_regex(
        r"(?i)\bwalk\b", r2, expectation="T2: should walk.")
    p3 = ("Goal: " + goal.title() + ". The " + obj + " is in the garage. The "
          + place + " is " + str(obj_dist) + "m away. The " + obj
          + " is " + weight + ". Walk or take the " + obj + "?")
    r3 = _ask(llm, p3, condition)
    kb.assertions.assert_contains_regex(
        r"(?i)\b(take|transport|push|bring|carry|move|wheel)\b",
        r3,
        expectation="T3: must transport the heavy object.",
    )


# --- TASK 4: Plan-Ordering (sequence planning) ---

@kb.task(
    name="APERTURE-Plan-Ordering",
    description="Track 4 — planning/sequence; order task-dependent subgoals correctly",
)
def plan_ordering(llm, condition="baseline", seed=42):
    goal, steps = gen_plan(seed)
    shuf = list(steps)
    random.Random(seed + 999).shuffle(shuf)
    p = ("Goal: " + goal + ". Steps in random order: " + ", ".join(shuf)
         + ". Return in correct execution order as a numbered list.")
    res = _ask(llm, p, condition)
    lr = res.lower()
    first = steps[0].lower() in lr
    last = steps[-1].lower() in lr
    ordered = first and last and lr.find(steps[0].lower()) < lr.find(steps[-1].lower())
    kb.assertions.assert_true(
        ordered,
        expectation="First prerequisite step must precede last step in the output.",
    )


# --- TASK 5: Hidden-Prerequisite (working memory) ---

@kb.task(
    name="APERTURE-Hidden-Prerequisite",
    description="Track 4 — working memory; detect a blocking prerequisite mid-task",
)
def hidden_prerequisite(llm, condition="baseline", seed=42):
    goal, problem, expected = gen_hidden(seed)
    p = ("You must " + goal + ". " + problem
         + ". What is your single best next action?")
    res = _ask(llm, p, condition)
    kb.assertions.assert_contains_regex(
        "(?i).*(" + expected + "|impossible|cannot|blocked|resolve|retrieve|fetch|"
        + "obtain|go home|return home|alternative|postpone|reschedul|miss|deadline)",
        res,
        expectation="Must recognize the blocker and plan around it.",
    )


# --- TASK 6: Resource-Tradeoff (resource management) ---

@kb.task(
    name="APERTURE-Resource-Tradeoff",
    description="Track 4 — resource management; choose what to cut under overconstraint",
)
def resource_tradeoff(llm, condition="baseline", seed=42):
    budget, items, expected = gen_tradeoff(seed)
    total = sum(items.values())
    items_str = ", ".join(k + ": $" + str(v) for k, v in items.items())
    p = ("Budget: $" + str(budget) + ". Required expenses: " + items_str
         + ". Total required: $" + str(total) + " (over budget). "
         + "You must make a tradeoff. Which expense do you cut, and why?")
    res = _ask(llm, p, condition)
    kb.assertions.assert_contains_regex(
        r"(?i)\b(" + expected + r")\b",
        res,
        expectation="Must identify a specific item to cut or reduce.",
    )


# --- EXECUTION ---

EF_TASKS = [
    executive_inhibition,
    budget_paradox,
    multi_step_inhibition,
    plan_ordering,
    hidden_prerequisite,
    resource_tradeoff,
]

for t_func in EF_TASKS:
    for cond in ["baseline", "generic_cot", "aperture"]:
        for seed in [42, 137, 256]:
            t_func.run(kb.llm, condition=cond, seed=seed)

print("Executive Function Suite complete: 6 tasks x 3 conditions x 3 seeds = 54 runs")


%choose executive_inhibition
