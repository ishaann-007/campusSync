# CampusSync — Technical Architecture

> **Status:** Initial architecture draft  
> **Purpose:** Technical blueprint for the agreed CampusSync MVP.  
> **Important:** This document describes decisions that have actually been made. Unresolved implementation details are explicitly marked rather than assumed.

---

## 1. Purpose

This document defines how the agreed CampusSync MVP is intended to be structured technically.

`research.md` defines the product requirements and major product decisions. This document translates those decisions into a technical architecture.

The architecture is intentionally kept simple because CampusSync is being developed during a 48-hour hackathon and the implementation team is working with beginner-level experience.

---

## 2. Architecture Overview

CampusSync will be implemented as a small web application with a server-side backend, a lightweight relational database, and a browser-based frontend.

The high-level architecture is:

```text
User Browser
     │
     ▼
Web Interface
(Jinja2 + HTML/CSS/JavaScript)
     │
     ▼
Flask Application
     │
     ├── Authentication & Role Access
     ├── Issue Management
     ├── Routing Logic
     └── Assignment Logic
     │
     ▼
SQLite Database
```

The application follows a simple request/response model rather than introducing a separate frontend application or distributed backend.

---

## 3. Technology Stack

The current MVP stack is:

| Layer | Technology | Purpose |
|---|---|---|
| Backend | Python + Flask | Web application and server-side logic |
| Database | SQLite | Persistent relational data storage |
| Templates | Jinja2 | Server-rendered HTML pages |
| Frontend | HTML, CSS, JavaScript | User interface and basic client-side behavior |

### Stack rationale

The stack is intentionally small and familiar enough to support rapid development.

A separate frontend framework or more complex database infrastructure is not required for the MVP.

---

## 4. Core Application Components

The application will be organized around the following logical responsibilities:

### 4.1 Authentication

Responsible for:

- Identifying users
- Handling login
- Establishing the current user session
- Enforcing role-based access

### 4.2 Issue Management

Responsible for:

- Creating issues
- Retrieving issues
- Displaying issue information
- Updating issue status
- Recording resolution time

### 4.3 Routing Logic

Responsible for:

- Taking the selected issue category
- Determining the responsible department
- Providing the resulting department for the Issue

The category-to-department mapping is deterministic and predefined.

### 4.4 Assignment Logic

Responsible for:

- Identifying Staff belonging to the responsible department
- Determining active workload
- Selecting the Staff member with the lowest active workload
- Creating the current Assignment

The exact implementation of these operations remains to be finalized.

### 4.5 Role-Based Views

The interface will provide different capabilities according to the user's role:

- Faculty: submit and track their issues
- Staff: view and manage assigned issues
- Management: view issues across departments

---

## 5. Data Model

The MVP has four core data objects:

1. User
2. Department
3. Issue
4. Assignment

No separate database objects are currently planned for routing rules, workload, categories, issue statuses, notifications, staff skills, staff locations, or assignment history.

---

### 5.1 User

Represents a person who interacts with CampusSync.

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

- Faculty
- Staff
- Management

`department_id` is primarily relevant to Staff and identifies their operational department.

Management has institution-wide visibility through its role and does not belong to a separate management department in the MVP.

---

### 5.2 Department

Represents an operational department responsible for handling issues.

```text
Department
├── department_id
└── name
```

Initial departments:

1. IT Department
2. Facilities Department
3. Academic Administration
4. General Administration

The category-to-department mapping is application logic rather than a separate data object.

---

### 5.3 Issue

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

#### Faculty-provided fields

- `problem` — short summary of the issue
- `description` — additional details
- `room_number` — location of the issue
- `category` — selected from the four predefined categories

Faculty selects the category but does not select the responsible department.

#### System-generated fields

- `issue_id` — unique identifier
- `submitted_by` — Faculty user who submitted the issue
- `department_id` — department determined by routing logic
- `status` — current issue lifecycle state
- `created_at` — submission time
- `resolved_at` — time the issue was marked resolved

Completion is represented by `status = Resolved`. A separate completion flag is not required.

---

### 5.4 Assignment

Represents the current Staff member responsible for an Issue.

```text
Assignment
├── assignment_id
├── issue_id
├── staff_id
└── assigned_at
```

The MVP uses one current Assignment per Issue.

Assignment history and reassignment history are outside the initial MVP scope.

Workload is not stored as a separate value. It is determined from the Staff member's active assigned issues.

