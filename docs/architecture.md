# CampusSync — Technical Architecture

> **Project:** CampusSync
> **Context:** 48-hour BuildSprint hackathon
> **Status:** Initial implementation architecture

---

## 1. Architecture Overview

CampusSync will use a simple monolithic web application architecture designed around the constraints of a solo beginner developer working within a 48-hour hackathon.

The architecture prioritizes:

* Simplicity
* Understandability
* Fast development
* Minimal infrastructure
* Reliable end-to-end functionality
* Clear separation of responsibilities

The system will not use separate frontend and backend services.

### High-Level Architecture

```text
Faculty / Staff / Management
            │
            ▼
      Web Interface
            │
            ▼
     Flask Application
            │
     ┌──────┴──────┐
     │             │
Business Logic   Authentication
     │
     ├── Routing
     ├── Assignment
     └── Issue Workflow
            │
            ▼
         SQLite
```

The application will be implemented as one Flask-based web application.

---

## 2. Technology Stack

| Layer                 | Technology     |
| --------------------- | -------------- |
| Backend               | Python + Flask |
| Database              | SQLite         |
| Server-side templates | Jinja2         |
| Frontend              | HTML           |
| Styling               | CSS            |
| Client-side behavior  | JavaScript     |
| Version control       | Git + GitHub   |

### Stack Rationale

The stack was selected because it is appropriate for a small, beginner-friendly hackathon project.

It avoids the additional complexity of:

* Separate frontend frameworks
* Separate backend services
* Multiple databases
* Microservices
* Complex deployment infrastructure

The goal is to build a complete working application rather than production-scale infrastructure.

---

## 3. Application Architecture

CampusSync follows a simple monolithic structure.

The major responsibilities are separated conceptually into:

```text
Presentation
     ↓
Request Handling
     ↓
Business Logic
     ↓
Data Access
     ↓
SQLite Database
```

### Presentation

Responsible for:

* HTML pages
* Jinja2 templates
* CSS
* JavaScript
* Forms
* Dashboard interfaces
* Issue details drawer

### Request Handling

Responsible for:

* Receiving browser requests
* Validating request data
* Calling appropriate application logic
* Returning pages or responses

### Business Logic

Responsible for:

* Category-to-department routing
* Staff eligibility
* Workload calculation
* Staff assignment
* Issue status transitions

### Data Access

Responsible for:

* Reading data from SQLite
* Creating data
* Updating data
* Maintaining relationships between data objects

The exact implementation approach will remain as simple as possible.

---

## 4. Core Data Model

The MVP contains four core data objects:

1. User
2. Department
3. Issue
4. Assignment

---

## 5. User

The User object represents a person using CampusSync.

Conceptually:

```text
User
├── user_id
├── name
├── email
├── password
├── role
└── department_id
```

### Roles

The application has exactly three roles:

* Faculty
* Staff
* Management

### Department Association

Staff users belong to an operational Department.

Faculty and Management do not require an operational department association for the MVP.

### Responsibility

User data is used for:

* Authentication
* Role identification
* Authorization
* Identifying issue submitters
* Identifying Staff members
* Linking Staff to departments

---

## 6. Department

The Department object represents an operational department responsible for handling issues.

Conceptually:

```text
Department
├── department_id
└── name
```

Initial departments:

* IT Department
* Facilities Department
* Academic Administration
* General Administration

Departments are used by the routing and Staff assignment logic.

---

## 7. Issue

The Issue object represents an operational problem submitted by Faculty.

Conceptually:

```text
Issue
├── issue_id
├── problem
├── description
├── room_number
├── category
├── submitted_by
├── department_id
├── status
├── created_at
└── resolved_at
```

### Faculty-provided fields

Faculty provides:

* Problem
* Description
* Room number
* Category

### System-controlled fields

The application determines or generates:

* Issue ID
* Submitting Faculty
* Responsible Department
* Assignment
* Status
* Created timestamp
* Resolution timestamp

Original issue details are read-only after submission in the MVP.

---

## 8. Assignment

The Assignment object represents the current Staff member responsible for an Issue.

Conceptually:

