"""
StudySync -- Find a Study Spot (Ticket 3, Tinker 3B).

RANKING LOGIC IMPLEMENTED:
  - load_study_spots()   -- reads CSV, converts numeric fields
  - score_study_spot()   -- weighted scoring with explanations
  - rank_study_spots()   -- top-k sorted descending
  - format_results()     -- human-readable output
"""

import csv

NOISE_ORDER = {"quiet": 0, "moderate": 1, "loud": 2}


# ---------------------------------------------------------------------
# Part 1: Load Real Data
# ---------------------------------------------------------------------

def load_study_spots(csv_path: str) -> list:
    """
    Load study spots from a CSV into a list of dicts.

    Converts "distance_miles" to float and "seats_available" to int.
    Keeps noise_level and wifi_quality as strings because they are
    ordered categories, not numbers.
    """
    spots: list = []
    try:
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                spots.append(
                    {
                        "id": int(row["id"]),
                        "name": row["name"],
                        "noise_level": row["noise_level"],       # categorical
                        "distance_miles": float(row["distance_miles"]),
                        "wifi_quality": row["wifi_quality"],     # categorical
                        "seats_available": int(row["seats_available"]),
                    }
                )
    except FileNotFoundError:
        raise FileNotFoundError(f"Study spots file not found: {csv_path}")
    return spots


# ---------------------------------------------------------------------
# Part 2: Score Against a Profile
# ---------------------------------------------------------------------

def score_study_spot(profile: dict, spot: dict) -> tuple:
    """
    Score one study spot against a student profile.

    Weighted scoring:
      - Noise level   -> 2.0 points if <= profile["max_noise"]
      - Distance      -> 1.5 points if <= profile["max_distance"]
      - Seats         -> 1.0 point  if >= profile["min_seats"]

    Noise gets the highest weight because studying requires quiet more
    than it requires proximity. Distance is second because a spot you
    won't walk to is useless. Seats is a soft constraint.

    Returns:
        (score: float, reasons: list[str])
        Every factor contributes a reason, whether it helped or hurt.
    """
    score = 0.0
    reasons: list[str] = []

    # Factor 1: Noise (weight 2.0)
    if NOISE_ORDER[spot["noise_level"]] <= NOISE_ORDER[profile["max_noise"]]:
        score += 2.0
        reasons.append(f"quiet enough ({spot['noise_level']})")
    else:
        reasons.append(f"too noisy ({spot['noise_level']})")

    # Factor 2: Distance (weight 1.5)
    if spot["distance_miles"] <= profile["max_distance"]:
        score += 1.5
        reasons.append(f"close enough ({spot['distance_miles']} mi)")
    else:
        reasons.append(f"too far ({spot['distance_miles']} mi)")

    # Factor 3: Seats (weight 1.0)
    if spot["seats_available"] >= profile["min_seats"]:
        score += 1.0
        reasons.append(f"has seats ({spot['seats_available']})")
    else:
        reasons.append(f"only {spot['seats_available']} seats")

    return score, reasons


# ---------------------------------------------------------------------
# Part 3: Rank and Explain
# ---------------------------------------------------------------------

def rank_study_spots(profile: dict, spots: list, k: int = 3) -> list:
    """
    Score every study spot, then return the top k as
    (spot, score, reasons) tuples, sorted by score descending.

    Uses Python's built-in sorted() with a lambda key, then slices
    the result to keep only the top k entries.
    """
    scored = [
        (spot, *score_study_spot(profile, spot)) for spot in spots
    ]
    ranked = sorted(scored, key=lambda item: item[1], reverse=True)
    return ranked[:k]


def format_results(ranked: list) -> None:
    """
    Print each ranked study spot with its score and reasons, one line each.

    Output format:
        "1. Innovation Commons -- Score: 4.5 -- Because: quiet enough, close enough, has seats"
    """
    for i, (spot, score, reasons) in enumerate(ranked, start=1):
        print(
            f"{i}. {spot['name']} -- Score: {score:.1f} "
            f"-- Because: {', '.join(reasons)}"
        )


# ---------------------------------------------------------------------
# Streamlit UI (already implemented by the starter)
# ---------------------------------------------------------------------

def render_study_spot_tab():
    import streamlit as st

    st.subheader("Find a Study Spot")
    max_noise = st.selectbox(
        "Max noise level", ["quiet", "moderate", "loud"], index=1
    )
    max_distance = st.slider("Max distance (miles)", 0.0, 3.0, 1.0)
    min_seats = st.number_input(
        "Minimum seats needed", min_value=1, value=4, step=1
    )

    if st.button("Find spots"):
        profile = {
            "max_noise": max_noise,
            "max_distance": max_distance,
            "min_seats": min_seats,
        }
        try:
            spots = load_study_spots("data/study_spots.csv")
            ranked = rank_study_spots(profile, spots, k=3)
            for spot, score, reasons in ranked:
                st.write(
                    f"**{spot['name']}** -- Score: {score:.1f} "
                    f"-- Because: {', '.join(reasons)}"
                )
        except NotImplementedError:
            st.warning(
                "🚧 Ranking isn't implemented yet -- that's Tinker 3B's ticket."
            )


# ---------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------

if __name__ == "__main__":
    spots = load_study_spots("data/study_spots.csv")
    profile = {"max_noise": "moderate", "max_distance": 1.0, "min_seats": 4}
    ranked = rank_study_spots(profile, spots, k=3)
    format_results(ranked)