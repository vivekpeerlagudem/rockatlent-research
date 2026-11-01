# REA capability assessment: reconstructing Rocketlane's architecture

Assessed 2026-10-31 in this cloud session. Rocketlane has **not** been investigated. The only REA runs were against a local test page I built for this purpose.

## How this was tested

| Check | Result |
|---|---|
| REA version and connection | 6.8.0, MCP connected, 229 tools advertised; Ghidra and JADX available |
| Network | Full: www, help and developer.rocketlane.com all return 200 |
| Browser | Pre-installed Chromium 153 runs headless; REA attached to it |
| `inspect_web_page` on test page | Worked. Captured DOM, scripts and resources. Recorded **0 network requests**, because the page loaded before the observation window opened |
| `analyze_web_bundle` on test page | Worked. Found the module import and the route `/projects/:id/meetings`. **Missed** the API call `/api/v1/projects`, which goes through a wrapper function |
| `capture_browser_scenario` on test page | Worked. REA launched Chromium itself and captured every request from page load, **including** `/api/v1/projects?pageSize=10` |
| Packet and proxy helpers | `tshark`, `capinfos` and `mitmdump` are **not installed** |
| Rocketlane web app without login | `app.rocketlane.com` returns a 7 KB pre-login shell |

---

## A. Direct capability verdict

**Partially now; mostly yes with the resources in section G.**

I can produce an evidence-backed **logical** architecture of Rocketlane: functions, business entities, public API, integrations, the meeting and AI workflow as documented, the event model, and the security posture. That's enough for an engineering team to design a comparable platform independently.

I **cannot** produce Rocketlane's **physical** implementation: backend code, service decomposition, database engine and schema, queues, AI prompts, model routing, or infrastructure topology. No public surface exposes them, and no responsible method reaches them. This isn't an REA gap: the only way to get them would be unauthorised access.

### Verdict per area

| Area | Verdict | Reason and evidence required |
|---|---|---|
| Product functionality and modules | **YES** | 410 help articles in 21 categories are reachable and inventoried. Confirming what a user actually sees needs a trial account |
| Frontend architecture | **PARTIALLY** | Without login, only the 7 KB shell and marketing site can be observed. With a trial, REA can capture the app's scripts, code chunks, routes and library fingerprints. The code is presumably minified; whether source maps are published is unknown until checked |
| Backend logical architecture | **PARTIALLY** | Logical: reconstructable from 91 API reference pages, webhook docs and observed in-app API calls. Physical services: not observable, so any boundary is Inferred |
| Business components and service boundaries | **PARTIALLY** | Business components: yes, from docs. Deployment boundaries: inferable only from hostnames, URL prefixes and status-page components |
| API architecture | **YES** (public API) / **PARTIALLY** (internal app API) | The public REST API is documented: resources, pagination, search, custom fields, webhooks. The internal API the web app uses needs logged-in observation |
| Database and data model | **PARTIALLY** | Conceptual and logical model: yes, from API object schemas and field docs. Physical database (engine, tables, indexes, tenancy): **NO** — nothing outside the servers exposes it |
| Entity relationships | **YES** (conceptual) | From API resources and their ID references (projects, phases, tasks, companies, users, spaces, time entries, allocations, budgets, invoices). Exact cardinalities: partly |
| Authentication and authorisation | **PARTIALLY** | Documented: SAML SSO (7 articles), roles and permissions, API authentication. With a trial: login redirects and token shape on the client side. Server-side session and permission enforcement: not observable |
| Third-party integrations | **YES** (functional) / **PARTIALLY** (mechanism) | Documented: Jira, Salesforce, HubSpot, Slack, Zapier, Workato, Teams, custom apps, and the sub-processor list. OAuth scopes and sync design only as far as documented |
| Meeting capture and processing | **PARTIALLY** | 11 Meeting Intelligence articles plus the Teams article. Capture happens server-side, so the method (bot, transcript API or a recording vendor) is known only if documented or named in the sub-processor list. Live observation needs a trial with the feature enabled and a Microsoft 365 tenant |
| AI and agent architecture | **PARTIALLY** | Documented: Signals, AI Fills, Documentation Agent, governance, credits, Rocketlane MCP (30 articles, 52 blog posts, 16 video pages). Prompts, orchestration and model choice: not observable. The model provider is known only if disclosed, e.g. on the sub-processor page |
| Event-driven workflows | **PARTIALLY** | External event model: yes, from automations (19 articles) and webhooks (event types, payloads, delivery). Internal queues and message bus: not observable |
| Security and governance | **PARTIALLY** | Trust page, security PDF, DPA, sub-processors, responsible disclosure, SSO and permission docs. The Sprinto trust centre refuses plain requests (403); retry with the browser. Internal controls only as disclosed |
| Infrastructure and deployment | **PARTIALLY** (edge level only) | Observable: DNS, CDN and TLS, status-page components, and disclosed hosting providers and regions. Compute, orchestration and topology: not observable |
| Observable technology stack | **PARTIALLY** | Front end: framework and libraries from code fingerprints. Edge: from headers. Third-party services: from the domains pages load. Back end: **UNKNOWN** unless job posts or engineering content name it |

