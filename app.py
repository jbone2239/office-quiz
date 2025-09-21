import streamlit as st
import random
from collections import defaultdict

# -----------------------------
# Characters (15 dimensions)
# -----------------------------
CHARACTERS = [
    "Michael", "Jim", "Pam", "Dwight", "Angela", "Kevin", "Kelly", "Stanley",
    "Oscar", "Creed", "Ryan", "Robert California", "Darryl", "Andy Bernard", "Toby"
]

# ---------------------------------------------------
# Archetype -> Character weight distributions
# (Fractional; sums ≈ 1.0; multiple characters get points)
# ---------------------------------------------------
ARCHETYPE_WEIGHTS = {
    # Work styles
    "planner":            {"Dwight":0.4, "Angela":0.2, "Oscar":0.1, "Ryan":0.2, "Toby":0.1},
    "joker":              {"Jim":0.3, "Michael":0.2, "Kevin":0.2, "Andy Bernard":0.2, "Darryl":0.1},
    "motivator":          {"Michael":0.3, "Andy Bernard":0.3, "Pam":0.2, "Kelly":0.1, "Robert California":0.1},
    "quiet_worker":       {"Pam":0.3, "Stanley":0.2, "Oscar":0.2, "Toby":0.2, "Darryl":0.1},

    # Conflict / credit
    "confront":           {"Dwight":0.3, "Michael":0.2, "Angela":0.2, "Andy Bernard":0.2, "Robert California":0.1},
    "prankster":          {"Jim":0.4, "Pam":0.2, "Creed":0.1, "Darryl":0.2, "Ryan":0.1},
    "escalate_hr":        {"Angela":0.2, "Oscar":0.3, "Toby":0.4, "Stanley":0.1},
    "shrug_it_off":       {"Kevin":0.3, "Creed":0.2, "Jim":0.2, "Darryl":0.2, "Pam":0.1},

    # Weekend / preferences
    "networking":         {"Michael":0.2, "Kelly":0.2, "Andy Bernard":0.2, "Robert California":0.2, "Ryan":0.2},
    "family_time":        {"Pam":0.3, "Jim":0.2, "Angela":0.2, "Darryl":0.2, "Stanley":0.1},
    "quirky_project":     {"Creed":0.3, "Dwight":0.2, "Oscar":0.1, "Ryan":0.2, "Andy Bernard":0.2},
    "relax_plan":         {"Stanley":0.3, "Kevin":0.2, "Toby":0.2, "Pam":0.2, "Robert California":0.1},

    # Meetings
    "joke_meeting":       {"Jim":0.3, "Michael":0.2, "Kelly":0.1, "Andy Bernard":0.2, "Darryl":0.2},
    "zone_out":           {"Stanley":0.3, "Kevin":0.2, "Creed":0.1, "Toby":0.2, "Pam":0.2},
    "serious_notes":      {"Angela":0.3, "Dwight":0.2, "Pam":0.1, "Oscar":0.2, "Ryan":0.2},
    "weird_thoughts":     {"Creed":0.3, "Oscar":0.2, "Kelly":0.1, "Robert California":0.2, "Ryan":0.2},

    # Confusing announcement
    "clarify":            {"Oscar":0.3, "Pam":0.2, "Angela":0.1, "Toby":0.3, "Darryl":0.1},
    "loyalist":           {"Michael":0.3, "Dwight":0.2, "Kelly":0.1, "Andy Bernard":0.2, "Robert California":0.2},
    "lighten_tension":    {"Jim":0.3, "Kevin":0.2, "Michael":0.2, "Darryl":0.2, "Ryan":0.1},
    "wait_watch":         {"Stanley":0.3, "Angela":0.1, "Creed":0.1, "Toby":0.3, "Ryan":0.2},

    # Parties
    "plan_party":         {"Angela":0.3, "Pam":0.2, "Kelly":0.2, "Andy Bernard":0.2, "Michael":0.1},
    "karaoke":            {"Kelly":0.3, "Michael":0.2, "Andy Bernard":0.2, "Ryan":0.2, "Robert California":0.1},
    "bring_food":         {"Kevin":0.3, "Stanley":0.2, "Pam":0.1, "Darryl":0.3, "Toby":0.1},
    "skip_event":         {"Creed":0.3, "Stanley":0.2, "Dwight":0.1, "Oscar":0.2, "Toby":0.2},

    # Stress
    "rules_push":         {"Dwight":0.3, "Angela":0.2, "Oscar":0.2, "Ryan":0.2, "Toby":0.1},
    "fun_distract":       {"Jim":0.2, "Michael":0.2, "Kelly":0.2, "Andy Bernard":0.2, "Darryl":0.2},
    "withdraw":           {"Stanley":0.3, "Pam":0.2, "Creed":0.2, "Toby":0.2, "Oscar":0.1},
    "snack":              {"Kevin":0.3, "Michael":0.1, "Kelly":0.1, "Darryl":0.2, "Andy Bernard":0.3},

    # Motivation
    "recognition":        {"Michael":0.2, "Kelly":0.2, "Andy Bernard":0.2, "Ryan":0.2, "Robert California":0.2},
    "security":           {"Pam":0.3, "Jim":0.2, "Angela":0.2, "Darryl":0.2, "Toby":0.1},
    "order":              {"Dwight":0.3, "Angela":0.2, "Oscar":0.1, "Toby":0.2, "Ryan":0.2},
    "paycheck":           {"Stanley":0.3, "Creed":0.1, "Kevin":0.2, "Darryl":0.2, "Robert California":0.2},

    # Desk items
    "bobblehead":         {"Dwight":0.3, "Michael":0.2, "Andy Bernard":0.2, "Kelly":0.1, "Ryan":0.2},
    "photo":              {"Pam":0.3, "Jim":0.2, "Angela":0.1, "Toby":0.2, "Darryl":0.2},
    "puzzle":             {"Stanley":0.3, "Oscar":0.2, "Kevin":0.1, "Toby":0.2, "Creed":0.2},
    "mystery":            {"Creed":0.3, "Ryan":0.2, "Robert California":0.2, "Kevin":0.2, "Oscar":0.1},

    # Roles
    "leader":             {"Michael":0.3, "Dwight":0.2, "Andy Bernard":0.2, "Robert California":0.2, "Ryan":0.1},
    "prankster_role":     {"Jim":0.3, "Creed":0.2, "Kelly":0.2, "Darryl":0.2, "Ryan":0.1},
    "caretaker":          {"Pam":0.3, "Angela":0.2, "Oscar":0.2, "Toby":0.2, "Darryl":0.1},
    "quiet_role":         {"Stanley":0.3, "Kevin":0.2, "Toby":0.2, "Oscar":0.2, "Pam":0.1},
}

