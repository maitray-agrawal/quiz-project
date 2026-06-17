import { useEffect, useState } from "react";
import { getStudents, predictStudent } from "../api";

export default function Students() {
  const [students, setStudents] = useState([]);

  useEffect(() => {
    getStudents().then(setStudents);
  }, []);

  const handlePredict = async (id) => {
    const res = await predictStudent(id);
    alert(JSON.stringify(res, null, 2));
  };

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Students</h1>

      {students.map((s) => (
        <div key={s.student_id} className="border p-4 mb-3">
          <p>{s.name}</p>
          <p>Attendance: {s.attendance_pct}%</p>

          <button
            className="bg-blue-500 text-white px-3 py-1 mt-2"
            onClick={() => handlePredict(s.student_id)}
          >
            Predict
          </button>
        </div>
      ))}
    </div>
  );
}