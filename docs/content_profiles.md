# Content Profiles

Different projects may have varying content boundaries. The agent supports multiple content profiles, defined here. Switching profiles controls what type of content the agent may generate or process.

## standard (default)

The `standard` profile is suitable for general automation. It allows typical corporate or personal content and prohibits explicit sexual content, violence, or other sensitive material. This profile is used by default unless the user specifies otherwise.

## strict

The `strict` profile is designed for publicly hosted or shared outputs. It minimizes risk by avoiding any potentially controversial topics, slang, or informal language. Use this profile when deploying content that will be visible to a broad or sensitive audience.

## nsfw_private

The `nsfw_private` profile is only for content consumed on the user’s personal device. It allows legal, adult‑only content but never involves minors or illegal material. Outputs generated under this profile must never be deployed publicly and must remain on the user’s device.

## Switching Rules

The profile is selected per project. Unless explicitly set to `strict` or `nsfw_private` by the user, the agent uses the `standard` profile. The agent must confirm with the user when switching from `strict` or `standard` to `nsfw_private`, ensuring that the user understands the privacy implications.