# -----------------------------
# Character trait blurbs (for explanations)
# -----------------------------
CHAR_TRAITS = {
    "Michael": "charismatic, approval-seeking, tries to motivate with heart and humor",
    "Jim": "dry wit, social glue, nudges culture with levity",
    "Pam": "steady, supportive, quietly competent and people-aware",
    "Dwight": "rules-forward, mission-first, meticulous planner",
    "Angela": "standards-focused, order-keeping, detail-driven",
    "Kevin": "laid-back, comfort-seeking, comic relief under stress",
    "Kelly": "expressive, social energy, loves recognition and fun",
    "Stanley": "practical, no-nonsense, values boundaries and calm",
    "Oscar": "accurate, policy- and clarity-oriented, analytical",
    "Creed": "unpredictable, weird, free-form problem solving",
    "Ryan": "ambitious, process/brand-aware, opportunistic",
    "Robert California": "enigmatic, persuasive, intense charisma",
    "Darryl": "grounded, dry humor, steady operator",
    "Andy Bernard": "pep & performance, approval and team hype",
    "Toby": "policy/HR minded, conflict-averse, calm/reserved",
}

# -----------------------------
# Fun one-liners for character reveals
# -----------------------------
CHAR_JOKES = {
    "Michael": "World’s Best Boss mug not included. (He bought it himself.)",
    "Jim": "Your pranks are harmless… mostly. Dwight’s stapler is nervous.",
    "Pam": "You’re the glue. Also the art. Also the receptionist. Triple threat.",
    "Dwight": "Identity theft is not a joke, Jim! Thousands of families suffer every year.",
    "Angela": "There are rules. And sub-rules. And cat-based bylaws.",
    "Kevin": "Why waste time say lot word when few word do trick? Also: chili.",
    "Kelly": "Fashion show at lunch! Also, did you get my text? And my other 47?",
    "Stanley": "Did I stutter? Wake me when it’s Pretzel Day.",
    "Oscar": "Technically… you’re correct. (The best kind of correct.)",
    "Creed": "You have a lot of experience… in something. Don’t ask follow-ups.",
    "Ryan": "Temp today, corporate tomorrow. (Then startup. Then… we don’t talk about it.)",
    "Robert California": "You don’t care if this makes sense. You only care if you feel it.",
    "Darryl": "Low drama, high forklift certification energy.",
    "Andy Bernard": "A-ca-awesome. Prepare the Nard-Dog a cappella solo.",
    "Toby": "Please keep it down. Also, here’s a form about keeping it down.",
}

