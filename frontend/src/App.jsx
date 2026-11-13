import { useState } from "react";

import { analyzeResume, searchJobs } from "./services/api";

import "./App.css";



function App() {

  const [activePage, setActivePage] = useState("dashboard");

  const [pageHistory, setPageHistory] = useState([]);



  const [file, setFile] = useState(null);

  const [career, setCareer] = useState("data_science");

  const [result, setResult] = useState(null);



  const [loading, setLoading] = useState(false);

  const [jobsLoading, setJobsLoading] = useState(false);

  const [jobs, setJobs] = useState([]);

  const [error, setError] = useState("");



  const careerNames = {

    data_science: "Data Scientist",

    machine_learning_engineer: "Machine Learning Engineer",

    python_developer: "Python Developer",

    data_analyst: "Data Analyst",

    full_stack_developer: "Full Stack Developer",

  };



  const formatCareerName = (value) => {

    return careerNames[value] || value;

  };



  const handleFileChange = (event) => {

    const selectedFile = event.target.files[0];



    if (!selectedFile) return;



    setFile(selectedFile);

    setResult(null);

    setJobs([]);

    setError("");

  };



  const handleAnalyze = async () => {

    if (!file) {

      setError("Please select a PDF resume first.");

      setActivePage("resume");

      return;

    }



    setLoading(true);

    setJobsLoading(false);

    setError("");

    setResult(null);

    setJobs([]);



    try {

      const data = await analyzeResume(file, career);



      if (!data.success) {

        setError(data.message || "Resume analysis failed.");

        return;

      }



      setResult(data);

      setActivePage("dashboard");



      const detectedSkills = data.skills || [];



      if (detectedSkills.length > 0) {

        setJobsLoading(true);



        try {

          const jobResponse = await searchJobs(detectedSkills, 10);



          if (jobResponse.success) {

            setJobs(jobResponse.jobs || []);

          } else {

            setJobs([]);

          }

        } catch (jobError) {

          console.error("Job search failed:", jobError);

          setJobs([]);

        } finally {

          setJobsLoading(false);

        }

      }

    } catch (err) {

      console.error(err);



      setError(

        err.response?.data?.detail ||

          "Failed to analyze resume. Please try again."

      );

    } finally {

      setLoading(false);

    }

  };



  const getResumeScore = () => {

    return result?.resume_score?.score ?? 0;

  };



  const getResumeScoreLabel = () => {

    return result?.resume_score?.label ?? "Not Available";

  };



  const getSkillCoverage = () => {

    return (

      result?.resume_score?.components?.skill_coverage ??

      result?.skill_analysis?.skill_score ??

      0

    );

  };



  const getCareerCompatibility = () => {

    return (

      result?.resume_score?.components?.career_compatibility ?? 0

    );

  };



  const getJobCompatibility = () => {

    if (jobs.length > 0) {

      return jobs[0]?.match_score ?? 0;

    }



    return result?.resume_score?.components?.job_compatibility ?? 0;

  };



  const getMissingSkills = () => {

    return result?.skill_analysis?.missing_skills || [];

  };



  const getMatchedSkills = () => {

    return result?.skill_analysis?.matched_skills || [];

  };



  const getRoadmap = () => {

    return result?.skill_analysis?.learning_roadmap || [];

  };



  const getPriorityClass = (priority) => {

    if (!priority) return "";



    return priority.toLowerCase().replace(/\s+/g, "-");

  };



  const navigation = [

    {

      id: "dashboard",

      icon: "⌂",

      label: "Dashboard",

    },

    {

      id: "resume",

      icon: "▣",

      label: "Resume Analysis",

    },

    {

      id: "career",

      icon: "◎",

      label: "Career Intelligence",

    },

    {

      id: "jobs",

      icon: "◈",

      label: "Job Matches",

    },

    {

      id: "roadmap",

      icon: "◇",

      label: "Learning Roadmap",

    },

  ];



  const pageTitles = {

    dashboard: {

      title: "Dashboard",

      subtitle: "Your career intelligence overview",

    },

    resume: {

      title: "Resume Analysis",

      subtitle: "Understand what your resume says about your skills",

    },

    career: {

      title: "Career Intelligence",

      subtitle: "Explore your compatibility with different career paths",

    },

    jobs: {

      title: "Job Matches",

      subtitle: "Jobs ranked according to your detected skills",

    },

    roadmap: {

      title: "Learning Roadmap",

      subtitle: "Build the skills required for your target career",

    },

  };



  const currentPage = pageTitles[activePage];



  const StatCard = ({ icon, label, value, suffix = "" }) => (

    <div className="stat-card">

      <div className="stat-card-top">

        <div className="stat-icon">{icon}</div>

        <span className="stat-label">{label}</span>

      </div>



      <div className="stat-value">

        {value}

        <span>{suffix}</span>

      </div>

    </div>

  );



  const EmptyState = ({

    title = "No analysis available",

    message = "Upload your resume to unlock this section.",

  }) => (

    <div className="empty-state">

      <div className="empty-state-icon">✦</div>

      <h3>{title}</h3>

      <p>{message}</p>



      <button

        className="primary-button"

        onClick={() => setActivePage("resume")}

      >

        Analyze Resume →

      </button>

    </div>

  );



  const renderDashboard = () => {

    if (!result) {

      return (

        <div className="dashboard-empty">

          <div className="hero-card">

            <div className="hero-glow"></div>



            <div className="hero-content">

              <span className="eyebrow">AI CAREER INTELLIGENCE</span>



              <h1>

                Turn your resume into a

                <span> career strategy.</span>

              </h1>



              <p>

                Analyze your resume, identify skill gaps, discover suitable

                career paths, and get personalized job and learning

                recommendations.

              </p>



              <button

                className="primary-button hero-button"

                onClick={() => setActivePage("resume")}

              >

                Start Resume Analysis →

              </button>

            </div>



            <div className="hero-orbit">

              <div className="orbit-center">AI</div>

              <div className="orbit-node node-one">CV</div>

              <div className="orbit-node node-two">SK</div>

              <div className="orbit-node node-three">JOB</div>

              <div className="orbit-node node-four">AI</div>

            </div>

          </div>



          <div className="feature-grid">

            <div className="feature-card">

              <span>01</span>

              <h3>Resume Intelligence</h3>

              <p>

                Extract skills and understand your current technical profile.

              </p>

            </div>



            <div className="feature-card">

              <span>02</span>

              <h3>Career Matching</h3>

              <p>

                Compare your profile with multiple technology career paths.

              </p>

            </div>



            <div className="feature-card">

              <span>03</span>

              <h3>Skill Roadmap</h3>

              <p>

                Discover what to learn next based on your missing skills.

              </p>

            </div>

          </div>

        </div>

      );

    }



    const insights = result.resume_insights?.insights || [];



    return (

      <div className="page-content">

        <div className="welcome-row">

          <div>

            <span className="eyebrow">CAREER OVERVIEW</span>

            <h1>Welcome back 👋</h1>

            <p>

              Here's the current intelligence report for your resume.

            </p>

          </div>



          <button

            className="secondary-button"

            onClick={() => setActivePage("resume")}

          >

            Analyze New Resume

          </button>

        </div>



        <div className="stats-grid">

          <StatCard

            icon="✦"

            label="Resume Score"

            value={getResumeScore()}

            suffix="/100"

          />



          <StatCard

            icon="◉"

            label="Skill Coverage"

            value={getSkillCoverage()}

            suffix="%"

          />



          <StatCard

            icon="◎"

            label="Career Match"

            value={getCareerCompatibility()}

            suffix="%"

          />



          <StatCard

            icon="◈"

            label="Best Job Match"

            value={getJobCompatibility()}

            suffix="%"

          />

        </div>



        <div className="dashboard-grid">

          <div className="panel score-panel">

            <div className="panel-header">

              <div>

                <span className="panel-kicker">AI EVALUATION</span>

                <h2>Resume Strength</h2>

              </div>



              <span className="status-pill">

                {getResumeScoreLabel()}

              </span>

            </div>



            <div className="score-display">

              <div className="score-ring">

                <div>

                  <strong>{getResumeScore()}</strong>

                  <span>/100</span>

                </div>

              </div>



              <div className="score-details">

                <div>

                  <span>Skill Coverage</span>

                  <strong>{getSkillCoverage()}%</strong>

                </div>



                <div>

                  <span>Career Compatibility</span>

                  <strong>{getCareerCompatibility()}%</strong>

                </div>



                <div>

                  <span>Job Compatibility</span>

                  <strong>{getJobCompatibility()}%</strong>

                </div>

              </div>

            </div>

          </div>



          <div className="panel career-panel">

            <div className="panel-header">

              <div>

                <span className="panel-kicker">TARGET CAREER</span>

                <h2>{formatCareerName(career)}</h2>

              </div>



              <span className="career-dot"></span>

            </div>



            <div className="career-summary">

              <div className="career-summary-score">

                {getCareerCompatibility()}%

              </div>



              <p>

                Your current profile has this level of compatibility with

                your selected career.

              </p>

            </div>



            <button

              className="text-button"

              onClick={() => setActivePage("career")}

            >

              View career intelligence →

            </button>

          </div>

        </div>



        <div className="dashboard-grid">

          <div className="panel">

            <div className="panel-header">

              <div>

                <span className="panel-kicker">SKILL INTELLIGENCE</span>

                <h2>Top Skill Gaps</h2>

              </div>



              <button

                className="text-button"

                onClick={() => setActivePage("roadmap")}

              >

                View roadmap →

              </button>

            </div>



            {getMissingSkills().length > 0 ? (

              <div className="dashboard-skills">

                {getMissingSkills().slice(0, 6).map((skill, index) => (

                  <div className="dashboard-skill-row" key={index}>

                    <span className="skill-number">

                      {String(index + 1).padStart(2, "0")}

                    </span>



                    <span>{skill}</span>



                    <span className="missing-dot"></span>

                  </div>

                ))}

              </div>

            ) : (

              <p className="muted-text">No major skill gaps detected.</p>

            )}

          </div>



          <div className="panel">

            <div className="panel-header">

              <div>

                <span className="panel-kicker">JOB INTELLIGENCE</span>

                <h2>Top Matches</h2>

              </div>



              <button

                className="text-button"

                onClick={() => setActivePage("jobs")}

              >

                View all →

              </button>

            </div>



            {jobsLoading ? (

              <div className="loading-state">

                Finding the best job matches...

              </div>

            ) : jobs.length > 0 ? (

              <div className="mini-job-list">

                {jobs.slice(0, 3).map((job, index) => (

                  <div className="mini-job" key={index}>

                    <div>

                      <strong>{job.title}</strong>

                      <span>

                        {job.company} · {job.location}

                      </span>

                    </div>



                    <b>{job.match_score}%</b>

                  </div>

                ))}

              </div>

            ) : (

              <p className="muted-text">No job matches available.</p>

            )}

          </div>

        </div>



        {insights.length > 0 && (

          <div className="panel">

            <div className="panel-header">

              <div>

                <span className="panel-kicker">AI CAREER INTELLIGENCE</span>

                <h2>Latest Insights</h2>

              </div>

            </div>



            <div className="insight-preview-grid">

              {insights.slice(0, 3).map((insight, index) => (

                <div className="insight-preview" key={index}>

                  <div className="insight-preview-icon">

                    {insight.type === "warning"

                      ? "!"

                      : insight.type === "success"

                      ? "✓"

                      : insight.type === "action"

                      ? "→"

                      : "i"}

                  </div>



                  <div>

                    <h3>{insight.title}</h3>

                    <p>{insight.message}</p>

                  </div>

                </div>

              ))}

            </div>

          </div>

        )}

      </div>

    );

  };



  const renderResumeAnalysis = () => {

    return (

      <div className="page-content">

        <div className="page-intro">

          <span className="eyebrow">RESUME INTELLIGENCE</span>

          <h1>Analyze your resume</h1>

          <p>

            Upload your resume and let SkillPulse AI identify your skills,

            gaps, evidence, and career readiness.

          </p>

        </div>



        <div className="upload-layout">

          <div className="panel upload-panel">

            <div className="upload-icon">↑</div>



            <h2>Upload Resume</h2>



            <p>

              Upload a PDF resume to begin your AI-powered career analysis.

            </p>



            <label className="file-dropzone">

              <input

                type="file"

                accept=".pdf"

                onChange={handleFileChange}

              />



              <span className="dropzone-icon">+</span>



              <strong>

                {file ? file.name : "Choose your PDF resume"}

              </strong>



              <small>

                {file

                  ? "Resume selected successfully"

                  : "PDF files only"}

              </small>

            </label>



            <div className="career-selector">

              <label htmlFor="career">Target Career</label>



              <select

                id="career"

                value={career}

                onChange={(event) => {

                  setCareer(event.target.value);

                  setResult(null);

                  setJobs([]);

                }}

              >

                <option value="data_science">Data Scientist</option>

                <option value="machine_learning_engineer">

                  Machine Learning Engineer

                </option>

                <option value="python_developer">

                  Python Developer

                </option>

                <option value="data_analyst">Data Analyst</option>

                <option value="full_stack_developer">

                  Full Stack Developer

                </option>

              </select>

            </div>



            {error && <div className="error-box">{error}</div>}



            <button

              className="primary-button full-width"

              onClick={handleAnalyze}

              disabled={loading}

            >

              {loading ? "Analyzing Resume..." : "Analyze Resume →"}

            </button>

          </div>



          <div className="panel upload-info-panel">

            <span className="panel-kicker">WHAT YOU GET</span>



            <h2>A complete career intelligence report.</h2>



            <div className="analysis-feature-list">

              <div>

                <span>01</span>

                <div>

                  <strong>Skill Detection</strong>

                  <p>Identify technical skills present in your resume.</p>

                </div>

              </div>



              <div>

                <span>02</span>

                <div>

                  <strong>Skill Gap Analysis</strong>

                  <p>Discover skills required for your selected career.</p>

                </div>

              </div>



              <div>

                <span>03</span>

                <div>

                  <strong>Job Matching</strong>

                  <p>Find job profiles compatible with your skills.</p>

                </div>

              </div>



              <div>

                <span>04</span>

                <div>

                  <strong>Learning Roadmap</strong>

                  <p>Get a structured path to close your skill gaps.</p>

                </div>

              </div>

            </div>

          </div>

        </div>



        {result && (

          <>

            <div className="section-divider"></div>



            <div className="section-title-row">

              <div>

                <span className="eyebrow">ANALYSIS RESULT</span>

                <h2>{result.filename}</h2>

              </div>



              <span className="status-pill success">Analysis Complete</span>

            </div>



            <div className="stats-grid">

              <StatCard

                icon="✦"

                label="Resume Score"

                value={getResumeScore()}

                suffix="/100"

              />



              <StatCard

                icon="◉"

                label="Required Skill Coverage"

                value={getSkillCoverage()}

                suffix="%"

              />



              <StatCard

                icon="✓"

                label="Detected Skills"

                value={result.skills?.length || 0}

              />



              <StatCard

                icon="!"

                label="Missing Skills"

                value={getMissingSkills().length}

              />

            </div>



            <div className="panel">

              <div className="panel-header">

                <div>

                  <span className="panel-kicker">DETECTED SKILLS</span>

                  <h2>Skills found in your resume</h2>

                </div>

              </div>



              {result.skills?.length > 0 ? (

                <div className="skill-cloud">

                  {result.skills.map((skill, index) => (

                    <span className="skill-chip detected" key={index}>

                      {skill}

                    </span>

                  ))}

                </div>

              ) : (

                <p className="muted-text">No skills detected.</p>

              )}

            </div>



            <div className="two-panel-grid">

              <div className="panel">

                <div className="panel-header">

                  <div>

                    <span className="panel-kicker">MATCHED</span>

                    <h2>Matched Skills</h2>

                  </div>

                </div>



                <div className="skill-cloud">

                  {getMatchedSkills().length > 0 ? (

                    getMatchedSkills().map((skill, index) => (

                      <span

                        className="skill-chip matched"

                        key={index}

                      >

                        ✓ {skill}

                      </span>

                    ))

                  ) : (

                    <p className="muted-text">

                      No required skills matched.

                    </p>

                  )}

                </div>

              </div>



              <div className="panel">

                <div className="panel-header">

                  <div>

                    <span className="panel-kicker">SKILL GAPS</span>

                    <h2>Missing Skills</h2>

                  </div>

                </div>



                <div className="skill-cloud">

                  {getMissingSkills().length > 0 ? (

                    getMissingSkills().map((skill, index) => (

                      <span

                        className="skill-chip missing"

                        key={index}

                      >

                        + {skill}

                      </span>

                    ))

                  ) : (

                    <p className="muted-text">No missing skills.</p>

                  )}

                </div>

              </div>

            </div>



            {result.skill_evidence &&

              Object.keys(result.skill_evidence).length > 0 && (

                <div className="panel">

                  <div className="panel-header">

                    <div>

                      <span className="panel-kicker">

                        AI EVIDENCE

                      </span>

                      <h2>Skill Evidence</h2>

                    </div>

                  </div>



                  <div className="evidence-grid">

                    {Object.entries(result.skill_evidence).map(

                      ([skill, evidence], index) => {

                        const confidence =

                          typeof evidence?.confidence === "number"

                            ? evidence.confidence

                            : 0;



                        return (

                          <div className="evidence-card" key={index}>

                            <div className="evidence-card-top">

                              <strong>{skill}</strong>

                              <span>{confidence}%</span>

                            </div>



                            <div className="evidence-progress">

                              <div

                                style={{

                                  width: `${confidence}%`,

                                }}

                              ></div>

                            </div>



                            {evidence?.level && (

                              <small>

                                Level: <strong>{evidence.level}</strong>

                              </small>

                            )}



                            {evidence?.evidence && (

                              <p>

                                "{evidence.evidence}"

                              </p>

                            )}

                          </div>

                        );

                      }

                    )}

                  </div>

                </div>

              )}

          </>

        )}

      </div>

    );

  };



  const renderCareer = () => {

    if (!result) {

      return (

        <div className="page-content">

          <EmptyState

            title="Career intelligence is waiting"

            message="Analyze your resume first to compare your profile with different career paths."

          />

        </div>

      );

    }



    const careers = result.career_compatibility || [];



    return (

      <div className="page-content">

        <div className="page-intro">

          <span className="eyebrow">CAREER INTELLIGENCE</span>

          <h1>Find your strongest career path</h1>

          <p>

            SkillPulse AI compares your detected skills with multiple

            technology career profiles.

          </p>

        </div>



        <div className="career-hero panel">

          <div>

            <span className="panel-kicker">SELECTED CAREER</span>

            <h2>{formatCareerName(career)}</h2>

            <p>

              Your current resume has a{" "}

              <strong>{getCareerCompatibility()}%</strong> compatibility

              score for this career.

            </p>

          </div>



          <div className="large-percentage">

            {getCareerCompatibility()}%

          </div>

        </div>



        <div className="panel">

          <div className="panel-header">

            <div>

              <span className="panel-kicker">CAREER COMPARISON</span>

              <h2>Compatibility across career paths</h2>

            </div>

          </div>



          <div className="career-list">

            {careers.map((item, index) => (

              <div className="career-row" key={item.career || index}>

                <div className="career-row-main">

                  <div className="career-rank">

                    {String(index + 1).padStart(2, "0")}

                  </div>



                  <div>

                    <strong>

                      {item.career_name ||

                        formatCareerName(item.career)}

                    </strong>



                    <div className="career-row-meta">

                      <span>

                        ✓ {item.matched_skills?.length || 0} matched

                      </span>



                      <span>

                        ! {item.missing_skills?.length || 0} missing

                      </span>

                    </div>

                  </div>

                </div>



                <div className="career-score-area">

                  <strong>{item.score ?? 0}%</strong>



                  <div className="career-progress">

                    <div

                      style={{

                        width: `${item.score ?? 0}%`,

                      }}

                    ></div>

                  </div>

                </div>

              </div>

            ))}

          </div>

        </div>



        <div className="two-panel-grid">

          <div className="panel">

            <div className="panel-header">

              <div>

                <span className="panel-kicker">YOUR STRENGTHS</span>

                <h2>Matched Skills</h2>

              </div>

            </div>



            <div className="skill-cloud">

              {getMatchedSkills().map((skill, index) => (

                <span className="skill-chip matched" key={index}>

                  ✓ {skill}

                </span>

              ))}

            </div>

          </div>



          <div className="panel">

            <div className="panel-header">

              <div>

                <span className="panel-kicker">YOUR GAPS</span>

                <h2>Priority Skills</h2>

              </div>

            </div>



            <div className="skill-cloud">

              {getMissingSkills().map((skill, index) => (

                <span className="skill-chip missing" key={index}>

                  + {skill}

                </span>

              ))}

            </div>

          </div>

        </div>

      </div>

    );

  };



  const renderJobs = () => {

    if (!result) {

      return (

        <div className="page-content">

          <EmptyState

            title="Job intelligence is waiting"

            message="Analyze your resume to generate personalized job matches."

          />

        </div>

      );

    }



    return (

      <div className="page-content">

        <div className="page-intro">

          <span className="eyebrow">JOB INTELLIGENCE</span>

          <h1>Recommended job matches</h1>

          <p>

            Job profiles are ranked according to the skills detected in your

            resume.

          </p>

        </div>



        <div className="job-toolbar panel">

          <div>

            <strong>{jobs.length}</strong>

            <span> job profiles analyzed</span>

          </div>



          <span className="job-disclaimer-small">

            Curated compatibility profiles · Not live openings

          </span>

        </div>



        {jobsLoading ? (

          <div className="panel loading-panel">

            <div className="loading-spinner"></div>

            <h3>Finding the best job matches...</h3>

            <p>Comparing your skills with available job profiles.</p>

          </div>

        ) : jobs.length > 0 ? (

          <div className="jobs-page-list">

            {jobs.map((job, index) => (

              <div className="job-card" key={`${job.title}-${index}`}>

                <div className="job-card-top">

                  <div className="job-rank">

                    {String(index + 1).padStart(2, "0")}

                  </div>



                  <div className="job-main-info">

                    <span className="job-category">

                      JOB MATCH

                    </span>



                    <h2>{job.title}</h2>



                    <p>

                      {job.company} · {job.location}

                    </p>

                  </div>



                  <div className="job-score">

                    <strong>{job.match_score ?? 0}%</strong>

                    <span>match</span>

                  </div>

                </div>



                <div className="job-progress">

                  <div

                    style={{

                      width: `${job.match_score ?? 0}%`,

                    }}

                  ></div>

                </div>



                <div className="job-skills-grid">

                  <div>

                    <span className="skill-heading success-heading">

                      MATCHED SKILLS

                    </span>



                    <div className="skill-cloud">

                      {job.matched_skills?.length > 0 ? (

                        job.matched_skills.map((skill, skillIndex) => (

                          <span

                            className="skill-chip matched"

                            key={skillIndex}

                          >

                            {skill}

                          </span>

                        ))

                      ) : (

                        <span className="muted-text">

                          No matching skills

                        </span>

                      )}

                    </div>

                  </div>



                  <div>

                    <span className="skill-heading danger-heading">

                      MISSING SKILLS

                    </span>



                    <div className="skill-cloud">

                      {job.missing_skills?.length > 0 ? (

                        job.missing_skills.map((skill, skillIndex) => (

                          <span

                            className="skill-chip missing"

                            key={skillIndex}

                          >

                            {skill}

                          </span>

                        ))

                      ) : (

                        <span className="muted-text">

                          No missing skills

                        </span>

                      )}

                    </div>

                  </div>

                </div>



                {job.job_search_url && (

                  <a

                    href={job.job_search_url}

                    target="_blank"

                    rel="noreferrer"

                    className="job-link"

                  >

                    Search Similar Jobs ↗

                  </a>

                )}

              </div>

            ))}

          </div>

        ) : (

          <div className="panel empty-state">

            <div className="empty-state-icon">◈</div>

            <h3>No matching jobs found</h3>

            <p>

              We couldn't find compatible profiles for your detected skills.

            </p>

          </div>

        )}

      </div>

    );

  };



  const renderRoadmap = () => {

    if (!result) {

      return (

        <div className="page-content">

          <EmptyState

            title="Your roadmap is waiting"

            message="Analyze your resume to generate a personalized learning roadmap."

          />

        </div>

      );

    }



    const roadmap = getRoadmap();



    return (

      <div className="page-content">

        <div className="page-intro">

          <span className="eyebrow">LEARNING INTELLIGENCE</span>

          <h1>Your personalized roadmap</h1>

          <p>

            A structured learning sequence generated from the skills missing

            for your target career.

          </p>

        </div>



        <div className="roadmap-summary panel">

          <div>

            <span className="panel-kicker">TARGET</span>

            <h2>{formatCareerName(career)}</h2>

            <p>

              Focus on the highest-priority skills first to improve your

              career compatibility.

            </p>

          </div>



          <div className="roadmap-count">

            <strong>{roadmap.length}</strong>

            <span>learning steps</span>

          </div>

        </div>



        {roadmap.length > 0 ? (

          <div className="roadmap-list">

            {roadmap.map((item, index) => (

              <div className="roadmap-card" key={item.skill || index}>

                <div className="roadmap-number">

                  {String(item.order || index + 1).padStart(2, "0")}

                </div>



                <div className="roadmap-body">

                  <div className="roadmap-card-header">

                    <div>

                      <span className="panel-kicker">LEARN NEXT</span>

                      <h2>{item.skill}</h2>

                    </div>



                    <div className="roadmap-tags">

                      <span

                        className={`priority-tag ${getPriorityClass(

                          item.priority

                        )}`}

                      >

                        {item.priority || "Medium"}

                      </span>



                      <span className="level-tag">

                        {item.level || "Beginner"}

                      </span>

                    </div>

                  </div>



                  {item.topics?.length > 0 && (

                    <div className="roadmap-topics">

                      <span>TOPICS</span>



                      <div>

                        {item.topics.map((topic, topicIndex) => (

                          <span key={topicIndex}>{topic}</span>

                        ))}

                      </div>

                    </div>

                  )}



                  {item.next_step && (

                    <div className="next-step">

                      <span>NEXT STEP</span>

                      <p>{item.next_step}</p>

                    </div>

                  )}

                </div>

              </div>

            ))}

          </div>

        ) : (

          <div className="panel empty-state">

            <div className="empty-state-icon">✓</div>

            <h3>No learning gaps found</h3>

            <p>

              Your current skill profile covers the available roadmap

              requirements.

            </p>

          </div>

        )}

      </div>

    );

  };



  const renderPage = () => {

    switch (activePage) {

      case "resume":

        return renderResumeAnalysis();



      case "career":

        return renderCareer();



      case "jobs":

        return renderJobs();



      case "roadmap":

        return renderRoadmap();



      case "dashboard":

      default:

        return renderDashboard();

    }

  };



  return (

    <div className="app-shell">

      <aside className="sidebar">

        <div className="brand">

          <div className="brand-mark">S</div>



          <div>

            <strong>

              SkillPulse <span>AI</span>

            </strong>



            <small>Career Intelligence</small>

          </div>

        </div>



        <div className="sidebar-section">

          <span className="sidebar-label">WORKSPACE</span>



          <nav className="sidebar-nav">

            {navigation.map((item) => (

              <button

                key={item.id}

                className={`nav-item ${

                  activePage === item.id ? "active" : ""

                }`}

                onClick={() => {
                  if (activePage !== item.id) {
                    setPageHistory((prev) => [...prev, activePage]);
                    setActivePage(item.id);
                  }
                }}

              >

                <span className="nav-icon">{item.icon}</span>

                <span>{item.label}</span>

              </button>

            ))}

          </nav>

        </div>



        <div className="sidebar-bottom">

          <div className="sidebar-status">

            <span className="online-dot"></span>



            <div>

              <strong>AI Engine</strong>

              <small>System operational</small>

            </div>

          </div>



          <div className="sidebar-version">

            SkillPulse AI · v1.0

          </div>

        </div>

      </aside>



      <main className="main-area">

        <header className="topbar">
          <div className="topbar-left">
            {pageHistory.length > 0 && (
              <button
                className="back-button"
                onClick={() => {
                  const previousPage = pageHistory[pageHistory.length - 1];
                  setPageHistory((prev) => prev.slice(0, -1));
                  setActivePage(previousPage);
                }}
                title="Go back"
                aria-label="Go back"
              >
                ←
              </button>
            )}

            <div>
              <span className="breadcrumb">SKILLPULSE AI /</span>
              <strong>{currentPage.title}</strong>
            </div>
          </div>

          <div className="topbar-right">

            {result && (

              <div className="topbar-career">

                <span>Target</span>

                <strong>{formatCareerName(career)}</strong>

              </div>

            )}



            <div className="avatar">P</div>

          </div>

        </header>



        <div className="page-wrapper">{renderPage()}</div>

      </main>

    </div>

  );

}



export default App;