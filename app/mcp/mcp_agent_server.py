import os
import zipfile
import io
import httpx
from fastmcp import FastMCP

# Initialize the Model Context Protocol Server
mcp = FastMCP("GitHub Artifact Fetcher")

@mcp.tool()
def fetch_latest_software_package(owner: str, repo: str) -> str:
    """
    Connects to the GitHub API, finds the latest compiled software artifact
    from a pipeline run, and downloads it into the workspace.

    Args:
        owner: The GitHub account or organization name (e.g., 'EHanZF').
        repo: The repository name (e.g., 'cdyp7-harness-webapp').
    """
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        return "Error: GITHUB_TOKEN environment variable is not set."

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28"
    }

    # Use httpx context manager for efficient network streaming
    with httpx.Client(headers=headers) as client:
        # 1. Look up recent repository workflow artifacts
        api_url = f"https://github.com{owner}/{repo}/actions/artifacts"
        response = client.get(api_url)

        if response.status_code != 200:
            return f"Failed to connect to GitHub API. Status code: {response.status_code}"

        data = response.json()
        artifacts = data.get("artifacts", [])

        if not artifacts:
            return f"No compiled software artifacts found for {owner}/{repo}."

        # 2. Extract metadata for the latest generated release bundle
        latest_artifact = artifacts[0]
        artifact_id = latest_artifact["id"]
        artifact_name = latest_artifact["name"]

        # 3. Stream the ZIP payload down from GitHub
        download_url = f"https://github.com{owner}/{repo}/actions/artifacts/{artifact_id}/zip"
        zip_response = client.get(download_url)

        if zip_response.status_code != 200:
            return f"Failed to download package artifact files. Status: {zip_response.status_code}"

        # 4. Automatically extract the archive into the local agent workspace
        try:
            with zipfile.ZipFile(io.BytesIO(zip_response.content)) as zip_ref:
                zip_ref.extractall("./downloaded_software")

            return f"Success! Programmatically downloaded '{artifact_name}' (ID: {artifact_id}) and extracted code modules to './downloaded_software'."
        except zipfile.BadZipFile:
            return "Downloaded file payload was corrupted or not a valid archive."

if __name__ == "__main__":
    # Start the server using standard input/output transport for host app discovery
    mcp.run(transport="sse")
