# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
========================================
Today's Schedule for Miranda
Time available: 90 minutes
========================================
Scheduled 4 task(s) using 65 minute(s):
  • [Milo] Give medication (meds) — 5 min, priority 5
  • [Rex] Morning walk (walk) — 30 min, priority 5
  • [Rex] Dinner (feeding) — 10 min, priority 4
  • [Rex] Fetch training (enrichment) — 20 min, priority 2
Skipped 1 task(s) that didn't fit the time budget:
  • [Milo] Laser play (enrichment) — 45 min, priority 1
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

Confidence Level 3 stars
```
collecting ... collected 5 items

tests/test_pawpal.py::test_task_completion PASSED                        [ 20%]
tests/test_pawpal.py::test_task_addition PASSED                          [ 40%]
tests/test_pawpal.py::test_sort_by_time_is_chronological PASSED          [ 60%]
tests/test_pawpal.py::test_completing_daily_task_creates_next_days_occurrence PASSED [ 80%]
tests/test_pawpal.py::test_detect_conflicts_flags_duplicate_times PASSED [100%]

============================== 5 passed in 0.02s ===============================
```

## 📐 Smarter Scheduling

┌──────────────────┬──────────────────────────────────────────────────────────────┬──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ Feature          │ Method(s)                                                    │ Description                                                                                                              │
├──────────────────┼──────────────────────────────────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ Task Sorting     │ • Scheduler.prioritize()                                     │ Orders tasks by highest priority first. If priorities are equal, shorter-duration                                        │
│                  │ • Scheduler.sort_by_time()                                   │ tasks come first so more tasks fit. sort_by_time() sorts scheduled tasks by                                              │
│                  │                                                              │ "HH:MM", with unscheduled tasks placed last.                                                                             │
├──────────────────┼──────────────────────────────────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ Filtering        │ • Scheduler.generate_plan()                                  │ generate_plan() ignores completed tasks and moves tasks that exceed the remaining                                        │
│                  │ • Scheduler.filter_tasks()                                   │ time budget into the skipped list. filter_tasks() filters tasks by pet name                                              │
│                  │                                                              │ and/or completion status.                                                                                               │
├──────────────────┼──────────────────────────────────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ Conflict         │ • Scheduler.detect_conflicts()                               │ Detects overlapping scheduled tasks on the same due_date when one task's                                                 │
│ Handling         │ • Scheduler.conflict_warnings()                              │ duration extends past the next task's start time. Warnings are advisory only                                             │
│                  │                                                              │ and list the affected pet(s) and times.                                                                                  │
├──────────────────┼──────────────────────────────────────────────────────────────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ Recurring Tasks  │ • Task.recurring                                             │ Tasks support frequencies of "once", "daily", or "weekly". Completing a recurring                                        │
│                  │ • Task.next_occurrence()                                     │ task automatically creates its next occurrence with an updated due_date                                                  │
│                  │ • Pet.mark_task_complete()                                   │ using timedelta, correctly handling month and year rollovers.                                                            │
└──────────────────┴──────────────────────────────────────────────────────────────┴──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
