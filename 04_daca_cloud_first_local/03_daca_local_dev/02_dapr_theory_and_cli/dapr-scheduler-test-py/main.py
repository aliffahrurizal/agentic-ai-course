import logging
import datetime
import os
import httpx  # Import httpx
# Added Path import for path parameters
from fastapi import FastAPI, Body, HTTPException, Path

logging.basicConfig(level=logging.INFO)

# Configuration
APP_ID = "scheduler-test-py"  # Still useful for context/logging
# JOB_NAME = "test-job-py" # We'll use path parameters instead of a fixed name
JOB_SCHEDULE_INTERVAL = "@every 10s"  # Default schedule
JOB_REPEATS = 3  # Default repeats
JOB_DATA = {"message": "Hello from Python Job!"}  # Default data
# Get Dapr port from environment variable (set by dapr run)
# Default to 3500 if not set
DAPR_HTTP_PORT = os.getenv("DAPR_HTTP_PORT", 3500)
DAPR_JOB_API_BASE = f"http://localhost:{DAPR_HTTP_PORT}/v1.0-alpha1/jobs"

# --- FastAPI App Setup ---
app = FastAPI(title=f"{APP_ID} Service")

# --- Dapr Job Handler Endpoint ---
# This endpoint receives the job invocation from the Dapr Scheduler sidecar
# It needs to handle potentially different job names if scheduled dynamically
# Using a path parameter for the job name


@app.post("/job/{job_name}")
async def job_handler(job_name: str = Path(...), job_data: dict = Body(...)):
    """Handles incoming job events from Dapr for any job name."""
    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
    logging.info(f"Received job '{job_name}' at {timestamp}")
    logging.info(f"Job data: {job_data}")
    # In a real app, perform the scheduled task here
    return {"status": "SUCCESS", "received_at": timestamp, "data": job_data}

# --- Endpoint to Schedule a Dapr Job ---


@app.post("/schedule-job/{job_name}")
async def schedule_job_endpoint(job_name: str = Path(...)):
    """Schedules the job using a direct HTTP call to the Dapr sidecar's Jobs API."""
    logging.info(f"Attempting to schedule job: {job_name}")

    # Using defaults, could be extended to take payload from request body
    job_payload = {
        "schedule": JOB_SCHEDULE_INTERVAL,
        "repeats": JOB_REPEATS,
        "data": JOB_DATA,
    }

    schedule_url = f"{DAPR_JOB_API_BASE}/{job_name}"
    logging.info(f"Calling Dapr Jobs API URL: POST {schedule_url}")

    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(schedule_url, json=job_payload)
            resp.raise_for_status()
            logging.info(f"Job scheduling response status: {resp.status_code}")
            if resp.status_code == 204:
                return {"status": "SUCCESS", "message": f"Job '{job_name}' scheduled successfully.", "response": resp.text}
            else:
                # httpx response.text is a property, not an awaitable method
                response_text = resp.text
                return {"status": "UNEXPECTED_STATUS", "message": f"Unexpected status code {resp.status_code}: {response_text}"}
    # ... (keep existing exception handling blocks) ...
    except httpx.RequestError as e:
        logging.error(
            f"HTTP Request Error scheduling job {job_name}: {e}", exc_info=True)
        raise HTTPException(
            status_code=500, detail=f"HTTP Request error communicating with Dapr sidecar: {str(e)}")
    except httpx.HTTPStatusError as e:
        logging.error(
            f"Dapr API Error scheduling job {job_name}: Status {e.response.status_code}, Response: {e.response.text}", exc_info=True)
        raise HTTPException(
            status_code=500, detail=f"Dapr API returned an error: Status {e.response.status_code} - {e.response.text}")
    except Exception as e:
        logging.error(
            f"Unexpected error scheduling job {job_name}: {e}", exc_info=True)
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred: {str(e)}")