```text
Assignment
├── assignment_id
├── issue_id
├── staff_id
└── assigned_at
```

The MVP stores only the **current assignment**.

Assignment history and reassignment history are outside the MVP.

An Issue has zero or one current Assignment.

---

## 9. Data Relationships

The conceptual relationships are:

```text
User (Faculty)
      │
      │ submits
      ▼
    Issue
      │
      │ routed to
      ▼
 Department
      │
      │ determines eligible Staff
      ▼
User (Staff)
      │
      │ current assignment
      ▼
Assignment
      │
      │ assigned to
      ▼
    Issue
```

More precisely:

* One Faculty User can submit many Issues.
* Each Issue has one submitting Faculty User.
* Each Issue has one responsible Department.
* A Department can be responsible for many Issues.
* A Staff User belongs to one operational Department.
* An Issue has zero or one current Assignment.
* An Assignment points to one Staff User.
* A Staff User can have multiple active assignments.

---

## 10. Issue Processing Flow

The intended application flow is:

```text
Faculty submits Issue
        ↓
Category is selected
        ↓
Routing logic determines Department
        ↓
Eligible Staff are identified
        ↓
Staff workloads are evaluated
        ↓
Lowest-workload eligible Staff member selected
        ↓
Assignment created
        ↓
Issue becomes Assigned
        ↓
Staff acknowledges issue
        ↓
Issue becomes In Progress
        ↓
Staff resolves issue
        ↓
Issue becomes Resolved
```

### No eligible Staff

If no eligible Staff member exists:

```text
Issue submitted
      ↓
Department determined
      ↓
No eligible Staff
      ↓
Issue remains Submitted
      ↓
No Assignment
```

Management can see the issue.

---

## 11. Routing Logic

CampusSync uses deterministic category-based routing.

| Category               | Department              |
| ---------------------- | ----------------------- |
| IT / Equipment         | IT Department           |
| Facilities / Classroom | Facilities Department   |
| Academic / Schedule    | Academic Administration |
| Miscellaneous          | General Administration  |

The Faculty member selects the category.

The application uses the predefined mapping to determine the responsible Department.

### Architectural Decision

The category-to-department mapping will be implemented as **application logic**, rather than creating a separate database table for routing rules.

This is appropriate because the MVP contains only four fixed mappings.

### Implementation Requirement

The routing logic should:

1. Receive the selected category.
2. Identify the corresponding Department.
3. Return the Department.
4. Reject invalid categories rather than silently assigning an incorrect department.

The exact function/module location will follow the project structure described below.

---

## 12. Automatic Staff Assignment

After routing, CampusSync automatically selects an eligible Staff member.

### Eligibility

Only Staff belonging to the responsible Department are considered.

### Active Workload

A Staff member's active workload consists of Issues in:

* `Assigned`
* `In Progress`

Resolved Issues do not count.

### Selection

The eligible Staff member with the lowest active workload is selected.

Example:

```text
Staff A → 4 active issues
Staff B → 2 active issues
Staff C → 1 active issue

New Issue
    ↓
Assigned to Staff C
```

### Tie-breaking

If multiple eligible Staff members have the same active workload, a deterministic tie-breaking mechanism will be used.

The exact tie-breaking mechanism is an implementation detail that should remain simple and deterministic.

### No Eligible Staff

If no eligible Staff member exists:

* No Assignment is created.
* The Issue remains `Submitted`.
* Management can see the Issue.

### Important Constraint

Assignment does not involve manual Staff selection in the MVP.

---

## 13. Issue Status Workflow

The issue lifecycle is:

```text
Submitted
    ↓
Assigned
    ↓
In Progress
    ↓
Resolved
```

### Transition Rules

| Current Status | Trigger               | Next Status |
| -------------- | --------------------- | ----------- |
| Submitted      | Successful assignment | Assigned    |
| Assigned       | Staff acknowledges    | In Progress |
| In Progress    | Staff marks resolved  | Resolved    |

Status transitions are strictly forward-only.

No arbitrary backward transitions are allowed.

### Resolved Issues

Once an Issue becomes `Resolved`, it cannot be reopened in the MVP.

