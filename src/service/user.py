from datetime import datetime, timedelta
from jose import JWTError, jwt
from model.user import User
from data import user as data_user
from passlib.context import CryptContext

# secret key
SECRET_KEY = "change this key in production"
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_hashed_password(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Create an access token.

    Args:
        data (dict): The data to be encoded in the token.
        expires_delta (timedelta | None, optional): The expiration time delta. Defaults to None.

    Returns:
        str: The encoded access token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_jwt_username(token: str) -> str | None:
    """
    Get the username from a JWT token.

    Args:
        token (str): The JWT token.

    Returns:
        str | None: The username extracted from the token, or None if the token is invalid.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if not (username := payload.get("sub")):
            return None
        return username
    except JWTError:
        return None


def lookup_user(username: str) -> User | None:
    """
    Look up a user by username.

    Args:
        username (str): The username of the user.

    Returns:
        User | None: The user with the given username, or None if the user does not exist.
    """
    if user := data_user.get_one(username):
        return user
    else:
        return None


def get_current_user(token: str) -> User | None:
    """
    Get the current user from a JWT token.

    Args:
        token (str): The JWT token.

    Returns:
        User | None: The current user, or None if the token is invalid.
    """
    if not (username := get_jwt_username(token)):
        return None
    if not (user := lookup_user(username)):
        return None
    return user


def auth_user(username: str, password: str) -> User | None:
    """
    Authenticate a user by username and password.

    Args:
        username (str): The username of the user.
        password (str): The password of the user.

    Returns:
        bool: True if the user is authenticated, False otherwise.
    """
    if not (user := lookup_user(username)):
        return None
    if not verify_password(password, user.hash):
        return None
    return user


# curd operations
def create(user: User) -> User:
    """
    Create a new user.

    Args:
        user (User): The user to be created.

    Returns:
        User: The created user.
    """
    user.hash = get_hashed_password(user.hash)
    return data_user.create(user)


def modify(name: str, user: User) -> User:
    """
    Modify a user.

    Args:
        name (str): The username of the user to be modified.
        user (User): The modified user.

    Returns:
        User: The modified user.
    """
    user.hash = get_hashed_password(user.hash)
    return data_user.modify(name, user)


def delete(name: str) -> None:
    """
    Delete a user.

    Args:
        name (str): The username of the user to be deleted.

    Returns:
        None
    """
    data_user.delete(name)


def get_one(name: str) -> User | None:
    """
    Get a user by username.

    Args:
        name (str): The username of the user.

    Returns:
        User | None: The user with the given username, or None if the user does not exist.
    """
    return data_user.get_one(name)


def get_all() -> list[User]:
    """
    Get all users.

    Returns:
        list[User]: A list of all users.
    """
    return data_user.get_all()
