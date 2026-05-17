import { useEffect, useState } from "react";
import API from "../api/client";
import RevenueChart from "../components/RevenueChart";
import FraudPanel from "../components/FraudPanel";


export default function Dashboard() {
  const [revenue, setRevenue] = useState([]);
  const [fraud, setFraud] = useState(null);

  useEffect(() => {
    fetchData();

    const interval = setInterval(fetchData, 5000); // realtime feel
    return () => clearInterval(interval);
  }, []);

  const fetchData = async () => {
    const res1 = await API.get("/analytics/daily-revenue?date=2026-05-17");
    const res2 = await API.get("/fraud/detect");

    console.log("REVENUE DATA:", revenue);
    setRevenue(Array.isArray(res1.data) ? res1.data : [res1.data]);
    setFraud(res2.data);
  };

  return (
  <div className="min-h-screen bg-gray-100 p-6">
    <h1 className="text-2xl font-bold text-gray-800 mb-6">
      📊 FinSight AI Dashboard
    </h1>

    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <RevenueChart data={revenue} />
      <div>
        {fraud && <FraudPanel data={fraud} />}
      </div>
    </div>
  </div>
  );
};