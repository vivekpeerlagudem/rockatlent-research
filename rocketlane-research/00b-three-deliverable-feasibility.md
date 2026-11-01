# Feasibility: three-deliverable architecture research

Assessed 2026-10-31 in this cloud session. **No research content was read.** Pages were loaded only to measure whether they're reachable and how much text can be extracted. Word counts include navigation and footer text, so they show that content can be extracted, not that it's complete.

---

## A. Environment and tool inventory

Every row was exercised in this session unless marked otherwise.

| Capability | Mechanism | Tested? | Result |
|---|---|---|---|
| Fetch static pages | `curl` through the session proxy (network: Full) | ✔ | Works on server-rendered sites. Bot-protected sites refuse it (support.monday.com: 403) |
| Render pages that need JavaScript, or that block plain requests | Pre-installed headless Chromium driven by Playwright scripts | ✔ | Works. It loaded support.monday.com, which refuses `curl`, and extracted 450 words |
| Follow links and enumerate a site | Sitemaps via `curl`; link extraction via Playwright | ✔ | Sitemaps found for Rocketlane, Kantata, GUIDEcx, Planhat and monday.com; Certinia's links extracted with the browser |
| Web search | `WebSearch` tool | ✔ (neutral query) | Works: returns titles, URLs and a summary. A search result is a lead, never evidence |
| Web reading through a subagent | `web-fetch` agent type | ✗ not retested | It failed earlier only because Rocketlane was blocked. I'll use `curl` and Playwright as the primary readers, so saved copies exist |
| REA web observation | `inspect_web_page`, `analyze_web_bundle`, `capture_browser_scenario`, `observe_web_session`, `inspect_web_network_capture` and others | ✔ on a local test page | Works. Useful only for observing a site's behaviour and technology, not for reading documentation |
| Read and search code | `Read`, `Grep`, `Glob`, `Bash` | ✔ (on the REA repo) | Works on any repository present on disk |
| Get a repository | `add_repo`, `list_repos`, `git clone` | ✔ | 7 repositories are accessible to this account. **None is Elevate or Kensium.** Nothing relevant is on disk |
| GitHub web pages and organisation API | `curl`, `gh` | ✔ | Organisation pages return 403. `gh` only works for repositories attached to this session. Public repositories can be cloned with `git`, though I haven't tried Certinia's |
| Diagrams | Mermaid text in Markdown | Not yet | Diagrams can be written. Rendered images aren't installed (`mermaid-cli` absent); rendering would need a published page |
| Structured reports | Markdown and CSV files | ✔ | `rocketlane-research/` already holds an inventory and an evidence ledger |
| Save and export | Local files; publishing an Artifact page; Claude Docs connector | Local files ✔; others available, not used yet | **This container is temporary and the folder isn't a git repository.** Final deliverables need a durable home: a published page or document, or a push to a repository you choose |
| Subagents | `Agent` tool | ✔ (used earlier) | They share this container's network and files, so they don't add access |

## B. Deliverable 1 (Rocketlane) feasibility

**Verdict: YES. Confidence: high** for a documentation-based functional and logical architecture.

**Basis:**
- The help centre has 410 articles, all inventoried. A sample article extracts 2,390 words, so content is in the page, not loaded by JavaScript.
- The developer docs have 103 entries, available as raw Markdown.
- Your supplied blog post is reachable.
- All 6 supplied help URLs and both supplied blog posts are reachable.

