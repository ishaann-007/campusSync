# CampusSync — Research & Product Definition

## 1. Project Overview

**CampusSync** is a centralized coordination platform for academic institutions.

The goal is to turn informal operational requests into a structured, trackable workflow.

### Core Concept

> Faculty submit operational issues, CampusSync automatically routes each issue to the appropriate department and assigns it to a staff member based on workload. Staff manage the issue through resolution, while management can monitor the overall workflow.

---

## 2. Problem Statement

Academic institutions often rely on fragmented communication between faculty, departments, facilities teams, and administration for everyday operational issues.

Examples include:

* IT or equipment malfunctions
* Classroom or facility problems
* Academic or schedule-related issues
* Miscellaneous institutional requests

These requests may be communicated through:

* WhatsApp
* Email
* Phone calls
* Verbal communication
* Other informal channels

This can result in:

* Unnecessary coordination overhead
* Repeated communication
* Unclear responsibility
* Delayed resolution
* Difficulty tracking issue status
* Additional workload for staff
* Limited visibility for management

---

## 3. Proposed Solution

CampusSync provides a centralized workflow for handling institutional operational requests.

The intended workflow is:

**Faculty → Automatic Routing → Department → Automatic Staff Assignment → Resolution → Management Visibility**

Instead of relying on informal communication, each issue becomes a structured record with an identifiable department, responsible staff member, and current status.

---

## 4. Target Users

The MVP contains exactly three user roles.

### Faculty

Faculty members can:

* Submit operational issues
* Provide issue details
* Track submitted issues

### Department Staff

Department staff can:

* Receive assigned issues
* View issue details
* Work on issues
* Update issue status
* Mark issues as resolved

### Management

Management can:

* View issues across departments
* Monitor issue statuses
* See responsible departments
* See responsible staff
* Gain overall visibility into unresolved requests

---

## 5. Issue Categories

The MVP uses four predefined issue categories:

1. **IT / Equipment**
2. **Facilities / Classroom**
3. **Academic / Schedule**
4. **Miscellaneous**

---

## 6. Department Routing

CampusSync will initially use predefined deterministic routing rules.

No AI-based issue classification is required for the MVP.

| Issue Category         | Responsible Department  |
| ---------------------- | ----------------------- |
| IT / Equipment         | IT Department           |
| Facilities / Classroom | Facilities Department   |
| Academic / Schedule    | Academic Administration |
| Miscellaneous          | General Administration  |

The routing process is:

**Issue Category → Predefined Rule → Responsible Department**

This keeps the routing system simple, predictable, and easy to demonstrate.

---

## 7. Automatic Staff Assignment

After an issue is routed to a department, CampusSync automatically assigns it to an available staff member.

### Assignment Strategy

The MVP uses **workload-based assignment**.

The system considers the number of active issues currently assigned to each staff member within the relevant department.

The new issue is assigned to the staff member with the lowest active workload.

Example:

| Staff Member | Active Issues |
| ------------ | ------------: |
| Staff A      |             4 |
| Staff B      |             2 |
| Staff C      |             1 |

A new issue is assigned to **Staff C**.

If multiple staff members have the same workload, a simple deterministic tie-breaking rule can be used.

The MVP does not require sophisticated workforce optimization.

---

## 8. Issue Lifecycle

The basic issue lifecycle is:

**Submitted → Assigned → In Progress → Resolved**

### Example

A faculty member submits:

> "Projector not working in Room 204."

CampusSync:

1. Receives the issue
2. Identifies the category as **IT / Equipment**
3. Routes the issue to the **IT Department**
4. Determines the appropriate staff member based on workload
5. Assigns the issue
6. Allows the staff member to work on the issue
7. Staff updates the status
8. Issue becomes **Resolved**
9. Management can monitor the issue and its status

---

## 9. MVP Scope

The MVP prioritizes a working, demonstrable core workflow over a large number of features.

### Required MVP Features

* Three user roles
* Faculty issue submission
* Four issue categories
* Issue details
* Automatic department routing
* Automatic staff assignment
* Issue status tracking
* Staff issue management
* Management visibility

### Features Outside Initial MVP Scope

The initial version will not include:

* Mobile applications
* Complex AI classification
* Advanced notification infrastructure
* Sophisticated analytics
* ERP integration
* Complex scheduling software
* Advanced workforce optimization
* Other unrelated institutional systems

Additional features should only be considered after the core MVP works reliably.

---

## 10. Technology Stack

The selected technology stack for the MVP is:

| Component              | Technology     |
| ---------------------- | -------------- |
| Backend                | Python + Flask |
| Database               | SQLite         |
| Server-side templating | Jinja2         |
| Frontend markup        | HTML           |
| Styling                | CSS            |
| Client-side behavior   | JavaScript     |
| Version control        | Git + GitHub   |

### Stack Selection Rationale

The stack was selected with the 48-hour development constraint and beginner development experience in mind.

The project will use a simple monolithic architecture rather than introducing unnecessary complexity such as:

* Separate frontend and backend applications
* React or another frontend framework
* Multiple backend services
* A separate database server
* Microservices
* Complex infrastructure

The priority is to produce a reliable end-to-end MVP that can be understood, tested, and demonstrated within the hackathon timeframe.

Detailed technical architecture will be documented separately in `docs/architecture.md` once the relevant technical decisions have been finalized.

---

## 11. UI/UX Direction

Although the technical architecture is intentionally simple, the final product should provide a polished and professional user experience.

### Visual Direction

**Clean, modern, professional academic SaaS.**

The interface should maintain a consistent design language across all three user roles.

The planned interface should prioritize:

* Clear navigation
* Consistent typography
* Good spacing and layout
* Responsive design
* Dashboard views
* Cards and summary information
* Tables where appropriate
* Clear issue status indicators
* Simple and understandable forms
* Clear actions and feedback
* Consistent components across roles

