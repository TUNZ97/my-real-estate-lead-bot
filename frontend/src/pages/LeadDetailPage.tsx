import { useParams } from "react-router-dom";

export default function LeadDetailPage() {
  const { leadId } = useParams();

  return (
    <div>
      <h1 style={{ marginTop: 0 }}>Lead Detail</h1>
      <p style={{ color: "#6b7280" }}>Lead ID: {leadId}</p>
      <p>
        This page will show customer info, requirements, qualification, conversation history,
        activity timeline, follow-ups, and sales actions.
      </p>
    </div>
  );
}
