
def user_schema(user) -> dict:
    return {
        "id": str(user["_id"]),
        "username": user["username"],
        "first_name": user["first_name"],
        "last_name": user["last_name"],
        "session_id": user["session_id"],
        "disabled": user["disabled"],
        "password": user["password"],
    }