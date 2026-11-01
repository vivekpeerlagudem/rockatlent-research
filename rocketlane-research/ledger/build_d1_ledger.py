"""Builds ledger/d1-evidence-ledger.csv for Deliverable 1 (Rocketlane).
Each row: finding, grade, confidence, source URL(s), verbatim quote(s) from the saved source.
Multiple URLs or quotes are separated by ' || '. Retrieval dates are filled from sources/manifest.csv.
Run: python3 -I build_d1_ledger.py
"""
import csv, os
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
H = 'https://help.rocketlane.com/support/solutions/articles/'
D = 'https://developer.rocketlane.com/'
MI = H + '67000739897-enabling-meeting-intelligence-in-rocketlane-for-admins-'
AIF = H + '67000747155-how-to-use-ai-fills'
SIG = H + '67000753773-introduction-to-signals-in-rocketlane'
TEAMS = H + '67000740226-connect-microsoft-teams-to-rocketlane'
JIRA = H + '67000701085-getting-started-with-rocketlane-s-jira-integration'
NPT = H + '67000755212-configuring-nitro-page-templates'
AIMM = H + '67000753317-rocketlane-ai-for-interaction-data-mental-model-and-behavior'
MATCH = H + '67000755648-how-rocketlane-matches-meetings-to-customers'
DA = H + '67000755211-documentation-agents-in-rocketlane'
CDA = H + '67000755213-creating-a-documentation-agent'
NP = H + '67000755214-creating-and-managing-nitro-pages-in-rocketlane'
EMAIL = H + '67000753774-email-intelligence-how-email-ingestion-works'
MPT = H + '67000753775-meeting-page-templates'
KB = H + '67000753781-setting-up-your-company-knowledge-base'
RBAC = H + '67000755650-configure-role-based-access-for-meeting-and-email-intelligence'
TSP = H + '67000755077-timesheet-policies-in-rocketlane'
MCP = H + '67000754589-guide-to-using-rocketlane-mcp-tools'
CRED = H + '67000755370-nitro-credit-consumption'
EXCL = H + '67000757523-excluding-meetings-and-emails-from-capture'
IDOM = H + '67000757522-managing-internal-domains-for-meetings-and-emails'
GONG = H + '67000739828-integrating-the-gong-app-to-your-rocketlane-account'
ZOOM = H + '67000739674-adding-the-zoom-app-to-your-rocketlane-account'
GMEET = H + '67000740155-adding-the-google-meet-app-to-your-rocketlane-account'
SHEETS = H + '67000748152-introduction-to-sheets-in-rocketlane'
ACC = H + '67000734659-setting-up-and-managing-accounts'
SF = H + '67000711953-getting-started-with-the-rocketlane-salesforce-integration'
SFMAP = H + '67000747098-salesforce-to-rocketlane-opportunity-to-projects-mapping-psa-best-practices-'
HUB = H + '67000715492-rocketlane-s-integration-for-hubspot'
SLACK = H + '67000696056-how-to-get-started-with-rocketlane-s-integration-for-slack-'
RAI = H + '67000724508-how-to-use-resource-ai-to-optimize-resource-allocation-'
PCREATE = H + '67000694722-how-to-create-a-rocketlane-project-'
PSET = H + '67000700077-project-settings'
PLAN = H + '67000699280-project-plan'
TASKS = H + '67000699662-basics-of-project-tasks'
SPACES = H + '67000701003-what-are-spaces-'
APPR = H + '67000732734-how-to-manage-approvals-for-tasks-and-documents'
WH = D + 'docs/webhooks-overview.md'
WHP = D + 'docs/event-payload.md'
WHD = D + 'docs/webhook-delivery.md'
GETP = D + 'reference/get-project.md'
GETT = D + 'reference/get-task.md'
GETTE = D + 'reference/get-time-entry.md'
GETINV = D + 'reference/get-invoice.md'
GETRA = D + 'reference/get-all-resource-allocations.md'
GETSP = D + 'reference/get-space.md'
GETC = D + 'reference/get-company.md'
BGOV = 'https://www.rocketlane.com/blogs/nitro-governance-agents'
BRAID = 'https://www.rocketlane.com/blogs/raid-management'

C, DB, VC, INF, UNK = 'CONFIRMED', 'DOCUMENTED BEHAVIOUR', 'VENDOR CLAIM', 'INFERRED', 'UNKNOWN'
J = ' || '