| Item | Verdict | Expected source |
|---|---|---|
| Modules and responsibilities | YES | 21 help categories, 87 folders |
| Central entities and relationships | YES (conceptual) | API reference: projects, phases, tasks, companies, spaces, time, allocations, budgets, invoices |
| Meeting Intelligence workflow | YES as documented | 11 Meeting Intelligence articles, including Teams |
| Capture, classification, transcription, AI extraction | PARTIAL | The user-visible behaviour is documented; any step not described will be UNKNOWN |
| Signals and delivery records | YES as documented | 6 Signals articles |
| AI Fills and Nitro agents | YES as documented | AI Fills, Documentation Agent, governance, credits and MCP articles; 52 relevant blog posts |
| Human approval points | PARTIAL | Only where the docs describe them. Gaps between blog claims and documented behaviour will be recorded as findings |
| Microsoft Teams / Microsoft 365 | YES as documented | The Teams article sits under Meeting Intelligence |
| Jira | YES | Jira articles plus Jira FAQs |
| CRM | YES | Salesforce (4) and HubSpot (1) articles |
| Documented limitations | YES | Whatever the vendor states; nothing more will be implied |

**Not accessible:**
- `app.rocketlane.com` needs a login, which isn't needed for this deliverable.
- The Sprinto-hosted trust centre returns 403 to plain requests; it needs browser retrieval.

## C. Deliverable 2 (competitive landscape) feasibility

**Verdict: PARTIAL. Confidence: medium.**

Four of the five vendors have reachable public help centres with readable articles. Certinia, the one central to the RAID question, splits its documentation between a public technical reference and a sign-in community. Its functional help and its Veda agent docs haven't been located yet.

| Vendor | Public docs reached | Readable sample | Login or gaps |
|---|---|---|---|
| **Certinia PSA and Veda** | Marketing site; developer.certinia.com (technical articles); **Technical Reference with per-product data dictionaries**: Professional Services Automation, PSA Core, PSA Direct for Jira, AI Core, Customer Success Cloud and more | Index pages load (38–149 words); **individual object pages not yet opened** | Community (`certinia.my.site.com`, `erp.force.com/community/login`) is sign-in only. `help.certinia.com` root is 404. Location of functional user guides and of Veda documentation is **unknown** |
| **Kantata** | Knowledge base (519 sitemap entries); API specification at developer.kantata.com | Article 1,485 words; API spec 3,174 words | Home page shows a sign-in prompt, so some articles may be restricted. The sitemap probably lists only public ones |
| **GUIDEcx** | Help centre (279 entries) | Article 1,368 words | API docs not located yet |
| **Planhat and Pi** | Help centre (465 entries) | Article 277 words | The developer page (100 words) looks sign-in-like. Pi documentation not located yet |
| **monday.com AI Notetaker** | Support centre (2,748 entries); developer docs (945 entries) | Support 288 words, through the browser only; developer article 1,183 words | Support refuses `curl` (403), so the browser is needed. The Notetaker article hasn't been located yet |

**RAID verification for Certinia:** feasible if the PSA data dictionary documents Risk, Issue, Action, Assumption, Decision and Dependency as objects with a lookup to Project. The dictionary for that product is public. Whether these objects appear in it is **not yet known**. If they only appear in community or marketing material, the finding is capped at VENDOR CLAIM or DOCUMENTED BEHAVIOUR.

**Marketing risk:** Veda, Pi and AI Notetaker may be documented mostly in marketing. Where no mechanism is documented, the gap itself will be reported as a finding.

## D. Deliverable 3 (new platform) feasibility

**Verdict: PARTIAL. Confidence: high** about what's missing.

| Part | Verdict | Reason |
|---|---|---|
| Inspect the Elevate repository | **NO** | No Elevate or Kensium repository is accessible. `list_repos` shows 7 repositories (Inventiglobe and personal ones), none matching. Nothing on disk. **I have read no Elevate code.** |
| Current architecture, data model, integrations, reusable parts, weaknesses, what not to carry forward | **NO until the repository is provided** | All require reading the code |
| Proposed architecture, entity relationships, agent workflows, integration boundaries, permissions, governance, audit model | **YES**, after deliverables 1 and 2 | This is design reasoning built on the evidence, labelled as proposal |

Once the repository is attached, the code analysis is **YES**. The tools are the standard ones: read and search the code, map database models, API routes and integration clients, and trace workflows. REA isn't needed for source code; its own guidance says so.

## E. Official documentation accessibility