# -----------------------------
# Human-readable behavior labels (for explanations)
# -----------------------------
ARCHETYPE_DESC = {
    "planner": "structured planning and checklists",
    "joker": "lightening the mood with humor",
    "motivator": "pep talks and rallying the team",
    "quiet_worker": "heads-down, low-drama execution",
    "confront": "direct confrontation to resolve issues",
    "prankster": "playful pranks and mischievous humor",
    "escalate_hr": "going through policy/HR channels",
    "shrug_it_off": "letting small slights go",
    "networking": "networking and socializing",
    "family_time": "family/security priorities",
    "quirky_project": "quirky personal projects",
    "relax_plan": "low-key rest and light planning",
    "joke_meeting": "jokes during meetings",
    "zone_out": "checking out in boring moments",
    "serious_notes": "serious notes, docs, and templates",
    "weird_thoughts": "odd or offbeat thinking",
    "clarify": "asking clarifying questions",
    "loyalist": "backing leadership and figuring it out later",
    "lighten_tension": "defusing tension with humor",
    "wait_watch": "waiting and watching before acting",
    "plan_party": "organizing events and details",
    "karaoke": "high-energy social fun (karaoke/games)",
    "bring_food": "sharing food and caretaking gestures",
    "skip_event": "skipping optional social events",
    "rules_push": "pushing through via rules/structure",
    "fun_distract": "using fun to manage stress",
    "withdraw": "quietly stepping back",
    "snack": "comfort snacks to cope",
    "recognition": "seeking recognition/status",
    "security": "seeking stability/security",
    "order": "order, rules, and process",
    "paycheck": "just here for the paycheck",
    "bobblehead": "quirky desk flair",
    "photo": "family-first desk vibes",
    "puzzle": "puzzles and calm focus",
    "mystery": "odd or mysterious trinkets",
    "leader": "taking the lead and coordinating",
    "prankster_role": "being the playful one on the team",
    "caretaker": "supporting and looking after others",
    "quiet_role": "quiet, reliable contributor",
}

