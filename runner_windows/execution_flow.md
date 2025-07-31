# Runner Execution Flow

This document describes the order of operations the Windows runner follows when executing steps. The flow ensures reliable communication with the orchestrator, deterministic execution via adapters, evidence capture, and safe interruption handling.

## A. Connect

Upon start, the runner establishes an outbound WebSocket connection to the orchestrator. If the connection fails, it retries with exponential backoff until successful.

## B. Heartbeat

Once connected, the runner sends a heartbeat message every 10 seconds. The heartbeat includes the runner’s status (idle, running, paused), available disk space, and any diagnostic flags.

## C. Receive Step → Validate → Refuse Unknown Tool

When a step is received, the runner validates the payload against the `Step` schema. If the adapter type is unknown or not allowed, the runner refuses to execute and returns an error. Otherwise, it proceeds to dispatch the step.

## D. Dispatch to the Correct Tool/Adapter

Based on the `adapter.type`, the runner invokes the corresponding adapter function with provided arguments. The adapter performs the action (e.g., navigate to a web page, click a button, write a file).

## E. Evidence Capture

Immediately after performing the action, the runner collects deterministic evidence: taking a screenshot, capturing the final URL or DOM checks, computing file hashes, or recording the JSON response from the finance broker. This evidence is attached to the `StepResult` and returned to the orchestrator.

## F. Kill Switch

The runner listens for a global hotkey or kill command from the user. If triggered, the runner stops execution promptly, cleans up any partial actions, and returns a `failed` status with the note “killed”.

## G. Logging

Each action is logged as a single line with a timestamp. Logs must redact secrets or sensitive values. The runner logs connection events, received steps, adapter dispatches, evidence capture, and heartbeat transmissions.
