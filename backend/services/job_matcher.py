# =========================================================
# AI JOB MATCHER
# =========================================================

from urllib.parse import quote


# =========================================================
# CURATED JOB PROFILES
# =========================================================
#
# These are demo/curated job profiles.
# They are NOT live job openings.
#
# Each job contains:
# - core_skills     -> most important skills
# - skills         -> complete required skill list
#
# Core skills receive higher weight during matching.
# =========================================================

JOBS = [
    {
        "title": "Junior Data Analyst",
        "company": "TechData Solutions",
        "location": "Remote",

        "core_skills": [
            "python",
            "sql",
            "pandas",
        ],

        "skills": [
            "python",
            "sql",
            "pandas",
            "numpy",
            "statistics",
            "data visualization",
            "git",
        ],
    },

    {
        "title": "Junior Data Scientist",
        "company": "AI Analytics Labs",
        "location": "Bangalore",

        "core_skills": [
            "python",
            "pandas",
            "numpy",
            "machine learning",
            "scikit-learn",
        ],

        "skills": [
            "python",
            "sql",
            "pandas",
            "numpy",
            "machine learning",
            "scikit-learn",
            "statistics",
            "data visualization",
            "git",
        ],
    },

    {
        "title": "Machine Learning Intern",
        "company": "Future AI",
        "location": "Pune",

        "core_skills": [
            "python",
            "numpy",
            "pandas",
            "machine learning",
            "scikit-learn",
        ],

        "skills": [
            "python",
            "numpy",
            "pandas",
            "machine learning",
            "scikit-learn",
            "deep learning",
            "git",
        ],
    },

    {
        "title": "Python Developer Intern",
        "company": "CodeWorks",
        "location": "Mumbai",

        "core_skills": [
            "python",
            "fastapi",
            "sql",
        ],

        "skills": [
            "python",
            "sql",
            "fastapi",
            "mysql",
            "git",
            "github",
            "docker",
        ],
    },

    {
        "title": "Full Stack Developer Intern",
        "company": "WebNova",
        "location": "Remote",

        "core_skills": [
            "javascript",
            "react",
            "node.js",
            "html",
            "css",
        ],

        "skills": [
            "html",
            "css",
            "javascript",
            "react",
            "node.js",
            "sql",
            "mongodb",
            "git",
            "github",
        ],
    },
]


# =========================================================
# NORMALIZE SKILLS
# =========================================================

def normalize_skills(found_skills):
    """
    Convert detected skills into a clean set.

    Supports:
    - strings
    - dictionaries containing a 'skill' field
    """

    skills = set()

    if not found_skills:
        return skills

    for item in found_skills:

        # -------------------------------------------------
        # Skill dictionary
        # -------------------------------------------------

        if isinstance(item, dict):

            skill = item.get("skill")

            if skill:

                skills.add(
                    str(skill)
                    .lower()
                    .strip()
                )

        # -------------------------------------------------
        # Skill string
        # -------------------------------------------------

        elif isinstance(item, str):

            skill = item.lower().strip()

            if skill:
                skills.add(skill)

    return skills


# =========================================================
# NORMALIZE JOB SKILLS
# =========================================================

def normalize_job_skills(skills):
    """
    Normalize a job's skill list.
    """

    return {
        str(skill).lower().strip()
        for skill in skills
        if skill
    }


# =========================================================
# JOB SEARCH URL
# =========================================================

def create_job_search_url(job_title):
    """
    Create a generic LinkedIn job-search URL.

    The companies in JOBS are curated/demo profiles,
    so we do not generate fake company application URLs.
    """

    query = quote(job_title)

    return (
        "https://www.linkedin.com/jobs/search/"
        f"?keywords={query}"
    )


# =========================================================
# CORE SKILL MATCH
# =========================================================

def calculate_core_skill_score(
    resume_skills,
    required_skills,
    core_skills,
):
    """
    Calculate how many important/core job skills
    are present in the resume.

    Core skills have more importance than secondary skills.
    """

    if not core_skills:
        return 0

    normalized_core = normalize_job_skills(
        core_skills
    )

    matched_core = resume_skills.intersection(
        normalized_core
    )

    total_core = len(normalized_core)

    if total_core == 0:
        return 0

    score = (
        len(matched_core)
        / total_core
    ) * 100

    return round(score, 2)


# =========================================================
# WEIGHTED SKILL SCORE
# =========================================================