# ---------------------------------------------------
# QUESTION_POOL: put ALL your questions here (any length)
# Each option references an archetype key above.
# ---------------------------------------------------
QUESTION_POOL = [
    {"q": "How do you prepare for a team project deadline?",
     "options": [("Create a detailed plan and timeline.", "planner"),
                 ("Crack jokes to keep the mood light.", "joker"),
                 ("Give a pep talk and rally the team.", "motivator"),
                 ("Quietly focus and do your part.", "quiet_worker")]},
    {"q": "A coworker takes credit for your idea. Your move?",
     "options": [("Confront them directly and set the record straight.", "confront"),
                 ("Plan a harmless prank as payback.", "prankster"),
                 ("Escalate it to HR/management.", "escalate_hr"),
                 ("Let it go and move on.", "shrug_it_off")]},
    {"q": "Your ideal weekend looks like…",
     "options": [("Networking or social events.", "networking"),
                 ("Quality time with family/loved ones.", "family_time"),
                 ("Quirky hobby or side project.", "quirky_project"),
                 ("Relaxing and planning the week ahead.", "relax_plan")]},
    {"q": "During a boring meeting, you’re most likely to…",
     "options": [("Crack a joke.", "joke_meeting"),
                 ("Zone out.", "zone_out"),
                 ("Take serious notes.", "serious_notes"),
                 ("Let your mind wander somewhere weird.", "weird_thoughts")]},
    {"q": "Your boss makes a confusing announcement. You…",
     "options": [("Ask clarifying questions.", "clarify"),
                 ("Back the boss—figure it out later.", "loyalist"),
                 ("Tell a joke to lighten the tension.", "lighten_tension"),
                 ("Stay quiet and wait it out.", "wait_watch")]},
    {"q": "Coworker’s birthday party coming up. You…",
     "options": [("Plan decor and cake.", "plan_party"),
                 ("Pitch karaoke or dancing.", "karaoke"),
                 ("Bring food and enjoy.", "bring_food"),
                 ("Try to skip it.", "skip_event")]},
    {"q": "When you’re stressed at work, you…",
     "options": [("Push through with rules and structure.", "rules_push"),
                 ("Distract with something fun.", "fun_distract"),
                 ("Withdraw for quiet time.", "withdraw"),
                 ("Snack your way through it.", "snack")]},
    {"q": "What motivates you most at work?",
     "options": [("Recognition.", "recognition"),
                 ("Family/security.", "security"),
                 ("Order and clear rules.", "order"),
                 ("The paycheck.", "paycheck")]},
    {"q": "Pick a desk accessory:",
     "options": [("A bobblehead.", "bobblehead"),
                 ("A framed family photo.", "photo"),
                 ("A crossword puzzle book.", "puzzle"),
                 ("A mysterious trinket you found.", "mystery")]},
    {"q": "How do you see your role on a team?",
     "options": [("The leader.", "leader"),
                 ("The prankster.", "prankster_role"),
                 ("The caretaker.", "caretaker"),
                 ("The quiet workhorse.", "quiet_role")]},
    # 35 more (same as before) ...
    {"q":"New process is rolling out with vague instructions. First move?",
     "options":[("Draft your own SOP from what’s known.","planner"),
                ("Crack a joke about the chaos.","joker"),
                ("Gather everyone and motivate alignment.","motivator"),
                ("Focus on your tasks while it clarifies.","quiet_worker")]},
    {"q":"Your teammate is behind schedule.",
     "options":[("Set a structure/checklist to help.","planner"),
                ("Lighten the mood and offer help.","joker"),
                ("Give an encouraging pep talk.","motivator"),
                ("Quietly pick up some slack.","quiet_worker")]},
    {"q":"The printer jammed for the 5th time today.",
     "options":[("Follow the manual step-by-step.","order"),
                ("Make a joke and call it cursed.","joke_meeting"),
                ("Ask office admin/HR to replace it.","escalate_hr"),
                ("Sigh and walk away for now.","withdraw")]},
    {"q":"You discover a policy violation that affects your work.",
     "options":[("Report it up the chain.","escalate_hr"),
                ("Confront the person violating it.","confront"),
                ("Joke privately about how silly it is.","prankster"),
                ("Do your job; let others handle it.","quiet_worker")]},
    {"q":"A last-minute presentation appears on your calendar.",
     "options":[("Create a rapid plan with bullet points.","planner"),
                ("Open with a light joke.","joker"),
                ("Pep talk: 'We’ve got this.'","motivator"),
                ("Keep it short and focused.","quiet_worker")]},
    {"q":"You’re asked to lead a new initiative.",
     "options":[("Yes—set structure and KPIs.","leader"),
                ("Yes—make it fun so people join in.","motivator"),
                ("Maybe—if there’s proper recognition.","recognition"),
                ("No—stay in your lane.","quiet_role")]},
    {"q":"Team conflict breaks out on Slack.",
     "options":[("Set rules for discussion.","order"),
                ("Drop a meme to cool it off.","fun_distract"),
                ("Facilitate a calm resolution.","caretaker"),
                ("Mute and continue your work.","withdraw")]},
    {"q":"Budget cuts: one subscription has to go.",
     "options":[("Build an objective rubric to decide.","serious_notes"),
                ("Vote with a fun poll.","joke_meeting"),
                ("Escalate to manager/finance.","escalate_hr"),
                ("Cut the most unused and move on.","quiet_worker")]},
    {"q":"Your coworker gets a promotion you wanted.",
     "options":[("Ask for feedback and plan growth.","clarify"),
                ("Congratulations + a joke about it.","lighten_tension"),
                ("Privately escalate your concerns.","escalate_hr"),
                ("Let it go; focus on your wins.","shrug_it_off")]},
    {"q":"Company all-hands starts late—again.",
     "options":[("Post a timetable suggestion.","planner"),
                ("Post a pun in the chat.","joker"),
                ("Post encouragement to keep energy up.","motivator"),
                ("Do other work until it starts.","quiet_worker")]},
    {"q":"A teammate is obviously burnt out.",
     "options":[("Offer structured help and coverage plan.","caretaker"),
                ("Tell a joke and send them a snack.","fun_distract"),
                ("Encourage time off and notify manager.","escalate_hr"),
                ("Quietly take tasks off their plate.","quiet_role")]},
    {"q":"Your manager asks for weekend availability.",
     "options":[("Ask clarifying Qs about urgency.","clarify"),
                ("Agree with a positive spin.","loyalist"),
                ("Deflect with humor if unreasonable.","lighten_tension"),
                ("Stay quiet if it’s optional.","wait_watch")]},
    {"q":"Team offsite theme?",
     "options":[("Structured workshop + outcomes.","planner"),
                ("Karaoke + games.","karaoke"),
                ("Service project together.","caretaker"),
                ("Low-key hangout, minimal agenda.","relax_plan")]},
    {"q":"Unexpected production bug.",
     "options":[("Create a triage process ASAP.","order"),
                ("Keep team calm with levity.","fun_distract"),
                ("Coordinate who does what.","leader"),
                ("Silently fix what you can.","quiet_worker")]},
    {"q":"Approach to learning a new tool?",
     "options":[("Write your own quickstart guide.","planner"),
                ("Find the funniest tutorial.","joker"),
                ("Start a study group for it.","motivator"),
                ("Deep dive solo in silence.","withdraw")]},
    {"q":"You discover a hidden supply closet.",
     "options":[("Inventory and label everything.","order"),
                ("Make a joke about hoarding.","joke_meeting"),
                ("Create a checkout system.","serious_notes"),
                ("Pocket a weird item.","mystery")]},
    {"q":"Coworker misses a deadline and blames the tool.",
     "options":[("Offer structure and training plan.","planner"),
                ("Make a light joke and move on.","joker"),
                ("Cheer them on; they’ll get it.","motivator"),
                ("Do your part; avoid drama.","quiet_worker")]},
    {"q":"New intern joins your team.",
     "options":[("Create a clear onboarding checklist.","serious_notes"),
                ("Break the ice with humor.","joke_meeting"),
                ("Mentor them actively.","caretaker"),
                ("Leave them to explore independently.","quiet_role")]},
    {"q":"The office coffee tastes awful.",
     "options":[("Propose a coffee rotation plan.","planner"),
                ("Make a joke and drink it anyway.","lighten_tension"),
                ("Escalate to office ops.","escalate_hr"),
                ("Bring your own; say nothing.","withdraw")]},
    {"q":"Company announces a surprise reorg.",
     "options":[("Ask for org charts and clarity.","clarify"),
                ("Pump people up: change = opportunity.","motivator"),
                ("Crack a joke to ease tension.","joker"),
                ("Wait for details; keep working.","wait_watch")]},
    {"q":"Your teammate wants to ship without QA.",
     "options":[("Set rules—no ship without checks.","order"),
                ("Joke about living dangerously.","joke_meeting"),
                ("Escalate to the lead.","escalate_hr"),
                ("Do minimal viable check and ship.","quiet_worker")]},
    {"q":"An optional after-hours hangout is planned.",
     "options":[("Organize details and sign-up sheet.","planner"),
                ("Pitch karaoke afterwards.","karaoke"),
                ("Suggest inclusive activities.","caretaker"),
                ("Skip and relax at home.","relax_plan")]},
    {"q":"You’re asked to write a policy doc.",
     "options":[("Structure with bullet-proof sections.","serious_notes"),
                ("Open with a witty intro.","joker"),
                ("Co-author with the team.","leader"),
                ("Keep it short; just the essentials.","quiet_worker")]},
    {"q":"The team wins a big deal. You celebrate by…",
     "options":[("Organizing a little party.","plan_party"),
                ("Karaoke night!","karaoke"),
                ("Bringing food for everyone.","bring_food"),
                ("A quiet pat on the back.","quiet_role")]},
    {"q":"A teammate makes a small but public error.",
     "options":[("Correct kindly and document process.","caretaker"),
                ("Defuse with a joke.","lighten_tension"),
                ("Escalate to the manager to fix.","escalate_hr"),
                ("Let it slide; not a big deal.","shrug_it_off")]},
    {"q":"You notice inconsistent meeting notes.",
     "options":[("Create a shared template.","planner"),
                ("Nickname the meeting for fun.","joker"),
                ("Motivate a rotating note-taker.","leader"),
                ("Take your own quiet notes.","quiet_worker")]},
    {"q":"Company swag choices:",
     "options":[("Organized notebook set.","serious_notes"),
                ("Funny T-shirt.","joke_meeting"),
                ("Charity tie-in swag.","caretaker"),
                ("Plain mug; no fuss.","quiet_role")]},
    {"q":"Someone is chronically late to meetings.",
     "options":[("Propose a timing rule.","order"),
                ("Make a running joke of it.","fun_distract"),
                ("Suggest a private check-in.","clarify"),
                ("Ignore it; get to work.","quiet_worker")]},
    {"q":"You have a brilliant idea.",
     "options":[("Outline a plan before sharing.","planner"),
                ("Tease it with humor first.","joker"),
                ("Rally support enthusiastically.","motivator"),
                ("Pilot quietly and show results.","quiet_worker")]},
    {"q":"Team lunch order?",
     "options":[("Coordinate dietary needs and orders.","caretaker"),
                ("Crack jokes about everyone’s picks.","joke_meeting"),
                ("Escalate to finance for reimbursement rules.","escalate_hr"),
                ("Pack your own lunch.","quiet_role")]},
    {"q":"Unexpected visitor tours the office.",
     "options":[("Give a structured mini-tour.","leader"),
                ("Make it entertaining!","motivator"),
                ("Point them to official channels.","escalate_hr"),
                ("Return to work; wave politely.","quiet_worker")]},
    {"q":"Favorite meeting format:",
     "options":[("Agenda with time boxes.","serious_notes"),
                ("Stand-up with a joke or two.","joke_meeting"),
                ("Round-robin encouragements.","motivator"),
                ("Async notes; minimal meetings.","withdraw")]},
    {"q":"Pet peeve at work?",
     "options":[("Lack of process.","order"),
                ("Low morale.","fun_distract"),
                ("Unclear responsibilities.","clarify"),
                ("Noise and interruptions.","withdraw")]},
    {"q":"Task estimation style:",
     "options":[("Breakdown and buffer.","planner"),
                ("Optimistic and upbeat.","motivator"),
                ("Realistic and rules-based.","order"),
                ("Do it, don’t talk about it.","quiet_worker")]},
    {"q":"Preferred recognition:",
     "options":[("Public shout-out.","recognition"),
                ("Personal note from manager.","security"),
                ("Badge/certification system.","order"),
                ("No recognition needed.","paycheck")]},
    {"q":"Coffee break time:",
     "options":[("Organize a quick stand-up.","leader"),
                ("Tell a funny story.","joker"),
                ("Check how others are doing.","caretaker"),
                ("Sip quietly at your desk.","quiet_role")]},
    {"q":"Email style:",
     "options":[("Bulleted, structured, clear.","serious_notes"),
                ("Warm opener with levity.","lighten_tension"),
                ("CC the right people for clarity.","clarify"),
                ("Short and to the point.","quiet_worker")]},
    {"q":"Office playlist control:",
     "options":[("Create a shared rules doc.","order"),
                ("Make it a fun rotating DJ.","fun_distract"),
                ("Vote for inclusive picks.","caretaker"),
                ("Headphones; no playlist needed.","withdraw")]},
    {"q":"You find out snacks are disappearing overnight.",
     "options":[("Install a sign-out sheet.","serious_notes"),
                ("Make a running joke about a snack bandit.","joke_meeting"),
                ("Raise it to office manager.","escalate_hr"),
                ("Bring your own snacks instead.","snack")]},
    {"q":"Client pushes for scope creep.",
     "options":[("Set clear boundaries/process.","order"),
                ("Add humor while pushing back.","lighten_tension"),
                ("Escalate to account lead.","escalate_hr"),
                ("Deliver MVP quietly.","quiet_worker")]},
    {"q":"Team photo day:",
     "options":[("Coordinate outfits/locations.","planner"),
                ("Silly props!","fun_distract"),
                ("Inclusive timing for all.","caretaker"),
                ("Skip photos; do work.","quiet_role")]},
    {"q":"Where do you keep your best ideas?",
     "options":[("A tidy, structured doc.","serious_notes"),
                ("A running jokes + ideas chat.","joke_meeting"),
                ("A team board with encouragements.","motivator"),
                ("A private notebook.","withdraw")]},
    {"q":"When you disagree in a meeting, you…",
     "options":[("Propose a structured alternative.","planner"),
                ("Use humor to soften your stance.","joker"),
                ("Encourage discussion and alignment.","leader"),
                ("Hold your view; follow up later quietly.","quiet_worker")]},
]

