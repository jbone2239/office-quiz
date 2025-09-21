1) Characters as overlapping behavioral profiles

Modeled each character as a blend of workplace behaviors (archetypes). A single answer never maps 100% to one character; instead it contributes fractional credit to several characters who plausibly exhibit that behavior. This mirrors the show: e.g., Jim jokes a lot, but so do Michael and Andy—just in different flavors.

2) Archetype → character mapping logic

Each archetype’s weights reflect how strongly and consistently a character exhibits that behavior in canon:

planner → {Dwight 0.4, Angela 0.2, Ryan 0.2, Oscar 0.1, Toby 0.1}
Dwight is hyper-structured (SOPs, security drills) → largest share.
Angela is detail/controls oriented (party planning “rules”).
Ryan shows “process-y” ambition during corporate phases.
Oscar/Toby add mild structure via policy/HR/compliance.

joker → {Jim 0.3, Michael 0.2, Kevin 0.2, Andy 0.2, Darryl 0.1}
Jim is the archetypal prankster (highest).
Michael/Andy use humor for attention/connection; Kevin for levity; Darryl is dry-witty.

motivator → {Michael 0.3, Andy 0.3, Pam 0.2, Kelly 0.1, Robert California 0.1}
Michael/Andy lead with pep, musical hype, “family” energy.
Pam’s quiet encouragement shows up often.
Kelly/Robert add performative/charismatic spin.

quiet_worker → {Pam 0.3, Stanley 0.2, Oscar 0.2, Toby 0.2, Darryl 0.1}
Pam gets heads-down work done; Stanley/Toby avoid drama; Oscar is diligent/accurate; Darryl steady.

confront → {Dwight 0.3, Angela 0.2, Andy 0.2, Michael 0.2, Robert California 0.1}
Dwight/Angela assert rules; Andy/Michael confront (often awkwardly); Robert is calmly forceful.

escalate_hr → {Toby 0.4, Oscar 0.3, Angela 0.2, Stanley 0.1}
HR escalation = Toby lead; Oscar’s procedural correctness; Angela rule-enforcement; Stanley minimal.

prankster / joke_meeting / lighten_tension distribute across Jim, Michael, Andy, Kelly, Darryl, Kevin with different mixes to reflect snark vs slapstick vs hype.

order / serious_notes bias toward Dwight, Angela, Oscar, Ryan, Toby (policy, accuracy, compliance).

recognition favors Michael, Kelly, Andy, Ryan, Robert (status/ego/brand).

paycheck / withdraw / quiet_role weight Stanley, Toby, Pam, Creed, Kevin depending on disengagement vs stoic focus.

weird_thoughts / mystery give Creed the largest share, with Robert California/Ryan getting some “enigmatic” spillover.

3) Anti-gaming by design

Fractional credit: Every option contributes to multiple characters → no obvious “Dwight-only” choice.

Diffuse archetypes: Similar behaviors appear in varied contexts (deadline, party, reorg), so cherry-picking answers spreads points.

Randomized order (questions + options): Removes memorized patterns.

4) Fairness + face validity

Face validity: If you read an option (e.g., “create a checklist”), the top recipient (Dwight/Angela) “feels right,” while others receive smaller plausible credit (Oscar/Toby).

Balance: No character dominates across many archetypes; jokers also earn points for leadership/recognition in some items, just as in the show.

Normalization: Results are shown as percentages, preventing a single extreme answer from locking a label.

5) Calibration approach (how we set the numbers)

Canonical traits: Start from widely recognized character behaviors.

Primary/secondary/tertiary: Assign ~0.3–0.4 to the most aligned character, ~0.2 to secondary fits, ~0.1 to tertiary fits.

Coverage sweep: Ensure each character receives credit from multiple archetypes (not just one).

Conflict pairs: Include archetypes that distinguish similar characters (e.g., Jim vs Michael both joke, but differ on recognition, leadership style, order).

Edge archetypes: Weirdness (Creed), charisma/ambiguity (Robert California), policy escalation (Toby) provide separation.

6) How to tune (if you collect data)

Outcome inspection: If “Dwight” shows up too often overall, reduce his primary weights by 0.05 on 2–3 archetypes and redistribute to secondaries.

Item discrimination: Identify questions where one answer overly drives a single character; shift 0.05–0.1 of weight into two plausible neighbors.

Internal consistency: Add two variants of the same behavior in different contexts; users gaming for one character will leak points on the variant.

A/B test: Randomly swap a few items/archetype weights and compare distribution of top matches across cohorts; aim for even spread while preserving face validity.

Person-fit check (optional): Track how often a user picks within the same “family” (structure/levity/quiet/escalate). If >70% in one family, slightly shrink the dominant family’s weights (e.g., ×0.9) before normalization to dampen intentional min-maxing.

7) Why percentages (not a single label)

People are multi-trait. Showing top 3 with percentages acknowledges nuance (e.g., “35% Jim, 27% Pam, 18% Darryl”), which aligns with the quiz’s multi-archetype scoring and reduces disappointment from a single forced label.
