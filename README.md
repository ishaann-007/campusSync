# CampusSync

CampusSync is a centralized coordination platform for academic institutions.

It turns faculty-reported operational issues into a structured workflow: an issue is submitted, routed to the appropriate department, automatically assigned to an eligible staff member based on active workload, worked on, and resolved.

Built for **BuildSprint 2026**.

---

## The Problem

Operational issues can be scattered across informal communication channels, making it difficult to determine:

- where an issue belongs
- who is responsible
- whether work has started
- whether the issue has been resolved

CampusSync provides a single workflow for **reporting, routing, assignment, tracking, and institutional oversight**.

---

## Core MVP

### Faculty

- Log in with a pre-created account.
- Submit an issue with a problem, description, room number, and category.
- View and track submitted issues.
- View routing and assignment information.

### Staff

- Log in with a pre-created account.
- View issues assigned to them.
- View issue details.
- Acknowledge assigned issues.
- Mark in-progress issues as resolved.

### Management

- View institution-wide issues.
- View issue status, responsible department, and assigned staff.
- View status summary counts.
- Filter issues by status, department, and category.
- View issue details.
- Management is read-only for the MVP workflow.

---

## Issue Routing

Each issue category maps deterministically to one responsible department.

| Category | Department |
|---|---|
| IT / Equipment | IT Department |
| Facilities / Classroom | Facilities Department |
| Academic / Schedule | Academic Administration |
| Miscellaneous | General Administration |

---

## Automatic Staff Assignment

Only Staff belonging to the responsible department are eligible for assignment.

Active workload is defined as the number of assigned issues with status `Assigned` or `In Progress`.

- Resolved issues do not count toward active workload.
- The eligible Staff member with the lowest active workload is selected.
- Equal workloads are resolved by alphabetical Staff name.
- If no eligible Staff member exists, no Assignment is created and the Issue remains `Submitted`.

---

## Issue Lifecycle

```text
Submitted
    ↓
Assigned
    ↓
In Progress
    ↓
Resolved
```

The MVP uses forward-only status transitions:

- `Submitted → Assigned` after successful automatic assignment
- `Assigned → In Progress` when Staff acknowledges the issue
- `In Progress → Resolved` when Staff resolves the issue

The `resolved_at` timestamp records when an issue is resolved.

Resolved issues cannot be reopened.

---

## Technology Stack

| Layer | Technology |
|---|---|
| Backend | Python + Flask |
| ORM | Flask-SQLAlchemy |
| Database | SQLite |
| Templates | Jinja2 |
| Frontend | HTML, CSS, JavaScript |
| Authentication | Flask sessions + Werkzeug password hashing |
| Version Control | Git + GitHub |

---

## Project Structure

```text
CampusSync/
├── app/
│   ├── __init__.py
│   ├── auth.py
│   ├── auth_routes.py
│   ├── models.py
│   ├── routes.py
│   ├── services.py
│   ├── templates/
│   └── static/
├── docs/
│   ├── architecture.md
│   ├── milestones.md
│   └── research.md
├── tests/
├── requirements.txt
├── run.py
├── seed.py
└── README.md
```

---

# Setup

## Prerequisites

Make sure Python is installed on your system.

The project dependencies are listed in `requirements.txt`.

## 1. Clone the repository

```bash
git clone <https://github.com/ishaann-007/campusSync>
cd CampusSync
```


## 2. Create a virtual environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 4. Seed the development database

```bash
python seed.py
```

This creates the predefined development/demo users, departments, and related seed data used by the MVP.

## 5. Run the application

```bash
python run.py
```

Then open:

```text
http://127.0.0.1:5000/
```

## 6. Run the test suite

```bash
python -m unittest discover -s tests
```

---

# Demo Accounts

CampusSync uses predefined accounts for the MVP rather than public registration.

Demo credentials are defined by `seed.py`.

| Role | Email | Password |
|---|---|---|
| Faculty | `faculty@campussync.edu` | `password123` |
| IT Staff | `staff.it@campussync.edu` | `password123` |
| Facilities Staff | `staff.facilities@campussync.edu` | `password123` |
| Management | `management@campussync.edu` | `password123` |

Use the seeded accounts to test the role-specific workflows.

---

# Testing

The automated test suite covers:

- authentication
- issue submission
- issue routing
- automatic Staff assignment
- Staff workflow
- Management visibility
- Management filtering
- issue ordering
- role-based access restrictions
- cross-department access restrictions
- end-to-end integration

Run the complete suite with:

```bash
python -m unittest discover -s tests
```

The final project test suite contains **48 tests** covering Milestones 1–9.

---

# Deliberate MVP Limitations

The current MVP intentionally excludes:

- Manual Staff selection
- Manual reassignment
- Assignment history
- Staff comments or chat
- Escalation/reassignment for urgent unacknowledged issues
- Issue reopening
- Issue editing after submission
- Issue deletion
- Notification infrastructure
- Advanced analytics
- AI-based routing
- Separate mobile application
- Complex workforce optimization
- ERP/institutional-system integration

These are deliberate scope boundaries and are not required for the current MVP.

---

# Documentation

Additional project documentation is available in the `docs/` directory:

- `docs/research.md` — research, requirements, decisions, and known limitations
- `docs/architecture.md` — application architecture and technical structure
- `docs/milestones.md` — implementation milestones and verification history

---

# Current Status

**MVP implementation complete through Milestone 9.**

The application has completed its planned MVP implementation, including:

- role-based authentication
- faculty issue submission and tracking
- deterministic department routing
- automatic workload-based Staff assignment
- Staff issue workflow
- Management oversight and filtering
- role and department access restrictions
- end-to-end integration testing
- responsive frontend and light/dark theme support
- final repository cleanup

The project is now in final preparation for demonstration and submission.
