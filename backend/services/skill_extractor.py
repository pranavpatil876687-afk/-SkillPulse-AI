import re

from services.semantic_matcher import semantic_skill_detection


# ==================================================
# SKILL DICTIONARY
# ==================================================

SKILLS = [

    # Programming
    "python",
    "java",
    "c++",
    "javascript",
    "typescript",

    # Web Development
    "html",
    "css",
    "react",
    "node.js",
    "express",
    "fastapi",

    # Databases
    "sql",
    "mysql",
    "postgresql",
    "mongodb",

    # Data Science
    "pandas",
    "numpy",
    "scikit-learn",
    "machine learning",
    "deep learning",
    "statistics",
    "data visualization",

    # Tools
    "git",
    "github",
    "docker",

    # BI
    "power bi",
    "tableau",

    # ML Frameworks
    "tensorflow",
    "pytorch",
]


# ==================================================
# FIND EXACT KEYWORD EVIDENCE
# ==================================================

def find_evidence(text: str, skill: str) -> str:

    sentences = re.split(
        r"(?<=[.!?])\s+|\n+",
        text
    )

    for sentence in sentences:

        if re.search(
            r"(?<!\w)" + re.escape(skill) + r"(?!\w)",
            sentence,
            re.IGNORECASE
        ):

            sentence = " ".join(
                sentence.split()
            )

            if len(sentence) > 180:
                sentence = sentence[:180] + "..."

            return sentence

    return "Skill identified from resume context."


# ==================================================
# DETECT SKILL LEVEL
# ==================================================

def detect_skill_level(
    text: str,
    skill: str,
    evidence: str
) -> str:

    context = f"{text} {evidence}".lower()

    skill_pattern = re.escape(skill.lower())

    # --------------------------------------------------
    # Beginner
    # --------------------------------------------------

    beginner_patterns = [

        rf"\b{skill_pattern}\s*\(\s*basic\s*\)",

        rf"\bbasic\s+{skill_pattern}\b",

        rf"\bbeginner\s+{skill_pattern}\b",

        rf"\b{skill_pattern}\s+beginner\b",

        rf"\b{skill_pattern}\s*\(\s*beginner\s*\)",

        rf"\bfundamentals\s+of\s+{skill_pattern}\b",
    ]

    for pattern in beginner_patterns:

        if re.search(
            pattern,
            context,
            re.IGNORECASE
        ):
            return "Beginner"


    # --------------------------------------------------
    # Advanced
    # --------------------------------------------------

    advanced_patterns = [

        rf"\badvanced\s+{skill_pattern}\b",

        rf"\b{skill_pattern}\s+advanced\b",

        rf"\b{skill_pattern}\s*\(\s*advanced\s*\)",

        rf"\bexpert\s+{skill_pattern}\b",

        rf"\b{skill_pattern}\s+expert\b",

        rf"\bexpertise\s+in\s+{skill_pattern}\b",
    ]

    for pattern in advanced_patterns:

        if re.search(
            pattern,
            context,
            re.IGNORECASE
        ):
            return "Advanced"


    # --------------------------------------------------
    # Intermediate
    # --------------------------------------------------

    intermediate_patterns = [

        rf"\bintermediate\s+{skill_pattern}\b",

        rf"\b{skill_pattern}\s+intermediate\b",

        rf"\b{skill_pattern}\s*\(\s*intermediate\s*\)",

        rf"\bproficient\s+in\s+{skill_pattern}\b",

        rf"\bproficiency\s+in\s+{skill_pattern}\b",
    ]

    for pattern in intermediate_patterns:

        if re.search(
            pattern,
            context,
            re.IGNORECASE
        ):
            return "Intermediate"


    # --------------------------------------------------
    # Default
    # --------------------------------------------------

    return "Intermediate"


# ==================================================
# KEYWORD CONFIDENCE
# ==================================================

def calculate_confidence(
    text: str,
    skill: str
) -> int:

    pattern = (
        r"(?<!\w)"
        + re.escape(skill)
        + r"(?!\w)"
    )

    matches = re.findall(
        pattern,
        text,
        re.IGNORECASE
    )

    count = len(matches)

    if count >= 3:
        return 98

    if count == 2:
        return 95

    return 90


# ==================================================
# EXTRACT EXACT KEYWORD SKILLS
# ==================================================

def extract_keyword_skills(text: str):

    found = []

    for skill in SKILLS:

        pattern = (
            r"(?<!\w)"
            + re.escape(skill)
            + r"(?!\w)"
        )

        if re.search(
            pattern,
            text,
            re.IGNORECASE
        ):

            evidence = find_evidence(
                text,
                skill
            )

            confidence = calculate_confidence(
                text,
                skill
            )

            level = detect_skill_level(
                text,
                skill,
                evidence
            )

            found.append(
                {
                    "skill": skill,
                    "confidence": confidence,
                    "evidence": evidence,
                    "level": level,
                    "method": "keyword"
                }
            )

    return found


# ==================================================
# EXTRACT SKILLS WITH AI + KEYWORD MATCHING
# ==================================================

def extract_skills_with_evidence(text: str):

    # --------------------------------------------------
    # Keyword Detection
    # --------------------------------------------------

    keyword_results = extract_keyword_skills(
        text
    )


    # --------------------------------------------------
    # Semantic AI Detection
    # --------------------------------------------------

    semantic_results = semantic_skill_detection(
        text,
        threshold=0.55
    )


    # --------------------------------------------------
    # Combine Results
    # --------------------------------------------------

    combined = {}


    # --------------------------------------------------
    # Add Keyword Results
    # --------------------------------------------------

    for item in keyword_results:

        skill = item["skill"]

        combined[skill] = item


    # --------------------------------------------------
    # Add / Improve With Semantic Results
    # --------------------------------------------------

    for skill, item in semantic_results.items():

        if skill in combined:

            # Keep stronger confidence
            if (
                item["confidence"]
                > combined[skill]["confidence"]
            ):

                evidence = item["evidence"]

                level = detect_skill_level(
                    text,
                    skill,
                    evidence
                )

                combined[skill] = {

                    "skill": skill,

                    "confidence": item["confidence"],

                    "evidence": evidence,

                    "level": level,

                    "method": "semantic_ai"
                }

        else:

            evidence = item["evidence"]

            level = detect_skill_level(
                text,
                skill,
                evidence
            )

            combined[skill] = {

                "skill": skill,

                "confidence": item["confidence"],

                "evidence": evidence,

                "level": level,

                "method": "semantic_ai"
            }


    # --------------------------------------------------
    # Sort Results
    # --------------------------------------------------

    return sorted(
        combined.values(),
        key=lambda item: item["skill"]
    )


# ==================================================
# MAIN FUNCTION
# ==================================================

def extract_skills(text: str):

    results = extract_skills_with_evidence(
        text
    )

    return [
        item["skill"]
        for item in results
    ]