# This can be extended later to support multiple users or login roles

def get_available_roles():
    return ["Faculty", "Admin", "Assistant"]

def default_user_role():
    return "Faculty"

def is_admin(role: str) -> bool:
    return role.lower() == "admin"
