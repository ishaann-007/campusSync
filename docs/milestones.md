# CampusSync --- Development Milestones

> **Project:** CampusSync\
> **Context:** 48-hour BuildSprint hackathon\
> **Purpose:** Track implementation progress without expanding scope
> unnecessarily.

------------------------------------------------------------------------

## How to Use This File

Development should proceed one milestone at a time.

For each milestone:

1.  Give LatentCode only the instructions for that milestone.
2.  Let it make the changes.
3.  Run and test the result locally.
4.  Fix problems before moving on.
5.  Mark the milestone complete only when its acceptance criteria pass.

Do not implement later milestones early unless required to make the
current milestone work.

------------------------------------------------------------------------

# Milestone 1 --- Project Foundation & Repository Structure

**Status:** ✅ Complete

### Goal

Create the basic Flask application, repository structure, SQLite
foundation, and development environment.

### Completed

-   Flask application created
-   Flask-SQLAlchemy configured
-   SQLite database foundation created
-   Application factory created
-   Basic repository structure created
-   `requirements.txt` created
-   `.gitignore` created
-   Basic templates/static directories created
-   Basic foundation test created
-   Virtual environment created and dependencies installed
-   Application successfully starts locally
-   Browser successfully reaches the application

### Verification

``` bash
python -m unittest tests/test_foundation.py
```

Expected result:

``` text
OK
```

Application:

``` bash
python run.py
```

Expected result:

``` text
http://127.0.0.1:5000/
```

------------------------------------------------------------------------

# Milestone 2 --- Authentication & Role Handling

**Status:** ✅ Complete


### Goal

Implement the minimum authentication system required for the three
CampusSync roles.

### Required

-   Pre-created users
-   Login
-   Password verification
-   Session handling
-   Role identification
-   Role-based access control
-   Logout

### Roles

-   Faculty
-   Staff
-   Management

### Acceptance Criteria

-   A valid user can log in.
-   An invalid login is rejected.
-   The application identifies the user's role.
-   Users cannot access pages outside their role.
-   A user can log out.
-   Passwords are not stored as plain text.

### Explicitly Excluded

-   Public registration
-   Password reset
-   Email verification
-   OAuth/social login
-   Advanced account management

------------------------------------------------------------------------

# Milestone 3 --- Faculty Issue Submission

**Status:** ✅ Complete


### Goal

Allow Faculty to create and view their own Issues.

### Required

Faculty can submit:

-   Problem
-   Description
-   Room number
-   Category

The system generates/stores:

-   Issue ID
-   Submitting Faculty
-   Created timestamp
-   Initial status

### Acceptance Criteria

-   Faculty can open the submission form.
-   Required fields are validated.
-   A valid Issue is stored in SQLite.
-   The Issue appears in the submitting Faculty member's issue list.
-   Faculty cannot see another Faculty member's Issues.
-   Original issue details are not editable after submission.

### Explicitly Excluded

-   Automatic routing
-   Automatic Staff assignment
-   Staff workflow
-   Management dashboard

------------------------------------------------------------------------

# Milestone 4 --- Department Routing

**Status:** ✅ Complete

### Goal

Automatically determine the responsible Department from the
Faculty-selected category.

### Routing Rules

  Category                 Department
  ------------------------ -------------------------
  IT / Equipment           IT Department
  Facilities / Classroom   Facilities Department
  Academic / Schedule      Academic Administration
  Miscellaneous            General Administration

### Acceptance Criteria

-   Each valid category maps to exactly one Department.
-   Invalid categories are rejected.
-   Faculty does not select the Department.
-   The Issue stores the responsible Department.

### Explicitly Excluded

-   AI classification
-   Dynamic routing rules
-   Manual Department selection

------------------------------------------------------------------------

# Milestone 5 --- Automatic Staff Assignment

**Status:** ✅ Complete


### Goal

Automatically assign a routed Issue to an eligible Staff member.

### Rules

Only Staff belonging to the responsible Department are eligible.

Active workload includes:

``` text
Assigned + In Progress
```

Resolved Issues do not count.

The eligible Staff member with the lowest active workload receives the
Issue.

Equal workloads are resolved by alphabetical Staff name.

### Acceptance Criteria

-   Only Staff from the correct Department are considered.
-   Active workload is calculated correctly.
-   The lowest-workload eligible Staff member is selected.
-   Equal workloads are handled deterministically.
-   An Assignment is created when eligible Staff exists.
-   The Issue becomes `Assigned` after successful assignment.
-   If no eligible Staff exists:
    -   No Assignment is created.
    -   The Issue remains `Submitted`.

### Explicitly Excluded

-   Manual reassignment
-   Assignment history
-   Complex workforce optimization
-   Proximity/room-distance assignment

------------------------------------------------------------------------

# Milestone 6 --- Staff Issue Workflow

**Status:** ✅ Complete


### Goal

Allow Staff to manage Issues assigned to them.

### Workflow

``` text
Assigned
    ↓
In Progress
    ↓
Resolved
```

### Required Actions

For `Assigned`:

**Acknowledge**

