import streamlit as st
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")
st.markdown("A smart pet care management system for busy pet owners.")

# ---- Session State Setup ----
if "owner" not in st.session_state:
    st.session_state.owner = None
if "scheduler" not in st.session_state:
    st.session_state.scheduler = None

st.divider()

# ---- Section 1: Owner Setup ----
st.subheader("👤 Step 1: Enter Owner Info")
col1, col2 = st.columns(2)
with col1:
    owner_name = st.text_input("Owner Name", value="Sarah")
with col2:
    owner_email = st.text_input("Owner Email", value="sarah@email.com")

if st.button("Create Owner"):
    st.session_state.owner = Owner(name=owner_name, email=owner_email)
    st.session_state.scheduler = Scheduler(st.session_state.owner)
    st.success(f"✅ Owner '{owner_name}' created successfully!")

st.divider()

# ---- Section 2: Add Pets ----
st.subheader("🐶 Step 2: Add a Pet")

if st.session_state.owner is None:
    st.warning("⚠️ Please create an owner first!")
else:
    col1, col2, col3 = st.columns(3)
    with col1:
        pet_name = st.text_input("Pet Name", value="Buddy")
    with col2:
        pet_species = st.selectbox("Species", ["Dog", "Cat", "Rabbit", "Bird", "Other"])
    with col3:
        pet_breed = st.text_input("Breed", value="Golden Retriever")

    if st.button("Add Pet"):
        new_pet = Pet(name=pet_name, species=pet_species, breed=pet_breed)
        st.session_state.owner.add_pet(new_pet)
        st.success(f"✅ Pet '{pet_name}' added successfully!")

    if st.session_state.owner.pets:
        st.markdown("**Current Pets:**")
        for pet in st.session_state.owner.pets:
            st.markdown(f"- 🐾 **{pet.name}** ({pet.species} — {pet.breed})")

st.divider()

# ---- Section 3: Add Tasks ----
st.subheader("📋 Step 3: Add a Task")

if st.session_state.owner is None or not st.session_state.owner.pets:
    st.warning("⚠️ Please create an owner and add at least one pet first!")
else:
    pet_names = [pet.name for pet in st.session_state.owner.pets]

    col1, col2 = st.columns(2)
    with col1:
        selected_pet = st.selectbox("Select Pet", pet_names)
        task_description = st.text_input("Task Description", value="Morning Walk")
        task_time = st.text_input("Due Time (HH:MM)", value="08:00")
    with col2:
        task_priority = st.selectbox("Priority", ["high", "medium", "low"])
        task_frequency = st.selectbox("Frequency", ["daily", "weekly", "once"])

    if st.button("Add Task"):
        for pet in st.session_state.owner.pets:
            if pet.name == selected_pet:
                new_task = Task(
                    description=task_description,
                    due_time=task_time,
                    frequency=task_frequency,
                    priority=task_priority
                )
                pet.add_task(new_task)
                st.success(f"✅ Task '{task_description}' added to {selected_pet}!")
                break

st.divider()

# ---- Section 4: Generate Daily Plan ----
st.subheader("📅 Step 4: Generate Daily Plan")

if st.session_state.scheduler is None or not st.session_state.owner or not st.session_state.owner.pets:
    st.warning("⚠️ Please set up your owner, pets, and tasks first!")
else:
    if st.button("Generate Schedule"):
        plan = st.session_state.scheduler.generate_daily_plan()
        conflicts = st.session_state.scheduler.detect_conflicts()

        if not plan:
            st.info("No tasks found. Add some tasks first!")
        else:
            if conflicts:
                st.error(f"⚠️ {len(conflicts)} Conflict(s) Detected!")
                for conflict in conflicts:
                    time, first, second = conflict
                    st.warning(
                        f"Conflict at **{time}**: {first[0]}'s '{first[1].description}' "
                        f"vs {second[0]}'s '{second[1].description}'"
                    )
            else:
                st.success("✅ No conflicts detected!")

            st.markdown("### 🗓️ Daily Plan")

            for item in plan:
                status = "✅" if item["completed"] else "⏳"
                conflict_flag = item["conflict"]

                if conflict_flag:
                    st.error(
                        f"{status} **{item['time']}** | 🐾 {item['pet']} | "
                        f"{item['task']} | Priority: `{item['priority']}` {conflict_flag}"
                    )
                elif item["priority"] == "high":
                    st.success(
                        f"{status} **{item['time']}** | 🐾 {item['pet']} | "
                        f"{item['task']} | Priority: `{item['priority']}`"
                    )
                elif item["priority"] == "medium":
                    st.info(
                        f"{status} **{item['time']}** | 🐾 {item['pet']} | "
                        f"{item['task']} | Priority: `{item['priority']}`"
                    )
                else:
                    st.markdown(
                        f"{status} **{item['time']}** | 🐾 {item['pet']} | "
                        f"{item['task']} | Priority: `{item['priority']}`"
                    )

            st.divider()
            st.markdown("### 🔥 Tasks by Priority")
            priority_sorted = st.session_state.scheduler.sort_by_priority()
            for pet_name, task in priority_sorted:
                st.markdown(
                    f"- **[{task.priority.upper()}]** {pet_name}: "
                    f"{task.description} at {task.due_time}"
                )