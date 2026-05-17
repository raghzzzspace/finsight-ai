import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

export default function RevenueChart({ data }) {
  if (!Array.isArray(data) || data.length === 0) {
    return (
      <div className="p-6 bg-white rounded-2xl shadow-md border">
        Loading chart...
      </div>
    );
  }

  return (
    <div className="bg-white p-6 rounded-2xl shadow-lg border w-full">
      <div className="mb-4">
        <h2 className="text-xl font-semibold text-gray-800">
          📈 Revenue Analytics
        </h2>
        <p className="text-sm text-gray-500">
          Daily net revenue performance
        </p>
      </div>

      <div style={{ width: "100%", height: 320 }}>
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data}>
            <XAxis dataKey="date" stroke="#888" />
            <YAxis stroke="#888" />
            <Tooltip />

            <Line
              type="monotone"
              dataKey="total_net"
              stroke="#4f46e5"
              strokeWidth={3}
              dot={{ r: 4 }}
              activeDot={{ r: 6 }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}