# ----------------- Helpers -----------------
def normalize(scores):
    total = sum(scores.values())
    if total <= 0:
        return {c: 0.0 for c in CHARACTERS}
    return {c: (scores.get(c, 0.0) / total) * 100.0 for c in CHARACTERS}

def tally_scores(archetypes):
    scores = defaultdict(float)
    for arch in archetypes:
        for char, w in ARCHETYPE_WEIGHTS.get(arch, {}).items():
            scores[char] += w
    return scores

def per_character_contributions(selected_archetypes):
    """
    Returns: dict[character] -> dict[archetype] -> contribution weight
    """
    contrib = defaultdict(lambda: defaultdict(float))
    for arch in selected_archetypes:
        for char, w in ARCHETYPE_WEIGHTS.get(arch, {}).items():
            contrib[char][arch] += w
    return contrib

def summarize_reason_for_char(char, char_pct, char_contribs, top_k=3):
    """
    Build a readable reason string for one character:
    - top contributing archetypes with human-readable names
    - brief trait blurb
    - fun one-liner joke
    """
    if not char_contribs:
        base = f"**{char} — {char_pct:.1f}%**"
        joke = CHAR_JOKES.get(char)
        if joke:
            base += f"\n\n> {joke}"
        return base

    total = sum(char_contribs.values()) or 1.0
    top_arch = sorted(char_contribs.items(), key=lambda x: x[1], reverse=True)[:top_k]

    bits = []
    for a, v in top_arch:
        desc = ARCHETYPE_DESC.get(a, a.replace('_',' '))
        share = (v / total) * 100.0
        bits.append(f"{desc} (~{share:.0f}%)")

    traits = CHAR_TRAITS.get(char, "").strip()
    joined = "; ".join(bits)
    base = (
        f"**{char} — {char_pct:.1f}%**  \n"
        f"Top signals: {joined}.  \n"
        f"Why it fits: _{traits}_."
    ) if traits else (
        f"**{char} — {char_pct:.1f}%**  \n"
        f"Top signals: {joined}."
    )

    # Add a fun one-liner
    joke = CHAR_JOKES.get(char)
    if joke:
        base += f"\n\n> {joke}"
    return base

