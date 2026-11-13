# =========================================================
# SKILLPULSE AI - MAIN BACKEND
# =========================================================

from pathlib import Path
import shutil
import traceback

from fastapi import (
    FastAPI,
    UploadFile,
    File,
    Form,
    HTTPException,
)

from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# =========================================================
# SERVICES
# =========================================================

from services.resume_parser import extract_text

from services.skill_extractor import (
    extract_skills_with_evidence,
)

from services.skill_gap import (
    analyze_skill_gap,
    analyze_all_careers,
)

from services.job_matcher import (
    match_jobs,
)

from services.live_job_search import (
    discover_jobs,
)

from services.resume_score import (
    calculate_resume_score,
)

from services.resume_insights import (
    generate_resume_insights,
)


# =========================================================
# FASTAPI APPLICATION
# =========================================================

app = FastAPI(
    title="SkillPulse AI",
    description="AI-Powered Resume Skill Gap Intelligence",
    version="1.0.0",
)


# =========================================================
# CORS
# =========================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# UPLOAD DIRECTORY
# =========================================================

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


# =========================================================
# JOB SEARCH REQUEST MODEL
# =========================================================

class JobSearchRequest(BaseModel):
    skills: list[str]
    limit: int = 10


# =========================================================
# HOME
# =========================================================

@app.get("/")
def home():
    return {
        "message": "SkillPulse AI Backend is running"
    }


# =========================================================
# HEALTH CHECK
# =========================================================

@app.get("/api/health")
def health():
    return {
        "status": "healthy"
    }


# =========================================================
# ANALYZE RESUME
# =========================================================

@app.post("/api/analyze-resume")
async def analyze_resume(
    file: UploadFile = File(...),
    career: str = Form("data_science"),
):

    try:

        # =================================================
        # STEP 0
        # VALIDATE FILE
        # =================================================

        if not file.filename:
            raise HTTPException(
                status_code=400,
                detail="No file selected.",
            )

        if not file.filename.lower().endswith(".pdf"):
            raise HTTPException(
                status_code=400,
                detail="Only PDF files are supported.",
            )

        # =================================================
        # SAVE FILE
        # =================================================

        file_path = UPLOAD_DIR / file.filename

        with file_path.open("wb") as buffer:
            shutil.copyfileobj(
                file.file,
                buffer,
            )

        # =================================================
        # START LOG
        # =================================================

        print("\n")
        print("=" * 50)
        print("SKILLPULSE AI")
        print("RESUME ANALYSIS STARTED")
        print("=" * 50)

        print(f"File: {file.filename}")
        print(f"Career: {career}")

        # =================================================
        # STEP 1
        # EXTRACT RESUME TEXT
        # =================================================

        print("\n[1/7] Extracting resume text...")

        text = extract_text(
            str(file_path)
        )

        print(f"Text length: {len(text)}")

        if not text.strip():
            raise HTTPException(
                status_code=400,
                detail="Could not extract text from the resume.",
            )

        # =================================================
        # STEP 2
        # DETECT SKILLS
        # =================================================

        print("\n[2/7] Detecting skills...")

        skill_details = extract_skills_with_evidence(
            text
        )

        print(
            f"Skills detected: {len(skill_details)}"
        )

        # =================================================
        # PREPARE SKILL LIST
        # =================================================

        skills = [
            item["skill"]
            for item in skill_details
        ]

        # =================================================
        # SKILL EVIDENCE
        # =================================================

        print("\nPreparing skill evidence...")

        skill_evidence = {}

        for item in skill_details:

            skill_evidence[item["skill"]] = {
                "confidence": float(
                    item["confidence"]
                ),
                "evidence": str(
                    item["evidence"]
                ),
                "level": str(
                    item.get(
                        "level",
                        "Intermediate",
                    )
                ),
                "method": str(
                    item.get(
                        "method",
                        "keyword",
                    )
                ),
            }

        # =================================================
        # STEP 3
        # SKILL GAP ANALYSIS
        # =================================================

        print("\n[3/7] Analyzing skill gap...")

        skill_analysis = analyze_skill_gap(
            skills,
            career,
        )

        # =================================================
        # STEP 4
        # CAREER COMPATIBILITY
        # =================================================

        print(
            "\n[4/7] Analyzing career compatibility..."
        )

        career_compatibility = analyze_all_careers(
            skills
        )

        # =================================================
        # FIND SELECTED CAREER SCORE
        # =================================================

        career_score = 0

        if career_compatibility:

            selected_career = next(
                (
                    item
                    for item in career_compatibility
                    if item.get("career") == career
                ),
                None,
            )

            if selected_career:
                career_score = selected_career.get(
                    "score",
                    0,
                )

        # =================================================
        # STEP 5
        # EXISTING JOB MATCHING
        # =================================================

        print(
            "\n[5/7] Matching curated jobs..."
        )

        job_matches = match_jobs(
            skills
        )

        print(
            f"Jobs matched: {len(job_matches)}"
        )

        # =================================================
        # FIND BEST JOB MATCH
        # =================================================

        job_score = 0

        if job_matches:

            job_score = max(
                job.get(
                    "match_score",
                    0,
                )
                for job in job_matches
            )

        print(
            f"Best job match: {job_score}%"
        )

        # =================================================
        # STEP 6
        # RESUME SCORE
        # =================================================

        print(
            "\n[6/7] Calculating resume score..."
        )

        # -------------------------------------------------
        # REQUIRED SKILL COVERAGE
        # -------------------------------------------------

        skill_coverage = skill_analysis.get(
            "skill_score",
            0,
        )

        # -------------------------------------------------
        # CALCULATE FINAL SCORE
        # -------------------------------------------------

        resume_score = calculate_resume_score(
            skill_coverage=skill_coverage,
            career_compatibility=career_score,
            job_match=job_score,
        )

        print(
            f"Resume Score: "
            f"{resume_score.get('score', 0)}%"
        )

        print(
            f"Resume Rating: "
            f"{resume_score.get('label', 'N/A')}"
        )

        # =================================================
        # STEP 7
        # AI RESUME IMPROVEMENT INSIGHTS
        # =================================================

        print(
            "\n[7/7] Generating AI resume insights..."
        )

        resume_insights = generate_resume_insights(
            skill_analysis=skill_analysis,
            career_compatibility=career_compatibility,
            job_matches=job_matches,
            resume_score=resume_score,
        )

        print(
            f"Insights generated: "
            f"{resume_insights.get('total_insights', 0)}"
        )

        # =================================================
        # FINAL RESPONSE
        # =================================================

        response = {

            # -------------------------------------------------
            # BASIC
            # -------------------------------------------------

            "success": True,
            "filename": file.filename,
            "career": career,

            # -------------------------------------------------
            # DETECTED SKILLS
            # -------------------------------------------------

            "skills": skills,
            "skill_evidence": skill_evidence,

            # -------------------------------------------------
            # SKILL ANALYSIS
            # -------------------------------------------------

            "skill_analysis": skill_analysis,

            # -------------------------------------------------
            # CAREER COMPATIBILITY
            # -------------------------------------------------

            "career_compatibility": career_compatibility,

            # -------------------------------------------------
            # EXISTING JOB MATCHING
            # -------------------------------------------------

            "job_matches": job_matches,

            # -------------------------------------------------
            # RESUME SCORE
            # -------------------------------------------------

            "resume_score": resume_score,

            # -------------------------------------------------
            # AI RESUME INSIGHTS
            # -------------------------------------------------

            "resume_insights": resume_insights,

            # -------------------------------------------------
            # TEXT INFORMATION
            # -------------------------------------------------

            "text_length": len(text),
        }

        # =================================================
        # SUCCESS LOG
        # =================================================

        print("\n")
        print("=" * 50)
        print("ANALYSIS SUCCESSFUL")
        print("=" * 50)

        print(
            f"Detected Skills: {len(skills)}"
        )

        print(
            f"Skill Coverage: {skill_coverage}%"
        )

        print(
            f"Career Compatibility: {career_score}%"
        )

        print(
            f"Best Job Match: {job_score}%"
        )

        print(
            f"Resume Score: "
            f"{resume_score.get('score', 0)}%"
        )

        print(
            f"AI Insights: "
            f"{resume_insights.get('total_insights', 0)}"
        )

        print("=" * 50)
        print("\n")

        return response

    # =====================================================
    # HTTP EXCEPTIONS
    # =====================================================

    except HTTPException:
        raise

    # =====================================================
    # UNEXPECTED ERRORS
    # =====================================================

    except Exception as error:

        print("\n")
        print("=" * 50)
        print("ANALYSIS FAILED")
        print("=" * 50)

        print(
            f"ERROR TYPE: "
            f"{type(error).__name__}"
        )

        print(
            f"ERROR: {error}"
        )

        print("\nFULL TRACEBACK:")

        traceback.print_exc()

        print("=" * 50)
        print("\n")

        raise HTTPException(
            status_code=500,
            detail=(
                f"{type(error).__name__}: "
                f"{error}"
            ),
        )


