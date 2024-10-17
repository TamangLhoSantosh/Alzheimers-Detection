from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
import os
import jwt
from jwt.exceptions import InvalidTokenError
import dotenv

dotenv.load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


class HospitalAccessMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        print("Request received:", request.method, request.url)
        current_user = None

        # Skip middleware for documentation endpoints
        if (
            request.url.path.startswith("/docs")
            or request.url.path.startswith("/redoc")
            or request.url.path == "/openapi.json"
        ):
            print("Skipping middleware for documentation endpoint:", request.url.path)
            return await call_next(request)

        try:
            authorization_header = request.headers.get("Authorization")
            if authorization_header:
                parts = authorization_header.split()

                if len(parts) == 2 and parts[0] == "Bearer":
                    token = parts[1]
                    decoded_token = jwt.decode(
                        token,
                        SECRET_KEY,
                        algorithms=[ALGORITHM],
                    )
                    print(f"Decoded token: {decoded_token}")
                    current_user = decoded_token

        except InvalidTokenError as e:
            print("Invalid token:", e)
            return Response(
                "Forbidden", status_code=403
            )  # Immediate response for invalid token
        except Exception as e:
            print("Error:", e)
            return Response("Forbidden", status_code=403)

        if current_user and current_user.get("is_admin"):
            print("Admin user detected. Allowing access.")
            return await call_next(request)

        if current_user and not current_user.get("hospital_id"):
            print("Non-admin user without hospital affiliation. Access denied.")
            return Response("Forbidden", status_code=403)

        # Allow access if no issues found
        print("Request processing complete.")
        return await call_next(request)