---

## 6. Entity Relationships

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

Conceptually:

- A Faculty user can submit multiple Issues.
- A Staff user belongs to an operational Department.
- An Issue is submitted by a Faculty user.
- An Issue is routed to one Department.
- An Issue has one current Assignment in the MVP.
- An Assignment identifies the Staff user responsible for that Issue.

---

## 7. Core Application Flow

The intended end-to-end flow is:

```text
Faculty
   │
   │ submits issue
   ▼
Issue Created
   │
   │ category selected by Faculty
   ▼
Routing Logic
   │
   │ determines department
   ▼
Department Assigned
   │
   │ identify eligible Staff
   ▼
Assignment Logic
   │
   │ compare active workloads
   ▼
Staff Assigned
   │
   ▼
Staff Works on Issue
   │
   ▼
Issue Resolved
   │
   ▼
Management Visibility
```

---

## 8. Issue Submission Flow

When a Faculty member submits an issue:

1. The Faculty member provides the problem.
2. The Faculty member provides a description.
3. The Faculty member provides the room number.
4. The Faculty member selects one of the predefined categories.
5. CampusSync identifies the current Faculty user.
6. The Issue is created.
7. The system records the submission timestamp.
8. Routing determines the responsible Department.
9. Assignment logic determines the Staff member responsible for the Issue.

The exact ordering of database operations and status transitions will be finalized during implementation design.

---

## 9. Department Routing

Routing is deterministic.

The current mapping is:

| Category | Department |
|---|---|
| IT / Equipment | IT Department |
| Facilities / Classroom | Facilities Department |
| Academic / Schedule | Academic Administration |
| Miscellaneous | General Administration |

The Faculty member chooses the category.

The system determines the Department.

The Department is then stored on the Issue through `department_id`.

### Implementation details — to be finalized

The following remain open:

- How the category-to-department mapping is represented internally
- Where the routing logic lives within the application structure
- How invalid or unexpected category values are handled

These decisions will be added once the implementation structure is chosen.

---

## 10. Automatic Staff Assignment

After routing, CampusSync selects a Staff member belonging to the responsible Department.

The intended rule is:

> Select the eligible Staff member with the lowest number of active assigned Issues.

Conceptually:

```text
Issue
  ↓
Responsible Department
  ↓
Staff belonging to Department
  ↓
Count active Issues
  ↓
Compare workloads
  ↓
Select lowest workload
  ↓
Create Assignment
```

An Issue is considered active for workload purposes when its status is not `Resolved`.

### Example

```text
Staff A → 4 active issues
Staff B → 2 active issues
Staff C → 1 active issue

New issue
    ↓
Staff C selected
```

### Implementation details — to be finalized

The following have deliberately not been assumed:

- Exact database query used to calculate workload
- Exact tie-breaking rule
- Behavior when no eligible Staff exists
- Exact transaction/order of assignment creation
- Behavior if an assignment operation fails
- Whether reassignment is needed during the MVP

These will be decided before implementation.

---

## 11. Issue Status Management

The agreed Issue lifecycle is:

```text
Submitted
    ↓
Assigned
    ↓
In Progress
    ↓
Resolved
```

### Status meanings

| Status | Meaning |
|---|---|
| `Submitted` | Issue has been submitted |
| `Assigned` | A Staff member has been assigned |
| `In Progress` | Staff member is actively working on the issue |
| `Resolved` | The issue has been completed |

When an Issue becomes `Resolved`, `resolved_at` records the resolution time.

A separate completion field is not required.

### Implementation details — to be finalized

The following remain open:

- Whether automatic assignment happens immediately after submission
- Exact allowed status transitions
- Which role can perform each transition
- Whether Staff can move directly from `Assigned` to `Resolved`
- Validation of invalid status transitions

---

## 12. Role-Based Access

The MVP has exactly three roles.

### Faculty

Faculty can:

- Submit issues
- View their submitted issues
- Track issue status

Faculty should not:

- Choose the responsible department
- Assign Staff
- Modify another user's issues
- Access institution-wide management information

### Staff

Staff can:

- View issues assigned to them
- View relevant issue details
- Update the status of assigned issues
- Mark assigned issues as resolved

Staff should not:

- Assign issues to themselves or other Staff manually unless this is explicitly added later
- Access management-only views

### Management

Management can:

