import streamlit as st
from pawpal_system import Owner, Pet, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan")
if "scheduler" not in st.session_state:
    st.session_state.scheduler = Scheduler()

st.subheader("Quick Demo Inputs")
owner_name = st.text_input("Owner name", value=st.session_state.owner.name)
st.session_state.owner.name = owner_name
pet_name = st.text_input("Pet name", value="Mochi")
species = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Add pet"):
    existing_pet = st.session_state.owner.get_pet(pet_name)
    if existing_pet is not None:
        st.warning(f"Pet '{pet_name}' already exists.")
    else:
        st.session_state.owner.add_pet(Pet(name=pet_name, species=species))
        st.success(f"Added pet: {pet_name} ({species})")

if st.session_state.owner.pets:
    st.write("Current pets:")
    st.table(
        [
            {"pet": pet.name, "species": pet.species, "task_count": len(pet.tasks)}
            for pet in st.session_state.owner.pets
        ]
    )
else:
    st.info("No pets yet. Add one above.")

st.markdown("### Tasks")
st.caption("Schedule a task for one of your pets.")

pet_options = [pet.name for pet in st.session_state.owner.pets]
selected_pet_name = st.selectbox("Select pet", pet_options, disabled=not pet_options)

col1, col2 = st.columns(2)
with col1:
    task_title = st.text_input("Task description", value="Morning walk")
with col2:
    task_time = st.text_input("Task time (HH:MM)", value="07:00")

task_frequency = st.selectbox("Frequency", ["daily", "weekly", "as needed"], index=0)

if st.button("Add task"):
    if not pet_options:
        st.error("Add a pet before adding tasks.")
    else:
        pet = st.session_state.owner.get_pet(selected_pet_name)
        if pet is None:
            st.error("Selected pet was not found. Please try again.")
        else:
            pet.add_task(
                Task(
                    description=task_title,
                    time_of_day=task_time,
                    frequency=task_frequency,
                )
            )
            st.success(f"Added task for {selected_pet_name}: {task_title}")

all_tasks = st.session_state.scheduler.organize_tasks(
    st.session_state.owner,
    include_completed=True,
)

if all_tasks:
    st.write("Current tasks:")
    st.table(
        [
            {
                "time": task.time_of_day,
                "pet": task.pet_name,
                "task": task.description,
                "frequency": task.frequency,
                "completed": task.completed,
            }
            for task in all_tasks
        ]
    )
else:
    st.info("No tasks yet. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("Generate today's ordered plan using your scheduler logic.")

if st.button("Generate schedule"):
    daily_plan = st.session_state.scheduler.build_daily_plan(st.session_state.owner)
    if not daily_plan:
        st.info("No pending tasks to schedule yet.")
    else:
        st.success("Today's Schedule")
        st.table(
            [
                {
                    "time": task.time_of_day,
                    "pet": task.pet_name,
                    "task": task.description,
                    "frequency": task.frequency,
                }
                for task in daily_plan
            ]
        )
