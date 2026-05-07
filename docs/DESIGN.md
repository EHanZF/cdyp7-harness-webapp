Design notes and brand guidance for the CDYP7 Dashboard
=====================================================

Goal
----
Provide a simple, professional dashboard UI that aligns with ZF's corporate brand
principles (engineering-focused, trustworthy, and professional). This document is
intended as a lightweight guide — for official assets (exact logo files, hex
values and typography rules) consult ZF's corporate identity portal or the ZF
Download Center: https://www.zf.com/mobile/en/company/downloadcenter/all.html

Brand tone
----------
- Professional and engineering-first: prioritise clarity, legibility and
  factual language.
- Trustworthy: clear affordances for audit, approval and provenance.
- Accessible: WCAG AA contrast and keyboard navigability.

Color palette (guidance — confirm with official CI)
-------------------------------------------------
- Primary accent: ZF Blue (use official hex from CI portal). If official value
  is not available during development, use #005EA6 as a temporary accent.
- Background: white (#ffffff) for content areas, light gray for surfaces.
- Text: near-black for body copy (#0f172a or similar). Muted tones for hints.

Typography
----------
- Use a neutral sans-serif for UI: Segoe UI (Windows), system-ui, Arial. If a
  custom ZF font is provided by the CI portal, prefer that in production.
- Sizes: base 16px, headings use comfortable scale (1.25–1.6x).

Imagery & icons
----------------
- Use engineering and mobility photography with high clarity and minimal
  overlays. Prefer images that illustrate systems and safe mobility.
- Use simple line icons for actions (upload, download, ingest, audit).

Layout & components
--------------------
- Top-level header + lightweight toolbar (actor identity, environment).
- Main content: two-column responsive layout (left: file list & actions; right:
  job/audit/status panels).
- File list: compact table with filename, size, uploaded-by, download link, and
  checkbox to select for ingestion.
- Upload flow: multipart form, show progress and resulting file id.
- Ingest flow: select files, click "Ingest"; provide job-id and polling.

Accessibility
-------------
- Ensure buttons and inputs have visible labels and focus styles.
- Use aria-live regions or clear textual status updates for long-running
  operations (ingest jobs).
- Make sure color contrast meets WCAG AA for text.

Assets & compliance
-------------------
- Do not embed ZF logos, fonts or trademarked materials into builds without
  checking the CI portal and legal guidance. Use placeholders in development
  and swap with official assets at release time.

Implementation notes for CDYP7
------------------------------
- Start with a static HTML + JS interface (see `app/static/dashboard.html`).
- Keep the UI decoupled from back-end endpoints — the front-end calls REST
  helpers under `/api/*` and uses the canonical MCP endpoint `/mcp` only for
  JSON-RPC interactions.
- Provide a light-mode default consistent with typical ZF corporate sites; the
  existing dark site used for the internal tooling UI is acceptable for dev but
  switch to light mode for production if aligning with ZF public sites.

Where to get official guidance
------------------------------
- ZF Download Center: https://www.zf.com/mobile/en/company/downloadcenter/all.html
- ZF corporate site: https://www.zf.com/

Notes
-----
This document is intentionally conservative: rely on official CI resources for
exact brand tokens (logo artwork, color swatches, and licensed fonts). If you
can provide access or a copy of the ZF CI PDF, I will update this file with
precise hex values, font stack, and logo usage rules.
