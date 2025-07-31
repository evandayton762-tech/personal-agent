# Windows Runner

This directory contains the Windows runner implementation and supporting assets.

## Setup

Before running the personal agent on a Windows machine, you need to install a few dependencies so that browser automation and OCR can work. A PowerShell script, `setup.ps1`, documents the required steps. Review the script and run it from an elevated PowerShell prompt:

```powershell
cd runner_windows
PowerShell -ExecutionPolicy Bypass -File .\setup.ps1
```

The script explains how to ensure Python 3.11 is available, how to install Playwright and its Chromium browser, and how to install Tesseract OCR if you want OCR functionality. These steps must be performed manually; the script itself does not install anything automatically.

## Running the Runner

Once your environment is prepared, you can start the runner. From the repository root:

```bash
python -m runner_windows.runner --server ws://<orchestrator-host>:<port>/ws
```

The runner will connect to the orchestrator’s WebSocket endpoint, send periodic heartbeat messages, process incoming steps via the adapters in `runner_windows/actions/`, and record logs under `runner_windows/logs/`.