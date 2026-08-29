# CampusSync — Technical Architecture

> **Status:** Final MVP architecture
>
> **Project:** BuildSprint 2026
>
> This document describes the technical architecture of the implemented CampusSync MVP. It is intentionally limited to the functionality present in the project rather than describing a future production system.

---

## 1. Purpose

CampusSync is a small server-rendered web application for coordinating academic-institution operational issues.

The architecture translates the product decisions documented in `research.md` into the actual implementation.

The MVP deliberately favors:

- a small technology stack
- server-side rendering
- a relational database
- explicit role-based access
- deterministic routing
- deterministic automatic assignment
- simple service-layer business logic
- automated tests around the core workflow

---

## 2. System Architecture

CampusSync uses a monolithic Flask application.

```text
User Browser
     |
     v
Jinja2 Templates
HTML / CSS / JavaScript
     |
     v
Flask Application
     |
     +----------------------+
     |                      |
     v                      v
Authentication        Application Routes
                           |
                           v
                      Service Layer
                    /       |        \
                   /        |         \
              Routing   Assignment   Workflow
                   \        |         /
                    \       |        /
                           v
                    SQLAlchemy ORM
                           |
                           v
                     SQLite Database
```

The application uses a conventional request/response model. There is no separate frontend application, REST API layer, microservice architecture, or external database service in the MVP.

---

## 3. Technology Stack

| Layer | Technology | Purpose |
|---|---|---|
| Backend | Python + Flask | Web application and request handling |
| ORM | Flask-SQLAlchemy | Database access and ORM models |
| Database | SQLite | Persistent relational storage |
| Templates | Jinja2 | Server-rendered HTML |
| Frontend | HTML, CSS, JavaScript | Interface and lightweight client-side behavior |
| Authentication | Flask sessions + Werkzeug password hashing | Login and protected access |
| Version control | Git + GitHub | Source control |

The declared Python dependencies are:

```text
Flask==3.0.3
Flask-SQLAlchemy==3.1.1
```

---

## 4. Repository Structure

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

### Module responsibilities

#### `app/__init__.py`

Creates and configures the Flask application and initializes the SQLAlchemy database extension.

#### `app/auth.py`

Contains authentication-related helpers and role-based access control.

#### `app/auth_routes.py`

Contains the login and logout routes.

#### `app/models.py`

Contains the SQLAlchemy models:

- `User`
- `Department`
- `Issue`
- `Assignment`

#### `app/routes.py`

Contains application routes for:

- Faculty
- Staff
- Management
- issue submission
- issue details
- Staff workflow actions

#### `app/services.py`

Contains business logic for:

- category-to-department routing
- automatic Staff assignment
- active workload calculation
- Staff status transitions
- Management dashboard data

#### `app/templates/`

Contains Jinja2 templates, including shared and role-specific views.

#### `app/static/`

Contains CSS and JavaScript assets.

#### `tests/`

Contains automated tests for authentication, routing, assignment, workflow, access control, ordering, Management functionality, and integration behavior.

#### `seed.py`

Creates the predefined departments and demo users required for the MVP.

#### `run.py`

Application entry point for local execution.

---

## 5. Data Model

The MVP uses four core database models:

1. `User`
2. `Department`
3. `Issue`
4. `Assignment`

### 5.1 User

```text
User
├── id
├── name
├── email
├── password_hash
├── role
└── department_id
```

Roles are:

- `faculty`
- `staff`
- `management`

Staff users may be associated with a Department through `department_id`.

Passwords are not stored as plaintext. `set_password()` stores a Werkzeug-generated password hash, and `check_password()` verifies submitted passwords against the stored hash.

### 5.2 Department

```text
Department
├── id
└── name
```

The seeded departments are:

- IT Department
- Facilities Department
- Academic Administration
- General Administration

### 5.3 Issue

```text
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

Faculty supplies:

- problem
- description
- room number
- category

The application determines:

- submitting Faculty user
- responsible Department
- status
- submission timestamp
- resolution timestamp

### 5.4 Assignment

```text
Assignment
├── id
├── issue_id
├── staff_id
└── assigned_at
```

`issue_id` is unique, so an Issue can have only one current Assignment in the MVP.

Assignment history and reassignment are intentionally not modeled.

---

## 6. Entity Relationships

```text
User (Faculty)
      |
      | submitted_by
      v
    Issue
      |
      | department_id
      v
 Department
      ^
      |
      | department_id
User (Staff)

Issue
  |
  | issue_id
  v
Assignment
  |
  | staff_id
  v