# =========================================================
# AI JOB DISCOVERY
# =========================================================

@app.post("/api/search-jobs")
def search_jobs(
    request: JobSearchRequest,
):

    try:

        print("\n")
        print("=" * 50)
        print("SKILLPULSE AI")
        print("JOB DISCOVERY STARTED")
        print("=" * 50)

        print(
            f"Resume skills: {request.skills}"
        )

        print(
            f"Requested limit: {request.limit}"
        )

        # =================================================
        # VALIDATE LIMIT
        # =================================================

        limit = max(
            1,
            min(
                request.limit,
                20,
            ),
        )

        # =================================================
        # DISCOVER JOBS
        # =================================================

        jobs = discover_jobs(
            resume_skills=request.skills,
            limit=limit,
        )

        # =================================================
        # LOG
        # =================================================

        print(
            f"Jobs discovered: {len(jobs)}"
        )

        # =================================================
        # SUCCESS RESPONSE
        # =================================================

        response = {
            "success": True,
            "total_jobs": len(jobs),
            "jobs": jobs,
        }

        print("=" * 50)
        print("JOB DISCOVERY SUCCESSFUL")
        print("=" * 50)
        print("\n")

        return response

    # =====================================================
    # UNEXPECTED ERROR
    # =====================================================

    except Exception as error:

        print("\n")
        print("=" * 50)
        print("JOB DISCOVERY FAILED")
        print("=" * 50)

        print(
            f"ERROR TYPE: "
            f"{type(error).__name__}"
        )

        print(
            f"ERROR: {error}"
        )

        traceback.print_exc()

        print("=" * 50)
        print("\n")

        raise HTTPException(
            status_code=500,
            detail=(
                f"{type(error).__name__}: "
                f"{error}"
            ),
        )