# CampusSync — Product Research & Decisions

> **Status:** Final MVP product definition
>
> **Project:** BuildSprint 2026
>
> This document records the problem, product decisions, scope, workflow, and deliberate limitations behind CampusSync. Technical implementation details are documented separately in `architecture.md`.

---

## 1. Problem

Academic institutions regularly handle operational issues such as:

- equipment failures
- classroom/facility problems
- academic scheduling issues
- miscellaneous operational requests

When these issues are reported through informal channels, it can be difficult to determine:

- where the issue belongs;
- which department is responsible;
- who should handle it;
- whether work has started;
- whether the issue has been resolved.

This creates coordination overhead and makes institutional visibility difficult.

---

## 2. Proposed Solution

CampusSync provides a centralized operational issue workflow.

A Faculty member submits an Issue. CampusSync determines the responsible Department from the selected category and automatically assigns the Issue to an eligible Staff member based on active workload.

The Staff member then works through the Issue lifecycle until resolution.

Management receives institution-wide visibility into Issues, their statuses, departments, and assignments.

The core workflow is:

```text
Faculty
   ↓
Submit Issue
   ↓
Category
   ↓
Department Routing
   ↓
Automatic Staff Assignment
   ↓
Staff Workflow
   ↓
Resolved
   ↓
Management Visibility
```

---

## 3. Product Goal

The MVP goal is:

> **Give every operational Issue a clear and traceable path from submission to resolution without requiring manual coordination for routing or initial assignment.**

The MVP is intentionally focused on the core workflow rather than broader institutional features.

---

## 4. Users and Responsibilities

CampusSync has three roles.

### Faculty

Faculty are Issue reporters.

They can:

- log in;
- submit Issues;
- view their own Issues;
- track Issue status;
- view routing and assignment information.

They do not choose the responsible Department or Staff member.

### Staff

Staff are operational handlers.

They can:

- log in;
- view Issues assigned to them;
- view Issue details;
- acknowledge assigned Issues;
- mark In Progress Issues as Resolved.

They cannot manually reassign Issues or change the original Issue details.

### Management

Management is an oversight role.

They can:

- view Issues across departments;
- view Issue details;
- view statuses;
- view responsible Departments;
- view assigned Staff;
- view summary counts;
- filter Issues.

Management does not modify the Issue workflow in the MVP.

---

## 5. Issue Categories

The MVP uses four categories:

| Category | Responsible Department |
|---|---|
| IT / Equipment | IT Department |
| Facilities / Classroom | Facilities Department |
| Academic / Schedule | Academic Administration |
| Miscellaneous | General Administration |

The category is selected by Faculty.

The responsible Department is determined automatically.

Faculty cannot override the routing result.

---

## 6. Department Routing Decision

### Decision

CampusSync uses **deterministic category-to-department routing**.

Each supported category has exactly one responsible Department.

### Reason

A deterministic mapping:

- is easy to understand;
- is predictable;
- is easy to test;
- avoids manual routing;
- avoids unnecessary AI or optimization complexity;
- is sufficient for the MVP.

The MVP deliberately does not attempt to infer departments from free-form text.

---

## 7. Automatic Staff Assignment

Once the responsible Department is known, CampusSync automatically selects a Staff member from that Department.

### Eligibility

Only Staff belonging to the responsible Department are eligible.

A Staff member from another Department cannot receive the Issue.

### Active workload

A Staff member's active workload is the number of assigned Issues with status:

- `Assigned`
- `In Progress`

Resolved Issues do not contribute to active workload.

### Selection rule

The eligible Staff member with the **lowest active workload** is selected.

### Tie-breaking

If multiple eligible Staff members have the same lowest workload, the Staff member whose name comes first alphabetically is selected.

This makes assignment deterministic.

### No eligible Staff

If no eligible Staff member exists:

- the Issue remains `Submitted`;
- no Assignment is created;
- Management can still see the Issue.

### Why automatic assignment?

The MVP aims to remove the manual question:

> "Who should handle this?"

from the initial coordination workflow.

