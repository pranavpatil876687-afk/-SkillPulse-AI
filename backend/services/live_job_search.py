# =========================================================
# SKILLPULSE AI
# JOB DISCOVERY ENGINE
# =========================================================

from urllib.parse import quote


# =========================================================
# JOB DATA
# =========================================================
# This is a provider-style job dataset.
# Later we can connect a real job API without changing
# the matching logic.
# =========================================================

JOB_DATABASE = [

    {
        "title": "Junior Data Analyst",
        "company": "TechData Solutions",
        "location": "Remote",

        "skills": [
            "python",
            "sql",
            "pandas",
            "numpy",
            "statistics",
            "data visualization",
            "git",
        ],

        "core_skills": [
            "python",
            "sql",
            "pandas",
        ],
    },


    {
        "title": "Junior Data Scientist",
        "company": "AI Analytics Labs",
        "location": "Bangalore",

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

        "core_skills": [
            "python",
            "pandas",
            "numpy",
            "machine learning",
            "scikit-learn",
        ],
    },


    {
        "title": "Machine Learning Intern",
        "company": "Future AI",
        "location": "Pune",

        "skills": [
            "python",
            "numpy",
            "pandas",
            "machine learning",
            "scikit-learn",
            "deep learning",
            "git",
        ],

        "core_skills": [
            "python",
            "numpy",
            "pandas",
            "machine learning",
            "scikit-learn",
        ],
    },


    {
        "title": "Python Developer Intern",
        "company": "CodeWorks",
        "location": "Mumbai",

        "skills": [
            "python",
            "sql",
            "fastapi",
            "mysql",
            "git",
            "github",
            "docker",
        ],

        "core_skills": [
            "python",
            "fastapi",
            "sql",
        ],
    },


    {
        "title": "Full Stack Developer Intern",
        "company": "WebNova",
        "location": "Remote",

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

        "core_skills": [
            "javascript",
            "react",
            "node.js",
            "html",
            "css",
        ],
    },


    {
        "title": "Data Science Intern",
        "company": "DataMind AI",
        "location": "Hyderabad",

        "skills": [
            "python",
            "pandas",
            "numpy",
            "sql",
            "statistics",
            "machine learning",
            "scikit-learn",
            "git",
        ],

        "core_skills": [
            "python",
            "pandas",
            "numpy",
            "machine learning",
        ],
    },


    {
        "title": "AI/ML Intern",
        "company": "NeuralTech",
        "location": "Bangalore",

        "skills": [
            "python",
            "numpy",
            "pandas",
            "machine learning",
            "deep learning",
            "scikit-learn",
            "tensorflow",
            "git",
        ],

        "core_skills": [
            "python",
            "machine learning",
            "scikit-learn",
            "deep learning",
        ],
    },


    {
        "title": "SQL Data Analyst Intern",
        "company": "InsightWorks",
        "location": "Remote",

        "skills": [
            "sql",
            "python",
            "pandas",
            "statistics",
            "data visualization",
            "power bi",
            "excel",
            "git",
        ],

        "core_skills": [
            "sql",
            "pandas",
            "data visualization",
        ],
    },

]


# =========================================================
# NORMALIZE SKILLS
# =========================================================

def normalize_skills(skills):

    normalized = set()

    if not skills:
        return normalized

    for item in skills:

        if isinstance(item, dict):

            skill = item.get("skill")

        else:

            skill = item

        if skill:

            normalized.add(
                str(skill)
                .lower()
                .strip()
            )

    return normalized


# =========================================================
# NORMALIZE JOB SKILLS
# =========================================================

def normalize_job_skills(skills):

    return {
        str(skill)
        .lower()
        .strip()

        for skill in skills

        if skill
    }


# =========================================================
# CREATE SEARCH URL
# =========================================================

def create_job_search_url(
    job_title,
    location=None,
):

    query = job_title

    if location:

        query += f" {location}"

    encoded_query = quote(query)

    return (
        "https://www.linkedin.com/jobs/search/"
        f"?keywords={encoded_query}"
    )


