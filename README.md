# CampusSync

**A centralized coordination platform for academic institutions.**

CampusSync helps faculty report operational issues, automatically routes them to the appropriate department, assigns them to a staff member based on current workload, and provides management with visibility into ongoing work.

> **Built for BuildSprint 2026**

---

## The Problem

Academic institutions often rely on multiple communication channels to handle everyday operational issues — messages, calls, emails, and verbal requests.

This creates unnecessary coordination overhead.

A simple issue such as a broken classroom projector can involve several people before reaching the person responsible for fixing it. There may also be no clear way to track who is handling the issue or whether it has been resolved.

**CampusSync turns this fragmented process into a single, structured, and trackable workflow.**

---

## How It Works

```text
Faculty
   │
   │ Submit Issue
   ▼
CampusSync
   │
   ├── Identify Category
   │
   ├── Route to Department
   │
   └── Assign Staff by Workload
   │
   ▼
Department Staff
   │
   │ Handle & Update
   ▼
Resolved
   │
   ▼
Management Visibility
```

### Example

A faculty member reports:

> **"Projector not working in Room 204."**

The faculty member selects **IT / Equipment** as the category.

CampusSync then:

1. Routes the issue to the **IT Department**.
2. Identifies eligible staff in that department.
3. Compares their active workloads.
4. Assigns the issue to the staff member with the lowest active workload.
5. Allows the issue to be tracked until resolution.

---

## Core Features

### Faculty

* Submit operational issues
* Select an issue category
* Provide problem details
* Provide the room number
* Track submitted issues

### Department Staff

* Receive automatically assigned issues
* View assigned issue details
* Update issue status
* Resolve assigned issues

### Management

* View issues across departments
* Monitor issue statuses
* See responsible departments and staff
* Monitor unresolved requests

### Automatic Routing & Assignment

CampusSync uses predefined deterministic rules to route issues from their selected category to the responsible department.

Once routed, the issue is automatically assigned to a staff member in that department based on active workload.

> **Goal:** reduce manual coordination and give every issue clear ownership.

---

## Issue Categories

| Category                   | Department              |
| :------------------------- | :---------------------- |
| **IT / Equipment**         | IT Department           |
| **Facilities / Classroom** | Facilities Department   |
| **Academic / Schedule**    | Academic Administration |
| **Miscellaneous**          | General Administration  |

Faculty members select the category. The responsible department is determined automatically by CampusSync.

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

Each issue has a defined status throughout its lifecycle.

When an issue is resolved, CampusSync records the resolution timestamp.

---

## User Roles

| Role                 | Purpose                            |
| :------------------- | :--------------------------------- |
| **Faculty**          | Submit and track issues            |
| **Department Staff** | Handle and resolve assigned issues |
| **Management**       | Monitor issues across departments  |

---

## Data Model

The MVP currently uses four core data objects:

```text
User
Department
Issue
Assignment
```

### User

Represents people who interact with CampusSync.

Users have one of three roles:

* Faculty
* Staff
* Management

Staff members are associated with an operational department.

### Department

Represents the departments responsible for handling issues.

The initial departments correspond to the four issue categories.

### Issue

Represents an operational problem submitted by Faculty.

An issue contains:

* Problem
* Description
* Room number
* Category
* Submitting Faculty member
* Responsible Department
* Status
* Submission timestamp
* Resolution timestamp

### Assignment

Represents the current Staff member responsible for an issue.

For the MVP, each issue has one current assignment.

Staff workload is determined from their active assigned issues rather than stored as a separate workload value.

---

## MVP

The initial version focuses on the core coordination workflow:

* [x] Project concept & workflow
* [x] Three user roles
* [x] Four issue categories
* [x] Department routing rules
* [x] Core data model
* [x] Technology stack
* [ ] User authentication
* [ ] Faculty issue submission
* [ ] Automatic department routing
* [ ] Automatic staff assignment
* [ ] Issue status tracking
* [ ] Staff interface
* [ ] Management interface
* [ ] End-to-end workflow testing
* [ ] UI polish

> The checklist reflects the current development stage and will be updated as CampusSync is built.

---

## Tech Stack

CampusSync uses a lightweight web stack selected for the 48-hour hackathon:

| Layer     | Technology                |
| :-------- | :------------------------ |
| Backend   | **Python + Flask**        |
| Database  | **SQLite**                |
| Templates | **Jinja2**                |
| Frontend  | **HTML, CSS, JavaScript** |

The architecture intentionally avoids a separate frontend framework or unnecessary infrastructure so that the team can focus on the core MVP.

---

## Project Structure

The repository currently contains:

```text
CampusSync/
├── docs/
│   ├── research.md
│   └── architecture.md
├── README.md
└── ...
```

### Documentation

* `docs/research.md` — product definition, requirements, scope, and major product decisions.
* `docs/architecture.md` — technical architecture and implementation decisions.

The project structure will evolve as development progresses.

---

## Development Approach

CampusSync is being developed as a 48-hour hackathon MVP.

Development will proceed incrementally:

```text
Application Setup
       ↓
Database & Data Model
       ↓
Authentication & Roles
       ↓
Faculty Issue Submission
       ↓
Department Routing
       ↓
Automatic Staff Assignment
       ↓
Staff Workflow
       ↓
Management Visibility
       ↓
End-to-End Testing
       ↓
UI Polish & Demo
```

The priority is a reliable end-to-end workflow rather than a large number of additional features.

---

## Roadmap

### Phase 1 — Core MVP

* Authentication
* Role-based access
* Issue submission
* Department routing
* Automatic staff assignment
* Issue status tracking
* Staff workflow
* Management visibility

### Phase 2 — Post-MVP Improvements

Potential improvements may include:

* Notifications
* More detailed reporting
* Improved workload balancing
* Additional operational insights

### Future

Further features will only be considered after the core MVP is working reliably.

---

## Why CampusSync?

CampusSync focuses on a simple institutional problem:

> **Getting the right issue to the right department and the right person without unnecessary coordination.**

Instead of relying on scattered conversations, every request becomes a structured and trackable workflow with clear ownership.

---

## Status

🚧 **In Development**

CampusSync is being developed during **BuildSprint 2026** as a 48-hour hackathon project.

---

## License

License information will be added after the project is finalized.
