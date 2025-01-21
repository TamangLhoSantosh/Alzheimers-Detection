import httpx
from fastapi import HTTPException
from typing import Any, Dict


async def analyze_image(image_path: str) -> Dict[str, Any]:
    """
    Sends an image to an external FastAPI service for analysis.

    Args:
        image_path (str): Path to the image that needs to be analyzed.

    Returns:
        Dict: The analysis result as a dictionary, if successful.

    Raises:
        HTTPException: If the external service fails or the response is invalid.
    """
    try:
        # Open the image file to send as form data
        with open(image_path, "rb") as image_file:
            files = {"file": (image_path, image_file, "image/jpeg")}

            async with httpx.AsyncClient() as client:
                # Send POST request to the analysis service
                response = await client.post(
                    "http://localhost:8080/predict", files=files
                )

                # Check if the request was successful
                response.raise_for_status()  # Raise an error for non-2xx responses

                # Parse the JSON response from the external service
                analysis_result = response.json()

                # Assuming the response is a JSON object, you can return it
                return analysis_result

    except httpx.RequestError as e:
        # Handle network-related errors (e.g., timeouts, connection issues)
        raise HTTPException(
            status_code=503,  # Service Unavailable
            detail=f"Error connecting to the analysis service: {e}",
        )
    except httpx.HTTPStatusError as e:
        # Handle non-2xx responses from the service
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"Analysis service returned an error: {e.response.text}",
        )
    except Exception as e:
        # General exception handling if something else goes wrong
        raise HTTPException(
            status_code=500, detail=f"Unexpected error during image analysis: {e}"
        )
