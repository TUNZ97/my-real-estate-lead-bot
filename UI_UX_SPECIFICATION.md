# UI/UX Specification

## 1. Purpose

Define the user experience for customers and PrimeHomes sales staff.

## 2. Primary surfaces

### Customer
- Conversation/chat screen.
- Optional lead/property requirement form.
- Clear status/confirmation messages.
- Human handoff indication.

### Sales team
- Lead dashboard.
- Lead list with search/filter.
- Lead detail view.
- Conversation history.
- Qualification and urgency indicators.
- Lead status controls.
- Follow-up management.
- Assignment and notification state.

## 3. Customer chat flow

1. Customer enters enquiry.
2. Show sending/loading state.
3. Display bot response.
4. Preserve conversation context.
5. Ask focused clarification questions.
6. Offer human handoff when appropriate.

## 4. Sales dashboard

Recommended columns/filters:
- Lead name/contact
- Intent
- Property type
- Location
- Budget
- Qualification
- Urgency
- Status
- Assigned agent
- Last activity
- Follow-up due

## 5. Lead detail

The detail page should separate:
- Customer information
- Requirements
- Qualification
- Conversation
- Activity timeline
- Follow-ups
- Sales actions

## 6. Interaction states

Every async operation needs loading, success, empty and error states. Destructive or consequential actions should require confirmation where appropriate.

## 7. Accessibility

Use semantic controls, keyboard accessibility, readable contrast, visible focus states, meaningful labels and accessible validation/error messages.

## 8. Responsive design

Customer chat must work on mobile first. Sales views should remain usable on smaller screens, with tables collapsing into cards or horizontally scrollable regions where appropriate.

## 9. Design principles

- Show the information needed for the current task.
- Avoid exposing internal AI reasoning.
- Distinguish qualification from status.
- Use clear language rather than technical system terms.
- Never imply a property is available unless confirmed by data.

## 12. Customer Chat Experience

The customer should see a simple conversational interface with clear message states, input validation, loading feedback and graceful failure. The UI should not expose internal AI scores or technical workflow details.

### Core states
- empty conversation;
- sending;
- processing;
- response received;
- retryable failure;
- human handoff;
- closed conversation.

## 13. Sales Dashboard

The sales view should prioritize actionable information:
- lead name/contact;
- intent;
- property requirement;
- location;
- budget;
- qualification;
- urgency;
- current status;
- assigned agent;
- next follow-up;
- latest conversation summary.

Filtering should support status, qualification, urgency, assignee and date.

## 14. Accessibility

Use semantic controls, keyboard navigation, readable contrast, visible focus states, meaningful labels, error messages associated with inputs and responsive layouts. Do not rely on color alone to communicate status.

## 15. Responsive Behavior

The customer experience must work on mobile-first layouts. The sales dashboard may use a desktop-oriented information density but should remain usable on smaller screens.
