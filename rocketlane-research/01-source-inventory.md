# Rocketlane research — Phase 1: Source inventory

Captured 2026-10-31. Inventory only: **no article content has been read yet**. Every entry is marked `not yet read`.

## Connectivity check

| URL | Result |
|---|---|
| https://www.rocketlane.com/ | 200 |
| https://help.rocketlane.com/support/solutions | 200 |
| https://developer.rocketlane.com/docs/overview | 200 |

## What was inventoried

| Source set | Count | How it was enumerated | File |
|---|---|---|---|
| Help centre articles | 410 (21 categories, 87 folders) | Sitemap plus a crawl of every category and folder page | `inventory/help-centre.csv` |
| Developer docs and API reference | 103 entries (12 guides, 91 API reference) | The site's own `llms.txt` index | `inventory/developer-docs.csv`, `inventory/developer-llms.txt` |
| Blog posts | 536 (89 relevant by title) | 14-page blog index plus the 2 supplied posts | `inventory/blogs.csv` |
| Other official and external sources | 42 | Site links, sitemap, legal pages | `inventory/other-sources.csv` |
| Evidence ledger (started) | 9 Phase 1 observations | — | `ledger/evidence-ledger.csv` |

All 8 supplied URLs are present and reachable. The six help articles sit in NITRO > Meeting Intelligence (3), NITRO > Signals (1), NITRO > Documentation Agent (1) and Integrations > JIRA (1).

## Help centre by category

| Articles | Category | Agent |
|---|---|---|
| 109 | FAQ (split by topic across agents) | A / C / D |
| 56 | Project Management | A |
| 40 | Financial Management | A |
| 34 | Rocketlane Video Academy (page text only) | A |
| 30 | NITRO | D |
| 19 | Automations | A |
| 17 | Reporting and Dashboard | A |
| 16 | Resource Management | A |
| 15 | Get Started (includes permissions and groups) | A / E |
| 12 | Invoicing | A |
| 11 | Time Tracking | A |
| 10 | Templates | A |
| 10 | Integrations (Slack, Salesforce, Jira, Zapier, Workato, HubSpot) | C |
| 7 | Customer Portal | A |
| 7 | Security and Compliance (SAML SSO) | E |
| 6 each | Best Practices; Sprint Planning | A |
| 1–2 each | Accounts, Plans and Billing, Mobile App, Custom Apps | A / C |

**NITRO folders:** Meeting Intelligence (11), Signals (6), **Rocketlane MCP (7)**, Documentation Agent (4), Policies and Governance (1), Nitro Credit Consumption (1).

**Public API resources:** Projects, Phases, Tasks, Spaces, Space Documents, Companies, Users, Fields (custom fields), Time Tracking, Time-Offs, Resource Allocations, Budgets, Invoices, Revenue Recognition Configs, and Webhooks (guides).

## Workload per agent

| Agent | Scope | Sources |
|---|---|---|
| A. Product and PSA | Projects, templates, portal, resources, time, financials, reports | about 330 help articles (many short FAQs) and 22 blog posts |
| B. Data model and API | Objects, fields, endpoints, auth, pagination, webhooks | 103 developer entries |
| C. Integrations | Jira, Teams/Graph, Salesforce, HubSpot, Slack, Zapier, Workato, custom apps | 43 help articles, 5 blog posts, the Zapier listing, integration pages |
| D. Meeting Intelligence and Nitro | Meeting pipeline, Signals, AI Fills, agents, governance, MCP, credits | 32 help articles, 52 blog posts, 16 Nitro video pages (text only), beta policy |
| E. Technology evidence (REA) | Headers, front-end code, sub-processors, trust, status, careers | 16 sources plus REA observation of public pages |
| F. Verifier | Checks claims against cited URLs | The merged ledger |

Agent A is the largest. I propose it reads every non-FAQ article in full and skims FAQs and Video Academy pages only for entities and limitations.

## Notable observations so far

These are in the ledger, where each entry has its evidence type and confidence.

1. **No meeting, transcript, signal or AI endpoints appear in the public API index** (P1-004). If Phase 2 confirms this, Rocketlane's AI output may not be reachable through its API. That bears directly on your Elevate brief.
2. **Rocketlane documents its own MCP server** (P1-009). This is new scope for Agents C and D.
3. **The Teams integration is documented as part of Meeting Intelligence**, not as a general integration (P1-003).
4. **The blog index is incomplete.** Your two supplied posts aren't listed, so more relevant posts may exist that are only reachable through links (P1-006).
5. **The website sitemap points to a staging host** (P1-005). I recorded this and did not probe that host.

## Gaps and access limits

| Gap | Effect | Proposed handling |
|---|---|---|
| Sprinto trust centre returns 403 to plain requests | Possible security and hosting evidence missing | Retry with REA's browser tools in Phase 3 |
| LinkedIn blocks automated access | No LinkedIn job evidence | Use Kula careers instead |
| StackShare rate-limited (429) | Third-party stack profile missing | Retry once later; low-reliability source anyway |
| Videos (Nitro videos, YouTube, Academy) | Spoken content can't be used | Page text and published descriptions only, labelled as such |
| No logged-in access | In-app behaviour only from docs | Unchanged unless you approve a trial account |
| Help sitemap has 4 fewer articles than the crawl | Minor | Crawl list is the master list |

## Decisions needed before Phase 2

1. **Approve the agent assignments above**, including the proposal to skim FAQs and Video Academy pages for Agent A.
2. **Logged-in observation with a trial account:** off unless you say yes.
3. **Android app analysis:** off unless you say yes.
4. **Final output format:** Markdown in this folder, or a shared document or page.
