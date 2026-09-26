/** Shared frontend types aligned with API schemas. */

export type LeadStatus =
  | "NEW"
  | "CONTACTED"
  | "QUALIFIED"
  | "FOLLOW_UP"
  | "PROPERTY_MATCHED"
  | "VIEWING_SCHEDULED"
  | "NEGOTIATION"
  | "CONVERTED"
  | "LOST"
  | "CLOSED"
  | "NOT_INTERESTED"
  | "UNQUALIFIED";

export type QualificationLevel = "LOW" | "MEDIUM" | "HIGH" | "UNKNOWN";
export type Urgency = "LOW" | "MEDIUM" | "HIGH" | "UNKNOWN";

export interface Lead {
  id: string;
  customer_id: string;
  status: LeadStatus;
  intent?: string | null;
  property_type?: string | null;
  location_text?: string | null;
  bedrooms?: number | null;
  budget_min?: number | null;
  budget_max?: number | null;
  currency?: string | null;
  timeframe?: string | null;
  qualification_level?: QualificationLevel | null;
  qualification_score?: number | null;
  urgency?: Urgency | null;
  assigned_to?: string | null;
  created_at: string;
  updated_at: string;
}
