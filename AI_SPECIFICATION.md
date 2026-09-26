# AI Specification

## 1. Purpose

Define how AI is used safely and predictably inside the Real Estate Lead Bot. AI is an interpretation and generation component, not the authoritative owner of business state.

## 2. AI responsibilities

### In scope
- Intent classification.
- Property requirement extraction.
- Budget and currency interpretation.
- Missing-information detection.
- Conversation-aware response drafting.
- Conversation summaries.
- Human-handoff recommendations.

### Out of scope
- Inventing listings.
- Final database decisions without validation.
- Deterministic qualification scoring.
- Autonomous negotiation.
- Legal or financial advice.

## 3. Processing modes

1. **Extraction:** convert a customer message into structured fields.
2. **Conversation:** generate a grounded customer response.
3. **Qualification support:** identify signals, while the deterministic qualification service calculates the score.
4. **Handoff:** identify cases that should involve a human.
5. **Summary:** summarize a conversation for sales staff.

## 4. Structured extraction contract

```json
{
  "intent": "BUY",
  "property_type": "APARTMENT",
  "bedrooms": 3,
  "location": "Lekki",
  "budget_min": 70000000,
  "budget_max": 80000000,
  "currency": "NGN",
  "timeframe": "WITHIN_1_MONTH",
  "customer": {"name": null, "email": null, "phone": null},
  "missing_information": [],
  "confidence": 0.94,
  "requires_human": false,
  "handoff_reason": null,
  "suggested_next_question": null,
  "response": "Thanks! I have the main details..."
}
```

The exact schema should be implemented as a versioned Pydantic model/JSON Schema and rejected when invalid.

## 5. Extraction rules

- Distinguish explicit facts from assumptions.
- Use `null`/unknown rather than guessing.
- Preserve ranges such as “between 50m and 70m”.
- Normalize common Nigerian expressions such as `80m`, `N80m`, `₦80 million`.
- Interpret “below 20m” as a maximum constraint, not an exact budget.
- Handle multiple requirements without silently dropping one.
- Flag contradictions instead of choosing arbitrarily.

## 6. Confidence

Confidence is about interpretation quality, not lead value. Low confidence should trigger clarification or human review depending on impact.

Suggested behavior:
- High confidence: continue normally.
- Medium confidence: continue with targeted clarification.
- Low confidence on critical fields: do not make irreversible decisions; request clarification or hand off.

## 7. Response generation

Responses must be grounded in known system data. The AI must not claim that a property exists, is available, has a specific price, or has a specific feature unless that information is supplied by an authoritative source.

A useful response should:
1. Acknowledge the request.
2. Reflect known requirements.
3. Ask the highest-value missing question when needed.
4. Avoid unnecessary questions.
5. Escalate when a human is needed.

## 8. Prompt architecture

Use separate, versioned prompts for extraction, response generation, summarization and handoff. Store prompt/model versions with AI processing logs where practical.

## 9. Conversation context

Provide the AI only the relevant conversation history and validated lead state. Do not repeatedly send unbounded history. Preserve customer facts in structured storage and use summaries for long conversations.

## 10. Safety and prompt injection

Customer messages are untrusted input. Instructions embedded in customer content must not override system rules, data-access policies or workflow controls. AI output cannot directly execute privileged actions without backend/workflow validation.

## 11. Human handoff

Escalate for explicit human requests, complaints, negotiation, viewing requests, sensitive/ambiguous cases, contradictions, low-confidence critical information, or workflow failures that require intervention.

## 12. AI vs deterministic logic

| Function | Owner |
|---|---|
| Language interpretation | AI |
| Structured extraction | AI + schema validation |
| Qualification score | Deterministic service |
| Urgency mapping | Deterministic rules using validated fields |
| Database persistence | Backend |
| Workflow routing | n8n |
| Property truth | Database/authorized source |
| Final authorization | Backend |

## 13. Evaluation

Maintain a golden dataset covering:
- clear enquiries
- incomplete enquiries
- ambiguous locations
- budget ranges
- Nigerian currency expressions
- multiple requirements
- contradictions
- follow-up context
- irrelevant messages
- prompt-injection attempts
- escalation scenarios

Track extraction accuracy, field-level accuracy, schema-valid rate, hallucination rate, clarification quality, handoff precision, latency and cost.

## 14. Definition of Done

AI functionality is complete only when its output is schema-valid, tested against representative cases, grounded in available data, observable, versioned and safely integrated with deterministic business rules.

## 18. Detailed AI Output Contract

The extraction agent should return only schema-conforming structured data. A representative contract is:

```json
{
  "intent": "BUY",
  "property_type": "APARTMENT",
  "bedrooms": 3,
  "location": "Lekki",
  "budget_min": 70000000,
  "budget_max": 80000000,
  "currency": "NGN",
  "timeframe": "WITHIN_1_MONTH",
  "missing_information": [],
  "confidence": 0.94,
  "requires_human": false,
  "handoff_reason": null,
  "suggested_next_question": null,
  "response": "Thanks. I have the main details. What is your preferred move-in or purchase timeframe?"
}
```

## 19. Confidence Rules

Confidence describes how confident the model is in its interpretation, not how valuable the lead is. Low confidence should increase the likelihood of clarification or human review. Confidence must not override backend authorization or business rules.

## 20. Prompt Design

Prompts should separate:
1. system instructions;
2. task instructions;
3. schema definition;
4. relevant conversation context;
5. authoritative business data;
6. explicit constraints.

Do not place secrets or unnecessary personal data in prompts.

## 21. Evaluation

Maintain a golden dataset containing complete enquiries, incomplete enquiries, ambiguous messages, Nigerian currency expressions, multiple requirements, contradictions, irrelevant questions, unsupported requests and prompt-injection attempts. Track extraction accuracy, schema validity, clarification quality, hallucination rate, escalation precision and response latency.

## 22. AI vs Deterministic Logic

AI is appropriate for interpreting natural language, extracting requirements, summarizing and drafting responses. Backend code is responsible for qualification scores, permission checks, status transitions, money normalization, persistence and other business-critical calculations.
