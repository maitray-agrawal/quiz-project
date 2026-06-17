const API = import.meta.env.VITE_API_URI;

export const getStudents = async () => {
  const res = await fetch(`${API}/students/`);
  return res.json();
};

export const predictStudent = async (student_id) => {
  const res = await fetch(`${API}/predict/student`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ student_id }),
  });
  return res.json();
};

export const chat = async (question) => {
  const res = await fetch(`${API}/chat/`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question }),
  });
  return res.json();
};