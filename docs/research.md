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

Instead of relying on informal communication, each issue becomes a structured record with:

* A defined category
* A responsible department
* A responsible staff member
* A current status
* Submission and resolution timestamps

---

## 4. Target Users

The MVP contains exactly three user roles.

### Faculty

Faculty members can:

* Submit operational issues
* Provide issue details
* Select an issue category
* Track their submitted issues
* View the responsible department and assigned Staff

Faculty cannot select the responsible department or Staff member.

### Department Staff

Department Staff can:

* View issues assigned to them
* View issue details
* Acknowledge assigned issues
* Work on issues
* Update issue status
* Mark issues as resolved

Staff cannot manually choose or reassign issues.

### Management

Management can:

* View issues across the institution
* Monitor issue statuses
* See responsible departments
* See assigned Staff
* Filter issues by status, department, and category
* View overall issue counts

Management is an oversight role in the MVP rather than an operational issue-handling role.

---

## 5. Issue Categories

The MVP uses four predefined issue categories:

1. **IT / Equipment**
2. **Facilities / Classroom**
3. **Academic / Schedule**
4. **Miscellaneous**

Faculty members select the category when submitting an issue.

---

## 6. Department Routing

CampusSync uses predefined deterministic routing rules.

No AI-based issue classification is required for the MVP.

| Issue Category         | Responsible Department  |
| ---------------------- | ----------------------- |
| IT / Equipment         | IT Department           |
| Facilities / Classroom | Facilities Department   |
| Academic / Schedule    | Academic Administration |
| Miscellaneous          | General Administration  |

The routing process is:

**Selected Category → Predefined Routing Rule → Responsible Department**

Faculty members select the category, while CampusSync determines the responsible department.

The category-to-department mapping is treated as application logic rather than a separate data object.

---

## 7. Automatic Staff Assignment

After an issue is routed to a department, CampusSync automatically assigns it to an eligible Staff member.

### Eligibility

Only Staff belonging to the responsible department are eligible for assignment.

### Assignment Strategy

The MVP uses **workload-based assignment**.

Active workload is the number of issues currently assigned to a Staff member whose status is:

* `Assigned`
* `In Progress`

Resolved issues do not count toward active workload.

The new issue is assigned to the eligible Staff member with the lowest active workload.

Example:

| Staff Member | Active Issues |
| ------------ | ------------: |
| Staff A      |             4 |
| Staff B      |             2 |
| Staff C      |             1 |

A new issue is assigned to **Staff C**.

If multiple Staff members have the same workload, a simple deterministic tie-breaking rule will be used.

### No Eligible Staff

If no eligible Staff member is available in the responsible department, the issue remains:

**`Submitted` and unassigned.**

The issue remains visible to Management.

### Reassignment

Manual reassignment is outside the MVP scope.

The MVP stores only the **current assignment** and does not maintain assignment history.

---

## 8. Issue Lifecycle

The MVP uses four issue statuses:

**Submitted → Assigned → In Progress → Resolved**

### Status meanings

| Status        | Meaning                                                                   |
| ------------- | ------------------------------------------------------------------------- |
| `Submitted`   | The Faculty member has submitted the issue                                |
| `Assigned`    | CampusSync has assigned the issue to a Staff member                       |
| `In Progress` | The assigned Staff member has acknowledged the issue and is working on it |
| `Resolved`    | The Staff member has completed the issue                                  |

### Status transitions

Status transitions are strictly forward-only.

```text
Submitted
    ↓
Assigned
    ↓
In Progress
    ↓
Resolved
```

The normal transitions are:

| Current Status | Trigger                         | Next Status   |
| -------------- | ------------------------------- | ------------- |
| `Submitted`    | Successful automatic assignment | `Assigned`    |
| `Assigned`     | Staff acknowledges the issue    | `In Progress` |
| `In Progress`  | Staff marks the issue resolved  | `Resolved`    |

If no eligible Staff member exists, the issue remains `Submitted`.

When an issue becomes `Resolved`, the system records the resolution timestamp.

A separate completion field is not required because completion is represented by the `Resolved` status.

---

## 9. User Flows & Interface Direction

CampusSync will be implemented as a **responsive web application**.

A separate mobile application is outside the MVP scope.

