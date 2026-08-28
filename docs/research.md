# CampusSync — Product Research & Requirements

> **Project:** CampusSync
> **Context:** 48-hour BuildSprint hackathon
> **Status:** Product definition substantially finalized

---

## 1. Problem

Academic institutions often rely on fragmented communication between faculty, departments, facilities teams, and administration for everyday operational issues.

Examples include:

* IT/equipment malfunctions
* Classroom/facility problems
* Academic or schedule changes
* Miscellaneous institutional requests

These requests may be communicated through WhatsApp, email, phone calls, verbal communication, or other informal channels.

This can result in:

* Unnecessary coordination overhead
* Repeated communication
* Unclear responsibility
* Delayed resolution
* Difficulty tracking issue status
* Additional workload for staff
* Limited visibility for management

---

## 2. Proposed Solution

**CampusSync** is a centralized coordination platform for academic institutions.

The goal is to turn informal operational requests into a structured and trackable workflow.

The core workflow is:

**Faculty → Automatic Routing → Department → Automatic Staff Assignment → Resolution → Management Visibility**

A Faculty member submits an operational issue.

CampusSync then:

1. Determines the responsible department from the selected category.
2. Identifies eligible Staff members in that department.
3. Assigns the issue to the Staff member with the lowest active workload.
4. Allows the Staff member to acknowledge and work on the issue.
5. Allows the Staff member to mark the issue as resolved.
6. Allows Management to monitor the overall workflow.

---

## 3. Target Users

The MVP has exactly three user roles.

### 3.1 Faculty

Faculty members can:

* Submit operational issues
* Provide issue details
* Select an issue category
* View their submitted issues
* Track issue status
* View issue details

Faculty do not choose the responsible department or Staff member.

---

### 3.2 Department Staff

Department Staff can:

* View issues assigned to them
* View issue details
* Acknowledge assigned issues
* Work on issues
* Mark issues as resolved

Staff cannot choose their assignments or modify the original issue details.

---

### 3.3 Management

Management can:

* View issues across the institution
* View issue details
* Monitor issue statuses
* See responsible departments and Staff
* View issue counts
* Filter issues by status, department, and category

Management has read-only visibility into issues in the MVP.

---

## 4. Issue Categories

The MVP contains four categories:

1. **IT / Equipment**
2. **Facilities / Classroom**
3. **Academic / Schedule**
4. **Miscellaneous**

Faculty members select the category when submitting an issue.

---

## 5. Department Routing

Each issue category is mapped to a responsible department.

| Category               | Department              |
| ---------------------- | ----------------------- |
| IT / Equipment         | IT Department           |
| Facilities / Classroom | Facilities Department   |
| Academic / Schedule    | Academic Administration |
| Miscellaneous          | General Administration  |

Routing uses predefined deterministic rules.

AI-based classification is not part of the MVP.

The Faculty member selects the category, and the application determines the responsible department.

---

## 6. Automatic Staff Assignment

After an issue is routed to a department, CampusSync automatically assigns it to an eligible Staff member.

### Eligibility

Only Staff members belonging to the responsible department are considered.

### Workload

A Staff member's active workload consists of issues currently in:

* `Assigned`
* `In Progress`

Resolved issues do not count toward active workload.

### Selection

The Staff member with the lowest active workload is selected.

Example:

| Staff   | Active Issues |
| ------- | ------------: |
| Staff A |             4 |
| Staff B |             2 |
| Staff C |             1 |

A new issue is assigned to **Staff C**.

If multiple Staff members have the same workload, a deterministic tie-breaking mechanism will be used.

### No eligible Staff

If no eligible Staff member exists:

* No Assignment is created.
* The issue remains `Submitted`.
* Management can see the issue.

Assignment history and manual reassignment are outside the MVP.

---

## 7. Issue Lifecycle

The MVP uses four issue statuses:

**Submitted → Assigned → In Progress → Resolved**

### Status meanings

#### Submitted

The Faculty member has submitted the issue.

If Staff is available, the system routes and assigns the issue.

If no eligible Staff member is available, the issue remains in this state.

#### Assigned

The system has assigned the issue to a Staff member, but the Staff member has not yet acknowledged it.

#### In Progress

