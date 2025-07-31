# Skill Specification: Social Automation

This document defines the MVP for automating social media posts. The agent acts within the scope of free tools or native web flows to publish content on behalf of the user.

## Auto‑Post MVP

1. **Prepare Content**: Accept or generate post content, including text, links, and optional images, based on user parameters and content policies.
2. **Authenticate to Platform**: Use a recipe to log into the selected platform (e.g., Twitter, LinkedIn) with stored credentials or ask the user to log in manually during first run.
3. **Create Post**: Navigate to the post creation interface via the web adapter and populate the post fields with the prepared content.
4. **Schedule or Publish**: If the platform supports scheduling, schedule the post at the desired time; otherwise, publish immediately. When scheduling, use only free tier capabilities or free third‑party tools.
5. **Verify Publication**: After posting, retrieve the post URL or check the timeline to confirm that the post appears with the correct timestamp.
6. **Capture Evidence**: Record the post URL or screenshot of the post, along with the profile timestamp, to confirm success.
7. **Park Conditions**: If login fails due to multi‑factor authentication, or if scheduling requires a paid plan, park the step with a reason and propose a free alternative (e.g., immediate posting or using a different platform).