User (Staff)
```

The important relationships are:

- A Faculty User can submit many Issues.
- A Staff User belongs to a Department.
- An Issue belongs to the Faculty member who submitted it.
- An Issue is routed to a Department.
- An Issue has at most one current Assignment.
- An Assignment points to a Staff User.

---

## 7. Authentication and Authorization

Users are pre-created for the MVP. There is no public registration flow.

The login route:

1. receives an email and password;
2. finds the corresponding User;
3. verifies the password hash;
4. clears the existing session;
5. stores the authenticated user's ID in the Flask session;
6. redirects the user according to their role.

The logout route clears the session and redirects to the login page.

Role restrictions are enforced with the `role_required` access-control decorator.

### Faculty access

Faculty can:

- access the Faculty dashboard
- submit Issues
- view their own Issue details
- track their Issues

Faculty cannot access Staff or Management functionality.

### Staff access

Staff can:

- access the Staff dashboard
- view Issues assigned to themselves
- view their assigned Issue details
- acknowledge assigned Issues
- resolve Issues that are In Progress

Staff cannot access Management functionality or operate on Issues assigned to another Staff member.

### Management access

Management can:

- access the Management dashboard
- view Issues across departments
- view Issue details
- view summary counts
- filter Issues

Management does not modify the Issue workflow in the MVP.

---

## 8. Issue Submission and Routing Flow

A Faculty submission follows this sequence:

```text
Faculty submits form
        |
        v
Validate required fields
        |
        v
Validate category
        |
        v
Determine Department
        |
        v
Create Issue with Submitted status
        |
        v
Attempt automatic Staff assignment
        |
        +----------------------+
        |                      |
 Eligible Staff           No eligible Staff
        |                      |
        v                      v
Create Assignment        Keep Submitted
Set status Assigned      No Assignment
```

The Department is not selected manually by Faculty.

---

## 9. Deterministic Department Routing

The application maintains a predefined category list:

```text
IT / Equipment
Facilities / Classroom
Academic / Schedule
Miscellaneous
```

The routing service maps these categories to:

| Category | Department |
|---|---|
| IT / Equipment | IT Department |
| Facilities / Classroom | Facilities Department |
| Academic / Schedule | Academic Administration |
| Miscellaneous | General Administration |

The resulting Department ID is stored on the Issue.

An invalid category is rejected during submission.

---

## 10. Automatic Staff Assignment

After routing, the assignment service identifies Staff belonging to the responsible Department.

Only Staff in that Department are eligible.

### Active workload

For each eligible Staff member, active workload is the number of their assigned Issues whose status is:

- `Assigned`
- `In Progress`

`Resolved` Issues are excluded.

### Selection algorithm

Eligible Staff are sorted by:

1. active workload ascending
2. Staff name ascending

The first Staff member is selected.

Therefore:

```text
lowest active workload
        +
alphabetical name as tie-breaker
        =
selected Staff
```

A new `Assignment` is created and the Issue status becomes `Assigned`.

### No eligible Staff

If no eligible Staff member exists:

- no Assignment is created;
- the Issue remains `Submitted`.

This behavior is intentional and is covered by automated tests.

---

## 11. Issue Status Workflow

The implemented lifecycle is:

```text
Submitted
    |
    v
Assigned
    |
    v
In Progress
    |
    v
Resolved
```

The transitions are:

| Current status | Action | Result |
|---|---|---|
| `Submitted` | Successful automatic assignment | `Assigned` |
| `Assigned` | Staff acknowledges | `In Progress` |
| `In Progress` | Staff resolves | `Resolved` |

Staff actions are validated against both:

- the Staff user's identity
- the current Issue status

When an Issue becomes `Resolved`, `resolved_at` is set to the current UTC timestamp.

Resolved Issues cannot be reopened.

---

## 12. Role-Specific Application Flows

### Faculty

```text
Login
  |
  v
Faculty Dashboard
  |
  +--> Submit Issue
  |
  +--> View Own Issues
             |
             v
        Issue Details
```

Faculty Issue details are accessed through the dedicated Faculty Issue detail route.

### Staff

```text
Login
  |
  v
Staff Dashboard
  |
  v
Assigned Issues
  |
  v
Issue Details
  |
  +--> Acknowledge
  |       |
  |       v
  |   In Progress
  |
  +--> Mark Resolved
          |
          v
       Resolved
```

### Management

```text
Login
  |
  v
Management Dashboard
  |
  +--> Summary Counts
  |
  +--> Filters
  |
  +--> Institution-wide Issue List
  |
  +--> Issue Details