def reset_quiz():
    # Keep the user's slider selection; only clear quiz state
    for k in list(st.session_state.keys()):
        if k.startswith(("q_", "quiz_order", "sampled_qs", "submitted", "sampled_qs_count")):
            try:
                del st.session_state[k]
            except KeyError:
                pass
    st.rerun()

# ----------------- UI -----------------
st.set_page_config(page_title="Which Office Character Are You?", page_icon="🧑‍💼", layout="centered")
st.title("Which Office Character Are You?")
st.caption("Answer honestly. Don't be a weirdo.")

# ---- Slider: choose how many questions (30–50). Preserve and resample on change.
default_qs = 45
question_count = st.sidebar.slider(
    "How many questions?",
    min_value=30,
    max_value=min(50, len(QUESTION_POOL)),
    value=min(default_qs, len(QUESTION_POOL)),
    step=1,
    key="question_count"
)

# Decide if we need to resample (first load or the slider changed)
need_resample = (
    "sampled_qs" not in st.session_state
    or st.session_state.get("sampled_qs_count") != st.session_state.question_count
)

if need_resample:
    sampled = random.sample(QUESTION_POOL, k=st.session_state.question_count)
    random.shuffle(sampled)  # randomize order of questions
    randomized = []
    for q in sampled:
        opts = q["options"][:]
        random.shuffle(opts)
        randomized.append({"q": q["q"], "options": opts})
    st.session_state.sampled_qs = randomized
    st.session_state.sampled_qs_count = st.session_state.question_count