# --- Endpoint to Get Dapr Job Data ---
@app.get("/get-job/{job_name}")
async def get_job_endpoint(job_name: str = Path(...)):
    """Gets job data using a direct HTTP call to the Dapr sidecar's Jobs API."""
    logging.info(f"Attempting to get job data for: {job_name}")
    get_url = f"{DAPR_JOB_API_BASE}/{job_name}"
    logging.info(f"Calling Dapr Jobs API URL: GET {get_url}")

    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(get_url)
            # Check for 404 specifically as Dapr might return that if job not found
            if resp.status_code == 404:
                raise HTTPException(
                    status_code=404, detail=f"Job '{job_name}' not found by Dapr.")
            resp.raise_for_status()  # Handle other errors (e.g., 500 from Dapr)
            logging.info(f"Get job response status: {resp.status_code}")
            job_details = resp.json()  # Get JSON response body
            return {"status": "SUCCESS", "job_details": job_details}
    # ... (keep existing exception handling blocks, adjusted for GET context) ...
    except httpx.RequestError as e:
        logging.error(
            f"HTTP Request Error getting job {job_name}: {e}", exc_info=True)
        raise HTTPException(
            status_code=500, detail=f"HTTP Request error communicating with Dapr sidecar: {str(e)}")
    except httpx.HTTPStatusError as e:
        # Catch 404 handled above, log others
        logging.error(
            f"Dapr API Error getting job {job_name}: Status {e.response.status_code}, Response: {e.response.text}", exc_info=True)
        raise HTTPException(
            status_code=500, detail=f"Dapr API returned an error: Status {e.response.status_code} - {e.response.text}")
    except Exception as e:
        logging.error(
            f"Unexpected error getting job {job_name}: {e}", exc_info=True)
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred: {str(e)}")


# --- Endpoint to Delete a Dapr Job ---
@app.delete("/delete-job/{job_name}")
async def delete_job_endpoint(job_name: str = Path(...)):
    """Deletes a job using a direct HTTP call to the Dapr sidecar's Jobs API."""
    logging.info(f"Attempting to delete job: {job_name}")
    delete_url = f"{DAPR_JOB_API_BASE}/{job_name}"
    logging.info(f"Calling Dapr Jobs API URL: DELETE {delete_url}")

    try:
        async with httpx.AsyncClient() as client:
            resp = await client.delete(delete_url)
            if resp.status_code == 404:
                logging.warning(
                    f"Attempted to delete job '{job_name}', but Dapr reported not found (404).")
                # Decide if 404 is an error or acceptable (treat as success here)
                return {"status": "SUCCESS", "message": f"Job '{job_name}' not found or already deleted."}
            resp.raise_for_status()  # Handle other errors
            logging.info(f"Delete job response status: {resp.status_code}")
            # Expect 204 No Content on successful delete
            if resp.status_code == 204:
                return {"status": "SUCCESS", "message": f"Job '{job_name}' deleted successfully."}
            else:
                return {"status": "UNEXPECTED_STATUS", "message": f"Unexpected status code {resp.status_code}"}
    except httpx.RequestError as e:
        logging.error(
            f"HTTP Request Error deleting job {job_name}: {e}", exc_info=True)
        raise HTTPException(
            status_code=500, detail=f"HTTP Request error communicating with Dapr sidecar: {str(e)}")
    except httpx.HTTPStatusError as e:
        # Catch 404 handled above, log others
        logging.error(
            f"Dapr API Error deleting job {job_name}: Status {e.response.status_code}, Response: {e.response.text}", exc_info=True)
        raise HTTPException(
            status_code=500, detail=f"Dapr API returned an error: Status {e.response.status_code} - {e.response.text}")
    except Exception as e:
        logging.error(
            f"Unexpected error deleting job {job_name}: {e}", exc_info=True)
        raise HTTPException(
            status_code=500, detail=f"An unexpected error occurred: {str(e)}")


@app.get("/")
async def root():
    return {"message": f"Welcome to {APP_ID}. Use POST /schedule-job/{{job_name}}, GET /get-job/{{job_name}}, DELETE /delete-job/{{job_name}}."}
