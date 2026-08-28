# CampusSync

CampusSync is a centralized coordination platform for academic
institutions. It turns faculty-reported operational issues into a
structured workflow: an issue is routed to the appropriate department,
automatically assigned to an eligible staff member based on active
workload, worked on, and resolved.

Built for **BuildSprint 2026**.

## The Problem

Operational issues can be scattered across informal communication
channels, making it difficult to determine where an issue belongs, who
is responsible, whether work has started, and whether it has been
resolved.

CampusSync provides a single workflow for reporting, routing,
assignment, tracking, and institutional oversight.

## Core MVP

### Faculty

-   Log in with a pre-created account.
-   Submit an issue with problem, description, room number, and
    category.
-   View and track submitted issues.
-   View routing and assignment information.

### Staff

-   Log in with a pre-created account.
-   View issues assigned to them.
-   View issue details.
-   Acknowledge assigned issues.
-   Mark in-progress issues as resolved.

### Management

-   View institution-wide issues.
-   View status, department, and assigned staff.
-   View status summary counts.
-   Filter by status, department, and category.
-   View issue details.
-   Management is read-only for the MVP workflow.

## Issue Routing

  Category                 Department
  ------------------------ -------------------------
  IT / Equipment           IT Department
  Facilities / Classroom   Facilities Department
  Academic / Schedule      Academic Administration
  Miscellaneous            General Administration

Routing is deterministic: each category maps to one responsible
department.

## Automatic Staff Assignment

Only Staff belonging to the responsible department are eligible.

Active workload is the number of assigned issues with status `Assigned`
or `In Progress`. Resolved issues do not count.

The eligible Staff member with the lowest active workload is selected.
Equal workloads are resolved by alphabetical Staff name.

If no eligible Staff member exists, no Assignment is created and the
Issue remains `Submitted`.

## Issue Lifecycle

``` text
Submitted
    ↓
Assigned
    ↓
In Progress
    ↓
Resolved
```

The MVP uses forward-only transitions:

-   `Submitted → Assigned` after successful automatic assignment
-   `Assigned → In Progress` when Staff acknowledges
-   `In Progress → Resolved` when Staff resolves

`resolved_at` records the resolution time. Resolved issues cannot be
reopened.

## Technology Stack

  Layer             Technology
  ----------------- --------------------------------------------
  Backend           Python + Flask
  ORM               Flask-SQLAlchemy
  Database          SQLite
  Templates         Jinja2
  Frontend          HTML, CSS, JavaScript
  Authentication    Flask sessions + Werkzeug password hashing
  Version control   Git + GitHub

## Project Structure

``` text
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
├── instance/
├── tests/
├── requirements.txt
├── run.py
├── seed.py
└── README.md
```

## Setup

### 1. Clone the repository

``` bash
git clone <repository-url>
cd CampusSync
```

Replace `<repository-url>` with the actual repository URL.

### 2. Create a virtual environment

Windows:

``` bash
python -m venv venv
venv\Scripts\activate
```

macOS/Linux:

``` bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

``` bash
pip install -r requirements.txt
```

### 4. Seed the development database

``` bash
python seed.py
```

This creates the pre-defined development/demo users and departments used
by the MVP.

### 5. Run the application

``` bash
python run.py
```

Then open:

``` text
http://127.0.0.1:5000/
```

### 6. Run tests

``` bash
python -m unittest discover -s tests
```

## Demo Accounts

Users are pre-created for the MVP rather than registered publicly.

The exact credentials should be documented from the current `seed.py`;
do not guess or substitute credentials.

  Role         Email           Password
  ------------ --------------- ---------------
  Faculty      See `seed.py`   See `seed.py`
  Staff        See `seed.py`   See `seed.py`
  Management   See `seed.py`   See `seed.py`

## Deliberate MVP Limitations

The current MVP intentionally excludes:

-   Manual Staff selection
-   Manual reassignment
-   Assignment history
-   Staff comments or chat
-   Escalation/reassignment for urgent unacknowledged issues
-   Issue reopening
-   Issue editing after submission
-   Issue deletion
-   Notification infrastructure
-   Advanced analytics
-   AI-based routing
-   Separate mobile application
-   Complex workforce optimization
-   ERP/institutional-system integration

These are deliberate scope boundaries, not requirements of the current
MVP.

## Testing

The test suite covers authentication, issue submission, routing,
automatic assignment, Staff workflow, Management visibility/filtering,
ordering, access restrictions, and end-to-end integration.

Run:

``` bash
python -m unittest discover -s tests
```

## Current Status

**MVP implementation complete through Milestone 9.**

The project is in final preparation: documentation verification, final
testing, and demonstration preparation.
