# CampusSync — Technical Architecture

> **Status:** Initial architecture — under development
> **Project:** CampusSync
> **Context:** 48-hour BuildSprint hackathon

---

## 1. Architecture Overview

CampusSync will use a simple web application architecture designed around the constraints of a solo beginner developer working within a 48-hour hackathon.

The architecture prioritizes:

* Simplicity
* Understandability
* Fast development
* Minimal infrastructure
* Reliable end-to-end functionality
* Clear separation between application responsibilities

The system will use a **monolithic web application** rather than separate frontend and backend services.

### High-Level Structure

```text
Faculty / Staff / Management
            │
            ▼
      Web Interface
            │
            ▼
      Flask Application
            │
      ┌─────┴─────┐
      │           │
 Business Logic  Authentication
      │
      ├── Routing
      ├── Assignment
      └── Issue Workflow
            │
            ▼
         SQLite
```

The exact internal structure and request flow will be finalized during the remaining architecture decisions.

---

## 2. Technology Stack

The current technology stack is:

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

The goal is to get a complete working application rather than build production-scale infrastructure.

---

## 3. Application Architecture

CampusSync will follow a simple monolithic structure.

The major responsibilities are expected to be separated into:

```text
Presentation
     ↓
Application / Request Handling
     ↓
Business Logic
     ↓
Data Access
     ↓
SQLite Database
```

The exact implementation of these layers and the project folder structure will be decided before implementation.

---

## 4. Core Data Model

The MVP contains four core data objects:

1. User
2. Department
3. Issue
4. Assignment

### 4.1 User

Represents a person using CampusSync.

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

Roles:

* Faculty
* Staff
* Management

Staff users are associated with an operational department.

Faculty and Management do not require an operational department association for the MVP.

---

### 4.2 Department

Represents an operational department responsible for handling issues.

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

---

### 4.3 Issue

Represents an operational problem submitted by Faculty.

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

Faculty provides:

* Problem
* Description
* Room number
* Category

The system determines:

* Responsible department
* Assignment
* Status
* Timestamps

---

### 4.4 Assignment

Represents the current Staff member responsible for an Issue.

```text
Assignment
├── assignment_id
├── issue_id
├── staff_id
└── assigned_at
```

The MVP stores only the **current assignment**.

Assignment history and reassignment history are outside the MVP.

---

## 5. Data Relationships

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

Issue
  │
  │ current assignment
  ▼
Assignment
  │
  │ assigned to
  ▼
User (Staff)
```

An Issue therefore has:

* One submitting Faculty user
* One responsible Department
* Zero or one current Assignment
* One current status

A Staff user belongs to one operational Department.

---

## 6. Issue Processing Flow

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

The exact technical implementation of routing and assignment is not yet finalized.

---

## 7. Routing Logic

CampusSync uses deterministic category-based routing.

The current mapping is:

| Category               | Department              |
| ---------------------- | ----------------------- |
| IT / Equipment         | IT Department           |
| Facilities / Classroom | Facilities Department   |
| Academic / Schedule    | Academic Administration |
| Miscellaneous          | General Administration  |

The Faculty member selects the category.

The application uses the predefined mapping to determine the responsible Department.

### Current architectural decision

The category-to-department mapping will be implemented as **application logic**, rather than creating a separate database table for routing rules.

### To be finalized

* Exact location of routing logic
* How the routing function is called during issue creation
* How invalid categories are handled
* How routing failures are handled

---

## 8. Automatic Staff Assignment

After routing, CampusSync automatically selects an eligible Staff member.

### Eligibility

Only Staff belonging to the responsible Department are considered.

### Workload

A Staff member's active workload is calculated from Issues currently in:

* `Assigned`
* `In Progress`

Resolved Issues do not count toward active workload.

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

If multiple Staff members have the same workload, a deterministic tie-breaking mechanism will be used.

### No eligible Staff

If no eligible Staff member exists:

* No Assignment is created
* Issue remains `Submitted`
* Management can see the issue

### To be finalized

* Exact workload query/calculation
* Exact tie-breaking rule
* Where assignment logic lives in the application
* Transaction/order of routing and assignment
* How assignment failures are handled

---

## 9. Issue Status Workflow

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

### Transition rules

| Current Status | Trigger               | Next Status |
| -------------- | --------------------- | ----------- |
| Submitted      | Successful assignment | Assigned    |
| Assigned       | Staff acknowledges    | In Progress |
| In Progress    | Staff marks resolved  | Resolved    |

Status transitions are **strictly forward-only**.

No arbitrary backward transitions are allowed.

### Resolved issues

Once an issue becomes `Resolved`, it cannot be reopened in the MVP.

If the same problem occurs again, Faculty submits a new Issue.

### Timestamps

The system records:

* `created_at` when the Issue is submitted
* `resolved_at` when the Issue becomes Resolved

---

## 10. Authentication & Authorization

CampusSync contains three roles:

```text
Faculty
Staff
Management
```

Users are pre-created for the MVP.

There is no public registration system.

### Role responsibilities

#### Faculty

Can:

* Submit issues
* View their own issues
* Track issue status
* View issue details

#### Staff

Can:

* View issues assigned to them
* Acknowledge assigned issues
* Mark issues as resolved
* View issue details

#### Management

Can:

* View institution-wide issues
* View issue details
* Filter issues
* Monitor issue status
* View issue counts

### Authorization

Users should only be able to perform actions appropriate to their role.

The exact authentication mechanism and authorization implementation will be finalized during architecture design.

---

## 11. Interface Architecture

CampusSync will be a responsive web application.

A separate mobile application is not part of the MVP.

### Shared interaction pattern

Issues can be opened using a **details drawer/sidebar** rather than requiring a separate issue-details page.

On smaller screens, the drawer may adapt to a larger or full-screen view.

### Faculty Interface

```text
Login
  ↓