def calculate_weighted_score(
    resume_skills,
    required_skills,
    core_skills,
):
    """
    Calculate weighted skill compatibility.

    Core skills:
        Weight = 2

    Other skills:
        Weight = 1

    This means important skills contribute more
    to the final score.
    """

    normalized_required = normalize_job_skills(
        required_skills
    )

    normalized_core = normalize_job_skills(
        core_skills
    )

    if not normalized_required:
        return 0

    total_weight = 0
    matched_weight = 0

    for skill in normalized_required:

        # ---------------------------------------------
        # Core skill
        # ---------------------------------------------

        if skill in normalized_core:
            weight = 2

        # ---------------------------------------------
        # Secondary skill
        # ---------------------------------------------

        else:
            weight = 1

        total_weight += weight

        if skill in resume_skills:
            matched_weight += weight

    if total_weight == 0:
        return 0

    score = (
        matched_weight
        / total_weight
    ) * 100

    return round(score, 2)


# =========================================================
# OVERALL MATCH SCORE
# =========================================================

def calculate_overall_match(
    skill_match_score,
    core_skill_score,
):
    """
    Calculate the final job compatibility score.

    Formula:

        70% = weighted skill match
        30% = core skill match

    This gives more importance to the actual required
    skills while still prioritizing critical skills.
    """

    overall_score = (
        (skill_match_score * 0.70)
        +
        (core_skill_score * 0.30)
    )

    return round(
        overall_score,
        2,
    )


# =========================================================
# MATCH JOBS
# =========================================================

def match_jobs(found_skills, limit=5):
    """
    Match resume skills against curated job profiles.

    Returns:

    - job title
    - company
    - location
    - overall match score
    - skill match score
    - core skill score
    - matched skills
    - matched core skills
    - missing skills
    - job search URL
    """

    # -----------------------------------------------------
    # Normalize resume skills
    # -----------------------------------------------------

    resume_skills = normalize_skills(
        found_skills
    )

    matches = []

    # -----------------------------------------------------
    # Check every job
    # -----------------------------------------------------

    for job in JOBS:

        # -----------------------------------------------
        # Normalize required skills
        # -----------------------------------------------

        required_skills = normalize_job_skills(
            job.get("skills", [])
        )

        core_skills = normalize_job_skills(
            job.get("core_skills", [])
        )

        # -----------------------------------------------
        # Matched skills
        # -----------------------------------------------

        matched_skills = sorted(
            resume_skills.intersection(
                required_skills
            )
        )

        # -----------------------------------------------
        # Missing skills
        # -----------------------------------------------

        missing_skills = sorted(
            required_skills - resume_skills
        )

        # -----------------------------------------------
        # Matched core skills
        # -----------------------------------------------

        matched_core_skills = sorted(
            resume_skills.intersection(
                core_skills
            )
        )

        # -----------------------------------------------
        # Basic skill match
        # -----------------------------------------------

        total_required = len(
            required_skills
        )

        skill_match_score = (
            round(
                (
                    len(matched_skills)
                    / total_required
                ) * 100,
                2,
            )
            if total_required
            else 0
        )

        # -----------------------------------------------
        # Core skill score
        # -----------------------------------------------

        core_skill_score = calculate_core_skill_score(
            resume_skills,
            required_skills,
            core_skills,
        )

        # -----------------------------------------------
        # Weighted skill score
        # -----------------------------------------------

        weighted_skill_score = calculate_weighted_score(
            resume_skills,
            required_skills,
            core_skills,
        )

        # -----------------------------------------------
        # Overall match
        # -----------------------------------------------

        overall_match = calculate_overall_match(
            weighted_skill_score,
            core_skill_score,
        )

        # -----------------------------------------------
        # Create result
        # -----------------------------------------------

        matches.append(
            {
                "title": job["title"],

                "company": job["company"],

                "location": job["location"],

                # Existing frontend field
                "match_score": overall_match,

                # New detailed scores
                "overall_match": overall_match,

                "skill_match_score": skill_match_score,

                "core_skill_score": core_skill_score,

                "weighted_skill_score": weighted_skill_score,

                # Skills
                "matched_skills": matched_skills,

                "matched_core_skills": matched_core_skills,

                "missing_skills": missing_skills,

                # Job search
                "job_search_url": create_job_search_url(
                    job["title"]
                ),
            }
        )

    # -----------------------------------------------------
    # Highest match first
    # -----------------------------------------------------

    matches.sort(
        key=lambda item: item["match_score"],
        reverse=True,
    )

    # -----------------------------------------------------
    # Return top jobs
    # -----------------------------------------------------

    return matches[:limit]