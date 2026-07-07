import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This app plans a day of pet care tasks for an owner based on their available time
and each task's priority. Your logic layer lives in `pawpal_system.py`; this file
wires that logic to the Streamlit UI.
"""
)

# ---------------------------------------------------------------------------
# Session state: Streamlit re-runs this whole script on every interaction, so
# we stash the Owner in st.session_state (a per-session "vault" that survives
# re-runs). We only build a fresh Owner the first time; after that we reuse the
# one already in the vault so pets and tasks persist as the user clicks around.
# ---------------------------------------------------------------------------
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan", minutes_available=60)

owner: Owner = st.session_state.owner

PRIORITY_MAP = {"low": 1, "medium": 2, "high": 3}
PRIORITY_LABEL = {1: "low", 2: "medium", 3: "high"}

st.divider()

# ---------------------------------------------------------------------------
# Owner settings
# ---------------------------------------------------------------------------
st.subheader("Owner")
owner.name = st.text_input("Owner name", value=owner.name)
minutes = st.number_input(
    "Minutes available today",
    min_value=1,
    max_value=600,
    value=owner.minutes_available,
)
owner.set_availability(int(minutes))

st.divider()

# ---------------------------------------------------------------------------
# Add a pet -> Owner.add_pet(Pet(...))
# ---------------------------------------------------------------------------
st.subheader("Add a Pet")
with st.form("add_pet", clear_on_submit=True):
    pet_name = st.text_input("Pet name", value="Mochi")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    age = st.number_input("Age (years)", min_value=0, max_value=40, value=2)
    if st.form_submit_button("Add pet"):
        owner.add_pet(Pet(name=pet_name, species=species, age=int(age)))
        st.success(f"Added {pet_name} the {species}.")

if not owner.pets:
    st.info("No pets yet. Add one above to start planning tasks.")

st.divider()

# ---------------------------------------------------------------------------
# Add a task to a chosen pet -> Pet.add_task(Task(...))
# ---------------------------------------------------------------------------
if owner.pets:
    st.subheader("Add a Task")
    with st.form("add_task", clear_on_submit=True):
        pet_names = [p.name for p in owner.pets]
        chosen_pet_name = st.selectbox("For which pet?", pet_names)
        task_title = st.text_input("Task title", value="Morning walk")
        category = st.text_input("Category", value="walk")
        col1, col2 = st.columns(2)
        with col1:
            duration = st.number_input(
                "Duration (minutes)", min_value=1, max_value=240, value=20
            )
        with col2:
            priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

        if st.form_submit_button("Add task"):
            pet = next(p for p in owner.pets if p.name == chosen_pet_name)
            pet.add_task(
                Task(
                    name=task_title,
                    category=category,
                    duration=int(duration),
                    priority=PRIORITY_MAP[priority],
                )
            )
            st.success(f"Added '{task_title}' for {chosen_pet_name}.")

    # Show every task across all pets so the user can see what will be planned.
    tasks = owner.all_tasks()
    if tasks:
        st.write("Current tasks:")
        st.table(
            [
                {
                    "pet": next(
                        p.name for p in owner.pets if t in p.tasks
                    ),
                    "task": t.name,
                    "category": t.category,
                    "duration": t.duration,
                    "priority": PRIORITY_LABEL.get(t.priority, t.priority),
                    "done": t.completed,
                }
                for t in tasks
            ]
        )
    else:
        st.info("No tasks yet. Add one above.")

st.divider()

# ---------------------------------------------------------------------------
# Build the schedule -> Scheduler.generate_plan(owner) + Scheduler.explain()
# ---------------------------------------------------------------------------
st.subheader("Build Schedule")
st.caption("Fits as many high-priority tasks as possible into the available time.")

if st.button("Generate schedule"):
    if not owner.all_tasks():
        st.warning("Add at least one task before generating a schedule.")
    else:
        scheduler = Scheduler()
        scheduler.generate_plan(owner)
        st.text(scheduler.explain())