The frontend will continue to use HTML, CSS, JavaScript, and Jinja2 rather than introducing a separate frontend framework solely for visual purposes.

UI/UX details will be designed separately before implementation.

---

## 12. Development Philosophy

CampusSync is being developed for a **48-hour hackathon**, so development will prioritize simplicity and reliability.

### Principles

* Work in small steps
* Establish the simplest working version first
* Test each milestone before moving forward
* Prefer simple implementations over sophisticated ones
* Avoid unnecessary libraries and infrastructure
* Avoid premature optimization
* Avoid feature creep
* Prioritize the end-to-end workflow
* Polish the interface after the core functionality is reliable

### Planned Development Progression

1. Get the basic application running
2. Set up user roles
3. Implement faculty issue submission
4. Implement issue categories
5. Implement department routing
6. Implement automatic staff assignment
7. Implement staff workflow
8. Implement management view
9. Test the complete workflow
10. Polish the UI and prepare the demo

This sequence may be adjusted if technical decisions require it.

---

## 13. Data Model

The MVP currently uses four core data objects:

* **User**
* **Department**
* **Issue**
* **Assignment**

The data model is intentionally limited to these objects to keep the MVP simple and achievable within the 48-hour hackathon.

### 13.1 User

Represents every person who interacts with CampusSync.

```text
User
├── user_id
├── name
├── email
├── password
├── role
└── department_id
```

#### Roles

The MVP contains exactly three roles:

* Faculty
* Staff
* Management

`department_id` is primarily relevant to Staff and identifies the operational department they belong to. This determines which department's issues they are eligible to handle.

Faculty and Management do not require an operational department association for the MVP.

Management receives institution-wide visibility through its role rather than belonging to a separate "Management Department."

### 13.2 Department

Represents an operational department responsible for handling issues.

```text
Department
├── department_id
└── name
```

The initial departments are:

1. IT Department
2. Facilities Department
3. Academic Administration
4. General Administration

The category-to-department mapping remains predefined application logic rather than a separate data object.

### 13.3 Issue

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

#### Faculty-provided information

* `problem` — short summary of the issue
* `description` — additional details about the problem
* `room_number` — location where the issue is occurring
* `category` — one of the four predefined issue categories

Faculty members select the category but do not select the responsible department.

#### System-generated information

* `issue_id` — unique identifier
* `submitted_by` — identifies the Faculty user who submitted the issue
* `department_id` — stores the department determined by routing logic
* `status` — tracks the issue lifecycle
* `created_at` — records when the issue was submitted
* `resolved_at` — records when the issue was marked resolved

Completion is represented by `status = Resolved`. A separate completion flag is not required.

### 13.4 Assignment

Represents the current Staff member responsible for an Issue.

```text
Assignment
├── assignment_id
├── issue_id
├── staff_id
└── assigned_at
```

The MVP uses **one current Assignment per Issue**.

Assignment history and reassignment history are outside the initial MVP scope.

The Assignment connects an Issue to a Staff user. Staff workload is calculated from their active assigned issues rather than stored as a separate value.

### 13.5 Data Relationships

The core relationships are:

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
      │ contains eligible Staff
      ▼
User (Staff)

Issue
  │
  │ has one current Assignment
  ▼
Assignment
  │
  │ assigned to
  ▼
User (Staff)
```

The overall workflow is:

```text
Faculty submits Issue
        ↓
Faculty selects Category
        ↓
Routing Logic determines Department
        ↓
Eligible Staff are identified from that Department
        ↓
Active workloads are compared
        ↓
Lowest-workload Staff member is selected
        ↓
Current Assignment is created
        ↓
Staff manages the Issue
        ↓
Issue becomes Resolved
```

### 13.6 Assignment and Routing — Implementation To Be Defined

The product-level decisions have been established, but the technical implementation has intentionally not been finalized yet.

The following decisions will be documented after the technical design is discussed:

* How category-to-department routing will be represented in the application
* How routing logic will be separated from data models
* How eligible Staff will be identified
* How active workload will be calculated
* How workload ties will be resolved
* How the current Assignment will be created
* What happens if no eligible Staff member is available
* Exact status transition behavior
* How these rules will be represented in the technical architecture

These are **implementation and architecture decisions**, not additional product requirements.

---

## 14. Current Development Status

The project is currently in the **planning and design stage**.

The product concept, MVP scope, technology stack, routing strategy, staff assignment strategy, issue lifecycle, UI direction, and core data model have been established.

The next stage is to make the remaining technical decisions needed to describe how the agreed product will actually be implemented.

Detailed technical architecture, including application structure, database relationships, routes, internal components, and implementation-level workflows, will be documented separately in:

`docs/architecture.md`

That document should be updated as technical decisions are finalized rather than being treated as a fixed specification before implementation decisions are made.

---

## 15. Repository Documentation

Current repository structure:

```text
CampusSync/
├── docs/
│   └── research.md
└── README.md
```

Planned documentation:

```text
CampusSync/
├── docs/
│   ├── research.md
│   └── architecture.md
├── README.md
└── ...
```

`research.md` defines the product problem, solution, users, workflow, MVP scope, and major product decisions.

`architecture.md` will describe the actual technical implementation and architecture after those decisions have been finalized.

---

## 14. Repository Documentation

Current repository structure:

```text
CampusSync/
├── docs/
│   └── research.md
└── README.md
```

Planned documentation:

```text
CampusSync/
├── docs/
│   ├── research.md
│   └── architecture.md
├── README.md
└── ...
```

`research.md` defines the product problem, solution, users, workflow, MVP scope, and major product decisions.

`architecture.md` will describe the actual technical implementation and architecture after those decisions have been finalized.
