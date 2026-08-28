# CampusSync --- Technical Architecture

> **Status:** Final MVP architecture

## 1. Overview

CampusSync is a small monolithic web application using a server-rendered
frontend, Flask application layer, Flask-SQLAlchemy ORM, and SQLite
database.

``` text
User Browser
     │
     ▼
Jinja2 + HTML/CSS/JavaScript
     │
     ▼
Flask Application
     │
     ├── Authentication & Authorization
     ├── Issue Management
     ├── Routing
     ├── Staff Assignment
     └── Workflow Operations
     │
     ▼
Flask-SQLAlchemy
     │
     ▼
SQLite
```

The architecture deliberately avoids a separate frontend application,
microservices, multiple databases, and unnecessary infrastructure.

## 2. Technology Stack

  -----------------------------------------------------------------------
  Layer                   Technology              Purpose
  ----------------------- ----------------------- -----------------------
  Backend                 Python + Flask          Web application and
                                                  request handling

  ORM                     Flask-SQLAlchemy        Database models and
                                                  access

  Database                SQLite                  Persistent relational
                                                  storage

  Templates               Jinja2                  Server-rendered pages

  Frontend                HTML/CSS/JavaScript     User interface and
                                                  lightweight client
                                                  behavior

  Authentication          Flask sessions +        Authentication and
                          Werkzeug password       protected access
                          hashing                 

  Version control         Git + GitHub            Source control
  -----------------------------------------------------------------------

## 3. Repository Structure

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

-   `app/__init__.py` --- application setup and database initialization.
-   `app/auth.py` --- authentication helpers and role access control.
-   `app/auth_routes.py` --- login/logout handling.
-   `app/models.py` --- SQLAlchemy ORM models.
-   `app/routes.py` --- role-specific request handling and application
    routes.
-   `app/services.py` --- routing, assignment, workload, workflow, and
    Management data logic.
-   `app/templates/` --- Jinja2 views.
-   `app/static/` --- CSS and JavaScript.
-   `tests/` --- automated tests.
-   `seed.py` --- pre-created development/demo users and departments.
-   `run.py` --- application entry point.
-   `instance/` --- local SQLite database storage.

## 4. Data Model

The MVP uses four core models:

1.  `User`
2.  `Department`
3.  `Issue`
4.  `Assignment`

### User

``` text
User
├── id
├── name
├── email
├── password_hash
├── role
└── department_id
```

Roles are `faculty`, `staff`, and `management`.

### Department

``` text
Department
├── id
└── name
```

### Issue

``` text
Issue
├── id
├── problem
├── description
├── room_number
├── category
├── status
├── submitted_by
├── department_id
├── created_at
└── resolved_at
```

### Assignment

``` text
Assignment
├── id
├── issue_id
├── staff_id
└── assigned_at
```

The MVP stores one current Assignment per Issue.

## 5. Relationships

``` text
Faculty User
     │
     │ submits
     ▼
   Issue
     │
     │ routed to
     ▼
 Department
     │
     │ contains eligible Staff
     ▼
 Staff User

Issue
  │
  │ has one current Assignment
  ▼
Assignment
  │
  ▼
Staff User
```

## 6. Authentication and Authorization

Users are pre-created for the MVP; there is no public registration.

Flask sessions maintain authenticated user identity. Werkzeug is used
for password hashing.

Faculty can submit and view their own issues. Staff can view and operate
on issues assigned to them. Management can view institution-wide issues
and filter them, but does not modify the workflow.

Cross-role and data-isolation checks are covered by tests.

## 7. Routing

Routing is deterministic and category-based:

  Category                 Department
  ------------------------ -------------------------
  IT / Equipment           IT Department
  Facilities / Classroom   Facilities Department
  Academic / Schedule      Academic Administration
  Miscellaneous            General Administration

The resulting Department is stored on the Issue.

## 8. Automatic Assignment

Eligible Staff are restricted to Staff in the responsible Department.

Active workload consists of Issues with status `Assigned` or
`In Progress`.

The Staff member with the lowest active workload is selected. Equal
workloads use alphabetical Staff name as the deterministic tie-breaker.

If there is no eligible Staff:

``` text
No Assignment
     ↓
Issue remains Submitted
     ↓
Management can see it
```

Manual selection and reassignment are outside the MVP.

## 9. Issue Workflow

``` text
Submitted
    ↓
Assigned
    ↓
In Progress
    ↓
Resolved
```

Allowed transitions:

  Current       Trigger                           Next
  ------------- --------------------------------- -------------
  Submitted     Successful automatic assignment   Assigned
  Assigned      Staff acknowledgement             In Progress
  In Progress   Staff resolution                  Resolved

When resolved, `resolved_at` is recorded. Resolved issues cannot be
reopened.

## 10. Interface Architecture

The application uses shared layout elements and role-specific
dashboards.

Faculty: - submit issues, - view their own issues, - track status.

Staff: - view assigned work, - acknowledge, - resolve.

Management: - view institution-wide issues, - view summary counts, -
filter by status, Department, and category, - inspect read-only details.

The interface supports light/dark themes and responsive layouts. There
is no separate mobile application.

## 11. Management Data

Management receives institution-wide visibility and summary counts for:

-   Submitted
-   Assigned
-   In Progress
-   Resolved
-   Total Issues

The Management dashboard supports filtering by status, Department, and
category.

## 12. Testing

The project uses Python `unittest`.

Tests cover foundation behavior, authentication, Faculty issue
submission, routing, assignment, Staff workflow, Management dashboard
behavior, ordering, and end-to-end integration.

Run:

``` bash
python -m unittest discover -s tests
```

## 13. Deliberate Architectural Limitations

The MVP does not include:

-   assignment history,
-   manual Staff selection,
-   manual reassignment,
-   Staff comments/chat,
-   escalation workflows,
-   reopening,
-   notifications,
-   advanced analytics,
-   AI routing,
-   complex workforce optimization,
-   separate mobile application.

The current Assignment model represents the current assignment rather
than a complete assignment history.

## 14. Architectural Principles

-   Keep the implementation simple.
-   Minimize infrastructure.
-   Separate responsibilities.
-   Avoid premature abstraction.
-   Preserve future flexibility where inexpensive.
-   Optimize for reliability.
-   Implement incrementally and verify each milestone.

## 15. Current Status

The MVP implementation is complete through Milestone 9.

The remaining project work is final documentation verification, final
testing/manual verification, and demonstration preparation.