At the same time, the algorithm remains simple enough to explain and test.

---

## 8. Assignment Model

The MVP represents the current assignment explicitly.

An Issue can have one current Assignment.

The Assignment records:

- the Issue;
- the assigned Staff member;
- the assignment timestamp.

Assignment history is not maintained.

Manual reassignment is not supported.

This is intentional because assignment history and reassignment are not required to demonstrate the core MVP workflow.

---

## 9. Issue Lifecycle

The Issue lifecycle is strictly forward-only:

```text
Submitted
    ↓
Assigned
    ↓
In Progress
    ↓
Resolved
```

### `Submitted`

The Faculty member has submitted the Issue.

If automatic assignment succeeds, the Issue moves to `Assigned`.

If no eligible Staff member exists, it remains `Submitted`.

### `Assigned`

A Staff member has been selected.

### `In Progress`

The assigned Staff member has acknowledged the Issue and begun work.

### `Resolved`

The Staff member has completed the Issue.

The resolution time is recorded.

Resolved Issues cannot be reopened.

---

## 10. Status Transition Rules

| Current Status | Trigger | Next Status |
|---|---|---|
| `Submitted` | Successful automatic assignment | `Assigned` |
| `Assigned` | Staff acknowledges | `In Progress` |
| `In Progress` | Staff resolves | `Resolved` |

There are no backward transitions in the MVP.

The Staff member performing the action must also be the Staff member assigned to the Issue.

---

## 11. Issue Data

An Issue contains:

### Faculty-provided information

- Problem
- Description
- Room number
- Category

### System-managed information

- Issue ID
- Submitting Faculty
- Responsible Department
- Status
- Submission timestamp
- Resolution timestamp
- Current Assignment

Faculty does not provide the Department or Staff member.

---

## 12. Authentication and Permissions

Users are pre-created for the MVP.

There is no public registration.

The system uses:

- email/password login;
- Flask sessions;
- Werkzeug password hashing;
- role-based access control.

Passwords must not be stored in plaintext.

The user's role determines the application areas they can access.

### Faculty restrictions

Faculty cannot:

- access Staff functionality;
- access Management functionality;
- select Staff assignment;
- modify the Department;
- resolve Issues;
- view another Faculty member's Issues.

### Staff restrictions

Staff cannot:

- access Management functionality;
- view another Staff member's assigned Issues;
- manually choose assignments;
- reassign Issues;
- modify original Issue details.

### Management restrictions

Management can monitor the system but does not perform operational status changes.

---

## 13. Faculty Experience

The Faculty workflow is:

```text
Login
  ↓
Faculty Dashboard
  ↓
Submit Issue
  ↓
Track Own Issues
  ↓
View Issue Details
```

The submission form contains:

- Problem
- Description
- Room number
- Category

After submission, the Department and Staff assignment are handled automatically.

Faculty can see the resulting routing and assignment information.

---

## 14. Staff Experience

The Staff workflow is:

```text
Login
  ↓
Staff Dashboard
  ↓
Assigned Issues
  ↓
Issue Details
  ↓
Acknowledge
  ↓
In Progress
  ↓
Resolve
  ↓
Resolved
```

Available actions depend on the Issue status:

| Status | Staff action |
|---|---|
| `Assigned` | Acknowledge |
| `In Progress` | Mark as Resolved |
| `Resolved` | No workflow action |

Staff do not edit the original Issue.

---

## 15. Management Experience

Management provides institution-wide oversight.

The dashboard includes:

### Summary counts

- Total Issues
- Submitted
- Assigned
- In Progress
- Resolved

### Issue visibility

Management can see Issues across all Departments.

### Filters

The MVP supports filtering by:

- Status
- Department
- Category

Advanced analytics, charts, trends, and workforce metrics are outside the MVP.

---

## 16. Issue Ordering

Operational visibility is prioritized by keeping unresolved work above completed work.

Faculty and Staff dashboards use:

1. active/non-Resolved Issues first;
2. newest Issues first within that group;
3. Resolved Issues last, also newest first within the resolved group.

