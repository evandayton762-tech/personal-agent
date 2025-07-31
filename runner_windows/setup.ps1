<#
    Runner setup script

    This PowerShell script prepares a Windows machine to run the personal agent
    runner with browser and OCR capabilities. It documents the steps required
    but does not perform any installations automatically. A human operator
    should review and run the commands as appropriate.

    Steps:
      1. Ensure Python 3.11 is installed and added to your PATH. You can download it from https://www.python.org/downloads/windows/.
      2. Install Playwright for Python:
           py -3.11 -m pip install --upgrade pip
           py -3.11 -m pip install playwright
           py -3.11 -m playwright install chromium
      3. Install Tesseract OCR (optional for OCR functionality):
           # Option A: Chocolatey (requires admin)
           #   Set-ExecutionPolicy Bypass -Scope Process -Force
           #   iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
           #   choco install tesseract
           
           # Option B: Manual installer
           #   Download the Windows installer from https://github.com/tesseract-ocr/tesseract/wiki
           #   Run the installer and ensure the tesseract executable is added to PATH.
      4. Verify installation:
           py -3.11 -c "from playwright.sync_api import sync_playwright; print('Playwright installed')"
           tesseract --version
      5. (Optional) Enable OCR support in the runner by ensuring that the Tesseract executable is discoverable.

    Save this file as setup.ps1 and run it from an elevated PowerShell prompt when preparing a new Windows runner.
#>