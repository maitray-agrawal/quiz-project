const colors = {
  high:   "bg-red-100 text-red-800 border border-red-200",
  medium: "bg-yellow-100 text-yellow-800 border border-yellow-200",
  low:    "bg-green-100 text-green-800 border border-green-200",
}

export default function RiskBadge({ tier }) {
  return (
    <span className={`text-xs font-medium px-2.5 py-1 rounded-full ${colors[tier] ?? "bg-gray-100 text-gray-600"}`}>
      {tier ?? "unassessed"}
    </span>
  )
}