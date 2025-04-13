import subprocess
import logging

# List of sessions to stop
sessions = [
    "Circular Kernel Context Logger",
    "DiagLog",
    "Diagtrack-Listener",
    "EventLog-Application",
    "EventLog-System",
    "iclsClient",
    "iclsProxy",
    "LwtNetLog",
    "Microsoft-Windows-Rdp-Graphics-RdpIdd-Trace",
    "NetCore",
    "NtfsLog",
    "PlatformLicenseManagerService",
    "RadioMgr",
    "UBPM",
    "WdiContextLog",
    "WiFiSession",
    "UserNotPresentTraceSession",
    "NVIDIA-NVTOPPS-NOCAT",
    "NVIDIA-NVTOPPS-FILTER",
    "ScreenOnPowerStudyTraceSession",
    "MBAMChameleon",
    "MBAMWebProtection",
    "MBAMFarFlt",
    "SHS-01082025-091704-7-7f",
    "MBAMProtection",
    "SgrmEtwSession"
]

# Set up logging to log to a file and console
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', handlers=[
    logging.FileHandler("logman_tasks.log"),
    logging.StreamHandler()
])

def query_active_sessions():
    """Query all active logman sessions."""
    try:
        result = subprocess.run(['logman', 'query'], capture_output=True, text=True, check=True)
        active_sessions = result.stdout.splitlines()
        return active_sessions
    except subprocess.CalledProcessError:
        logging.error("Failed to query logman sessions.")
        return []

def stop_logman_sessions():
    # First, get the list of active sessions
    active_sessions = query_active_sessions()

    if not active_sessions:
        logging.warning("No active logman sessions found.")
        return
    
    for session in sessions:
        # Check if the session is active
        if any(session in active_session for active_session in active_sessions):
            try:
                # Stop the logman session using subprocess
                logging.info(f"Stopping {session}...")
                subprocess.run(['logman', 'stop', session, '-ets'], check=True)
                logging.info(f"Successfully stopped {session}.")
            except subprocess.CalledProcessError:
                logging.error(f"Failed to stop {session} or session not found.")
            except Exception as e:
                logging.error(f"An error occurred while stopping {session}: {e}")
        else:
            logging.warning(f"{session} is not active or does not exist.")

if __name__ == "__main__":
    stop_logman_sessions()