## B. REA tools actually available

These names come from the connected MCP server, and I ran the ones marked ✔.

| Capability | Tools | Notes |
|---|---|---|
| Website inspection | `inspect_web_page` ✔, `capture_web_screenshot`, `inspect_web_event_listeners`, `compare_web_screenshots` | Passive: attaches to a running page |
| Browser interaction | `capture_browser_scenario` ✔, `observe_web_session`, `list_browser_targets` ✔ | Only `capture_browser_scenario` performs actions (click, type, wait). `observe_web_session` records navigation a person performs during a time window |
| Front-end code analysis | `analyze_web_bundle` ✔, `compare_bundles`, `compare_source_to_bundle` | Parses code without running it. Finds code-chunk links, routes, endpoint candidates and library fingerprints |
| JavaScript extraction | `export_web_scripts`, `recover_javascript_sources`, `trace_web_source_location` | Readable sources only where source maps exist |
| Module and dependency analysis | `trace_web_module_imports`, `analyze_javascript_application`, `trace_javascript_semantics` | |
| Network traffic | `capture_browser_scenario` (network events) ✔, `observe_web_session`, `inspect_web_network_capture`, `compare_web_captures`, `compare_process_captures` | |
| HAR and SAZ files | `inspect_web_network_capture` | HAR 1.2 and Fiddler SAZ work now. mitmproxy files need `mitmdump`, which isn't installed |
| Packet captures | `inspect_pcap_capture`, `inspect_packet_capture`, `inspect_pcap_client` | **Unusable here**: `tshark` and `capinfos` are not installed |
| HTTP headers | `inspect_web_page` metadata; full HAR view in `inspect_web_network_capture` | **No dedicated header-fingerprint tool.** Live browser capture keeps only an allowlisted subset of headers, and never cookies or authorisation headers |
| API discovery | `analyze_web_bundle` (static candidates), `capture_browser_scenario` and HAR (observed calls), `discover_webmcp_tools`, `export_environment_bundle` | Static detection misses wrapped clients, as the test showed |
| Workflow capture | `capture_browser_scenario`, `observe_web_session`, `observe_web_execution`, `export_environment_bundle` | |
| Authenticated app inspection | `capture_browser_scenario` with declared secrets (read from environment variables) and storage seeds; or attaching to a browser a person already logged into | Needs credentials. Interactive SSO or MFA can't be completed headless here |
| Third-party service discovery | `inspect_web_page` (resource and script origins), `analyze_web_bundle` (library fingerprints) | |
| Desktop, mobile and binary tools | `inspect_android_package`, `decode_android_resources`, JADX and Ghidra tools, and more | Relevant only if you approve analysing the mobile app |

## C. What I can do now, without help

