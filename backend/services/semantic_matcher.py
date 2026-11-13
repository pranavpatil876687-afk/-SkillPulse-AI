from sentence_transformers import SentenceTransformer
import re


# ==================================================
# MODEL
# ==================================================

_model = None


def get_model():
    """
    Load the SentenceTransformer model only when
    semantic matching is required.
    """

    global _model

    if _model is None:
        _model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

    return _model


# ==================================================
# SKILL DESCRIPTIONS
# ==================================================

SKILL_DESCRIPTIONS = {

    "python":
        "Python programming language, Python development, scripting and programming",

    "sql":
        "SQL databases, database queries, relational databases, joins and data querying",

    "numpy":
        "NumPy numerical computing, arrays, mathematical operations and scientific computing",

    "pandas":
        "Pandas data analysis, data manipulation, data cleaning, dataframes and CSV processing",

    "statistics":
        "statistics, probability, distributions, statistical analysis and hypothesis testing",

    "data visualization":
        "data visualization, charts, graphs, dashboards and visual data analysis",

    "machine learning":
        "machine learning, predictive modeling, classification, regression and machine learning algorithms",

    "scikit-learn":
        "Scikit-learn, sklearn, machine learning implementation, preprocessing, pipelines and model evaluation",

    "deep learning":
        "deep learning, neural networks, CNN, RNN, backpropagation and neural network models",

    "tensorflow":
        "TensorFlow machine learning framework, neural networks and model training",

    "pytorch":
        "PyTorch deep learning framework, tensors, neural networks and model training",

    "git":
        "Git version control, source control, commits, branches, merge and repository management",

    "github":
        "GitHub repositories, pull requests, collaboration, branches and code hosting",

    "docker":
        "Docker containers, Docker images, Dockerfile and application deployment",

    "fastapi":
        "FastAPI Python backend, REST API, API development and web services",

    "mysql":
        "MySQL relational database, SQL queries, tables and database management",

    "postgresql":
        "PostgreSQL relational database, SQL queries, tables and database management",

    "mongodb":
        "MongoDB NoSQL database, collections, documents and database queries",

    "javascript":
        "JavaScript programming, web scripting, ES6 and frontend development",

    "typescript":
        "TypeScript programming, typed JavaScript and frontend development",

    "react":
        "React frontend development, components, hooks, state and user interfaces",

    "html":
        "HTML web pages, semantic markup, forms and web structure",

    "css":
        "CSS styling, responsive design, Flexbox, Grid and web layouts",
}


# ==================================================
# CREATE RESUME TEXT CHUNKS
# ==================================================

def create_chunks(text: str):

    text = re.sub(
        r"\s+",
        " ",
        text
    ).strip()

    if not text:
        return []

    chunks = re.split(
        r"[.!?\n]+",
        text
    )

    chunks = [
        chunk.strip()
        for chunk in chunks
        if len(chunk.strip()) >= 15
    ]

    return chunks


# ==================================================
# SEMANTIC SKILL DETECTION
# ==================================================

def semantic_skill_detection(
    text: str,
    threshold: float = 0.55
):

    chunks = create_chunks(text)

    if not chunks:
        return {}

    # ----------------------------------------------
    # Load AI model only when required
    # ----------------------------------------------

    model = get_model()

    # ----------------------------------------------
    # Encode resume chunks
    # ----------------------------------------------

    chunk_embeddings = model.encode(
        chunks,
        normalize_embeddings=True
    )

    # ----------------------------------------------
    # Prepare skills
    # ----------------------------------------------

    skills = list(
        SKILL_DESCRIPTIONS.keys()
    )

    descriptions = [
        SKILL_DESCRIPTIONS[skill]
        for skill in skills
    ]

    # ----------------------------------------------
    # Encode skill descriptions
    # ----------------------------------------------

    skill_embeddings = model.encode(
        descriptions,
        normalize_embeddings=True
    )

    results = {}

    # ----------------------------------------------
    # Compare resume chunks with skills
    # ----------------------------------------------

    for skill_index, skill in enumerate(skills):

        best_score = 0.0
        best_chunk = ""

        for chunk_index, chunk in enumerate(chunks):

            score = float(
                chunk_embeddings[chunk_index]
                @ skill_embeddings[skill_index]
            )

            if score > best_score:

                best_score = score
                best_chunk = chunk

        # ------------------------------------------
        # Accept semantic match
        # ------------------------------------------

        if best_score >= threshold:

            results[skill] = {

                "confidence": round(
                    best_score * 100,
                    2
                ),

                "evidence": best_chunk,

                "method": "semantic"
            }

    return results