```

---

## 13. Issue Ordering

Faculty and Staff dashboards intentionally prioritize unresolved work.

The implemented ordering is:

1. non-Resolved Issues first;
2. within each group, newest `created_at` first;
3. Resolved Issues therefore appear after active Issues.

The automated ordering tests verify this behavior for both Faculty and Staff dashboards.

Management's filtered Issue list is ordered by newest `created_at` first.

---

## 14. Management Dashboard

The Management service calculates institution-wide counts for:

- Submitted
- Assigned
- In Progress
- Resolved
- Total

Management can filter the Issue list by:

- status
- department
- category

The filters are combined when multiple filter values are supplied.

Management remains read-only with respect to the Issue workflow.

---

## 15. Frontend Architecture

The frontend is server-rendered with Jinja2.

There is:

- one shared base layout;
- role-specific dashboard templates;
- role-specific Issue detail templates;
- a Faculty submission template;
- shared CSS;
- lightweight JavaScript.

The frontend does not use React, Vue, Angular, or another separate frontend framework.

The current implementation also includes a light/dark theme toggle and responsive layout behavior.

The frontend is intentionally separate from business logic: routing, assignment, authorization, and workflow decisions remain server-side.

---

## 16. Security Boundaries

The MVP enforces several important boundaries.

### Authentication boundary

Protected role routes require an authenticated session.

### Role boundary

Users cannot use routes belonging to another role.

### Faculty data isolation

A Faculty member can access only their own Issues.

### Staff assignment isolation

A Staff member can access and modify only Issues assigned to that Staff member.

### Assignment integrity

Faculty input cannot override the automatic Staff assignment.

### Password handling

Passwords are hashed using Werkzeug before storage.

These boundaries are exercised by the automated test suite.

---

## 17. Testing Architecture

The project uses Python's built-in `unittest` framework.

The tests use isolated SQLite in-memory databases for application behavior tests.

Important tested areas include:

- password hashing
- valid and invalid authentication
- login/logout
- unauthenticated access protection
- role-based access control
- Faculty data isolation
- category routing
- department-specific Staff eligibility
- workload-based assignment
- alphabetical tie-breaking
- exclusion of Resolved Issues from workload
- no-eligible-Staff behavior
- Staff status transitions
- invalid status actions
- resolution timestamps
- Faculty and Staff issue ordering
- Management visibility and filtering
- end-to-end workflow behavior

The project currently reports **48 passing tests** across the completed MVP test suite.

---

## 18. Architecture Decisions

| Decision | Implementation | Reason |
|---|---|---|
| Application style | Monolithic Flask application | Small and appropriate for MVP |
| Backend | Flask | Simple server-side web framework |
| ORM | Flask-SQLAlchemy | Provides relational models without unnecessary complexity |
| Database | SQLite | Minimal setup for hackathon MVP |
| Frontend | Jinja2 + HTML/CSS/JavaScript | Avoids a separate frontend application |
| Authentication | Flask sessions | Simple session-based authentication |
| Password storage | Werkzeug hashing | Passwords must not be stored in plaintext |
| Roles | Faculty, Staff, Management | Matches MVP responsibilities |
| Routing | Deterministic category mapping | Predictable behavior |
| Assignment | Lowest active workload | Automatic assignment without complex optimization |
| Tie-breaking | Alphabetical Staff name | Deterministic and reproducible |
| Workload | Calculated from active Issues | Avoids redundant stored workload state |
| Assignment history | Excluded | Outside MVP scope |
| Reassignment | Excluded | Outside MVP scope |
| Issue reopening | Excluded | Forward-only MVP lifecycle |
| Management changes | Read-only | Management is an oversight role |

---

## 19. Known Architectural Limitations

The MVP intentionally does not implement:

- assignment history
- manual reassignment
- issue reopening
- issue editing after submission
- issue deletion
- notifications
- escalation workflows
- Staff comments or chat
- advanced analytics
- AI-based routing
- separate mobile application
- complex workforce optimization
- ERP or institutional-system integration

These limitations are scope decisions rather than missing requirements for the current MVP.

---

## 20. Development and Maintenance Principles

The architecture follows these principles:

### Keep it simple

Prefer the smallest implementation that satisfies the MVP.

### Separate responsibilities

Authentication, routing, assignment, workflow, and presentation have distinct responsibilities.

### Avoid premature abstraction

The project does not introduce infrastructure or abstractions for features that are outside the MVP.

### Preserve deterministic behavior

Routing, assignment, tie-breaking, and status transitions should remain predictable.

### Protect the core workflow

Changes to the frontend should not alter established backend workflow rules unless a verified defect requires it.

### Test before changing scope

Core behavior should remain covered by automated tests before additional features are considered.

---

## 21. Final Architecture Status

**Status: Complete for the MVP.**

The architecture now describes the implemented CampusSync system rather than an earlier planned version.

The MVP consists of:

```text
Authentication
      ↓
Faculty Submission
      ↓
Department Routing
      ↓
Automatic Staff Assignment
      ↓
Staff Workflow
      ↓
Resolution
      ↓
Management Visibility
```

The implementation is intentionally small, deterministic, and suitable for the BuildSprint 2026 MVP scope.
