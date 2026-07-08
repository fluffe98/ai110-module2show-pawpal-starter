# PawPal+ Reflection

## Section 1: System Design

### 1a. Initial Design

I designed PawPal+ around four core classes:

- **Task**: Represents a single pet care activity. It holds the description, due time, frequency (once/daily/weekly), priority (low/medium/high), completion status, and due date. The key method is `mark_complete()` which also handles recurring task rescheduling.

- **Pet**: Represents an individual pet. It stores the pet's name, species, and breed, and maintains a list of Task objects. Methods include `add_task()`, `remove_task()`, `get_tasks()`, and `get_pending_tasks()`.

- **Owner**: Represents the pet owner. It stores the owner's name and email and maintains a list of Pet objects. The key method `get_all_tasks()` retrieves tasks from ALL pets, making it the bridge between the Owner and Scheduler.

- **Scheduler**: The brain of the system. It takes an Owner as input and provides algorithmic features like sorting by time, sorting by priority, filtering by pet or status, conflict detection, and daily plan generation — all operating across multiple pets.

The relationship chain is: Owner → Pets → Tasks → Scheduler manages everything.

### 1b. Design Changes

After reviewing the initial skeleton, I added the following based on AI feedback:

- Added `sort_by_priority()` in addition to `sort_by_time()` to give more scheduling intelligence
- Added `generate_daily_plan()` as a single method that combines sorting and conflict detection into one readable output
- Used Python dataclasses for Task, Pet, and Owner to keep the code clean and readable
- Added `due_date` field to Task to support recurring task rescheduling using `timedelta`

---

## Section 2: Algorithmic Decisions

### 2a. Algorithms Implemented

1. **Sorting by Time** (`Scheduler.sort_by_time()`): Uses Python's `sorted()` with a lambda function to sort tasks by their `due_time` string in HH:MM format. Since the format is consistent, string comparison works correctly for chronological ordering.

2. **Sorting by Priority** (`Scheduler.sort_by_priority()`): Maps priority levels to numbers (high=0, medium=1, low=2) and sorts using a tuple key — priority first, then time. This ensures high priority tasks always appear first.

3. **Filtering by Pet** (`Scheduler.filter_by_pet()`): Uses a list comprehension to return only tasks belonging to a specific pet name.

4. **Filtering by Status** (`Scheduler.filter_by_status()`): Uses a list comprehension to return only completed or pending tasks based on the boolean parameter.

5. **Conflict Detection** (`Scheduler.detect_conflicts()`): Uses a dictionary to track which time slots are already taken. If a task's due_time already exists in the dictionary, a conflict is recorded and a warning is returned.

6. **Recurring Tasks** (`Task.mark_complete()`): When a daily task is marked complete, a new Task object is created with `due_date + timedelta(days=1)`. For weekly tasks, `timedelta(weeks=1)` is used.

### 2b. Tradeoffs

One key tradeoff my scheduler makes is checking for **exact time matches** rather than overlapping durations. For example, a task at 09:00 lasting 30 minutes and another at 09:15 would NOT be flagged as a conflict, even though they overlap in real life. This keeps the conflict detection simple and fast, but it means the system is not a true time-blocking scheduler. A future improvement would be to add a `duration` field to Task and check for time range overlaps instead of just exact matches.

---

## Section 3: AI Collaboration

### 3a. AI Strategy

I used AI assistance throughout this project in the following ways:

- **Class Design**: I asked AI to help brainstorm the four core classes and their relationships. The AI suggested using Python dataclasses for Task, Pet, and Owner, which kept the code cleaner than traditional classes.

- **Algorithm Implementation**: I asked AI to suggest how to sort Task objects by time using a lambda function. The AI suggested using `sorted(tasks, key=lambda x: x[1].due_time)` which worked perfectly.

- **Test Generation**: I asked AI to draft pytest test cases for the most important behaviors — task completion, sorting correctness, conflict detection, and recurring task rescheduling.

- **Code Review**: I asked AI to review my Scheduler class to ensure it operated across multiple pets, not just one.

### 3b. AI Suggestions Accepted

- Using dataclasses for cleaner class definitions — accepted because it reduced boilerplate code significantly
- Using a dictionary for conflict detection instead of nested loops — accepted because it is more efficient (O(n) vs O(n²))
- Using `timedelta` for recurring task rescheduling — accepted because it handles date math correctly

### 3c. AI Suggestions Rejected or Modified

- AI initially suggested using a single `get_tasks()` method in Scheduler that only looked at one pet. I rejected this and modified it to iterate across ALL pets in the Owner's pet list, because the grading rubric specifically required multi-pet support.
- AI suggested using a complex priority queue for sorting. I simplified this to a basic `sorted()` with a lambda because readability was more important than marginal performance gains for this use case.

### 3d. How I Verified Correctness

I verified correctness by:
1. Running `python main.py` and checking the terminal output matched expected behavior
2. Running `python -m pytest tests/test_pawpal.py -v` and confirming all 5 tests passed
3. Manually checking that conflict detection flagged the 09:00 time slot correctly
4. Manually checking that the priority sort put high priority tasks first

### 3e. What I Learned

Being the "lead architect" means AI is a tool, not the decision maker. AI helped me write faster, but I had to make the important decisions — like ensuring the Scheduler worked across multiple pets, choosing between simple and complex algorithms, and deciding which AI suggestions actually fit my design. The most important skill I developed was evaluating AI output critically rather than accepting it blindly.