1. Read and extract all 410 help articles, 103 developer-doc pages, the relevant blog posts and the legal and trust pages, recording each finding with its evidence type.
2. Reconstruct the functional architecture, business workflows, conceptual entity model and public API architecture from the documentation.
3. Run REA on every **public** Rocketlane page:
   - marketing site
   - help and developer portals
   - status page
   - the app's pre-login shell
   - the Sprinto trust centre, through the browser

   This gives front-end technology fingerprints, third-party domains, routes visible before login and declared security headers.
4. Collect edge and stack evidence that doesn't need REA: DNS records, TLS certificates and raw response headers, using `curl -I`.
5. Read the sub-processor list, DPA, security PDF and careers posts on Kula for disclosed vendors and technologies.

## D. What I cannot do

| Item | Why | Permanent? |
|---|---|---|
| See backend code, services, database schema, queues, prompts or models | No public surface exposes them; reaching them would mean unauthorised access | **Permanent** |
| Observe the logged-in app or its internal API | Needs an account, which I don't have | Fixable with a trial account |
| Let you log in through a browser in this session | This cloud container has no display you can see. `observe_web_session` needs a person driving a browser | Permanent here; fixable on your laptop with HAR files |
| Watch videos | No audio or video processing; text only | Permanent; partly covered by published transcripts or descriptions |
| Read packet captures or mitmproxy files | `tshark` and `mitmdump` aren't installed | Fixable: I can install them here |
| Use LinkedIn or StackShare | LinkedIn blocks automated access (status 999); StackShare rate-limits (429) | LinkedIn: permanent. StackShare: retry later |
| Observe the meeting capture itself | It runs on Rocketlane's servers and Microsoft's, not in the browser | Permanent for the mechanism; results visible in the UI with a trial |

## E. Exact restrictions

| # | Restriction | Why it blocks | Affects | Permanent? | Alternative |
|---|---|---|---|---|---|
| R1 | `app.rocketlane.com` serves only a 7 KB pre-login shell; the product UI and its API calls are behind login | No product screens or internal API calls to observe | Frontend, internal API, auth flow, meeting and AI UI | No: needs a trial account | Docs and the public API reference |
| R2 | REA's passive browser tools deliberately don't navigate, type or run page code (documented non-goal). Only `capture_browser_scenario` performs actions | Multi-step workflows need scripted actions or a person | Workflow capture, frontend | No | Scripted scenarios with secrets; or HAR files you record on your laptop |
| R3 | Passive inspection records only during its window; page-load traffic is missed (shown in the test) | Missing early API calls | API architecture | No | `capture_browser_scenario` or HAR, which capture from the start |
| R4 | Static analysis misses API calls made through wrapper functions (shown in the test); the code is presumably minified | Incomplete endpoint list | API architecture | Partly | Combine with captured traffic; fetch source maps if Rocketlane publishes them |
| R5 | Live capture discards most response headers, and always cookies and authorisation headers | Less stack evidence from headers | Stack report | No | `curl -I` for public pages; full view of a HAR file |
| R6 | No public surface exposes database, services, queues, prompts or models | Physical architecture can't be observed | Backend, database, infrastructure, AI internals | **Yes** | Logical reconstruction from API schemas, webhook events, sub-processors and job posts, labelled Inferred |
| R7 | How well AI agents and human approval steps are documented is not yet known (pages not read) | Possible gaps in the agent model | AI architecture | Not yet known | Read the 30 NITRO articles; inspect the Rocketlane MCP server's tool list with a trial |
| R8 | Meeting Intelligence needs the feature enabled (it may be a paid add-on using Nitro credits), Microsoft 365 admin consent and real meetings | Can't observe the pipeline's inputs and outputs | Meeting sequence diagram | Partly | Docs; a trial plus a test Microsoft 365 tenant |
| R9 | LinkedIn blocks bots (999), StackShare rate-limits (429), Sprinto refuses plain requests (403) | Missing stack and security evidence | Stack, security | LinkedIn: yes. Others: no | Kula careers; StackShare retry; Sprinto through the browser |
| R10 | This session's REA is in the cloud. Your laptop's REA isn't connected to any agent, Claude Code isn't installed there, and Remote Control doesn't support Windows | I can't use your laptop's browser or files | Anything that needs a person to log in | No | Record HAR files on your laptop and upload them here |
| R11 | Videos can't be watched | Content from demos and talks is lost | AI, workflows | Yes | Page text, descriptions and published transcripts |
| R12 | Rocketlane's terms of service haven't been checked | Logged-in capture and code analysis may be restricted | All logged-in work | Not yet known | You review https://www.rocketlane.com/legal/terms before logged-in work |
| R13 | Receiving real webhook payloads needs a public endpoint; this container has no public inbound address | Can't capture live webhook events | Event model | Partly | Payload examples in the docs; a trial plus a tunnel or request-catcher service |
| R14 | `tshark`, `capinfos` and `mitmdump` aren't installed | Packet and mitmproxy files can't be read | Network evidence | No | Install here, or use HAR instead |