The assigned Staff member has acknowledged the issue and is handling it.

#### Resolved

The Staff member has marked the issue as resolved.

Resolved issues cannot be reopened in the MVP.

If the same problem occurs again, Faculty submits a new issue.

---

## 8. Status Transition Rules

Status transitions are strictly forward-only.

| Current Status | Trigger                     | Next Status |
| -------------- | --------------------------- | ----------- |
| Submitted      | Successful Staff assignment | Assigned    |
| Assigned       | Staff acknowledges          | In Progress |
| In Progress    | Staff marks resolved        | Resolved    |

There are no arbitrary backward transitions.

A resolved issue cannot return to an earlier status.

---

## 9. Issue Information

When Faculty submits an issue, they provide:

* Problem
* Description
* Room number
* Category

The system generates or determines:

* Issue ID
* Submitting Faculty member
* Responsible Department
* Assignment
* Status
* Submission timestamp
* Resolution timestamp

The original issue details are intentionally stable after submission.

---

## 10. Data Objects

The MVP uses four core data objects.

### User

Represents a person using CampusSync.

Conceptually contains:

* User ID
* Name
* Email
* Password
* Role
* Department association where applicable

Roles:

* Faculty
* Staff
* Management

Staff members belong to an operational department.

---

### Department

Represents an operational department responsible for handling issues.

Conceptually contains:

* Department ID
* Department name

Initial departments:

* IT Department
* Facilities Department
* Academic Administration
* General Administration

---

### Issue

Represents an operational problem submitted by Faculty.

Conceptually contains:

* Issue ID
* Problem
* Description
* Room number
* Category
* Submitting Faculty
* Responsible Department
* Status
* Created timestamp
* Resolved timestamp

---

### Assignment

Represents the current Staff member responsible for an Issue.

Conceptually contains:

* Assignment ID
* Issue ID
* Staff ID
* Assignment timestamp

The MVP stores only the current assignment.

Assignment history and reassignment history are not required.

---

## 11. User Flows

### Faculty

```text
Login
  ↓
Faculty Dashboard
  ↓
Submit Issue
  ↓
Automatic Routing
  ↓
Automatic Assignment
  ↓
View / Track Issue
```

Faculty can open an issue using a details drawer/sidebar.

---

### Staff

```text
Login
  ↓
Staff Dashboard
  ↓
View Assigned Issues
  ↓
Open Issue
  ↓
Acknowledge
  ↓
In Progress
  ↓
Mark Resolved
  ↓
Resolved
```

Staff only see issues assigned to them.

---

### Management

```text
Login
  ↓
Management Dashboard
  ↓
Summary Counts
  ↓
View All Issues
  ↓
Filter Issues
  ↓
Open Issue Details
```

Management can view institution-wide issues.

---

## 12. Interface Direction

CampusSync will be a responsive web application.

A separate mobile application is not part of the MVP.

The interface should provide a good-looking, clear, and usable experience on both desktop and smaller screens.

Issues will generally be opened using a **details drawer/sidebar** rather than a separate issue-details page.

On smaller screens, the drawer may adapt to a larger or full-screen presentation.

---

## 13. Management Dashboard

Management will have a dedicated oversight dashboard.

It will contain simple summary counts:

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

## 14. Issue Editing & Deletion Rules

### Faculty

Faculty cannot edit an issue after submission.

### Staff

Staff cannot modify the original issue details.

The following remain unchanged:

* Problem
* Description
* Room number
* Category

### Management

Management has read-only visibility.

### Deletion

Issues cannot be deleted in the MVP.

### Reopening

Resolved issues cannot be reopened.

If the problem occurs again, a new issue is submitted.

---

## 15. Product Decisions

The following decisions have been made during product planning.

### Decision 1 — Issue Lifecycle

The issue lifecycle is:

**Submitted → Assigned → In Progress → Resolved**

Staff acknowledgement moves an issue from `Assigned` to `In Progress`.

Staff resolution moves an issue from `In Progress` to `Resolved`.

---

### Decision 2 — Department Routing

Routing is deterministic and category-based.

Faculty selects the category.

The application determines the responsible department using the predefined category-to-department mapping.

---

### Decision 3 — Automatic Staff Assignment