# =========================================================
# CALCULATE MATCH
# =========================================================

def calculate_match(
    resume_skills,
    job_skills,
    core_skills,
):

    job_skills = normalize_job_skills(
        job_skills
    )

    core_skills = normalize_job_skills(
        core_skills
    )


    if not job_skills:

        return {
            "match_score": 0,
            "skill_match_score": 0,
            "core_skill_score": 0,
        }


    # -----------------------------------------------------
    # NORMAL SKILL MATCH
    # -----------------------------------------------------

    matched_skills = (
        resume_skills
        .intersection(job_skills)
    )


    skill_match_score = (
        len(matched_skills)
        /
        len(job_skills)
    ) * 100


    # -----------------------------------------------------
    # CORE SKILL MATCH
    # -----------------------------------------------------

    if core_skills:

        matched_core = (
            resume_skills
            .intersection(core_skills)
        )

        core_skill_score = (
            len(matched_core)
            /
            len(core_skills)
        ) * 100

    else:

        core_skill_score = 0


    # -----------------------------------------------------
    # FINAL SCORE
    # -----------------------------------------------------
    # Core skills are more important than secondary skills.
    # -----------------------------------------------------

    final_score = (
        skill_match_score * 0.60
        +
        core_skill_score * 0.40
    )


    return {

        "match_score": round(
            final_score,
            2,
        ),

        "skill_match_score": round(
            skill_match_score,
            2,
        ),

        "core_skill_score": round(
            core_skill_score,
            2,
        ),
    }


# =========================================================
# FIND JOBS
# =========================================================

def discover_jobs(
    resume_skills,
    limit=10,
):

    resume_skills = normalize_skills(
        resume_skills
    )


    jobs = []


    # =====================================================
    # PROCESS EVERY JOB
    # =====================================================

    for job in JOB_DATABASE:

        required_skills = (
            normalize_job_skills(
                job.get(
                    "skills",
                    [],
                )
            )
        )

        core_skills = (
            normalize_job_skills(
                job.get(
                    "core_skills",
                    [],
                )
            )
        )


        # -------------------------------------------------
        # MATCH
        # -------------------------------------------------

        score = calculate_match(
            resume_skills,
            required_skills,
            core_skills,
        )


        # -------------------------------------------------
        # MATCHED SKILLS
        # -------------------------------------------------

        matched_skills = sorted(
            resume_skills
            .intersection(
                required_skills
            )
        )


        # -------------------------------------------------
        # MISSING SKILLS
        # -------------------------------------------------

        missing_skills = sorted(
            required_skills
            -
            resume_skills
        )


        # -------------------------------------------------
        # MATCHED CORE SKILLS
        # -------------------------------------------------

        matched_core_skills = sorted(
            resume_skills
            .intersection(
                core_skills
            )
        )


        # -------------------------------------------------
        # CREATE RESULT
        # -------------------------------------------------

        job_result = {

            "title": job["title"],

            "company": job["company"],

            "location": job["location"],

            "match_score": score[
                "match_score"
            ],

            "skill_match_score": score[
                "skill_match_score"
            ],

            "core_skill_score": score[
                "core_skill_score"
            ],

            "matched_skills":
                matched_skills,

            "matched_core_skills":
                matched_core_skills,

            "missing_skills":
                missing_skills,

            "required_skills":
                sorted(
                    required_skills
                ),

            "job_search_url":
                create_job_search_url(
                    job["title"],
                    job["location"],
                ),
        }


        jobs.append(
            job_result
        )


    # =====================================================
    # SORT BY MATCH SCORE
    # =====================================================

    jobs.sort(
        key=lambda job:
            job["match_score"],

        reverse=True,
    )


    # =====================================================
    # RETURN TOP JOBS
    # =====================================================

    return jobs[:limit]