If the same problem occurs again, Faculty submits a new Issue.

### Timestamps

The system records:

* `created_at` when the Issue is submitted
* `resolved_at` when the Issue becomes `Resolved`

---

## 14. Authentication & Authorization

CampusSync has three roles:

```text
Faculty
Staff
Management
```

Users are pre-created for the MVP.

There is no public registration system.

### Faculty Permissions

Faculty can:

* Submit Issues
* View their own Issues
* Track Issue status
* View Issue details

Faculty cannot:

* View other Faculty members' Issues
* Change the Department
* Choose Staff assignment
* Edit an Issue after submission
* Delete Issues

### Staff Permissions

Staff can:

* View Issues assigned to them
* View Issue details
* Acknowledge assigned Issues
* Mark assigned Issues as resolved

Staff cannot:

* View unrelated Staff assignments
* Choose their assignments
* Reassign Issues
* Modify original Issue details
* Delete Issues

### Management Permissions

Management can:

* View institution-wide Issues
* View Issue details
* View Issue counts
* Filter Issues
* Monitor Issue status

Management does not modify the Issue workflow in the MVP.

### Authentication Implementation

The exact Flask authentication/session mechanism and password-handling implementation will be chosen during implementation of the authentication milestone, using a simple established approach appropriate for the stack.

The implementation must not store passwords as plain text.

---

## 15. Interface Architecture

CampusSync is a responsive web application.

A separate mobile application is not part of the MVP.

### Shared Layout

The application should use a shared visual/layout structure where practical.

The role-specific dashboard provides the main content for each user.

### Issue Details

Issues use a **details drawer/sidebar** rather than requiring a separate issue-details page.

On smaller screens, the drawer can adapt to a larger or full-screen presentation.

---

## 16. Faculty Interface

Conceptual flow:

```text
Login
  ↓
Faculty Dashboard
  ├── Submit Issue
  └── View Submitted Issues
          ↓
      Details Drawer
```

The Faculty dashboard should primarily focus on the Faculty member's own issues.

The submission form contains:

* Problem
* Description
* Room number
* Category

The Department and Staff member are determined automatically.

---

## 17. Staff Interface

Conceptual flow:

```text
Login
  ↓
Staff Dashboard
  ↓
Assigned Issues
  ↓
Details Drawer
  ↓
Acknowledge / Resolve
```

Staff should primarily see their assigned work.

### Actions

For an `Assigned` Issue:

> Acknowledge

Result:

`Assigned → In Progress`

For an `In Progress` Issue:

> Mark as Resolved

Result:

`In Progress → Resolved`

For a `Resolved` Issue:

No workflow action is available.

---

## 18. Management Interface

Management has institution-wide visibility.

The dashboard contains:

### Summary Counts

* Total Issues
* Assigned
* In Progress
* Resolved

### Issue List

Management can view issues across all departments.

### Filters

The MVP supports basic filtering by:

* Status
* Department
* Category

### Issue Details

Clicking an Issue opens the details drawer.

Advanced analytics and charts are not required.

---

## 19. Project Structure

The repository will use a simple monolithic Flask structure.

```text
CampusSync/
│
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   ├── services.py
│   │
│   ├── templates/
│   │   ├── base.html
│   │   ├── login.html
│   │   ├── faculty/
│   │   ├── staff/
│   │   └── management/
│   │
│   └── static/
│       ├── css/
│       └── js/
│
├── docs/
│   ├── research.md
│   └── architecture.md
│
├── instance/
│   └── campus_sync.db
│
├── tests/
│
├── .gitignore
├── requirements.txt
├── run.py
└── README.md
```

### `app/`

Contains the application itself.

### `app/__init__.py`

Responsible for application initialization and configuration.

### `app/models.py`

Contains the application's core data models:

* User
* Department
* Issue
* Assignment

### `app/routes.py`

Contains web request handling and role-specific application routes.

### `app/services.py`

Contains the main business logic, including:

* Department routing
* Staff assignment
* Workload calculation
* Issue workflow operations

The application should not be split into many small service modules unless implementation makes that necessary.

### `app/templates/`

Contains Jinja2 templates.

