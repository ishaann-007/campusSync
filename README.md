# CampusSync

**A centralized coordination platform for academic institutions.**

CampusSync helps faculty report operational issues and requests, automatically routes them to the appropriate department, assigns them to available staff, and provides management with a clear view of ongoing work.

> **Built for BuildSprint 2026**

---

## The Problem

Academic institutions rely on multiple communication channels to handle everyday operational issues — messages, calls, emails, and verbal requests.

This creates unnecessary coordination overhead.

A simple issue such as a broken classroom projector can involve several people before reaching the person responsible for fixing it. There may also be no clear way to track who is handling the issue or whether it has been resolved.

**CampusSync turns this fragmented process into a single, trackable workflow.**

---

## How It Works

```text
Faculty
   │
   │  Submit Issue
   ▼
CampusSync
   │
   ├── Identify Category
   │
   ├── Route to Department
   │
   └── Assign Staff
   │
   ▼
Department Staff
   │
   │  Handle & Update
   ▼
Resolved
   │
   ▼
Management
```

### Example

A faculty member reports:

**"Projector not working in Room 204."**

CampusSync identifies the request as **IT / Equipment**, routes it to the **IT Department**, and assigns it to a staff member based on their current workload.

The issue can then be tracked until resolution.

---

## Core Features

### Faculty

* Submit operational issues
* Select a relevant category
* Provide issue details and location
* Set priority
* Track submitted requests

### Department Staff

* Receive automatically assigned issues
* View issue details
* Update issue status
* Resolve assigned requests

### Management

* View issues across departments
* Monitor current issue status
* See responsible departments and staff
* Track unresolved requests

### Automatic Routing & Assignment

CampusSync uses predefined routing rules to determine the responsible department.

Once routed, issues are automatically assigned based on staff workload.

**Goal:** reduce manual coordination and ensure every issue has clear ownership.

---

## Issue Categories

| Category                   | Department              |
| :------------------------- | :---------------------- |
| **IT / Equipment**         | IT Department           |
| **Facilities / Classroom** | Facilities Department   |
| **Academic / Schedule**    | Academic Administration |
| **Miscellaneous**          | General Administration  |

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

Every request has a clear state and responsible party throughout its lifecycle.

---

## User Roles

| Role                 | Purpose                            |
| :------------------- | :--------------------------------- |
| **Faculty**          | Report and track issues            |
| **Department Staff** | Handle and resolve assigned issues |
| **Management**       | Monitor institutional operations   |

---

## MVP

The initial version focuses on the core coordination workflow:

* [x] Project concept & workflow
* [x] Four issue categories
* [x] Department routing rules
* [ ] User authentication
* [ ] Faculty issue submission
* [ ] Automatic department routing
* [ ] Automatic staff assignment
* [ ] Issue status tracking
* [ ] Staff dashboard
* [ ] Management dashboard

> The checklist reflects the current development stage and will be updated as CampusSync is built.

---

## Tech Stack

**To be finalized during development.**

The project will use a lightweight stack suitable for building and demonstrating the MVP within the hackathon timeframe.

---

## Project Structure

```text
CampusSync/
├── docs/
│   └── research.md
├── README.md
└── ...
```

The project structure will evolve as development progresses.

---

## Roadmap

### Phase 1 — Core MVP

* Authentication
* Issue submission
* Routing
* Staff assignment
* Status tracking

### Phase 2 — Management

* Management dashboard
* Cross-department visibility
* Basic operational insights

### Phase 3 — Future Enhancements

* Notifications
* Advanced analytics
* Issue history and reporting
* Improved workload balancing
* Institutional system integrations

---

## Why CampusSync?

CampusSync focuses on a simple but common institutional problem:

> **Getting the right issue to the right person without unnecessary coordination.**

Instead of relying on scattered conversations, every request becomes a structured, trackable workflow with clear ownership.

---

## Status

🚧 **In Development**

CampusSync is being developed during **BuildSprint 2026** as a 48-hour hackathon project.

---

## License

License information will be added after the project is finalized.
