# =========================================================
# SKILLPULSE AI
# AI RESUME SCORE ENGINE
# =========================================================


def safe_percentage(value):
    """
    Convert a value into a safe percentage
    between 0 and 100.
    """

    try:
        value = float(value)

    except (TypeError, ValueError):

        return 0.0

    return max(
        0.0,
        min(value, 100.0)
    )


def get_score_label(score):
    """
    Convert the numerical resume score
    into a human-readable rating.
    """

    if score >= 85:

        return "Excellent"

    if score >= 70:

        return "Strong"

    if score >= 55:

        return "Good Potential"

    if score >= 40:

        return "Needs Improvement"

    return "Beginner"


def calculate_resume_score(
    skill_coverage,
    career_compatibility,
    job_match,
):
    """
    Calculate the overall AI Resume Score.

    Score components:

    50% -> Required Skill Coverage
    25% -> Career Compatibility
    25% -> Job Compatibility
    """

    # =====================================================
    # NORMALIZE INPUTS
    # =====================================================

    skill_coverage = safe_percentage(
        skill_coverage
    )

    career_compatibility = safe_percentage(
        career_compatibility
    )

    job_match = safe_percentage(
        job_match
    )


    # =====================================================
    # WEIGHTS
    # =====================================================

    SKILL_WEIGHT = 0.50

    CAREER_WEIGHT = 0.25

    JOB_WEIGHT = 0.25


    # =====================================================
    # CALCULATE SCORE
    # =====================================================

    score = (
        (skill_coverage * SKILL_WEIGHT)
        +
        (career_compatibility * CAREER_WEIGHT)
        +
        (job_match * JOB_WEIGHT)
    )


    # =====================================================
    # KEEP SCORE BETWEEN 0 AND 100
    # =====================================================

    score = round(
        max(
            0.0,
            min(score, 100.0)
        ),
        2,
    )


    # =====================================================
    # SCORE LABEL
    # =====================================================

    label = get_score_label(
        score
    )


    # =====================================================
    # RETURN RESULT
    # =====================================================

    return {

        "score": score,

        "label": label,

        "components": {

            "skill_coverage": round(
                skill_coverage,
                2,
            ),

            "career_compatibility": round(
                career_compatibility,
                2,
            ),

            "job_compatibility": round(
                job_match,
                2,
            ),
        },

        "weights": {

            "skill_coverage": 50,

            "career_compatibility": 25,

            "job_compatibility": 25,
        },
    }