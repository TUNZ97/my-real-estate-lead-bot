# Lead Qualification Specification

## 1. Purpose

Define a transparent, deterministic method for evaluating lead value and urgency from validated customer information.

## 2. Separate concepts

- **Lead status:** where the opportunity is in the sales process.
- **Qualification:** current quality/value based on evidence.
- **Urgency:** how soon action may be required.
- **AI confidence:** confidence in interpretation.

## 3. Inputs

Intent, property type, location, bedrooms, budget, timeframe, contactability, engagement and completeness.

## 4. Data quality

Classify extracted information as known, unknown, inferred, contradictory or invalid. Only validated values should affect deterministic scoring.

## 5. MVP score

Total: 0–100.

| Factor | Weight |
|---|---:|
| Intent clarity | 20 |
| Budget clarity | 20 |
| Timeframe | 20 |
| Location | 15 |
| Property requirements | 10 |
| Contactability | 10 |
| Engagement | 5 |

Levels:
- `LOW`: 0–39
- `MEDIUM`: 40–69
- `HIGH`: 70–100

These thresholds are configuration, not immutable facts, and should be calibrated with real data.

## 6. Urgency

- `HIGH`: immediate / within 1 month.
- `MEDIUM`: within 3 months.
- `LOW`: over 3 months / researching.
- `UNKNOWN`: insufficient evidence.

Urgency must not be derived from qualification score alone.

## 7. Missing information

Prioritize questions that materially affect qualification, matching or next action. For example, for “I want a house in Lekki,” intent and location may be known while budget, property type/bedrooms and timeframe remain useful missing fields.

## 8. Hard escalation triggers

Escalate or flag for human attention when the customer requests a human, asks for viewing, begins negotiation, raises a complaint, supplies contradictory critical data, or requires information unavailable to the system.

## 9. Nigerian budget normalization

Support expressions such as `N80m`, `₦80 million`, `80m`, `below 20m`, `up to 50m`, `around 80m`, `minimum 50m`, and ranges. Preserve the semantic constraint rather than converting every expression into an exact amount.

## 10. Recalculation

Recalculate qualification when new validated information materially changes the lead. Record the score/version and important changes in activity/audit data.

## 11. Notifications

Sales notifications should use qualification, urgency and explicit escalation rules rather than arbitrary AI judgments.

## 12. Multiple requirements

If a customer has multiple property requirements, store them without silently overwriting one with another. The MVP may model a primary lead plus structured notes/requirements until a full requirement entity is justified.

## 13. Testing

Test boundary scores, missing values, contradictory values, budget ranges, timeframe changes, duplicate messages and recalculation behavior.

## 13. Detailed Scoring Model

The MVP score is deterministic:

| Dimension | Weight |
|---|---:|
| Intent clarity | 20 |
| Budget clarity | 20 |
| Timeframe | 20 |
| Location | 15 |
| Property requirements | 10 |
| Contactability | 10 |
| Engagement | 5 |
| **Total** | **100** |

Suggested interpretation:
- 0–39 = LOW
- 40–69 = MEDIUM
- 70–100 = HIGH

These thresholds are configuration, not AI output.

## 14. Recalculation

Qualification should be recalculated when material lead information changes. The system should retain the current result and record the scoring version so historical changes can be explained.

## 15. Hard Escalation Conditions

Regardless of score, escalate when the customer requests a human, requests a viewing, enters negotiation, makes a complaint, provides unresolved contradictory information or reaches an unsupported business scenario.

## 16. Follow-Up Priority

Follow-up urgency should consider both qualification and customer timeframe. A high-value lead with a distant timeframe should not automatically be treated as urgent; value and urgency are separate dimensions.
