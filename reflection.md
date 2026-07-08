# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

For the three main core actions, we should be able to edit, add, and remove tasks for the pet’s care, and we should also be able to see the pet's daily routine and owner/pet information. For the initial design, I included the classes Owner, Pet, Tasks, Scheduler, and DailyRoutine. The Owner class can edit/view/add a pet and its associated daily tasks. The Pet class includes information/attributes of a pet. The Tasks class includes information about individual tasks. The Scheduler class can manage and track tasks, and the DailyRoutine class keeps track of pets' routines by date.

**b. Design changes**

After generating the new diagram using AI, I realized that the DailyRoutine class was redundant and I could just add the attributes to the Scheduler class instead. I also made these changes in the following classes:

*Task class
Added a unique id field (auto-generated UUID) so tasks can be reliably targeted for edit/remove even as the list changes.
Widened edit() from just (duration, priority) to also allow updating name and category, with all fields optional (only non-None values change).

*Pet class
Changed remove_task(task) to remove_task(task_id) — removal now targets a stable id instead of a list position that shifts when items are deleted.

*Owner class
Made the pets: list[Pet] attribute explicit to realize the "owns" relationship from the UML.

*Scheduler class
Removed the duplicated time_budget and generic tasks attributes (the time constraint now lives in one place: Owner.minutes_available).
Added scheduled and skipped result lists so the plan and its leftovers are stored on the object.
Simplified generate_plan(owner, pet) to generate_plan(owner) — it pulls tasks from all of the owner's pets and reads the time budget from the owner.
explain() now has stored results (scheduled/skipped) to describe, instead of having nothing to reference.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?

1. Task priority (primary sort key) — In pawpal_system.py:145, prioritize() sorts by -t.priority first. Higher-priority tasks (meds = 5, walk = 5) get placed before low-priority ones (laser play = 1). This is the dominant constraint.

2. Duration (tie-breaker + budget gate) — Within the same priority, shorter tasks come first (t.duration). This is deliberate: fitting the short task first leaves more room, so more tasks fit overall. Duration also acts as a hard gate — generate_plan() only schedules a task if task.duration <= budget remaining.

3. Time budget (Owner.minutes_available) — The scheduler is greedy against a fixed minutes budget; once it runs out, remaining tasks go to skipped rather than being crammed in.

4. Completion status — Already-completed tasks are filtered out (if not t.completed) so they don't consume budget.

5. Time-of-day (time) and due date — Used by sort_by_time() and conflict_warnings(), but note: these currently drive display and warnings, not the plan itself. The greedy fitter doesn't yet reorder around clock conflicts.

6. Preferences — Owner.preferences exists in the model but the scheduler does not read it yet. Honest gap worth naming in your reflection.

- How did you decide which constraints mattered most?

Priority is first because skipping a pet's medication is worse than skipping a play session. Duration is second and only as a tie-breaker, chosen to maximize task count within the budget rather than to honor a specific clock schedule.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.

The most important trade-off is that the scheduler optimizes how many important tasks fit, not when they happen. That's why time and preferences are tracked but not enforced.

- Why is that tradeoff reasonable for this scenario?

This tradeoff is reasonable because for a busy owner the priority is making sure the essential care tasks (like medication and walks) actually get done within their limited time, not that they happen at an exact minute. 

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
