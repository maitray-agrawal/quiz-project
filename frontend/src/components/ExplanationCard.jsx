export default function ExplanationCard({ data }) {
  if (!data) return null
  const { prediction, confidence, top_factors } = data

  return (
    <div className="mt-4 p-4 rounded-xl border border-gray-200 bg-white">
      <div className="flex items-center gap-3 mb-4">
        <span className={`text-sm font-medium px-3 py-1 rounded-full ${
          prediction === "pass" ? "bg-green-100 text-green-800" : "bg-red-100 text-red-800"
        }`}>
          Predicted: {prediction}
        </span>
        <span className="text-sm text-gray-500">
          {(confidence * 100).toFixed(0)}% confidence
        </span>
      </div>
      <p className="text-xs text-gray-500 mb-3">Top factors driving this prediction</p>
      <div className="space-y-2">
        {top_factors?.map((f, i) => (
          <div key={i} className="flex items-center gap-3">
            <span className="text-xs text-gray-600 w-44 truncate">{f.feature.replace(/_/g, " ")}</span>
            <div className="flex-1 h-2 rounded-full bg-gray-100 overflow-hidden">
              <div
                className={`h-full rounded-full ${f.direction === "reduces_risk" ? "bg-green-400" : "bg-red-400"}`}
                style={{ width: `${Math.min(Math.abs(f.shap_value) * 100, 100)}%` }}
              />
            </div>
            <span className={`text-xs font-medium w-16 text-right ${
              f.direction === "reduces_risk" ? "text-green-700" : "text-red-700"
            }`}>
              {f.direction === "reduces_risk" ? "+" : "-"}{Math.abs(f.shap_value).toFixed(3)}
            </span>
          </div>
        ))}
      </div>
    </div>
  )
}