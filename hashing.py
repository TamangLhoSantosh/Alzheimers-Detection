# To hash plain text
from passlib.context import CryptContext

# Create a CryptContext object with bcrypt as the hashing scheme
pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hash:
    def bcrypt(password: str) -> str:
        """
        Hashes a plain text password using bcrypt.

        Args:
            password (str): The plain text password to be hashed.

        Returns:
            str: The hashed password.
        """
        return pwd_cxt.hash(password)

    def verify(hashed_password: str, plain_password: str) -> bool:
        """
        Verifies a plain text password against a hashed password.

        Args:
            hashed_password (str): The hashed password to verify against.
            plain_password (str): The plain text password to check.

        Returns:
            bool: True if the plain password matches the hashed password, otherwise False.
        """
        return pwd_cxt.verify(plain_password, hashed_password)