- View issues across departments
- View issue statuses
- View responsible departments
- View responsible Staff
- Monitor unresolved issues

The exact access-control implementation will be defined during technical design.

---

## 13. Authentication

Authentication is required because CampusSync has role-specific functionality.

The system must be able to determine:

1. Who the current user is.
2. What role they have.
3. Which department they belong to when they are Staff.

### Current architectural requirement

The authenticated user identity should be available to the application when processing protected operations.

### Implementation details — to be finalized

The following have not yet been selected:

- Session implementation
- Password hashing approach
- Login/logout flow details
- Authentication-related libraries
- Initial user creation or seed-data approach

These should be selected based on simplicity and the 48-hour constraint.

---

## 14. Project Structure

The exact Python module and file structure has not yet been finalized.

The intended structure should separate major responsibilities without introducing unnecessary abstraction.

At minimum, the project will need areas for:

```text
Application
├── Flask application
├── Authentication
├── Issue management
├── Routing logic
├── Assignment logic
├── Database/data access
├── Templates
└── Static frontend assets
```

The concrete directory and file structure will be decided before implementation.

---

## 15. Architecture Decisions

| Decision | Current Choice | Reason |
|---|---|---|
| Backend | Python + Flask | Simple server-side web application |
| Database | SQLite | Minimal setup and suitable for MVP |
| Frontend | Jinja2 + HTML/CSS/JavaScript | Avoid unnecessary frontend complexity |
| Application model | Server-rendered web application | Keeps the architecture small |
| Routing | Deterministic category-to-department rules | Predictable and simple |
| Assignment | Lowest active workload | Provides automatic assignment without complex optimization |
| Data objects | User, Department, Issue, Assignment | Keeps MVP data model small |
| Assignment history | Not included initially | Outside MVP scope |
| Workload storage | Calculated from active issues | Avoids redundant workload data |
| Completion tracking | Issue status + `resolved_at` | Avoids a redundant completion flag |

---

## 16. Open Technical Decisions

The architecture is intentionally incomplete in areas where a technical choice has not yet been made.

Before implementation, the following should be resolved:

### Data and database

- Exact database schema and data types
- Foreign-key constraints
- Uniqueness constraints
- Initial/seed data

### Authentication

- Session mechanism
- Password hashing
- Login/logout implementation
- User creation strategy

### Routing

- Internal representation of category-to-department rules
- Location of routing logic in the application

### Assignment

- Active workload query/calculation
- Deterministic tie-breaking rule
- No-eligible-staff behavior
- Assignment creation behavior

### Status workflow

- Exact allowed transitions
- Role permissions for transitions
- Automatic versus manual status changes

### Application structure

- Exact directory/file structure
- Flask route organization
- Data-access approach

These should be decided one at a time rather than all being designed in advance.

---

## 17. Testing Strategy

Testing will focus on the core MVP workflow rather than comprehensive production-level testing.

The most important scenarios are:

1. Faculty can authenticate.
2. Faculty can submit an issue.
3. The selected category produces the correct Department.
4. An eligible Staff member is automatically selected.
5. Staff can view their assigned issue.
6. Staff can update the issue status.
7. Resolving an issue records `resolved_at`.
8. Resolved issues are no longer counted as active workload.
9. Faculty can track their submitted issues.
10. Management can view issues across departments.
11. Users cannot access functionality outside their role.

Testing details can be expanded after the implementation structure is finalized.

---

## 18. Development Approach

Because the project has a 48-hour deadline, implementation should proceed incrementally.

Recommended order:

1. Get the Flask application running.
2. Establish the database and core data model.
3. Implement authentication and roles.
4. Implement Faculty issue submission.
5. Implement category-to-department routing.
6. Implement automatic Staff assignment.
7. Implement Staff issue management.
8. Implement Management visibility.
9. Test the complete workflow.
10. Polish the interface and prepare the demo.

Each milestone should be tested before moving to the next.

---

## 19. Current Status

| Area | Status |
|---|---|
| Product definition | Complete |
| MVP scope | Complete |
| Technology stack | Decided |
| Core data model | Decided |
| High-level architecture | Established |
| Routing implementation | To be finalized |
| Assignment implementation | To be finalized |
| Authentication implementation | To be finalized |
| Exact project structure | To be finalized |
| Implementation | Not started |

This document should be updated as technical decisions are made. Existing decisions should be edited in place rather than creating multiple competing versions of the same architecture.
