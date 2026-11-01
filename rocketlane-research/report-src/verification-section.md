The verification pass had two stages.

**Stage 1: automated quote check** (`ledger/verify_ledger.py`). For every row, the script checks:
- the grade is valid;
- every cited source exists as a saved copy with retrieval time and hash;
- every verbatim quote appears in the saved text of the cited source;
- CONFIRMED and DOCUMENTED BEHAVIOUR rows cite official documentation, and VENDOR CLAIM rows cite marketing;
- INFERRED rows include written reasoning, and UNKNOWN rows say what was searched.

**Negative control:** I planted three errors (an altered quote, a source that wasn't saved, and a blog quote graded CONFIRMED). The script caught all three and exited with a failure, then passed again once the ledger was restored.

**Final result:** all 80 rows pass (`ledger/d1-verification-report.md`).

**Stage 2: independent semantic check** (`ledger/d1-semantic-verification.md`). A separate checker agent, with no web access, re-read the cited sources in context. It judged whether each finding is actually supported, correctly graded and free of missing qualifiers.

| Verdict | Rows (of 75 checked) |
|---|---|
| SUPPORTED | 58 |
| OVERSTATED | 9 |
| WRONG GRADE | 3 |
| CONTRADICTED by another saved document | 5 |
| UNSUPPORTED | 0 |

Before applying any correction, I confirmed each quote the checker relied on in the saved sources (11 of 11 found).

**Corrections applied:**

| Row | Correction |
|---|---|
| D1-012 | Split into a CONFIRMED row (RAID logs and risk registers are Sheets use cases) and a new INFERRED row D1-015 ("no dedicated RAID object", an absence claim). Removed the incorrect note "'risk log' occurs nowhere" |
| D1-013 | Note corrected: Sheets do have a "Task link" column (new row D1-016) |
| D1-014 | Regraded to INFERRED (absence). The saved API inventory is marked as not exhaustive, because an "Addresses API" is referenced but undocumented |
| D1-017 | New INFERRED row, split out of D1-043: AI action items aren't turned into tasks |
| D1-021, D1-033, D1-034, D1-047, D1-070, D1-085 | Restored source qualifiers: "eligible", "solely for recording ingestion", "currently", "by default", "when enabled", "typically" |
| D1-025 | Notes that the docs specify application (not delegated) permissions |
| D1-029 | Adds the third matching variant, from the Signals article |
| D1-063 | Adds that deletion is permitted; records the inconsistent "Project access" scope |
| D1-065 | New CONFIRMED row: an "analyst report" agent run exists (credits doc) |
| D1-073 | Corrected the resource list (budgets have full create/read/update/delete; revenue-recognition configs added); marked not exhaustive |
| D1-075 / D1-076 | Webhooks corrected to "currently task triggers only", citing the setup guide |
| D1-077 | Adds receiver authentication: Basic Authentication only |
| D1-090 | Approval-point synthesis rewritten: timesheet policies are off until enabled and testing is optional; meeting and email page generation listed as automatic; a manual trigger is not a review |
| D1-095 / D1-098 | New CONFIRMED row: disclosed authentication migration from Okta to AWS Cognito |
| D1-097 | Narrowed to retention periods, since deletion is documented |

**Residual cautions:**
- Absence findings depend on the saved help centre (410 articles) and API reference as of 2026-10-31.
- Unpublished features and unlisted endpoints can't be excluded.