Staff assignment is automatic.

The system considers only Staff belonging to the responsible department and assigns the issue to the Staff member with the lowest active workload.

Active workload includes:

* Assigned issues
* In Progress issues

Resolved issues are excluded.

---

### Decision 4 — Authentication & Permissions

The MVP has exactly three roles:

* Faculty
* Staff
* Management

Users are pre-created for the MVP.

There is no public registration system.

Each role has access only to the functionality appropriate to that role.

---

### Decision 5 — Faculty Flow

Faculty uses a dashboard to:

* Submit issues
* View submitted issues
* Track issue status

Issue details open through a drawer/sidebar.

The MVP is a responsive web application rather than a separate mobile application.

---

### Decision 6 — Staff Flow

Staff uses a dashboard showing their assigned issues.

Opening an issue provides the appropriate workflow action.

`Acknowledge` immediately changes:

**Assigned → In Progress**

`Mark as Resolved` changes:

**In Progress → Resolved**

Staff cannot modify the original issue details.

---

### Decision 7 — Management Flow

Management uses a dedicated dashboard containing:

* Summary issue counts
* Institution-wide issue list
* Status filtering
* Department filtering
* Category filtering
* Issue details drawer

Advanced analytics are excluded from the MVP.

---

### Decision 8 — Issue Editing & Status Rules

The MVP uses stable issue records.

* Faculty cannot edit after submission.
* Staff cannot edit original issue details.
* Management has read-only visibility.
* Issues cannot be deleted.
* Resolved issues cannot be reopened.
* Status transitions are strictly forward-only.

---

## 16. MVP Scope

The MVP must provide:

* Three user roles
* Faculty issue submission
* Four issue categories
* Issue details
* Automatic department routing
* Automatic Staff assignment
* Workload-based assignment
* Issue status tracking
* Staff issue management
* Management visibility
* Basic Management filtering
* Responsive web interface

The priority is a reliable end-to-end workflow rather than a large number of features.

---

## 17. Explicitly Out of Scope

The following are not required for the MVP:

* Mobile application
* AI-based classification
* Advanced notification infrastructure
* Advanced analytics
* ERP integration
* Complex scheduling software
* Advanced workforce optimization
* Manual reassignment
* Assignment history
* Issue reopening
* Issue deletion
* Issue editing after submission
* Staff comments or chat
* Escalation workflows
* Other unrelated institutional systems

Optional features should only be considered after the core MVP is working reliably.

---

## 18. Known MVP Limitations

The MVP intentionally uses simplified workflows suitable for a 48-hour hackathon.

Examples include:

* No issue editing after submission
* No manual reassignment
* No assignment history
* No reopening of resolved issues
* No notifications
* No escalation mechanism
* No staff comments or chat
* No advanced workforce management

These limitations may be revisited if the core MVP is completed early.

---

## 19. Development Philosophy

CampusSync is being built by a solo beginner within a 48-hour hackathon.

Therefore development should prioritize:

* Small implementation steps
* Simple solutions
* Understandability
* Reliable functionality
* Frequent testing
* Minimal infrastructure
* Avoiding unnecessary dependencies
* Avoiding premature optimization
* Avoiding feature creep

The intended progression is:

```text
1. Basic application
       ↓
2. Authentication
       ↓
3. Faculty issue submission
       ↓
4. Department routing
       ↓
5. Automatic Staff assignment
       ↓
6. Staff workflow
       ↓
7. Management dashboard
       ↓
8. Complete workflow testing
       ↓
9. UI polish
       ↓
10. Demo preparation
```

---

## 20. Future Improvements

If sufficient time remains after the MVP is reliable, possible future improvements include:

* Issue editing/correction workflows
* Manual reassignment
* Assignment history
* Notifications
* Escalation mechanisms
* Staff notes
* Issue reopening
* Advanced analytics
* AI-assisted classification
* Mobile application

These are future possibilities and are not requirements for the hackathon MVP.

---

## 21. Product Status

**Current status:** Core product definition substantially finalized.

The major product decisions have been made.

Further decisions should be made only when they are necessary for implementation or are required to resolve an actual ambiguity.

The project should now move from product planning toward technical implementation.
