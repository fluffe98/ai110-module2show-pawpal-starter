from pawpal_system import Owner, Pet, Task, Scheduler
from datetime import date

# Create Owner
owner = Owner(name="Sarah", email="sarah@email.com")

# Create Pets
dog = Pet(name="Buddy", species="Dog", breed="Golden Retriever")
cat = Pet(name="Whiskers", species="Cat", breed="Persian")

# Add Tasks to Buddy (Dog)
dog.add_task(Task(
    description="Morning Walk",
    due_time="08:00",
    frequency="daily",
    priority="high"
))
dog.add_task(Task(
    description="Feeding",
    due_time="09:00",
    frequency="daily",
    priority="high"
))
dog.add_task(Task(
    description="Evening Walk",
    due_time="17:00",
    frequency="daily",
    priority="medium"
))

# Add Tasks to Whiskers (Cat)
cat.add_task(Task(
    description="Feeding",
    due_time="09:00",  # Same time as Buddy - triggers conflict!
    frequency="daily",
    priority="high"
))
cat.add_task(Task(
    description="Medication",
    due_time="12:00",
    frequency="daily",
    priority="high"
))
cat.add_task(Task(
    description="Grooming",
    due_time="15:00",
    frequency="weekly",
    priority="low"
))

# Add pets to owner
owner.add_pet(dog)
owner.add_pet(cat)

# Create Scheduler
scheduler = Scheduler(owner)

# Print Daily Plan
print("=" * 50)
print(f"🐾 Daily Care Plan for {owner.name}'s Pets")
print("=" * 50)

plan = scheduler.generate_daily_plan()
for item in plan:
    status = "✅" if item["completed"] else "⏳"
    conflict = item["conflict"]
    print(f"{status} {item['time']} | {item['pet']:<10} | {item['task']:<20} | Priority: {item['priority']:<6} {conflict}")

# Print Conflicts
print("\n" + "=" * 50)
print("⚠️  Conflict Detection")
print("=" * 50)
conflicts = scheduler.detect_conflicts()
if conflicts:
    for conflict in conflicts:
        time, first, second = conflict
        print(f"Conflict at {time}: {first[0]}'s '{first[1].description}' vs {second[0]}'s '{second[1].description}'")
else:
    print("No conflicts detected!")

# Print Filtered - Pending Tasks Only
print("\n" + "=" * 50)
print("📋 Pending Tasks Only")
print("=" * 50)
pending = scheduler.filter_by_status(completed=False)
for pet_name, task in pending:
    print(f"  {pet_name}: {task.description} at {task.due_time}")

# Print Sorted by Priority
print("\n" + "=" * 50)
print("🔥 Tasks Sorted by Priority")
print("=" * 50)
priority_tasks = scheduler.sort_by_priority()
for pet_name, task in priority_tasks:
    print(f"  [{task.priority.upper()}] {pet_name}: {task.description} at {task.due_time}")