| Source | Status | Method |
|---|---|---|
| help.rocketlane.com | ✅ public, 410 articles | `curl` |
| developer.rocketlane.com | ✅ public, 103 entries (raw Markdown) | `curl` |
| rocketlane.com blog, legal pages, trust page | ✅ public | `curl` |
| Rocketlane trust centre (Sprinto) | ⚠ 403 to plain requests | Retry with the browser |
| app.rocketlane.com | 🔒 login | Not needed |
| certinia.com, developer.certinia.com | ✅ public | `curl` and browser |
| Certinia Technical Reference | ✅ public index; object pages untested | Browser |
| Certinia Community | 🔒 sign-in | Not accessible |
| Certinia functional help and Veda docs | ❓ location unknown | Search and link-following |
| knowledge.kantata.com | ✅ public articles (some may be gated) | `curl` |
| developer.kantata.com | ✅ public API spec | `curl` |
| help.guidecx.com | ✅ public | `curl` |
| GUIDEcx API docs | ❓ not located | Search |
| help.planhat.com | ✅ public | `curl` and browser |
| Planhat developer docs | ⚠ sign-in-like landing page | Browser, then verify |
| Pi documentation | ❓ not located | Search |
| support.monday.com | ✅ via browser only (403 to `curl`) | Browser |
| developer.monday.com | ✅ public | `curl` |
| Public GitHub (Certinia and others) | ⚠ organisation pages 403; `git clone` of public repos expected to work | `git` |
| LinkedIn | ❌ blocks bots (999) | — |
| StackShare | ⚠ rate-limited (429) | Retry |

## F. Repository inspection capability

- **Capability:** yes. I can read, search and map any repository present in the session, and I can attach repositories this account can access.
- **Status:** no Elevate repository is available. Nothing about Elevate's code has been read, and nothing will be claimed about it until it is.
- **To fix:** give me the GitHub `owner/repo`.
  - If it's in an organisation, the Claude GitHub App must be installed on that repository by an organisation owner. Then I attach it, or you start a new session with it selected.
  - Alternatively, upload a zip of the code to this chat.

## G. Evidence collection and citation

| Requirement | How it's met |
|---|---|
| Direct URL for every finding | The ledger stores the source URL and retrieval date per finding |
| Proof of what was read | Raw HTML or Markdown of every page used is saved, with a SHA-256 hash. A finding without a saved source can't be graded CONFIRMED |
| Searching ≠ reading | Search results are recorded as leads. If only a title or listing was seen, the ledger says exactly that |
| Load ≠ extraction | Extracted text is checked for the article body, not just navigation. Pages that come back empty or are cut off get flagged |

**Classification rules:**

| Grade | Rule |
|---|---|
| CONFIRMED | The statement appears in an official page I saved and read |
| DOCUMENTED BEHAVIOUR | The vendor's documentation explains the mechanism: steps, triggers, inputs and outputs |
| VENDOR CLAIM | Marketing, a blog post or a video page asserts it without explaining the mechanism |
| INFERRED | My reconstruction, with the reasoning written down |
| UNKNOWN | Not public. Backend language, database, infrastructure and internal services stay UNKNOWN unless the vendor discloses them |

## H. Exact restrictions and causes