with st.form("quiz"):
    selections = []
    total_qs = len(st.session_state.sampled_qs)
    st.caption(f"Loaded {total_qs} questions from a pool of {len(QUESTION_POOL)}.")
    for i, qd in enumerate(st.session_state.sampled_qs, start=1):
        st.markdown(f"### Q{i}/{total_qs}. {qd['q']}")
        labels = [opt[0] for opt in qd["options"]]
        values = [opt[1] for opt in qd["options"]]
        choice = st.radio(
            "Choose one:",
            options=list(range(len(labels))),
            format_func=lambda idx, labels=labels: labels[idx],
            key=f"q_{i}",
            horizontal=False,
        )
        selections.append(values[choice])
        st.divider()

    submit = st.form_submit_button("Show my result")

col1, col2 = st.columns(2)
with col1:
    if st.button("🔁 Restart quiz"):
        reset_quiz()
with col2:
    st.write("")

if submit:
    raw = tally_scores(selections)
    pct = normalize(raw)
    ranked = sorted(pct.items(), key=lambda x: x[1], reverse=True)

    # Compute per-character contribution breakdown and explain top 3
    contrib = per_character_contributions(selections)

    st.subheader("Your Top Matches (with reasons)")
    top3 = ranked[:3]
    for idx, (char, val) in enumerate(top3, start=1):
        reason = summarize_reason_for_char(char, val, contrib.get(char, {}), top_k=3)
        st.markdown(f"**{idx}.** {reason}")

    with st.expander("See full breakdown"):
        for char, val in ranked:
            st.write(f"- {char}: {val:.1f}%")

    st.info(
        "These explanations look at which behaviors you chose most often "
        "(e.g., planning, clarifying, joking) and how they map—fractionally—to multiple characters."
    )
