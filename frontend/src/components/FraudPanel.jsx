export default function FraudPanel({ data }) {
  return (
    <div className="bg-white p-6 rounded-2xl shadow-lg border mt-6">
      <h2 className="text-xl font-semibold text-red-600 mb-4">
        🚨 Fraud Detection Alerts
      </h2>

      {/* High Amounts */}
      <div className="mb-6">
        <h3 className="text-md font-semibold text-gray-700 mb-2">
          High Amount Transactions
        </h3>

        {data?.high_amount_anomalies?.length > 0 ? (
          <div className="space-y-2">
            {data.high_amount_anomalies.map((item, i) => (
              <div
                key={i}
                className="flex justify-between p-3 bg-red-50 border border-red-100 rounded-lg"
              >
                <span className="text-gray-700">
                  {item.transaction_id}
                </span>
                <span className="font-semibold text-red-600">
                  ${item.amount}
                </span>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-gray-400 text-sm">No anomalies detected</p>
        )}
      </div>

      {/* Refund Abuse */}
      <div>
        <h3 className="text-md font-semibold text-gray-700 mb-2">
          Refund Abuse Patterns
        </h3>

        {data?.refund_abuse?.length > 0 ? (
          <div className="space-y-2">
            {data.refund_abuse.map((item, i) => (
              <div
                key={i}
                className="flex justify-between p-3 bg-yellow-50 border border-yellow-100 rounded-lg"
              >
                <span className="text-gray-700">
                  {item.customer_id}
                </span>
                <span className="font-semibold text-yellow-600">
                  {item.refund_count} refunds
                </span>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-gray-400 text-sm">No refund abuse detected</p>
        )}
      </div>
    </div>
  );
}