## F. Deliverable feasibility

✅ = yes with current access · 🟡 = yes once a trial account and HAR files are provided · 🔶 = logical or inferred only · ❌ = not achievable

| # | Deliverable | Feasible | Evidence required | Logical or physical |
|---|---|---|---|---|
| 1 | Product architecture | ✅ | Help centre, marketing pages, pricing | Logical |
| 2 | Functional architecture | ✅ | 410 help articles, API resources | Logical |
| 3 | System context | ✅ | Integrations, sub-processors, user roles, external systems | Logical (C4 level 1) |
| 4 | Frontend architecture | 🟡 | Logged-in bundle analysis and routes; public shell now | Observed client-side structure |
| 5 | Backend logical architecture | 🔶 | API reference, observed internal API, webhook events | Logical only; service split Inferred |
| 6 | Component architecture | 🔶 | Grouping of API resources, URL prefixes, hostnames | Inferred |
| 7 | API architecture | ✅ public / 🟡 internal | Developer docs; HAR or scenario capture | Observed and documented |
| 8 | Integration architecture | ✅ | Integration docs, Zapier listing, sub-processors, MCP docs | Documented behaviour |
| 9 | Database conceptual architecture | 🔶 | API object schemas, custom-field docs | Conceptual only; physical ❌ |
| 10 | ER diagrams | ✅ conceptual | API ID references | Conceptual |
| 11 | Meeting Intelligence sequence | 🔶 / 🟡 | Meeting Intelligence docs; trial with Microsoft 365 for the visible steps | Documented, with server steps Inferred |
| 12 | AI agent architecture | 🔶 | NITRO docs, MCP tool list, governance and beta policy | Documented behaviour; internals ❌ |
| 13 | Data-flow diagrams | 🔶 | Integration, webhook and meeting docs; captured traffic | Logical |
| 14 | Security architecture | 🔶 | Trust page, security PDF, DPA, SSO and permission docs, response headers | Disclosed posture; internals ❌ |
| 15 | Deployment and infrastructure | 🔶 (edge only) | DNS, TLS, CDN, status page, disclosed hosting | Mostly UNKNOWN beyond the edge |
| 16 | Technology stack report | ✅ observable parts | Code fingerprints, headers, third-party domains, job posts, sub-processors | Observed; back end mostly UNKNOWN |
| 17 | Complete HLD | 🔶 | All of the above | A reference design labelled by evidence type, **not** Rocketlane's actual HLD |

## G. Additional resources required from you