Templates are organized by shared and role-specific interfaces.

### `app/static/`

Contains frontend assets:

* CSS
* JavaScript

### `docs/`

Contains project documentation.

### `instance/`

Contains the local SQLite database.

The database file should not be committed to GitHub.

### `tests/`

Contains tests for important application behavior.

Priority should be given to:

* Routing
* Assignment
* Status transitions

### `requirements.txt`

Lists Python dependencies required by the application.

### `run.py`

Provides the entry point for running the application locally.

### `.gitignore`

Prevents generated files, local database files, environment files, and other unnecessary files from being committed.

---

## 20. Database Architecture

SQLite is the MVP database.

The database will represent the four core objects:

```text
User
Department
Issue
Assignment
```

Relationships will use primary and foreign keys.

### Important Relationships

```text
User.department_id
        ↓
    Department

Issue.submitted_by
        ↓
      User

Issue.department_id
        ↓
    Department

Assignment.issue_id
        ↓
      Issue

Assignment.staff_id
        ↓
      User
```

The exact SQLite schema, constraints, and indexes should be finalized during implementation setup.

Only indexes with a clear practical benefit should be introduced.

---

## 21. Request and Data Flow

A typical Faculty issue submission follows:

```text
Faculty browser
      ↓
Issue submission route
      ↓
Validate submitted data
      ↓
Determine Department
      ↓
Find eligible Staff
      ↓
Calculate active workloads
      ↓
Select Staff member
      ↓
Create Issue
      ↓
Create Assignment if Staff exists
      ↓
Set appropriate Issue status
      ↓
Store in SQLite
      ↓
Return updated Faculty interface
```

The exact transaction and database operation ordering will be implemented so that an Issue cannot incorrectly appear assigned without a corresponding Assignment.

---

## 22. Workload Calculation

The assignment system needs the number of active Issues for each eligible Staff member.

Active Issues are:

```text
Assigned
In Progress
```

Resolved Issues are excluded.

Conceptually:

```text
For each eligible Staff member:

    active workload
        =
    number of assigned Issues
    +
    number of in-progress Issues
```

The Staff member with the lowest workload is selected.

The implementation should keep this calculation straightforward and understandable.

---

## 23. Issue Editing & Deletion Rules

Issue records are intentionally stable after submission.

### Faculty

Cannot edit an Issue after submission.

### Staff

Cannot modify the original:

* Problem
* Description
* Room number
* Category

Staff only changes the Issue through its defined status workflow.

### Management

Has read-only visibility.

### Deletion

Issues cannot be deleted in the MVP.

### Reopening

Resolved Issues cannot be reopened.

---

## 24. Error and Edge-Case Behavior

The MVP should handle important predictable edge cases without creating a large error-handling system.

### Invalid Category

An invalid category should be rejected rather than routed incorrectly.

### No Eligible Staff

The Issue remains:

`Submitted`

with no Assignment.

Management can see it.

### Invalid Status Action

An action should only be accepted when valid for the Issue's current status.

Examples:

* Cannot acknowledge an already resolved Issue.
* Cannot resolve an `Assigned` Issue without first moving it to `In Progress`.

### Unauthorized Access

Users should not be able to access or modify data outside their role permissions.

---

## 25. Testing Strategy

Testing will focus on the business rules most likely to cause incorrect behavior.

### Routing

Test all four mappings:

```text
IT / Equipment
        ↓
IT Department

Facilities / Classroom
        ↓
Facilities Department

Academic / Schedule
        ↓
Academic Administration

Miscellaneous
        ↓
General Administration
```

### Assignment

Test:

* Lowest workload selection
* Multiple Staff members
* Equal workloads
* No eligible Staff

### Status Workflow

Test:

```text
Submitted → Assigned
Assigned → In Progress
In Progress → Resolved
```

Also verify invalid backward transitions are rejected.

### Permissions

Verify:

* Faculty sees only their Issues.
* Staff sees only their assignments.
* Management sees institution-wide Issues.

---

## 26. Development Strategy

Implementation will proceed incrementally.

### Milestone 1 — Application Foundation

Establish:

* Flask application
* Project structure
* Dependencies
* SQLite connection
* Basic application startup

### Milestone 2 — Authentication

Implement:

* Login
* Pre-created users
* Role identification
* Basic role-based access

### Milestone 3 — Faculty Issue Submission

Implement:

* Faculty dashboard
* Issue submission form
* Issue storage
* Issue display

### Milestone 4 — Routing

Implement:

* Category validation
* Category-to-department routing
* Department association

### Milestone 5 — Automatic Assignment

Implement:

* Eligible Staff selection
* Active workload calculation
* Lowest-workload selection
* Deterministic tie-breaking
* Assignment creation

### Milestone 6 — Staff Workflow

Implement:

* Staff dashboard
* Assigned Issue display
* Acknowledge action
* Resolution action
* Status transitions
* Resolution timestamp

### Milestone 7 — Management

Implement:

* Management dashboard
* Summary counts
* Institution-wide Issue list
* Basic filters
* Issue details drawer

### Milestone 8 — Integration Testing

Test:

```text
Faculty
  ↓
Issue Submission
  ↓
Routing
  ↓
Assignment
  ↓
Staff
  ↓
In Progress
  ↓
Resolved
  ↓
Management
```

### Milestone 9 — UI Polish

After the core workflow is reliable:

* Improve visual consistency
* Improve layout
* Improve forms
* Improve dashboard presentation
* Improve responsive behavior
* Improve issue details drawer

### Milestone 10 — Demo Preparation

Prepare:

* Demo users
* Demo issues
* Representative workloads
* Complete demonstration workflow
* Final README updates
* Screenshots if useful

---

## 27. Development Principles

### Keep It Simple

Prefer the simplest solution that satisfies the MVP.

### Minimize Infrastructure

Avoid unnecessary services, frameworks, databases, and dependencies.

### Separate Responsibilities

Routing, assignment, authentication, and issue workflow should have clearly understandable responsibilities.

### Avoid Premature Abstraction

Do not create generalized systems for functionality that only has one use case in the MVP.

### Preserve Future Flexibility Where Inexpensive

Avoid architectural choices that unnecessarily prevent future improvements, but do not implement hypothetical features.

### Optimize for Reliability

A smaller reliable system is preferable to a larger partially working system.

### Incremental Implementation

The application should be implemented and tested in small milestones.

A working milestone should be verified before proceeding to the next major feature.

---

## 28. Known Architectural Limitations

The MVP intentionally does not support:

* Assignment history
* Manual reassignment
* Issue reopening
* Issue deletion
* Issue editing after submission
* Notifications
* Escalation workflows
* Staff comments or chat
* Advanced analytics
* AI-based routing
* Separate mobile application
* Complex workforce optimization

These limitations may be revisited only after the core MVP is complete and reliable.

---

## 29. Pending Technical Decisions

The following details do not need to be fully specified before beginning implementation and may be finalized when the relevant milestone is reached.

### Database

* Exact SQLite column types
* Exact constraints
* Exact indexes
* Database initialization/seed mechanism

### Backend

* Exact Flask route organization
* Exact database access implementation
* Exact validation implementation

### Authentication

* Exact Flask session/authentication mechanism
* Exact password hashing implementation
* Login/session error handling

### Routing

* Exact function placement
* Invalid-category handling details

### Assignment

* Exact workload query
* Exact deterministic tie-breaking implementation
* Exact transaction ordering

### Frontend

* Exact page/template breakdown
* Exact JavaScript implementation
* Exact CSS organization
* Exact drawer behavior on small screens

### Deployment

* Hosting method
* Production configuration
* Database handling for the deployed demo

These decisions should be made only when they become necessary and should favor simple solutions compatible with the existing architecture.

---

## 30. Architecture Status

**Current status:** Ready for implementation.

The product behavior has been substantially defined in `docs/research.md`.

The technical architecture, technology stack, core data model, application responsibilities, repository structure, and implementation progression have now been defined sufficiently to begin the MVP.

Remaining technical details should be resolved incrementally during implementation rather than delaying development for unnecessary upfront design.

The architecture describes the intended MVP implementation, not a production-scale future system.