The same general interaction pattern will be used across the application: users can open an issue to view its details in a **drawer/sidebar** rather than navigating to a separate issue-details page.

On smaller screens, the drawer can adapt into a larger or full-screen details view.

### 9.1 Faculty Flow

```text
Login
  ↓
Faculty Dashboard
  ↓
Submit Issue / Track Issues
  ↓
Issue Details Drawer
```

The Faculty issue submission form contains:

* Problem
* Description
* Room number
* Category

Faculty does not provide:

* Department
* Staff member

These are determined automatically by CampusSync.

### 9.2 Staff Flow

```text
Login
  ↓
Staff Dashboard
  ↓
Assigned Issues
  ↓
Issue Details Drawer
  ↓
Acknowledge
  ↓
In Progress
  ↓
Mark Resolved
  ↓
Resolved
```

Staff see only issues currently assigned to them.

### 9.3 Management Flow

```text
Login
  ↓
Management Dashboard
  ↓
Summary Counts
  ↓
All Institutional Issues
  ↓
Filter / Inspect Issue
  ↓
Issue Details Drawer
```

The Management dashboard provides simple summary counts for:

* Total Issues
* Assigned
* In Progress
* Resolved

Management can filter the issue list by:

* Status
* Department
* Category

Advanced analytics are outside the MVP.

---

## 10. Issue Editing & Status Rules

The MVP intentionally keeps issue records stable after submission.

### Faculty Editing

Faculty cannot edit an issue after submission.

This is an explicit MVP limitation.

If a correction or new problem needs to be reported, a new issue should be submitted.

### Staff Editing

Staff cannot modify the original issue details.

The following remain unchanged after submission:

* Problem
* Description
* Room number
* Category

Staff interact with the issue through its status workflow rather than modifying the original report.

### Issue Deletion

Issues cannot be deleted in the MVP.

This preserves the issue record and avoids deletion-related assignment and history handling.

### Reopening

Resolved issues cannot be reopened in the MVP.

If the same problem occurs again, Faculty submits a new issue.

Therefore:

**Resolved → End**

---

## 11. MVP Scope

The MVP prioritizes a working, demonstrable core workflow over a large number of features.

### Required MVP Features

* Three user roles
* User authentication
* Faculty issue submission
* Four issue categories
* Issue details
* Automatic department routing
* Automatic Staff assignment
* Workload-based assignment
* Issue status tracking
* Staff issue management
* Management visibility
* Management filtering
* Responsive web interface

### Features Outside Initial MVP Scope

The initial version will not include:

* Separate mobile applications
* AI-based issue classification
* Advanced notification infrastructure
* Escalation systems
* Manual reassignment workflows
* Assignment history
* Staff comments or chat
* Sophisticated analytics
* Staff performance metrics
* ERP integration
* Complex scheduling software
* Advanced workforce optimization
* Other unrelated institutional systems

Additional features should only be considered after the core MVP works reliably.

---

## 12. Technology Stack

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

Detailed technical implementation will be documented separately in:

`docs/architecture.md`

---

## 13. UI/UX Direction

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
* Tables or issue lists where appropriate
* Clear issue status indicators
* Simple and understandable forms
* Clear actions and feedback
* Consistent components across roles

The frontend will continue to use HTML, CSS, JavaScript, and Jinja2 rather than introducing a separate frontend framework solely for visual purposes.

UI/UX details can be refined during implementation without changing the underlying product workflow.

---

## 14. Data Model

The MVP uses four core data objects:

* **User**
* **Department**
* **Issue**
* **Assignment**

The data model is intentionally limited to these objects to keep the MVP manageable within the 48-hour hackathon.

### 14.1 User

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

`department_id` is primarily relevant to Staff and identifies the operational department they belong to.

Faculty and Management do not require an operational department association for the MVP.

Management receives institution-wide visibility through its role rather than belonging to a separate Management Department.

---

### 14.2 Department

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

The category-to-department mapping is predefined application logic rather than a separate data object.

---

### 14.3 Issue

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
* `category` — selected from the four predefined categories

Faculty selects the category but does not select the responsible department or Staff member.

#### System-generated information

* `issue_id` — unique identifier
* `submitted_by` — Faculty user who submitted the issue
* `department_id` — department determined by routing logic
* `status` — current issue lifecycle state
* `created_at` — time the issue was submitted
* `resolved_at` — time the issue was marked resolved