# id, area, finding, grade, confidence, urls, quotes, reasoning/notes, unknowns
ROWS = [
# ---------------- Modules and central entities ----------------
('D1-001', 'Entities', 'The Account is documented as the central container for AI and interaction data: it houses projects and customer interactions.', C, 'High', AIMM,
 'At its core, Rocketlane organizes your work around the Account.' + J + 'An Account acts as the primary container. It houses one or more Projects, representing the specific work being delivered, alongside all associated customer interactions.', '', ''),
('D1-002', 'Entities', 'In the public API the customer organisation is a "company" resource; a project carries one customer company and optional partner companies.', C, 'High', GETP,
 '"customer"' + J + '"partnerCompanies"', 'Field names taken from the OpenAPI response schema of Get project by Id.', 'Whether the API "company" and the UI "Account" are the same stored object is not stated (see D1-003).'),
('D1-003', 'Entities', 'The UI "Account" and the API "company" are very likely the same object.', INF, 'Medium', GETC + J + ACC,
 '', 'The API company carries an accountOwner field (Get company by Id schema), and the Accounts article states an account can be created "by simply adding the customer information while creating a project", which is the same step that selects the project customer company. The docs never state the equivalence explicitly.', 'Exact identity of Account vs Company storage.'),
('D1-004', 'Entities', 'A project is created for a customer, optionally from one or more templates, with an owner, status, start and due dates, team members and a customer champion.', DB, 'High', PCREATE,
 'Select a Customer name .' + J + 'Use Add another template to combine phases from multiple templates if needed.' + J + 'You can also assign the role of Champion and invite members from the customer\'s team by providing their email addresses.', '', ''),
('D1-005', 'Entities', 'Projects are divided into phases; phases contain tasks; tasks can have subtasks, dependencies, milestones and an at-risk flag.', C, 'High', PLAN + J + TASKS,
 'Rocketlane projects are divided into phases for easier planning and execution.' + J + 'Each project phase consists of tasks, which make it easier to delegate resources and manage the project in detail.' + J + 'Mark as \'At risk\' / Remove \'At risk\' Flags the task as at risk, or removes the flag.', '', ''),
('D1-006', 'Entities', 'The task API object links to project, phase, parent task, dependencies, assignees (members and placeholders), followers, budgets and revenue-recognition details.', C, 'High', GETT,
 '"phase"' + J + '"parent"' + J + '"dependencies"' + J + '"placeholders"' + J + '"revenueRecognitionDetails"', 'Field names from the Get task OpenAPI schema.', ''),
('D1-007', 'Entities', 'Time entries link to a user, task, project phase, project, budget and category, with approval fields (submittedBy, approvedBy, rejectedBy) and bill and cost rates.', C, 'High', GETTE,
 '"projectPhase"' + J + '"approvedBy"' + J + '"rejectedBy"' + J + '"billRate"' + J + '"costRate"', 'Field names from the Get time entry OpenAPI schema.', ''),
('D1-008', 'Entities', 'Resource allocations link a member or placeholder to a project, budget and tasks.', C, 'High', GETRA,
 '"member"' + J + '"placeholder"' + J + '"budget"', 'Field names from the Get all resource allocations schema.', ''),
('D1-009', 'Entities', 'Invoices link to a company, one or more projects and budgets, with line items and payments.', C, 'High', GETINV,
 '"company"' + J + '"projects"' + J + '"budgets"', 'Field names from the Get invoice schema.', ''),
('D1-010', 'Entities', 'Spaces belong to a project and hold documents (private or shared with the customer).', C, 'High', GETSP + J + SPACES,
 '"project"' + J + 'Private Spaces Allows you to privately share documents within your team without involving the customer\'s team.', '', ''),
('D1-011', 'Entities', 'Approvals exist for tasks and documents, with an approver, due date and a private or shared flag.', DB, 'High', APPR,
 'In the approval pane, mark the approval as private or shared with customers.' + J + 'If you want to request changes to the task, click Change required and add your comments.', '', ''),
('D1-012', 'Entities', 'The help centre documents RAID logs as a use case of Sheets, a generic project-scoped table built from a sheet template (example template name "RAID Log"); "Risk registers" is also listed as a Sheets use case.', C, 'High', SHEETS + J + H + '67000754878-rocketlane-sheets-shortcuts-tips',
 'RAID logs' + J + 'Give your template a descriptive name (for example, "RAID Log").' + J + 'Project-scoped Information is specific to that project, so you always know exactly where to find the data without unnecessary hunting.' + J + 'Risk registers',
 '', ''),
('D1-015', 'Entities', 'No dedicated RAID object (a typed Risk / Assumption / Issue / Dependency record) is documented; RAID is handled through Sheets (D1-012) and, for AI-maintained risk lists, the Nitro Record Block (D1-053).', INF, 'High', SHEETS + J + NPT,
 '', 'Absence claim. Searched all 410 saved help articles: "RAID" occurs only in three Sheets articles; risk logs appear as Sheets use cases and as a Nitro Record Block example ("a running risks log"). No article, API resource or MCP tool defines a RAID entity.', 'Whether an unpublished native RAID object exists.'),
('D1-013', 'Entities', 'Marketing describes RAID items as structured objects inside the project, linked to the tasks they affect, with the project plan reflecting overdue dependencies automatically.', VC, 'High', BRAID,
 'The platform keeps RAID items inside the project as structured objects linked to the tasks they affect.' + J + 'When the dependency is overdue, the project plan reflects it automatically.', 'Partly backed: Sheets offer a "Task link" column (D1-016), but no documented mechanism makes the project plan react to a RAID row automatically.', 'Whether Sheet rows affect the project plan.'),
('D1-016', 'Entities', 'Sheets support a "Task link" column type: a URL to a task in the current project.', C, 'High', SHEETS,
 'Task link Allows a URL to a task that exists within the current project.', 'A URL column, not a documented structured relationship with plan effects.', ''),
('D1-014', 'Entities', 'Sheets, meetings, signals, AI pages and Nitro pages have no resource in the public REST API reference as saved.', INF, 'High', D + 'docs/overview.md',
 '', 'Absence established by parsing the 79 endpoints of the saved API reference (analysis/api-endpoints.csv). The inventory is known to be incomplete: the Companies reference mentions an "Addresses API" that has no saved reference page, so other unlisted resources are possible.', 'Private or unlisted endpoints.'),
# ---------------- Meeting pipeline ----------------
('D1-020', 'Meetings: capture', 'Meetings are captured from cloud recording sources (Gong, Zoom, Microsoft Teams, Google Meet) or by the Rocketlane AI Notetaker, and the sources are additive.', DB, 'High', MI,
 'Receives recordings from Gong, Zoom, Microsoft Teams, Google Meet, or the Rocketlane AI Notetaker.' + J + 'The sources are additive and do not require an account-wide choice between one recorder and another.', '', ''),
('D1-021', 'Meetings: capture', 'Eligible recordings from cloud sources are retrieved after the meeting ends through each provider API; no bot is needed, and participants do not need Rocketlane licences solely for recording ingestion.', DB, 'High', MI + J + GONG + J + ZOOM + J + GMEET,
 'Rocketlane retrieves completed recordings and transcripts directly from connected providers after a meeting ends.' + J + 'Rocketlane matches and retrieves eligible recordings through the provider\'s API.' + J + 'No Rocketlane bot is required for Gong recording retrieval.' + J + 'No Rocketlane bot is required for cloud recording retrieval.', '', 'Polling interval or event subscription used for retrieval; latency.'),
('D1-022', 'Meetings: capture', 'The AI Notetaker joins scheduled Zoom, Teams or Meet calls as a participant; each host needs a licence and a connected Google or Outlook calendar.', DB, 'High', MI,
 'The Rocketlane AI Notetaker joins scheduled Zoom, Microsoft Teams, or Google Meet calls as a meeting participant and records them.' + J + 'Connect their Google Calendar or Outlook calendar to Rocketlane.', '', 'Notetaker implementation and vendor.'),
('D1-023', 'Meetings: Teams', 'Teams recordings and transcripts are retrieved through Microsoft Graph with tenant admin consent and a Teams application access policy.', DB, 'High', TEAMS,
 'Rocketlane retrieves eligible completed meeting recordings and transcripts from the connected Microsoft tenant through Microsoft Graph.' + J + 'Grant administrator consent to complete the connection.' + J + 'Microsoft requires an application access policy before applications using application permissions can access certain online meeting recordings and transcripts.', 'The docs place the integration in Microsoft\'s application-permission (not delegated) model; permission names are not given.', 'Exact Graph permission names; whether change-notification subscriptions or polling are used.'),
('D1-024', 'Meetings: Teams', 'Teams retrieval covers users in the tenant covered by the access policy, including non-Rocketlane users and ad hoc meetings not on a connected calendar.', DB, 'High', TEAMS,
 'These users do not need to be Rocketlane team members.' + J + 'Cloud retrieval can include eligible ad hoc meetings.', '', ''),
('D1-025', 'Meetings: Teams', 'Which Microsoft Graph mechanism is used (change-notification subscriptions or polling) and which Graph permissions are requested are not documented.', UNK, 'High', TEAMS,
 '', 'Teams article read in full: it names Microsoft Graph, admin consent, application permissions and the application access policy, but not subscription type, permission names or retrieval frequency.', ''),
('D1-026', 'Meetings: duplicates', 'When the same meeting arrives from more than one source the docs say Rocketlane "handles" it, but the de-duplication method is not described.', UNK, 'High', MI,
 '', 'Admin article says: "If the same meeting is received from more than one source, Rocketlane handles the recordings without requiring you to disable either source." No mechanism given.', 'De-duplication key and which copy is kept.'),
('D1-027', 'Meetings: classification', 'Participants are classified internal or external; a meeting with at least one external participant is a customer meeting.', DB, 'High', MI,
 'Rocketlane classifies meeting participants as internal or external.' + J + 'A meeting is treated as a customer meeting when it includes at least one participant who is not recognized as an internal team member or partner.', '', ''),
('D1-028', 'Meetings: matching', 'Customer matching runs three exact steps in order (exact email, contact domain, company website) and leaves a meeting unassociated rather than guessing.', DB, 'High', MATCH,
 'Rocketlane evaluates three exact matching methods in order. It stops when it identifies one customer company.' + J + 'Rocketlane does not use fuzzy company-name matching.', '', ''),
('D1-029', 'Meetings: matching', 'Documentation inconsistency: the admin and Teams articles list company names as a matching input, while the matching article says fuzzy company-name matching is not used.', C, 'High', MI + J + TEAMS + J + MATCH,
 'Rocketlane uses participant emails, contact domains, company websites, and company names to identify the appropriate company.' + J + 'Rocketlane matches historical meetings using available customer contacts, participant domains, company website information, and company names.' + J + 'Rocketlane now uses only exact email, contact-domain, and company-website matches.', 'Recorded as a finding; the dedicated matching article is the more specific source. A third variant: the Signals article links transcripts to accounts by project membership or domain matching against Account domain fields (D1-045 source), which also differs from the three-step method.', 'Whether exact (non-fuzzy) company-name comparison is used anywhere; whether Signals and meeting pages use the same matching.'),
('D1-030', 'Meetings: pages', 'A meeting page is created for every captured meeting, including internal or unmatched meetings.', C, 'High', MI,
 'Creates a meeting page for every captured meeting, including meetings that are not associated with a customer.', '', ''),
('D1-031', 'Meetings: pages', 'Meeting pages are generated from meeting page templates selected by account and meeting field conditions, first match wins.', DB, 'High', MPT,
 'Templates follow first-match logic.' + J + 'Choose from Account fields (for example ARR, MAU, Billing Cycle) or Meeting fields (for example Meeting Type, Participants).', '', ''),
('D1-032', 'Meetings: transcript', 'Meetings and emails are normalised into a common transcript object that feeds the AI pipeline.', DB, 'High', AIMM,
 'Rocketlane AI treats different interaction sources (meetings and emails) as a common transcript object that the pipeline can process consistently.', '', 'Transcript schema and storage.'),
('D1-033', 'Meetings: project link', 'Transcripts are currently associated only with accounts, not projects; by default meetings and signals are not associated with projects, and association to a project is manual.', C, 'High', SIG + J + MPT,
 'Transcripts are currently associated only with accounts, not projects.' + J + 'By default, meetings are not associated with projects. You must manually associate meetings to projects.', 'Tension: the matching article says a matched meeting "appears in the customer’s meeting history and relevant project context", without explaining how project context is determined.', 'How "relevant project context" is derived.'),
('D1-034', 'Meetings: history', 'When enabled, historical retrieval runs for cloud sources on triggers such as creating a customer company; the new-customer lookback is capped at 30 days.', DB, 'High', MI,
 'Enable the setting.' + J + 'The retrieval period used for a newly created customer is limited to the configured period, up to 30 days.' + J + 'Historical retrieval applies only to connected cloud recording sources.', '', ''),
('D1-035', 'Meetings: exclusions', 'Exclusions by person, domain or keyword skip meetings and emails before capture, and apply only going forward.', DB, 'High', EXCL,
 'Rocketlane’s recorder does not join, and the meeting is not processed.' + J + 'Exclusions apply only to new meetings and emails.', '', ''),
('D1-036', 'Email', 'Email Intelligence ingests per-user authenticated inboxes at thread level, skips internal-only threads, and shows a thread only if it maps to an existing account (typically via CRM-synced contacts and domains).', DB, 'High', EMAIL,
 'Each team member must individually connect their inbox to Rocketlane.' + J + 'A thread only becomes visible in Rocketlane if the system can successfully map an external domain or individual contact to an existing account.' + J + 'This mapping typically depends on your CRM integrations, such as Salesforce or HubSpot', '', 'Mail provider APIs and permissions requested.'),
# ---------------- AI layer ----------------
('D1-040', 'AI: AI Fills', 'An AI Fill combines selected meetings, a template (Summary, Action Items or Extract Information) and an output location (project update, document or chat).', DB, 'High', AIF,
 'An AI Fill combines three elements:' + J + 'Under Generate As , select Summary , Action Items , or Extract Information .', '', ''),
('D1-041', 'AI: AI Fills', 'AI Fills is user-invoked: a user types / in an editor, picks a template and meetings, generates, and reviews before publishing.', DB, 'High', AIF,
 'Type / to open the insert menu.' + J + 'Review and edit the result before publishing or sharing it.', '', ''),
('D1-042', 'AI: AI Fills', 'Human gate: AI Fill output is placed into a draft (update, document or chat) that a person reviews and publishes; the docs instruct review before sharing or updating records.', DB, 'High', AIF,
 'AI-generated content should be reviewed before it is shared with customers or used to update project records.' + J + 'Publish or send the project update.', '', ''),
('D1-043', 'AI: AI Fills', 'AI Fills does not automatically write extracted values back to the project field used for its choices.', C, 'High', AIF,
 'AI Fills does not automatically update the field.' + J + 'It does not automatically write the generated answer back to that field.', '', ''),
('D1-017', 'AI: AI Fills', 'AI Fills action items are generated as content, not as task records; no documented in-product path converts them into tasks.', INF, 'Medium', AIF,
 '', 'Absence claim. The AI Fills article describes action items only as generated text placed in updates, documents or chat ("Review generated ownership and due-date information before sharing or acting on it"); no passage describes creating tasks. The only documented task-creation path from meeting notes is MCP via an external assistant (D1-072).', 'Whether an unpublished feature converts AI action items into tasks.'),
('D1-044', 'AI: Signals', 'Signals classify interaction insights as Risk, Opportunity or Operational, with reason code, description, citations, date and the people who raised it.', C, 'High', SIG,
 'Signals are classified into three broad types:' + J + 'Citations: Excerpts or references from the transcript', '', ''),
('D1-045', 'AI: Signals', 'Signal pipeline: a new transcript triggers detection; it must link to a customer account; filters gate eligibility; the AI evaluates conditions; on a match a signal occurrence is created.', DB, 'High', SIG,
 'The process triggers immediately whenever a new transcript - whether from a recorded meeting or a synced email thread - arrives in the system.' + J + 'Conditions act as a gate - if a transcript is not eligible, Rocketlane does not run detection for it.' + J + 'If the AI confirms a match, a signal occurrence is created and surfaced directly in your Signals UI.', '', 'Models used; prompt structure; batching.'),
('D1-046', 'AI: Signals', 'Signal definitions are authored in natural language with Nitro AI, refined via clarifying questions, compiled into instructions, filters and positive and negative examples, and tested on a chosen transcript before creation.', DB, 'High', SIG,
 'Rocketlane asks clarifying questions before finalizing the configuration to narrow down the specifics.' + J + 'Select the transcript source: Meetings or Emails .', '', ''),
('D1-047', 'AI: Signals', 'Human gate for signals sits at definition time (a user with signal-configuration permission reviews and tests the generated configuration); signal occurrences are raised automatically, and there is currently no mechanism to automatically resolve or close a signal.', DB, 'High', SIG,
 'After testing, proceed to create the signal if it is satisfactory, or continue to tweak it in the chat window.' + J + 'There is currently no mechanism to automatically resolve or close a signal once it is raised.', '', 'Whether users can manually close signals (only "hide" is documented).'),
('D1-048', 'AI: Signals', 'Business context for signal interpretation comes from a knowledge base built from AI pages, API docs, websites or uploaded files.', DB, 'High', KB + J + SIG,
 'AI pages (information derived from transcripts)' + J + 'This context is sourced from a knowledge base.', '', ''),
('D1-049', 'AI: pages', 'AI pages is the umbrella for meeting pages (per meeting), email pages (per thread) and Nitro pages (per document).', C, 'High', AIMM,
 'AI pages is the umbrella term for structured AI-extracted content.', '', ''),
('D1-050', 'AI: Documentation Agent', 'A Documentation Agent binds a Nitro page template to sources (meetings and/or emails filtered by template), optional input fields, knowledge bases and a trigger (Manual or On event).', DB, 'High', CDA,
 'A Documentation Agent connects a Nitro page template to selected sources, knowledge bases, and a trigger.' + J + 'Runs the agent automatically based on account field conditions.', '', ''),
('D1-051', 'AI: Documentation Agent', 'With "Living document" enabled, the generated document updates continuously from new matching calls and emails, with no documented approval step.', DB, 'High', CDA + J + NP,
 'The document updates continuously using subsequent calls and emails that match the configured criteria.' + J + 'the page will automatically update itself with new meetings and emails as they occur.',
 'Read both Documentation Agent articles and the Nitro Pages article in full: review aids are citations, sources panel, manual edit and Answer History; none is described as an approval gate.', 'Whether updates are staged anywhere before publishing.'),
('D1-052', 'AI: Documentation Agent', 'Nitro pages are saved under the Account (Accounts > Nitro pages tab), not under a project.', DB, 'High', NP,
 'Generated Nitro pages are saved under the account.', '', ''),
('D1-053', 'AI: Documentation Agent', 'Nitro page templates include a Record Block for structured records that persist and update across meetings, such as a running risks log.', C, 'High', NPT,
 'The Record Block is similar to Table Details but is designed for structured records that persist and update across meetings, such as a running risks log or open issues list.',
 '', 'Whether Record Block rows are queryable records elsewhere (API, MCP, reports) or exist only inside the Nitro page.'),
('D1-054', 'AI: Documentation Agent', 'Marketing says the Documentation Agent creates draft RAID entries for PM review and one-click confirmation.', VC, 'High', BRAID,
 'The Documentation Agent ingests meeting transcripts and identifies new RAID items, populating draft entries for PM review and one-click confirmation.',
 'No help article describes draft RAID entries or a confirmation step (see D1-051, D1-012). The gap between claim and documented mechanism is itself a finding.', ''),
('D1-055', 'AI: governance', 'Timesheet Governance agent: natural-language policies compile into Flag for review, Block creation or Block submission rules, evaluated as time is logged, testable in a sandbox, and forward-looking only.', DB, 'High', TSP,
 'Timesheet Policies are part of Rocketlane’s Timesheet Governance agent, available under Nitro AI capabilities.' + J + 'A Block creation policy prevents a time entry from being saved if it violates the rule.' + J + 'Existing entries are not retroactively flagged or blocked. Policies are forward-looking.', '', ''),
('D1-056', 'AI: governance', 'Marketing says Governance Agents block non-compliant project actions such as stage gates, out-of-sequence task completion and project closure with open invoices.', VC, 'High', BGOV + J + BRAID,
 'When something violates a policy, the agent doesn\'t just flag it. It blocks the action, explains exactly what needs attention, and tells the person what to do next.' + J + 'The agent blocks the action and surfaces the gap in real time.',
 'Help centre has one Policies and Governance article and it covers timesheets only; "project governance" returns no help article.', 'Project-level governance mechanism.'),
('D1-057', 'AI: governance', 'Whether a Project Governance agent exists as configurable product functionality, and how it blocks actions, is not documented in the help centre.', UNK, 'High', '',
 '', 'Searched all 410 saved help articles for "project governance" and "governance agent": only the Timesheet Policies article matches.', ''),
('D1-058', 'AI: analyst', 'Marketing describes an AI Analyst that answers natural-language portfolio questions; no help article documents an AI Analyst feature.', VC, 'Medium', BRAID,
 'The AI Analyst answers natural-language queries:', '"AI Analyst" and "Nitro Analyst" have no help article. The help centre only references a "Signal Analyst" permission (D1-059) and "creating an analyst report" as an example Nitro agent run (D1-065).', 'Scope and data access of the analyst.'),
('D1-065', 'AI: analyst', 'Some analyst capability exists: the credits article lists "creating an analyst report" as an example Nitro agent run.', C, 'Medium', CRED,
 'One complete execution of a Nitro agent, such as generating a meeting summary, detecting signals, or creating an analyst report.', '', 'What the analyst report contains and what data it reads.'),
('D1-059', 'AI: analyst', 'A Signal Analyst feature exists, gated by a permission.', C, 'High', SIG,
 'Can access Signal Analyst', '', 'What Signal Analyst does is not described.'),
('D1-060', 'AI: Resource AI', 'Resource AI proposes a project team by Load balance, Maximize margins or Manual methods; the user then plans, reviews financials and allocates.', DB, 'Medium', RAI,
 'Resource AI guides you through selecting a project, choosing a planning goal, planning the team, reviewing financials, and allocating resources.', '', 'Whether Resource AI uses an LLM or deterministic optimisation (the documented load-balance logic is rule-based).'),
('D1-061', 'AI: credits', 'Nitro usage is metered in credits per agent run; runs record who triggered them, and system-triggered runs show a Nitro tag.', DB, 'High', CRED,
 'Each time a Nitro agent runs, it consumes credits based on the work performed.' + J + 'System-triggered runs display a Nitro tag instead of a user’s name.', '', 'Credit cost per agent type.'),
('D1-062', 'AI: models', 'Which AI or LLM models and providers power Nitro, AI Fills, Signals and Documentation Agents is not documented in any article read.', UNK, 'High', '',
 '', 'Not stated in any of the NITRO articles read in full; sub-processor disclosures are deferred to the technology deliverable.', ''),
('D1-063', 'AI: access', 'RBAC scopes meeting and email page access (Global, Account, Group, Only me), separately from settings and template permissions; permitted users can delete meeting and email pages.', DB, 'High', RBAC,
 'Settings permissions are separate from page and template permissions.' + J + 'Can delete meeting pages Delete meeting pages within the selected scope.', 'Inconsistency: the Meeting Page Templates article lists a fifth scope, "Project access", absent from this RBAC article.', ''),
('D1-064', 'AI: Vault', 'A project-level "Vault" setting appears only when AI agents are enabled; its purpose is not described.', C, 'Medium', PSET,
 'Vault appears only when AI agents are enabled for your account.', '', 'What Vault stores.'),
# ---------------- MCP and API ----------------
('D1-070', 'MCP', 'Rocketlane MCP currently exposes 24 tools (12 read, 12 write) over projects, tasks, phases, time entries, users, companies, fields, templates and comments, with no meeting, transcript, signal or AI-page tools.', C, 'High', MCP,
 'Rocketlane MCP currently supports 24 tools.' + J + 'get_my_profile , get_projects , get_tasks , get_users , get_phases , get_fields , get_customer_companies , get_time_entries , get_time_entry_categories , get_task_comments , get_conversations , get_project_comments', '', ''),
('D1-071', 'MCP', 'MCP limits stated by the vendor: no financial field updates, no time-entry deletion, no at-risk filtering, unreliable phase privacy, immediately published templates with no draft or update.', C, 'High', MCP,
 'Project financial fields such as budgeted hours or project fee are not supported through MCP project update parameters.' + J + 'Setting a phase as private is not reliable through MCP.' + J + 'There is no draft state through MCP.', '', ''),
('D1-072', 'MCP', 'MCP can create tasks from meeting notes or action items, but only when an external AI assistant is given those notes; the MCP itself exposes no meeting data.', INF, 'High', MCP,
 '', 'The guide lists "tasks from meeting notes" as a create_task use case, while the read tool list has no meeting or transcript tool, so the notes must come from outside Rocketlane MCP.', ''),
('D1-073', 'API', 'The public REST API (api.rocketlane.com/api/1.0) uses API-key security. Saved reference pages cover projects, phases, tasks, companies, users (read), fields, spaces, space documents, time entries, time-offs, budgets, custom revenue-recognition configs, resource allocations (read) and invoices (read).', C, 'High', GETP,
 'https://api.rocketlane.com/api' + J + '"api-key"', 'Resource list from parsing the 79 saved endpoints. Not exhaustive: an "Addresses API" is referenced but has no saved page (D1-014).', 'Rate limits for the public API (a help article cites 100 requests per minute for in-app bulk updates, which is not stated for the public API).'),
('D1-074', 'API', 'The public OpenAPI definition lists two non-production server URLs (labelled Staging and Orbits) besides production.', C, 'High', GETP,
 'https://api.nitro.run/api' + J + 'https://project.api.orbits.run/api', 'Observation only; these hosts were not probed. No inference is drawn about their purpose beyond the labels.', ''),
('D1-075', 'Webhooks', 'Webhooks are HTTPS event notifications; the payload doc lists task, project and phase event types, with a change log on update events.', DB, 'High', WHP,
 'TASK\\_CREATED' + J + 'PROJECT\\_ARCHIVED' + J + 'This will be sent only in events with the `_UPDATED` *eventType*.', 'Availability is narrower than this list: see D1-076.', ''),
('D1-076', 'Webhooks', 'Currently only task triggers are supported for webhooks (setup guide), and TASK is the only supported resource type, although project and phase event types are listed (internal inconsistency). No meeting, signal or AI events are listed.', C, 'High', WHP + J + D + 'docs/setting-up-webhooks-in-rocketlane.md',
 'Currently supported resource types:' + J + 'Currently, we only support task triggers for webhooks.', '', 'When project and phase events become available.'),
('D1-077', 'Webhooks', 'Delivery succeeds on 200 or 204; a 10-second timeout counts as failure; ordering is not guaranteed; the docs state exactly-once delivery; receiver authentication is currently Basic Authentication only.', DB, 'High', WHD + J + D + 'docs/setting-up-webhooks-in-rocketlane.md',
 'if no response is received for 10 seconds and the HTTP POST request times out' + J + 'Rocketlane guarantees exactly one delivery per event.' + J + 'Only Basic Authentication is supported currently.', 'Exactly-once is a vendor statement in docs; no retry policy is described, which makes the guarantee unverifiable. No payload signing is documented.', 'Retry schedule; payload signing.'),
# ---------------- Integrations ----------------
('D1-080', 'Jira', 'Jira integration: OAuth-style login, create or link a Jira issue from a task, sync status (category or custom mapping), due dates and comments; template tasks can auto-create Jira issues.', DB, 'High', JIRA,
 'Once this field is checked, Rocketlane will update its task status as the linked Jira issue status changes.' + J + 'Comments made on Jira issues will appear as a private messages on linked Rocketlane tasks.' + J + 'When a project is created out of the templates, the Jira issues for the corresponding task will be automatically created as well.', '', 'Webhook versus polling for Jira status sync; sync latency.'),
('D1-081', 'Jira', 'The documented Jira link is task-to-issue; status and due date flow Jira to Rocketlane, comments flow both ways.', INF, 'Medium', JIRA,
 '', 'Status and due-date sync are described only in the Jira-to-Rocketlane direction ("update its task status as the linked Jira issue status changes"; "updates the due date of the Rocketlane task if the due date of Jira is updated"). Comments are described both ways. No other object mapping (project, phase, epic sync) is described.', 'Whether Rocketlane changes propagate to Jira status.'),
('D1-082', 'CRM: Salesforce', 'Salesforce integration auto-creates projects from any selected object, including custom objects, and field-syncs; recommended model is one Salesforce project record to one Rocketlane project with idempotent creation.', DB, 'High', SF + J + SFMAP,
 'Any objects (including custom objects) can be selected to auto-create projects and for field-sync.' + J + 'Project creation is idempotent.', '', ''),
('D1-083', 'CRM: Salesforce', 'The help centre describes an embedded iPaaS that can handle routing, scripting, retries, dead-letter queues and audit logs for complex Salesforce setups.', C, 'Medium', SFMAP,
 'Rocketlane’s embedded iPaaS can sit between systems to handle routing, scripting, retries, dead-letter queues, and audit logs.', '', 'Which iPaaS; how it is configured.'),
('D1-084', 'CRM: HubSpot', 'HubSpot: OAuth connection; HubSpot workflows call a Rocketlane "Create Project" action on deal stages; one-way or two-way field sync between HubSpot objects and project fields.', DB, 'High', HUB,
 'In the action sidebar, go to Integrated Apps > Rocketlane and select Create Project .' + J + 'Fields sync allows one-way and two-way flow of data between HubSpot and Rocketlane.', '', ''),
('D1-085', 'CRM: email', 'Email-to-account mapping for Email Intelligence typically depends on CRM integrations (Salesforce or HubSpot).', C, 'High', EMAIL,
 'This mapping typically depends on your CRM integrations, such as Salesforce or HubSpot' + J + 'Accounts and contacts are synced directly from your CRM.', '', ''),
('D1-086', 'Slack', 'Slack integration sends project updates to channels, can create a channel per project, and notifies users.', C, 'Medium', SLACK,
 'A Slack channel is created when a new project is created.', '', ''),
# ---------------- Approval points summary rows ----------------
('D1-090', 'Approval points', 'Documented human control points in the AI layer: (1) AI Fill output is reviewed and edited before publishing; (2) signal definitions are reviewed (and can be tested) before creation; (3) timesheet policies are previewed, are disabled by default when created, and must be enabled (testing optional); (4) Resource AI allocations follow user review. A Documentation Agent manual trigger only starts a run; it does not review the output. Automatic paths with no per-output gate: meeting and email page generation, signal occurrences, living-document updates, on-event agent runs, timesheet policy enforcement once enabled.', INF, 'High', '',
 '', 'Synthesised from D1-030, D1-031, D1-036, D1-042, D1-047, D1-050, D1-051, D1-055 and D1-060, plus the Timesheet Policies statement "Policies are disabled by default when first created." The gated-versus-automatic classification is my reconstruction.', 'Any audit or approval workflow not described in docs.'),
# ---------------- Unknowns ----------------
('D1-095', 'Unknowns', 'Backend language, frameworks, databases, queues, application hosting and multi-tenancy model.', UNK, 'High', '',
 '', 'Not stated in any help or developer document captured. The only infrastructure disclosure found is an authentication migration (D1-098). Stack evidence is out of scope for this deliverable; no inference made here.', ''),
('D1-098', 'Disclosed infrastructure', 'Rocketlane discloses that it is migrating its internal authentication infrastructure from Okta to AWS Cognito.', C, 'High', H + '67000755973-updating-sso-for-rocketlane-s-authentication-migration',
 'Rocketlane is migrating its internal authentication infrastructure from Okta to AWS Cognito.', 'Only shows the identity provider used for authentication; it says nothing about where the application or data is hosted.', ''),
('D1-096', 'Unknowns', 'Transcription engine for AI Notetaker recordings, and whether provider transcripts are re-transcribed.', UNK, 'High', '',
 '', 'Meeting articles say transcripts are retrieved from providers and the notetaker records, but never name a transcription method.', ''),
('D1-097', 'Unknowns', 'Retention periods for recordings, transcripts and AI pages.', UNK, 'Medium', '',
 '', 'Not stated in any NITRO article. Deletion is documented: permitted users can delete meeting and email pages (D1-063); disconnecting a source keeps previously retrieved meetings; exclusions do not delete captured data. Legal or DPA pages are not part of this deliverable.', ''),
]


def main():
    dates = {r['url']: r['retrieved_utc'] for r in csv.DictReader(open(os.path.join(ROOT, 'sources', 'manifest.csv')))}
    out = os.path.join(HERE, 'd1-evidence-ledger.csv')
    with open(out, 'w', newline='') as fh:
        w = csv.writer(fh)
        w.writerow(['id', 'area', 'finding', 'grade', 'confidence', 'source_url', 'retrieved_utc', 'verbatim_quote', 'reasoning_or_notes', 'unknowns'])
        for rid, area, finding, grade, conf, urls, quotes, notes, unk in sorted(ROWS, key=lambda r: r[0]):
            ds = ' || '.join(dates.get(u.strip(), 'NOT SAVED') for u in urls.split(' || ') if u.strip())
            w.writerow([rid, area, finding, grade, conf, urls, ds, quotes, notes, unk])
    print(len(ROWS), 'rows written to', out)


if __name__ == '__main__':
    main()
