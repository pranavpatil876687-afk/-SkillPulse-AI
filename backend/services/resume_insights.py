# =========================================================
# SKILLPULSE AI
# AI RESUME IMPROVEMENT INSIGHTS
# =========================================================


def generate_resume_insights(
    skill_analysis,
    career_compatibility,
    job_matches,
    resume_score,
):
    """
    Generate actionable insights from resume analysis.
    """

    insights = []

    # =====================================================
    # GET DATA
    # =====================================================

    skill_score = float(
        skill_analysis.get(
            "skill_score",
            0,
        )
    )

    missing_skills = skill_analysis.get(
        "missing_skills",
        [],
    )

    score = float(
        resume_score.get(
            "score",
            0,
        )
    )

    # =====================================================
    # SCORE INSIGHT
    # =====================================================

    if score < 40:

        insights.append({
            "type": "warning",
            "title": "Resume needs improvement",
            "message": (
                "Your resume currently has limited "
                "alignment with the selected career."
            ),
        })

    elif score < 70:

        insights.append({
            "type": "info",
            "title": "Good potential",
            "message": (
                "Your resume has a reasonable foundation, "
                "but additional skills can improve "
                "career compatibility."
            ),
        })

    else:

        insights.append({
            "type": "success",
            "title": "Strong resume alignment",
            "message": (
                "Your resume demonstrates strong "
                "alignment with the selected career."
            ),
        })

    # =====================================================
    # SKILL COVERAGE
    # =====================================================

    if skill_score < 50:

        insights.append({
            "type": "warning",
            "title": "Increase required skill coverage",
            "message": (
                f"Your resume currently covers "
                f"{skill_score}% of the required skills."
            ),
        })

    # =====================================================
    # MISSING SKILLS
    # =====================================================

    if missing_skills:

        priority_skills = missing_skills[:5]

        insights.append({
            "type": "action",
            "title": "Priority skills to learn",
            "skills": priority_skills,
            "message": (
                "Adding these skills can improve "
                "your career and job compatibility."
            ),
        })

    # =====================================================
    # CAREER COMPATIBILITY
    # =====================================================

    selected_career_score = 0

    if career_compatibility:

        selected = career_compatibility[0]

        selected_career_score = float(
            selected.get(
                "score",
                0,
            )
        )

    if selected_career_score < 50:

        insights.append({
            "type": "info",
            "title": "Improve career compatibility",
            "message": (
                "Focus on the missing skills required "
                "for your selected career path."
            ),
        })

    # =====================================================
    # JOB MATCHING
    # =====================================================

    if job_matches:

        best_job = job_matches[0]

        best_score = float(
            best_job.get(
                "match_score",
                0,
            )
        )

        if best_score < 50:

            insights.append({
                "type": "warning",
                "title": "Low job compatibility",
                "message": (
                    f"Your best current job match is "
                    f"{best_score}%. "
                    "Adding relevant skills and projects "
                    "can improve your matches."
                ),
            })

        else:

            insights.append({
                "type": "success",
                "title": "Good job compatibility",
                "message": (
                    f"Your best current job match is "
                    f"{best_score}%."
                ),
            })

    # =====================================================
    # RETURN
    # =====================================================

    return {
        "total_insights": len(insights),
        "insights": insights,
    }