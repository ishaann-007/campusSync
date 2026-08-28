# CampusSync --- Product Research & Decisions

## 1. Problem

Academic institutions can receive operational issues through fragmented
communication channels. This can make it difficult to determine which
department should handle an issue, who is responsible, whether work has
started, and whether it has been resolved.

CampusSync addresses this by turning operational requests into a
structured, trackable workflow.

## 2. Proposed Solution

CampusSync centralizes issue reporting and coordination.

A Faculty member provides:

-   Problem
-   Description
-   Room number
-   Category

CampusSync then determines the responsible Department, automatically
assigns eligible Staff based on active workload, and provides
role-specific tracking and oversight.

## 3. User Roles

### Faculty

Faculty report and track their own issues.

### Staff

Staff work on issues assigned to them and move them through the
operational workflow.

### Management

Management has institution-wide visibility and monitors issues without
modifying their workflow in the MVP.

## 4. Categories and Routing

  Category                 Department
  ------------------------ -------------------------
  IT / Equipment           IT Department
  Facilities / Classroom   Facilities Department
  Academic / Schedule      Academic Administration
  Miscellaneous            General Administration

Faculty select a category rather than a Department. The
category-to-department mapping is predefined and deterministic.

## 5. Automatic Assignment Decision

Only Staff belonging to the routed Department are eligible.

Active workload is the number of Issues in `Assigned` or `In Progress`.

The eligible Staff member with the lowest active workload is selected.

If workloads tie, alphabetical Staff name provides deterministic
selection.

If no eligible Staff exists, the Issue remains `Submitted` and
unassigned.

### Reasoning

This provides automatic coordination without introducing complex
workforce optimization or manual coordination into the MVP.

## 6. Issue Lifecycle Decision

``` text
Submitted
    ↓
Assigned
    ↓
In Progress
    ↓
Resolved
```

The lifecycle is forward-only.

-   `Submitted → Assigned`: successful automatic assignment.
-   `Assigned → In Progress`: Staff acknowledgement.
-   `In Progress → Resolved`: Staff resolution.

The system records `resolved_at` when an issue is resolved.

Resolved issues cannot be reopened. A recurrence is treated as a new
issue.

## 7. Editing and Deletion Decisions

Faculty cannot edit submitted issue details.

Staff cannot modify the original problem, description, room number, or
category.

Issues cannot be deleted in the MVP.

These decisions preserve the submitted issue as a stable record.

## 8. Authentication and Permissions

Users are pre-created for the MVP. There is no public registration.

The system uses role-based authorization for Faculty, Staff, and
Management.

Passwords are not stored as plain text.

## 9. Interface Direction

CampusSync is a responsive web application.

The MVP uses role-specific dashboards, issue detail views, and a shared
interface structure. Light and dark themes are supported.

A separate mobile application is outside the MVP.

## 10. MVP Scope

The MVP provides:

-   three user roles,
-   four issue categories,
-   issue submission,
-   issue details,
-   deterministic department routing,
-   automatic Staff assignment,
-   workload-based assignment,
-   deterministic tie-breaking,
-   issue status tracking,
-   Staff issue management,
-   Management visibility,
-   Management filtering,
-   responsive web UI,
-   authentication and role-based access,
-   automated unit and integration testing.

The priority is a reliable end-to-end workflow rather than a large
number of features.

## 11. Deliberate MVP Limitations

The following are intentionally excluded:

-   Manual Staff selection
-   Manual reassignment
-   Assignment history
-   Staff comments or chat
-   Escalation/reassignment for urgent unacknowledged issues
-   Issue reopening
-   Issue editing after submission
-   Issue deletion
-   Notifications
-   Advanced analytics
-   AI-based routing
-   Complex workforce optimization
-   Separate mobile application
-   ERP/institutional-system integration

These are scope boundaries, not defects in the current MVP.

## 12. Why Features Were Deferred

The project is constrained by a 48-hour hackathon.

Manual reassignment, assignment history, comments, notifications,
escalation, and similar features introduce additional state, data
relationships, interface behavior, and testing requirements.

The MVP therefore focuses on the central coordination workflow while
keeping the architecture small and understandable.

## 13. Development Philosophy

CampusSync prioritizes:

-   small implementation steps,
-   simple solutions,
-   understandability,
-   reliable functionality,
-   frequent testing,
-   minimal infrastructure,
-   avoiding unnecessary dependencies,
-   avoiding premature abstraction,
-   preserving inexpensive future flexibility,
-   and avoiding feature creep.

## 14. Product Flow

``` text
Faculty
  │
  │ Submit Issue
  ▼
Issue Created
  │
  │ Category
  ▼
Department Routing
  │
  │ Eligible Staff
  ▼
Workload-Based Assignment
  │
  ▼
Assigned
  │
  │ Staff Acknowledges
  ▼
In Progress
  │
  │ Staff Resolves
  ▼
Resolved
  │
  ├── Faculty tracks result
  └── Management monitors institution-wide
```

## 15. Product Status

The core MVP has been implemented and verified through the development
milestones.

The current phase is final preparation: documentation verification,
final testing/manual verification, and demonstration preparation.