``` text
Assigned → In Progress
```

For `In Progress`:

**Mark as Resolved**

``` text
In Progress → Resolved
```

When resolved, record `resolved_at`.

### Acceptance Criteria

-   Staff sees only Issues assigned to them.
-   Staff can view Issue details.
-   A Staff member can acknowledge an assigned Issue.
-   Acknowledgement changes the Issue to `In Progress`.
-   A Staff member can resolve an `In Progress` Issue.
-   Resolution changes the Issue to `Resolved`.
-   Resolution timestamp is recorded.
-   Invalid status actions are rejected.
-   Resolved Issues cannot be reopened.

### Explicitly Excluded

-   Staff comments/chat
-   Reassignment
-   Reopening
-   Editing original Issue details

------------------------------------------------------------------------

# Milestone 7 --- Management Dashboard

**Status:** ✅ Complete


### Goal

Give Management institution-wide visibility into Issues.

### Required

Summary counts:

-   Total Issues
-   Assigned
-   In Progress
-   Resolved

Issue list showing institution-wide Issues.

Basic filters:

-   Status
-   Department
-   Category

Issue details drawer/sidebar.

### Acceptance Criteria

-   Management can see Issues across departments.
-   Summary counts are correct.
-   Filters produce the correct Issue list.
-   Management can open Issue details.
-   Management cannot modify Issue workflow.

### Explicitly Excluded

-   Advanced analytics
-   Complex charts
-   Management editing
-   Management reassignment
-   Reporting/export systems

------------------------------------------------------------------------

# Milestone 8 --- End-to-End Integration Testing

**Status:** ⬜ Not started

### Goal

Verify the complete CampusSync workflow.

### Primary Test

``` text
Faculty Login
    ↓
Submit Issue
    ↓
Category Selected
    ↓
Department Determined
    ↓
Staff Automatically Assigned
    ↓
Staff Login
    ↓
Acknowledge
    ↓
In Progress
    ↓
Resolve
    ↓
Resolved
    ↓
Management Login
    ↓
Issue Visible
```

### Required Testing

Test:

-   All four categories
-   Multiple Staff workloads
-   Equal Staff workloads
-   No eligible Staff
-   Invalid login
-   Role restrictions
-   Faculty data isolation
-   Staff assignment isolation
-   Invalid status transitions
-   Management filtering
-   Timestamps

### Acceptance Criteria

The primary workflow completes successfully without manual database
manipulation.

------------------------------------------------------------------------

# Milestone 9 --- UI & UX Polish

**Status:** ⬜ Not started

### Goal

Turn the functional MVP into a polished-looking final product.

### Focus

-   Consistent visual design
-   Dashboard layouts
-   Navigation
-   Forms
-   Issue lists
-   Status badges
-   Issue details drawer/sidebar
-   Spacing and typography
-   Responsive behavior
-   Loading states
-   Empty states
-   Error states

### Rule

Do not change core business logic unless testing reveals a real defect.

The goal is polish, not new functionality.

------------------------------------------------------------------------

# Milestone 10 --- Demo Preparation & Final Repository Cleanup

**Status:** ⬜ Not started

### Goal

Prepare CampusSync for the hackathon demonstration.

### Required

-   Reliable demo users
-   Representative demo Issues
-   Representative Staff workloads
-   Complete demo workflow
-   Final end-to-end test
-   README update
-   Repository cleanup
-   Remove unnecessary files/debug output

### Optional if Time Allows

-   Screenshots
-   Additional UI polish
-   Small usability improvements
-   Additional tests

------------------------------------------------------------------------

# Priority Rules

If time becomes limited, use this priority order.

## Priority 1 --- Must Work

``` text
Authentication
    ↓
Faculty Issue Submission
    ↓
Routing
    ↓
Assignment
    ↓
Staff Workflow
    ↓
Management Visibility
```

## Priority 2 --- Should Look Good

-   Dashboard UI
-   Issue drawer
-   Forms
-   Responsive layout
-   Status presentation

## Priority 3 --- Nice to Have

Anything outside the defined MVP.

Do not sacrifice the core workflow to add optional features.

------------------------------------------------------------------------

# Current Progress

``` text
[██████████] Milestone 1 — Foundation          ✅
[██████████] Milestone 2 — Authentication       ✅
[██████████] Milestone 3 — Issue Submission     ✅
[██████████] Milestone 4 — Routing              ✅
[██████████] Milestone 5 — Assignment           ✅
[██████████] Milestone 6 — Staff Workflow       ✅
[██████████] Milestone 7 — Management           ✅
[----------] Milestone 8 — Integration Testing  ⬜
[----------] Milestone 9 — UI Polish            ⬜
[----------] Milestone 10 — Demo Preparation    ⬜
```

------------------------------------------------------------------------

# Development Rule

**One milestone at a time.**

Do not move forward until the current milestone has been implemented and
verified.

If implementation reveals an ambiguity or architectural problem, stop
and resolve it before building further functionality.

The goal is a small, reliable, understandable CampusSync MVP rather than
a larger partially working system.
