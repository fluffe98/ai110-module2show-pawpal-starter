from pawpal_system import Owner, Pet, Task, Scheduler
from datetime import date, timedelta

# ---- Setup Helper ----
def make_sample_owner():
    owner = Owner(name="Sarah", email="sarah@email.com")
    dog = Pet(name="Buddy", species="Dog", breed="Golden Retriever")
    cat = Pet(name="Whiskers", species="Cat", breed="Persian")
    dog.add_task(Task(description="Morning Walk", due_time="08:00", frequency="daily", priority="high"))
    dog.add_task(Task(description="Feeding", due_time="09:00", frequency="daily", priority="high"))
    cat.add_task(Task(description="Medication", due_time="12:00", frequency="daily", priority="high"))
    cat.add_task(Task(description="Grooming", due_time="15:00", frequency="weekly", priority="low"))
    owner.add_pet(dog)
    owner.add_pet(cat)
    return owner

# ---- Test 1: Task Completion ----
def test_task_mark_complete():
    task = Task(description="Walk", due_time="08:00", frequency="once", priority="high")
    assert task.completed == False
    task.mark_complete()
    assert task.completed == True

# ---- Test 2: Adding Task Increases Count ----
def test_add_task_increases_count():
    pet = Pet(name="Buddy", species="Dog", breed="Golden Retriever")
    assert len(pet.get_tasks()) == 0
    pet.add_task(Task(description="Walk", due_time="08:00", frequency="daily", priority="high"))
    assert len(pet.get_tasks()) == 1

# ---- Test 3: Sorting Correctness ----
def test_sort_by_time():
    owner = make_sample_owner()
    scheduler = Scheduler(owner)
    sorted_tasks = scheduler.sort_by_time()
    times = [task.due_time for _, task in sorted_tasks]
    assert times == sorted(times)

# ---- Test 4: Conflict Detection ----
def test_conflict_detection():
    owner = Owner(name="Sarah", email="sarah@email.com")
    dog = Pet(name="Buddy", species="Dog", breed="Golden Retriever")
    cat = Pet(name="Whiskers", species="Cat", breed="Persian")
    dog.add_task(Task(description="Feeding", due_time="09:00", frequency="daily", priority="high"))
    cat.add_task(Task(description="Feeding", due_time="09:00", frequency="daily", priority="high"))
    owner.add_pet(dog)
    owner.add_pet(cat)
    scheduler = Scheduler(owner)
    conflicts = scheduler.detect_conflicts()
    assert len(conflicts) > 0

# ---- Test 5: Recurring Task Rescheduling ----
def test_recurring_task_creates_new():
    today = date.today()
    task = Task(description="Feeding", due_time="09:00", frequency="daily", priority="high", due_date=today)
    new_task = task.mark_complete()
    assert new_task is not None
    assert new_task.due_date == today + timedelta(days=1)