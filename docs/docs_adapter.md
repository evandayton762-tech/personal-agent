# Google Docs Adapter Specification

This document describes the integration between the personal agent and Google Docs/Drive via the DocsAdapter. The adapter allows the agent to maintain a living project log and to insert content into documents.

## A. Required Scopes

The DocsAdapter requires the following OAuth scopes:

- **documents**: Allows reading and writing Google Docs.
- **drive.file**: Allows creating and modifying files in the user’s Drive (limited to files created by the agent).

## B. Local Token Location

The OAuth device code flow will store the refresh token and access token in a local file. By default, this file is located at:

```
C:\Users\<you>\.agent\google_token.json
```

Replace `<you>` with the Windows username running the agent. The token file must be protected by OS file permissions to prevent unauthorized access.

## C. Functions to Implement

The DocsAdapter exposes the following functions:

- **ensure_doc(project_name) → doc_id**: Create a new Google Doc with the given `project_name` if it doesn’t already exist, or return the existing document’s ID.
- **append_section(doc_id, heading, markdown_or_struct)**: Append a new section to the document identified by `doc_id`. The section begins with `heading` and contains either markdown text or a structured object (which the adapter will format appropriately).
- **insert_table(doc_id, rows)**: Insert a table into the document. `rows` is an array of arrays representing rows and columns.
- **insert_image(doc_id, image_path_or_drive_id)**: Insert an image into the document using a local path or a drive file ID.
- **link_artifact(doc_id, title, href)**: Insert a hyperlink with `title` pointing to `href`.
- **update_toc(doc_id)**: Refresh the document’s table of contents so that new headings appear.

## D. Nightly Summary

The Scheduler will trigger a nightly summary job. At the end of each day, the agent appends a “Run Summary” section to the project document. The summary includes tasks executed, token and cost usage, and a list of parked items. The document’s table of contents is updated thereafter.
