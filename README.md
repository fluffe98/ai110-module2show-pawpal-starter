# 🐾 PawPal+

A smart pet care management system that helps owners keep their pets happy and healthy by tracking daily routines, medications, appointments, and more.

---

## Scenario

A busy pet owner needs help staying consistent with pet care. PawPal+ helps them:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

---

## 📋 System Overview

PawPal+ is built around four core classes:

| Class | Responsibility |
|-------|---------------|
| `Task` | Represents a single care activity with time, priority, frequency, and completion status |
| `Pet` | Stores pet info and manages a collection of tasks |
| `Owner` | Manages multiple pets and provides access to all their tasks |
| `Scheduler` | The brain — sorts, filters, detects conflicts, and generates daily plans across all pets |

---

## 🚀 Getting Started

### Setup
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Run the demo:
```bash
python main.py
```

### Run the Streamlit app:
```bash
streamlit run app.py
```

### Run the tests:
```bash
python -m pytest tests/test_pawpal.py -v
```

---

## 🖥️ Sample Output

```
==================================================
🐾 Daily Care Plan for Sarah's Pets
==================================================
⏳ 08:00 | Buddy      | Morning Walk         | Priority: high   
⏳ 09:00 | Buddy      | Feeding              | Priority: high   ⚠️ CONFLICT
⏳ 09:00 | Whiskers   | Feeding              | Priority: high   ⚠️ CONFLICT
⏳ 12:00 | Whiskers   | Medication           | Priority: high   
⏳ 15:00 | Whiskers   | Grooming             | Priority: low    
⏳ 17:00 | Buddy      | Evening Walk         | Priority: medium 
==================================================
⚠️  Conflict Detection
==================================================
Conflict at 09:00: Buddy's 'Feeding' vs Whiskers's 'Feeding'
==================================================
📋 Pending Tasks Only
==================================================
  Buddy: Morning Walk at 08:00
  Buddy: Feeding at 09:00
  Buddy: Evening Walk at 17:00
  Whiskers: Feeding at 09:00
  Whiskers: Medication at 12:00
  Whiskers: Grooming at 15:00
==================================================
🔥 Tasks Sorted by Priority
==================================================
  [HIGH] Buddy: Morning Walk at 08:00
  [HIGH] Buddy: Feeding at 09:00
  [HIGH] Whiskers: Feeding at 09:00
  [HIGH] Whiskers: Medication at 12:00
  [MEDIUM] Buddy: Evening Walk at 17:00
  [LOW] Whiskers: Grooming at 15:00
```

---

## 📐 Smarter Scheduling

| Feature | Method | Notes |
|---------|--------|-------|
| Sort by time | `Scheduler.sort_by_time()` | Sorts all tasks chronologically across all pets |
| Sort by priority | `Scheduler.sort_by_priority()` | Sorts high > medium > low, then by time |
| Filter by pet | `Scheduler.filter_by_pet(pet_name)` | Shows tasks for one specific pet |
| Filter by status | `Scheduler.filter_by_status(completed)` | Shows pending or completed tasks |
| Conflict detection | `Scheduler.detect_conflicts()` | Warns when two tasks are at the same time |
| Recurring tasks | `Task.mark_complete()` | Auto-creates next task for daily/weekly tasks |
| Daily plan | `Scheduler.generate_daily_plan()` | Full sorted plan with conflict warnings |

---

## 🧪 Testing PawPal+

```bash
python -m pytest tests/test_pawpal.py -v
```

### What the tests cover:
- Task completion status changes correctly
- Adding a task increases the pet's task count
- Sorting returns tasks in chronological order
- Conflict detection flags duplicate time slots
- Recurring tasks auto-schedule for the next day

### Sample test output:
```
collected 5 items

tests/test_pawpal.py::test_task_mark_complete          PASSED [ 20%]
tests/test_pawpal.py::test_add_task_increases_count    PASSED [ 40%]
tests/test_pawpal.py::test_sort_by_time                PASSED [ 60%]
tests/test_pawpal.py::test_conflict_detection          PASSED [ 80%]
tests/test_pawpal.py::test_recurring_task_creates_new  PASSED [100%]

5 passed in 0.05s
```

### Confidence Level: ⭐⭐⭐⭐⭐ (5/5)

---

## 📸 Demo Walkthrough

1. Run `python main.py` to see the full CLI demo in the terminal
2. Owner "Sarah" has two pets: Buddy (Golden Retriever) and Whiskers (Persian Cat)
3. Each pet has multiple tasks with different times and priorities
4. The Scheduler automatically sorts all tasks by time across both pets
5. A conflict is detected at 09:00 — both pets have feeding scheduled at the same time
6. Tasks are displayed with conflict warnings so the owner knows what to fix
7. Priority sorting shows high priority tasks first, then medium, then low
8. Run `streamlit run app.py` to use the interactive web UI
9. In the UI you can add owners, pets, tasks and view the generated daily plan

---

## 📐 UML Diagram

See `diagrams/uml.mmd` for the full Mermaid class diagram showing all four classes and their relationships.