| Resource | What it unlocks | Fixes | Required? |
|---|---|---|---|
| **Your confirmation that Rocketlane's terms allow this** (https://www.rocketlane.com/legal/terms) | Permission to do logged-in capture and code analysis | R12 | **Yes, before any logged-in work** |
| **An authorised trial or sandbox account**, ideally a throwaway workspace with Nitro and Meeting Intelligence enabled, and no SSO or MFA (or a test identity provider) | Logged-in UI, internal API, app code, permission behaviour, AI and meeting screens, the Rocketlane MCP tool list | R1, R2, R7, R8 | Strongly recommended |
| **HAR files** recorded on your laptop while you walk through set workflows (I'll provide the script) | Exact request sequences, payload shapes, internal endpoints; full headers | R3, R4, R5, R10 | Recommended |
| **A test Microsoft 365 tenant** with admin rights, plus a test Jira site | Observing Teams meeting capture and Jira sync from both ends | R8 | Optional; high value for the meeting diagram |
| **Screenshots or screen recordings** of AI and meeting screens, if a trial isn't possible | Visual evidence of AI output and the approval steps | R1, R7 | Fallback |
| Approval to install `tshark` and `mitmproxy` here | Packet and mitmproxy captures | R14 | Optional; HAR covers most needs |
| Approval to analyse the Android app | Mobile code, endpoints, libraries | — | Optional; check its terms first |
| Human review by your architects | Judging Inferred items and choosing between options | — | Recommended at the gap review |

**Not needed:** your personal or company credentials, customer data, or anything confidential. A throwaway trial account is enough. If credentials are provided, they go into environment variables for the scenario tool and are never written to files or reports.

## H. Proposed solutions

1. **Logged-in access:** a trial account, used through `capture_browser_scenario` with declared secrets. Where SSO or MFA blocks headless login, you record HAR files on your laptop instead and upload them.
2. **Workflows:** I write a capture script for each workflow, e.g. create project → add phase and task → log time → open meeting summary → accept an AI suggestion. You either let REA run it with the trial account, or follow it on your laptop while recording a HAR file.
3. **API completeness:** combine three sources: the public API reference (documented), code analysis (static candidates) and captured traffic (observed). Each endpoint gets a coverage tag.
4. **Stack evidence:** REA code fingerprints, plus `curl -I`, DNS and TLS checks, plus sub-processors and Kula job posts. Anything unproven is recorded as UNKNOWN.
5. **AI architecture:** read the NITRO docs, then connect the Rocketlane MCP server with the trial account to list its tools and schemas. That is strong, first-hand evidence of what AI and external agents can read and write.
6. **Meetings:** docs first. With a trial and a test Microsoft 365 tenant, run one internal Teams meeting and record what appears in Rocketlane and when.
7. **Missing tools:** install `tshark` and `mitmproxy` only if you want packet-level evidence.

## I. Recommended execution plan

| Phase | Work | Needs from you | Output |
|---|---|---|---|
| 0 | Done: source inventory and this assessment | — | `01-source-inventory.md` |
| 1 | Read the documentation (subagents A–D) | Approval | Evidence ledger: functions, API, integrations, AI |
| 2 | REA on public pages, `curl -I`, DNS and TLS, sub-processors, careers (subagent E) | Approval | Stack evidence (public) |
| 3 | Gap review | You review the gaps | Decide which gaps a trial would close |
| 4 | Logged-in capture: scenarios or HAR files, MCP tool list, meeting test | Terms confirmed, trial account, optionally Microsoft 365 | Observed internal API, front end, AI and meeting behaviour |
| 5 | Verification (subagent F) | — | Verified ledger |
| 6 | Architecture deliverables 1–17 | Review | Diagrams and HLD, every element tagged Documented, Observed or Inferred |

Phases 1–2 need nothing beyond your approval.

## J. Honest conclusion

- **With the current setup:** I can deliver about two-thirds of the reference architecture to a standard an engineering team can use. That covers the functional model, conceptual data model, public API, integrations, the documented AI and meeting behaviour, the security posture, and the public stack evidence.
- **With a trial account, HAR files and optionally a test Microsoft 365 tenant:** the front end, internal API, logged-in workflows, AI approval steps and the visible meeting pipeline move from inferred to observed. That makes the reference strong enough to design a comparable platform from.
- **Not at all, with any resources:** Rocketlane's private backend code, database schema, service layout, AI prompts and models, and infrastructure. These will appear as UNKNOWN or clearly labelled reconstructions, never as findings.

**Answer to your question in section 6:** Yes. With the product URL, official documentation, public technical material and authorised access, I can reconstruct a detailed enough **logical** architecture for an engineering team to design a comparable SaaS platform independently. It will not be Rocketlane's actual implementation, and the report will mark the difference on every element.
