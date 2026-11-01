import subprocess
import sys
import time
import os
from pathlib import Path

# Ensure playwright is installed – this script expects it to be available.
# If not, user can run: pip install playwright && python -m playwright install chromium

def start_streamlit(app_path: str, port: int = 8501) -> subprocess.Popen:
    """Start the Streamlit app in a subprocess.
    Returns the Popen object so the caller can terminate it later.
    """
    cmd = [sys.executable, "-m", "streamlit", "run", app_path, "--server.port", str(port), "--server.headless", "true"]
    # Redirect stdout/stderr to DEVNULL to keep console clean
    proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return proc

def wait_for_server(port: int = 8501, timeout: int = 30) -> bool:
    """Poll localhost until the Streamlit server responds or timeout expires."""
    import socket
    start = time.time()
    while time.time() - start < timeout:
        try:
            with socket.create_connection(("127.0.0.1", port), timeout=1):
                return True
        except OSError:
            time.sleep(0.5)
    return False

def capture_screenshot(url: str, output_path: Path, width: int = 1920, height: int = 1080):
    """Use Playwright to capture a full‑page screenshot of the given URL."""
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(viewport={"width": width, "height": height})
        page = context.new_page()
        page.goto(url, wait_until="networkidle")
        # Give a short pause for any heavy Plotly rendering
        time.sleep(2)
        page.screenshot(path=str(output_path), full_page=True)
        browser.close()

def main():
    project_root = Path(__file__).resolve().parents[1]
    app_path = project_root / "dashboard" / "app.py"
    output_path = project_root / "reports" / "visualizations" / "dashboard_preview.png"

    # Ensure output directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Start Streamlit server
    proc = start_streamlit(str(app_path))
    try:
        if not wait_for_server():
            sys.exit("Streamlit server did not start within timeout.")
        # Capture screenshot
        capture_screenshot("http://localhost:8501", output_path)
        print(f"Dashboard screenshot saved to {output_path}")
    finally:
        # Shut down the server
        proc.terminate()
        proc.wait()

if __name__ == "__main__":
    main()