Completion is represented by `status = Resolved`. A separate completion flag is not required.

---

### 14.4 Assignment

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

The Assignment connects an Issue to a Staff user.

Staff workload is calculated from their active assigned Issues rather than stored as a separate value.

---

### 14.5 Data Relationships

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
      │ identifies eligible Staff
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

The overall product workflow is:

```text
Faculty submits Issue
        ↓
Faculty selects Category
        ↓
Routing Logic determines Department
        ↓
Eligible Staff are identified
        ↓
Active workloads are compared
        ↓
Lowest-workload Staff member is selected
        ↓
Current Assignment is created
        ↓
Staff acknowledges the issue
        ↓
Issue becomes In Progress
        ↓
Staff resolves the issue
        ↓
Issue becomes Resolved
        ↓
Management can monitor the issue
```

### 14.6 Data Objects Deliberately Not Included

The MVP does not use separate data objects for:

* Routing Rules
* Workload
* Assignment History
* Categories
* Issue Statuses
* Notifications
* Staff Skills
* Staff Locations
* Analytics
* Comments or chat

Where appropriate, these are represented through predefined values or application logic.

---

## 15. Development Philosophy

CampusSync is being developed for a **48-hour hackathon**, so development will prioritize simplicity and reliability.

### Principles

* Work in small steps
* Establish the simplest working version first
* Test each milestone before moving forward
* Prefer simple implementations over sophisticated ones
* Avoid unnecessary libraries and infrastructure
* Avoid premature optimization
* Avoid feature creep
* Prioritize the complete end-to-end workflow
* Polish the interface after the core functionality is reliable
* Do not add optional features until the MVP is working reliably

### Planned Development Progression

1. Get the basic application running
2. Establish the database and core data model
3. Set up authentication and user roles
4. Implement Faculty issue submission
5. Implement category selection
6. Implement department routing
7. Implement automatic Staff assignment
8. Implement Staff workflow
9. Implement Management dashboard and filtering
10. Test the complete workflow
11. Polish the UI
12. Prepare the final demo

This sequence may be adjusted if technical decisions require it.

---

## 16. Known MVP Limitations

The following limitations are intentional scope decisions for the hackathon:

* Faculty cannot edit issues after submission.
* Staff cannot modify the original issue details.
* Issues cannot be deleted.
* Resolved issues cannot be reopened.
* Manual reassignment is not supported.
* Assignment history is not stored.
* If no eligible Staff member exists, an issue remains `Submitted` and unassigned.
* No notification or escalation system is included.
* No separate mobile application is included.
* Management receives basic counts and filtering rather than advanced analytics.
* No chat, comments, or communication system is included.
* No AI classification is used for routing.

These limitations can be revisited after the core MVP is complete if sufficient development time remains.

---

## 17. Current Development Status

The project is currently transitioning from **product definition to technical architecture and implementation planning**.

### Completed

* Problem definition
* Proposed solution
* User roles
* Issue categories
* Department routing strategy
* Automatic assignment strategy
* Issue lifecycle
* User flows
* Management dashboard scope
* Core data model
* MVP limitations
* Technology stack

### Next Stage

The next stage is to finalize the technical architecture, including:

* Database implementation
* Application structure
* Routing implementation
* Assignment implementation
* Authentication implementation
* Role-based access implementation
* Application flows
* Project folder structure

These technical decisions will be documented in:

`docs/architecture.md`

---

## 18. Repository Documentation

Current repository structure:

```text
CampusSync/
├── docs/
│   └── research.md
└── README.md
```

Planned structure:

```text
CampusSync/
├── docs/
│   ├── research.md
│   └── architecture.md
├── README.md
└── ...
```

### Documentation Responsibilities

`research.md` defines:

* The problem
* The proposed solution
* Product requirements
* User roles
* Product workflow
* MVP scope
* Product-level decisions
* Known limitations

`architecture.md` defines:

* How the agreed product is implemented technically
* Application structure
* Database relationships
* Routing implementation
* Assignment implementation
* Authentication architecture
* Role-based access
* Technical workflows
* Project structure

The two documents should be maintained separately to avoid unnecessary duplication.

Existing decisions should be edited in place rather than creating multiple competing versions of the same decision.