This means a recently submitted active Issue does not get buried beneath older resolved Issues.

Management's Issue list is ordered by newest creation time.

---

## 17. Interface Direction

CampusSync is a responsive web application.

The intended interface characteristics are:

- clean;
- modern;
- professional;
- easy to scan;
- consistent across roles;
- responsive on smaller screens;
- clear about Issue status and available actions.

The implemented frontend uses:

- Jinja2 templates;
- HTML;
- CSS;
- JavaScript;
- a shared base layout;
- light/dark theme support;
- responsive layouts.

A separate mobile application is not part of the MVP.

---

## 18. Product Scope

The MVP includes:

- three user roles;
- pre-created authentication accounts;
- Faculty Issue submission;
- four Issue categories;
- deterministic Department routing;
- automatic Staff assignment;
- workload-aware assignment;
- deterministic tie-breaking;
- Staff acknowledgement;
- Staff resolution;
- resolution timestamps;
- Faculty Issue tracking;
- Staff work queue;
- Management dashboard;
- Management filters;
- role-based access restrictions;
- Issue ordering;
- automated testing;
- responsive web interface;
- light/dark theme support.

---

## 19. Deliberate MVP Limitations

The following are intentionally excluded.

### Manual Staff selection

Faculty cannot select a Staff member.

### Manual reassignment

Staff or Management cannot manually reassign an Issue.

### Assignment history

Only the current Assignment is represented.

### Issue editing

Faculty cannot edit an Issue after submission.

Staff cannot modify the original Issue details.

### Issue deletion

Issues cannot be deleted through the MVP workflow.

### Issue reopening

Resolved Issues cannot be reopened.

If the same problem occurs again, a new Issue is submitted.

### Notifications

There is no email, push, or in-application notification infrastructure.

### Escalation

There is no escalation or automatic reassignment workflow for unacknowledged Issues.

### Staff communication

There is no comments, chat, or notes system.

### Advanced analytics

The Management dashboard provides counts and filters but does not provide advanced analytics, trends, or staff-performance metrics.

### AI routing

Routing is deterministic rather than AI-based.

### Mobile application

The MVP is a responsive web application and does not include a separate native mobile application.

### Institutional integrations

There is no ERP, campus-management, timetable, or other institutional-system integration.

---

## 20. Technology Decision

The MVP uses:

```text
Python
   +
Flask
   +
Flask-SQLAlchemy
   +
SQLite
   +
Jinja2
   +
HTML / CSS / JavaScript
```

### Why this stack?

The project was developed within a 48-hour hackathon constraint.

The chosen stack minimizes:

- infrastructure;
- dependency count;
- frontend complexity;
- deployment complexity;
- development overhead.

This allows the project to focus on the actual coordination workflow.

---

## 21. Development Philosophy

The project follows these principles:

### Build the core first

The end-to-end Issue workflow is more important than optional features.

### Prefer deterministic behavior

Routing and assignment should produce predictable results.

### Keep infrastructure small

The MVP does not require microservices, a separate frontend, or multiple databases.

### Avoid feature creep

Features outside the agreed MVP scope are deferred rather than added late in development.

### Test the important behavior

Authentication, authorization, routing, assignment, workflow transitions, ordering, and Management visibility are covered by automated tests.

### Polish after functionality

Visual polish is secondary to a reliable core workflow.

---

## 22. Research Conclusions

The research and design process led to the following core conclusion:

> CampusSync does not need a complex optimization system to demonstrate useful operational coordination.

A small deterministic workflow can provide:

1. clear ownership;
2. automatic routing;
3. balanced initial assignment;
4. visible progress;
5. institutional oversight.

The MVP therefore intentionally favors transparency and predictability over sophisticated optimization.

---

## 23. Final Product Status

**Product definition: Complete.**

The MVP behavior, user roles, workflow, routing rules, assignment rules, access boundaries, scope, and limitations are defined.

The technical implementation is documented in `docs/architecture.md`.

The project is intended to remain within this scope for the BuildSprint 2026 submission unless a verified defect requires a change.
