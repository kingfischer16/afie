# Templates
Template files for use in management of the game design project and its associated artifacts.

## **`example_ledger_entry.json`**
An example file for an entry in the `ledger.json` record file, which is a list of these structures and is used as a master record for all features (and their statuses) in the active game project. An entry to the ledger file is created for each feature, and the status of each feature is updated as it progresses through the game design process. Each entry in the ledger file is a JSON object with the following fields:

| Field | Type | Description & Purpose |
| ----- | ---- | --------------------- |
| `feature_id` | JSON Key (field name is not used) | Primary Key. A unique, sequential identifier (e.g., "FEAT-001"). Generated by the ProjectLedgerManager. This is used to link everything together. Composed of the project name abbrevaiation and number. |
| `type` | String | Categorization. Defines the nature of the work. Essential for filtering and understanding intent. Allowed values: "new_feature", "bug_fix", "refactor", "enhancement". |
| `status` | String | Workflow State. The current stage of the feature in the Antigine pipeline. This is the primary field the Orchestrator uses to manage the process. Allowed values: "requested", "in_review", "awaiting_implementation", "awaiting_validation", "validated", "superseded". |
| `title` | String | A short, human-friendly title for the feature (e.g., "Player Dash Ability"). |
| `description` | String | The concise, AI-generated summary (max 120 words) that describes the feature's purpose and implementation highlights. This is a key field for RAG and agent context. |
| `keywords` | List[String] | AI-generated keywords for improved searchability and filtering. |
| `dates` | Object | Auditing & Timestamps. Records key milestones in the feature's lifecycle. All dates should be in ISO 8601 format (UTC). |
| `dates.created` | String | Timestamp when the feature was first requested. |
| `dates.fip_approved` | String (nullable) | Timestamp when the FIP passed all reviews. |
| `dates.implemented` | String (nullable) | Timestamp when the human submitted the commit hash for validation. |
| `dates.validated` | String (nullable) | Timestamp when the Implementation Validator passed the feature. |
| `dates.superseded` | String (nullable) | Timestamp if another feature makes this one obsolete. |
| `artifacts` | Object | Content Pointers. Direct relative paths to the detailed content files within the ledger directory. This keeps the master file clean while providing direct access to the "source of truth" content. |
| `artifacts.request` | String | Path to the request.md file. |
| `artifacts.fip` | String (nullable) | Path to the fip.md file. |
| `artifacts.adr` | String (nullable) | Path to the adr.md file. |
| `relations` | List[Object] | Dependency Graph. Defines relationships between features, which is critical for the Technical Architect to understand context and impact. |
| `relations[].type` | String | The nature of the relationship. Allowed values: "builds_on", "supersedes", "refactors", "fixes". |
| `relations[].target_id` | String | The feature_id of the related feature. |
| `implementation` | Object (nullable) | Ground Truth Link. Connects the feature directly to the codebase reality. This object is null until the feature is implemented. |
| `implementation.commit_hash` | String | The specific Git commit hash where this feature was implemented. This provides perfect traceability. |
| `implementation.changed_files` | List[String] | A list of files modified in that commit. Useful for quickly scoping future reviews or refactors. |