| # | What can't be done | Cause | Permanent? | What would help | Alternative | Still UNKNOWN after the fix |
|---|---|---|---|---|---|---|
| 1 | Read Elevate's code | Missing resource: no repository attached or accessible | No | `owner/repo` with GitHub access, or a zip upload | None. Deliverable 3's current-state analysis needs the code | Nothing. Runtime configuration and production data aren't needed |
| 2 | Read Certinia community content | Authentication (sign-in community) | Yes, for me | Exported or printed docs you're entitled to share; never a password | Technical Reference data dictionaries, developer articles, public release notes, AppExchange listing | Anything that exists only in the community |
| 3 | Locate Certinia functional help and Veda docs | Not yet found; may be gated | Not yet known | Search and link-following in Phase 1 | Data dictionary (objects, fields, relationships) and developer articles | Veda internals if only marketing describes them |
| 4 | Verify Certinia RAID records and their link to projects | Not yet checked | Not yet known | Open the PSA data dictionary object pages | Search the developer articles | If absent from the dictionary, a VENDOR CLAIM at best |
| 5 | Fetch monday.com support with `curl` | Website bot protection | No | — | Headless browser (works) | — |
| 6 | Pi, AI Notetaker and Veda mechanisms | Vendor information may be marketing-only | Partly | Public docs, if any exist | Help articles, API docs (e.g. monday GraphQL types for notetaker data, if exposed) | Models, prompts and orchestration for all vendors |
| 7 | Logged-in product behaviour (any vendor) | Authentication | No | Authorised trials. Not required for these deliverables | Documentation | Server-side internals |
| 8 | Watch demo videos and webinars | Tooling: no audio or video processing | Yes | Published transcripts | Page text and descriptions | Spoken-only content |
| 9 | Rendered diagram images | `mermaid-cli` not installed | No | Install it, or render on a published page | Mermaid source in Markdown | — |
| 10 | Keep outputs after the session ends | The container is temporary and the folder isn't a repository | No | A destination: repository, document or published page | Publish as I go | — |
| 11 | LinkedIn and StackShare | Bot block and rate limit | LinkedIn yes; StackShare no | — | Vendor careers pages, engineering blogs | Stack details only shared on LinkedIn |
| 12 | Kantata and Planhat restricted articles | Possible sign-in gating | Partly | Customer access you're entitled to | Public articles and API specs | Gated-only content |

**Even with every restriction fixed, these stay UNKNOWN for all vendors:** backend languages, databases, queues, cloud topology, AI models, prompts and agent orchestration, unless the vendor discloses them.

**What can still be reconstructed without them:** behaviour from the documented steps; entities and relationships from the API and data-dictionary schemas; event models from webhook and automation docs; integration contracts from integration guides and permission scopes; approval steps from the documented user flows.

## I. Additional resources or access required

| Need | Unlocks | Required? |
|---|---|---|
| **The Elevate repository** (`owner/repo` plus GitHub access, or a zip) | Deliverable 3's current-state analysis | **Yes, for Deliverable 3** |
| **Where to save the deliverables** (a repository, a shared document, or published pages) | Durable output | **Yes, before the work grows** |
| Certinia documentation you're entitled to share (exported PDFs from the community, if your organisation is a customer) | Gated Certinia functional docs | Optional |
| Authorised product trials | Observed behaviour beyond the docs | Optional; not needed for these deliverables |
| Approval to install `mermaid-cli` | Rendered diagram images | Optional |

No passwords or credentials are needed.

## J. Overall verdict and recommended sequence

| Deliverable | Verdict | Confidence |
|---|---|---|
| 1. Rocketlane | **YES** | High |
| 2. Competitive landscape | **PARTIAL**: four vendors well covered; Certinia RAID and Veda pending source location | Medium |
| 3. New platform | **PARTIAL**: design yes; repository analysis **NO** until the code is provided | High |

**Recommended sequence:**
1. **You:** provide the Elevate repository and choose an output destination.
2. **Deliverable 1:** read the 8 supplied Rocketlane sources first, then the linked NITRO, integration and API pages. The inventory already exists.
3. **Deliverable 2 source location:** find Certinia functional help, Veda and the RAID objects; locate GUIDEcx's API docs, Planhat developer docs and Pi; find monday.com's AI Notetaker articles. I'll report the inventory before the deep read.
4. **Deliverable 2 deep read:** one agent per vendor, all writing to the shared ledger, plus a verifier.
5. **Deliverable 3, current state:** read the Elevate code, focusing on its data model, integrations (Graph, Recall, Jira, Tempo), prompts and insight taxonomy.
6. **Deliverable 3, design:** the reference architecture, citing which Rocketlane and competitor patterns are borrowed or rejected, and why.
7. **Verification pass, then publish.**