Faculty Dashboard
  ├── Submit Issue
  └── View Submitted Issues
          ↓
      Details Drawer
```

### Staff Interface

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

### Management Interface

```text
Login
  ↓
Management Dashboard
  ├── Summary Counts
  ├── Issue List
  ├── Status Filter
  ├── Department Filter
  └── Category Filter
          ↓
      Details Drawer
```

The exact page structure and frontend component organization will be finalized during implementation planning.

---

## 12. Management Dashboard

Management has institution-wide visibility.

The dashboard will provide simple summary counts:

* Total Issues
* Assigned
* In Progress
* Resolved

Management can filter the issue list by:

* Status
* Department
* Category

Advanced analytics are not part of the MVP.

---

## 13. Issue Editing & Deletion Rules

Issue records are intentionally stable after submission.

### Faculty

Cannot edit an Issue after submission.

### Staff

Cannot modify the original Issue details.

The following fields remain unchanged:

* Problem
* Description
* Room number
* Category

### Management

Management has read-only visibility into the Issue.

### Deletion

Issues cannot be deleted in the MVP.

### Reopening

Resolved Issues cannot be reopened.

These rules reduce the amount of state-changing behavior that the application must support.

---

## 14. Project Structure

The final project structure has not yet been finalized.

The current repository contains:

```text
CampusSync/
├── docs/
│   ├── research.md
│   └── architecture.md
└── README.md
```

The application source structure will be decided after the remaining technical architecture decisions.

The final structure should remain simple and avoid unnecessary abstraction.

---

## 15. Pending Architecture Decisions

The following technical decisions remain open.

### Database

* Exact SQLite schema
* Primary/foreign keys
* Constraints
* Indexes where necessary

### Backend

* Flask application structure
* Routes
* Request handling
* Business logic organization
* Database access approach

### Authentication

* Password handling
* Login/session mechanism
* Role-based route protection

### Routing

* Exact implementation of category-to-department routing
* Validation
* Error handling

### Assignment

* Workload calculation
* Tie-breaking
* Assignment transaction flow
* Handling assignment failures

### Frontend

* Page structure
* Shared layout
* Dashboard structure
* Forms
* Details drawer implementation
* Responsive behavior

### Deployment

* Hosting/deployment method
* Production configuration
* Database handling after deployment

These decisions will be added to this document as they are finalized.

---

## 16. Development Strategy

Because CampusSync is being built by a solo beginner within a 48-hour hackathon, implementation will proceed incrementally.

The architecture should support the following progression:

```text
1. Application starts
       ↓
2. Database works
       ↓
3. Authentication works
       ↓
4. Faculty can submit issues
       ↓
5. Routing works
       ↓
6. Assignment works
       ↓
7. Staff workflow works
       ↓
8. Management dashboard works
       ↓
9. Complete workflow tested
       ↓
10. UI polished
       ↓
11. Demo prepared
```

Each major stage should be tested before moving to the next.

Optional features should not be implemented until the core workflow is reliable.

---

## 17. Architecture Principles

The following principles guide technical decisions:

### Keep it simple

Prefer the simplest solution that satisfies the MVP.

### Minimize infrastructure

Avoid unnecessary services, frameworks, and dependencies.

### Separate responsibilities

Routing, assignment, authentication, and issue workflow should have clearly understandable responsibilities.

### Avoid premature abstraction

Do not create generalized systems for functionality that only has one use case in the MVP.

### Preserve future flexibility where inexpensive

The architecture should avoid unnecessarily preventing future improvements, but future features should not be implemented solely for hypothetical requirements.

### Optimize for reliability

A smaller reliable system is preferable to a larger partially working system.

---

## 18. Known Architectural Limitations

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

These limitations may be revisited after the MVP is complete if sufficient time remains.

---

## 19. Architecture Status

**Current status:** Incomplete — architecture decisions are still being finalized.

Product behavior has been substantially defined in `docs/research.md`.

The next step is to finalize the remaining technical decisions and update this document incrementally rather than rewriting it from scratch.

The final architecture should describe the actual implementation used by CampusSync, rather than an idealized future architecture.
