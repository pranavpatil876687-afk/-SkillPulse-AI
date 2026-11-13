import axios from "axios";

const api = axios.create({
  baseURL: "http://127.0.0.1:8000",
  timeout: 120000,
});

// Analyze Resume
export const analyzeResume = async (file, career) => {
  const formData = new FormData();

  formData.append("file", file);
  formData.append("career", career);

  const response = await api.post(
    "/api/analyze-resume",
    formData,
    {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    }
  );

  return response.data;
};

// Search Jobs
export const searchJobs = async (skills, limit = 10) => {
  const response = await api.post(
    "/api/search-jobs",
    {
      skills: skills,
      limit: limit,
    }
  );

  return response.data;
};

// Backend Health Check
export const checkHealth = async () => {
  const response = await api.get("/api/health");

  return response.data;
};

export default api;