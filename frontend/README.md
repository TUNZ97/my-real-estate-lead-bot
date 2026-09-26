# Frontend — React + Vite + TypeScript

Customer chat and sales dashboard for the Real Estate Lead Bot.

## Scripts

```bash
npm install
npm run dev      # http://localhost:5173
npm run build
npm run preview
```

## Structure

- `src/pages/ChatPage.tsx` — customer conversation UI
- `src/pages/DashboardPage.tsx` — sales lead list
- `src/pages/LeadDetailPage.tsx` — single lead view
- `src/services/api.ts` — backend API client
- `src/types/` — shared TypeScript types

Proxy to backend is configured in `vite.config.ts` for local development.
