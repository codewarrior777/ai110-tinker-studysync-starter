"""
StudySync -- Session Log (Ticket 2, Tinker 2B).

TICKET: the click counter below doesn't survive a Streamlit rerun. The
session list accepts empty subjects and bad durations. PlainSession is
still a hand-written class. Recurring sessions and time conflicts aren't
detected yet.
"""

from datetime import date, timedelta
from dataclasses import dataclass

FREQUENCY_DAYS = {"daily": 1, "weekly": 7}


class PlainSession:
    def __init__(self, subject, minutes, priority="medium"):
        self.subject = subject
        self.minutes = minutes
        self.priority = priority

    def __repr__(self):
        return f"PlainSession(subject={self.subject!r}, minutes={self.minutes}, priority={self.priority!r})"


@dataclass
class SessionDC:
    """Dataclass equivalent of PlainSession -- __init__, __repr__ and
    __eq__ are generated automatically."""
    subject: str
    minutes: int
    priority: str = "medium"


def next_occurrence(last_date: date, frequency: str) -> date:
    """
    Return the next scheduled date given the last session date and a
    frequency label ("daily" or "weekly"), using FREQUENCY_DAYS and timedelta.
    """
    if frequency not in FREQUENCY_DAYS:
        raise ValueError(f"Unknown frequency: {frequency!r}")
    return last_date + timedelta(days=FREQUENCY_DAYS[frequency])


def find_conflicts(sessions: list) -> list:
    """
    sessions: list of dicts, each with a "slot" key, e.g. {"subject": "Calc II", "slot": "08:00"}.

    Return a list of (session_a, session_b) tuples for every pair that shares
    the same "slot". Must NOT crash on an empty list or a list with no conflicts.
    """
    conflicts = []
    for i in range(len(sessions)):
        for j in range(i + 1, len(sessions)):
            if sessions[i]["slot"] == sessions[j]["slot"]:
                conflicts.append((sessions[i], sessions[j]))
    return conflicts


def render_session_log_tab():
    import streamlit as st

    st.subheader("Parts 1-2: Log a Session")

    # ---------------------------------------------------------------
    # Part 1 -- BROKEN (kept for comparison)
    # Plain variable: Streamlit resets it to 0 on every rerun.
    # ---------------------------------------------------------------
    count = 0
    if st.button("Log a session (broken)"):
        count += 1
    st.metric("Sessions logged (broken)", count)

    # ---------------------------------------------------------------
    # Part 1 -- FIXED (uses st.session_state)
    # Initialize ONCE, then increment inside the handler.
    # ---------------------------------------------------------------
    if "fixed_count" not in st.session_state:
        st.session_state.fixed_count = 0
    if st.button("Log a session (fixed)"):
        st.session_state.fixed_count += 1
    st.metric("Sessions logged (fixed)", st.session_state.fixed_count)

    st.divider()
    st.subheader("Part 2: Session List (with validation)")

    if "mini_sessions" not in st.session_state:
        st.session_state.mini_sessions = []

    subject = st.text_input("Subject")
    duration = st.number_input("Duration (minutes)", value=30, step=1)

    if st.button("Add session"):
        # ---------------------------------------------------------
        # Part 2 -- Validation BEFORE append(...)
        # ---------------------------------------------------------
        if not subject or not subject.strip():
            st.error("Subject cannot be empty.")
        elif duration <= 0:
            st.error("Duration must be greater than 0.")
        else:
            st.session_state.mini_sessions.append(
                {"subject": subject.strip(), "duration": duration}
            )
            st.success(f"Added: {subject.strip()} ({duration} min)")

    st.write(st.session_state.mini_sessions)

    st.divider()
    st.subheader("Part 4: Conflict Check")
    if st.button("Check for time conflicts"):
        sample = [
            {"subject": "Calc II", "slot": "08:00"},
            {"subject": "Chem Lab", "slot": "08:00"},
            {"subject": "History", "slot": "09:00"},
        ]
        conflicts = find_conflicts(sample)
        st.write(conflicts if conflicts else "No conflicts found.")


if __name__ == "__main__":
    # Part 3 -- compare PlainSession vs SessionDC
    plain = PlainSession("Study group: Calc II", 45, priority="high")
    print("PlainSession:", plain)

    dc = SessionDC("Study group: Calc II", 45, priority="high")
    print("SessionDC:   ", dc)

    # Part 4 -- next_occurrence
    print(next_occurrence(date(2026, 1, 1), "daily"))    # 2026-01-02
    print(next_occurrence(date(2026, 1, 1), "weekly"))   # 2026-01-08

    # Part 4 -- find_conflicts
    print(
        find_conflicts(
            [
                {"subject": "Calc II", "slot": "08:00"},
                {"subject": "Chem Lab", "slot": "08:00"},
                {"subject": "History", "slot": "09:00"},
            ]
        )
    )
    print(find_conflicts([]))