# Skill Specification: Jobs and Outreach

This document defines the MVP for automating job applications or outreach tasks. The agent uses deterministic web flows to fill forms and upload documents.

## Auto‑Apply MVP

1. **Identify Target Listing**: Accept a URL or search criteria for job postings. Use allowed platforms and ensure that duplication is prevented by hashing previously applied URLs.
2. **Gather Profile Data**: Pull or prompt for user profile information (e.g., name, contact details) and resume file. Ensure the file exists and is hashed for deduplication.
3. **Navigate and Fill Form**: Use the web adapter to navigate to the job application form. Fill out required fields using stored profile data and any additional parameters (cover letter, answers to screening questions).
4. **Upload Resume/Attachments**: Upload the resume using the file adapter; confirm that the file has uploaded successfully.
5. **Submit Application**: Submit the form. If the website uses multi‑factor authentication or a captcha, park the step and request manual intervention.
6. **Capture Evidence**: Capture confirmation text or the resulting URL indicating that the application was submitted. Record a hash of the URL to avoid duplicate applications.
7. **Park Conditions**: If a duplicate application is detected, or if required information is missing, park the task with a reason and note requested info (e.g., missing resume or incomplete profile).
