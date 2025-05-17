from typing import Optional

from fastapi import FastAPI, HTTPException
import httpx

from app.core.config import settings

app = FastAPI()

# Configuration
logto_endpoint = settings.logto_endpoint
token_endpoint = settings.logto_token_endpoint
application_id = settings.logto_app_id
application_secret = settings.logto_app_secret
admin_api_resource = settings.admin_api_resource or "default"
logto_json_path = settings.logto_json_path


async def fetch_access_token():
    try:
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        payload = {
            "grant_type": "client_credentials",
            "client_id": application_id,
            "client_secret": application_secret,
            "scope": "all",
            "resource": admin_api_resource,
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(token_endpoint, headers=headers, data=payload)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.json())

        return response.json()["access_token"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def create_resource_if_missing(client: httpx.AsyncClient, headers: dict, resource_data: dict):
    try:
        resp = await client.get(f"{logto_endpoint}/api/resources", headers=headers)
        if resp.status_code == 200:
            existing = resp.json()
            if any(r["identifier"] == resource_data["identifier"] for r in existing):
                print(f"ℹ️ Resource '{resource_data['identifier']}' already exists.")
                return

        resp = await client.post(f"{logto_endpoint}/api/resources", headers=headers, json=resource_data)
        if resp.status_code == 201:
            print(f"✅ Created resource: {resource_data['identifier']}")
        elif resp.status_code == 409:
            print(f"⚠️ Resource '{resource_data['identifier']}' already exists.")
        else:
            print(f"❌ Failed to create resource: {resp.text}")
    except Exception as e:
        print(f"❌ Exception while creating resource: {e}")


async def create_scopes(client: httpx.AsyncClient, headers: dict, scopes: set):
    for scope in scopes:
        try:
            resp = await client.post(
                f"{logto_endpoint}/api/scopes",
                json={"name": scope, "description": f"Auto-seeded scope: {scope}", "resource": admin_api_resource},
                headers=headers
            )
            if resp.status_code not in (201, 409):
                print(f"❌ Failed to create scope '{scope}': {resp.text}")
        except Exception as e:
            print(f"❌ Exception while creating scope '{scope}': {e}")


async def create_roles_and_assign_permissions(client: httpx.AsyncClient, headers: dict, roles: list) -> dict:
    role_name_to_id = {}

    existing_roles_resp = await client.get(f"{logto_endpoint}/api/roles", headers=headers)
    existing_roles = existing_roles_resp.json() if existing_roles_resp.status_code == 200 else []

    for role in roles:
        role_payload = {
            "name": role["role"],
            "description": f"Auto-seeded role: {role['role']}",
            "permissions": role["permissions"],
        }

        # Check if role exists
        existing = next((r for r in existing_roles if r["name"] == role["role"]), None)
        if existing:
            role_id = existing["id"]
            print(f"ℹ️ Role '{role['role']}' already exists.")
        else:
            resp = await client.post(
                f"{logto_endpoint}/api/roles",
                json=role_payload,
                headers=headers
            )
            if resp.status_code == 201:
                role_id = resp.json()["id"]
                print(f"✅ Created role: {role['role']}")
            elif resp.status_code == 409:
                role_id = next((r["id"] for r in existing_roles if r["name"] == role["role"]), None)
                print(f"⚠️ Role '{role['role']}' already exists (409).")
            else:
                print(f"❌ Failed to create role '{role['role']}': {resp.text}")
                continue

        role_name_to_id[role["role"]] = role_id

    return role_name_to_id


async def create_users(client: httpx.AsyncClient, headers: dict, users: list, role_mapping: dict) -> dict:
    """
    Create users and assign roles using role IDs.

    Args:
        client: The HTTP client instance.
        headers: Headers for the request (e.g., authorization).
        users: List of user data containing roles.
        role_mapping: Dictionary that maps role names to role IDs.

    Returns:
        A dictionary mapping usernames to user IDs.
    """
    user_name_to_id = {}
    print("users",users)
    for user in users:
        username = user["username"]
        email = user["email"]
        password = user["password"]
        roles = user.get("roles", [])

        # Clean username (Logto requires alphanumeric usernames)
        safe_username = "".join(c if c.isalnum() else "_" for c in username.lower())

        try:
            # Check if user already exists
            resp = await client.get(f"{logto_endpoint}/api/users?username={safe_username}", headers=headers)
            await find_user_by_phone_number(username)
            existing_users = resp.json()
            print("existing_users",existing_users)
            if existing_users:
                user_id = existing_users[0]["id"]
                print("user_id", user_id)

                print(f"ℹ️ User already exists: {username}")
            else:
                # Create user
                resp = await client.post(
                    f"{logto_endpoint}/api/users",
                    headers=headers,
                    json={
                        "username": safe_username,
                        "email": email,
                        "password": password,
                    }
                )
                if resp.status_code != 201:
                    print(f"❌ Failed to create user '{username}': {resp.text}")
                    continue
                user_id = resp.json()["id"]
                print(f"✅ Created user: {username}")

            # Convert role names to role IDs
            role_ids = [role_mapping.get(role) for role in roles if role_mapping.get(role)]

            # If there are role IDs, assign them via POST request to /api/roles/{id}/users
            for role_id in role_ids:
                post_resp = await client.post(
                    f"{logto_endpoint}/api/roles/{role_id}/users",  # Post request to assign role to user
                    headers=headers,
                    json={"userIds": [user_id]}  # Pass user_id in userIds array
                )
                if post_resp.status_code == 201:
                    print(f"✅ Assigned role {role_id} to {username}")
                else:
                    print(f"❌ Failed to assign role {role_id} to {username}: {post_resp.text}")

            user_name_to_id[safe_username] = user_id

        except Exception as e:
            print(f"❌ Exception while processing user '{username}': {e}")
            continue

    return user_name_to_id



async def assign_roles_to_users(client: httpx.AsyncClient, headers: dict, users: list, role_name_to_id: dict,
                                user_name_to_id: dict):
    for user in users:
        username = user["username"]
        if username.isdigit():
            username = f"user_{username}"

        role = user["role"]
        user_id = user_name_to_id.get(username)
        role_id = role_name_to_id.get(role)

        if not user_id or not role_id:
            print(f"⚠️ Cannot assign role '{role}' to user '{username}' — missing ID.")
            continue

        try:
            await client.put(
                f"{logto_endpoint}/api/users/{user_id}/roles",
                json={"roles": [role]},
                headers=headers
            )
            print(f"✅ Assigned role '{role}' to user '{username}'")
        except Exception as e:
            print(f"❌ Failed to assign role to user '{username}': {e}")


# async def seed_roles_and_users(access_token: str, seed_data: dict):
#     if not all(k in seed_data for k in ("resource", "permissions", "roles", "users")):
#         raise ValueError("Seed data must include 'resource', 'permissions', 'roles', and 'users'.")
#
#     headers = {
#         "Authorization": f"Bearer {access_token}",
#         "scope": "all",
#         "Content-Type": "application/json"
#     }
#
#     async with httpx.AsyncClient() as client:
#         await create_resource_if_missing(client, headers, seed_data["resource"])
#         role_name_to_id = await create_roles_and_assign_permissions(client, headers, seed_data["roles"])
#         user_name_to_id = await create_users(client, headers, seed_data["users"])
#         await assign_roles_to_users(client, headers, seed_data["users"], role_name_to_id, user_name_to_id)




def create_resources_with_scopes(access_token, resources):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    with httpx.Client() as client:
        for resource in resources:
            res_data = {
                "name": resource["name"],
                "indicator": resource.get("indicator", resource["name"]),
                "isDefault": False,
                "accessTokenTtl": 3600,
                "scopes": [
                    {
                        "name": scope,
                        "description": f"Permission to {scope.replace(':', ' ')}"
                    }
                    for scope in resource["scopes"]
                ]
            }

            # **Create resource**
            response = client.post(f"{logto_endpoint}/api/resources", json=res_data, headers=headers)
            response.raise_for_status()
            resource_data = response.json()
            resource_id = resource_data.get("id")  # Assuming the API returns the resource ID

            print(f"Created resource: {resource['name']} ✅ (ID: {resource_id})")

            # **Create scopes for the generated resource ID**
            for scope in resource["scopes"]:
                scope_data = {
                    "name": scope,
                    "description": f"Permission to {scope.replace(':', ' ')}"
                }
                scope_response = client.post(f"{logto_endpoint}/api/resources/{resource_id}/scopes", json=scope_data, headers=headers)
                scope_response.raise_for_status()
                print(f"Added scope: {scope} to resource {resource_id} ✅")

    return "success"




def create_roles_logto(access_token: str, roles: list):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    with httpx.Client() as client:
        for role in roles:
            # Step 1: Create the role
            role_payload = {
                "name": role["name"],
                "description": role["description"]
            }

            response = client.post(f"{logto_endpoint}/api/roles", json=role_payload, headers=headers)
            print(f"response {response}")
            response.raise_for_status()
            role_data = response.json()
            print(f"role_data {role_data}")

            role_id = role_data.get("id")

            print(f"role_id {role_id}")

            print(f"✅ Created role: {role['name']} (ID: {role_id})")

            # Step 2: Assign scopes (permissions)
            permissions = role.get("permissions", [])
            print(f"permissions {permissions}")

            if permissions:
                scope_payload = {"scopeIds": permissions}
                scope_response = client.post(
                    f"{logto_endpoint}/api/roles/{role_id}/scopes",
                    json=scope_payload,
                    headers=headers
                )
                scope_response.raise_for_status()
                print(f"✅ Assigned scopes to role {role['name']}: {permissions}")

    return "✅ All roles created and permissions assigned"



async def find_user_by_phone_number(msisdn: str) -> Optional[str]:
    access_token = await fetch_access_token()
    headers = {
            "Authorization": f"Bearer {access_token}",
            "scope": "all",
            "Content-Type": "application/json"
        }
    async with httpx.AsyncClient() as client:
        res = await client.get(
            f"{logto_endpoint}/api/users",
            headers=headers
        )
        users = res.json()
        print(f"users {users}")
        for user in users:
            if user.get("primaryPhone") == msisdn:
                print(f"{user['id']}")
                return user["id"]


    return None


async def get_user_roles(user_id: str) -> list[str]:
    access_token = await fetch_access_token()
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    async with httpx.AsyncClient() as client:
        res = await client.get(
            f"{logto_endpoint}/api/users/{user_id}/roles",
            headers=headers
        )
        res.raise_for_status()
        roles = res.json()
        print(f"roles {roles}")
        return [role["name"] for role in roles]





async def create_user_and_assign_role( username: str, phone_number: str, session_id: str, role_name: str) -> bool:
    access_token = await fetch_access_token()
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    role_id  = await get_role_id(role_name)
    print(f"role_id: {role_id}")
    """
    Create a user, retrieve the user ID, and assign a specified role.

    Args:
        client: The HTTP client instance.
        headers: Headers for the request (e.g., authorization).
        username: The username of the user.
        email: The user's email.
        phone_number: The user's phone number.
        session_id: The session ID to be used as the password.
        role_name: The role to be assigned.
        role_mapping: Dictionary that maps role names to role IDs.

    Returns:
        True if the user is created and the role is successfully assigned, False otherwise.
    """
    # Clean username (Logto requires alphanumeric usernames)
    safe_username = "".join(c if c.isalnum() else "_" for c in username.lower())
    print(f"safe_username: {safe_username}")

    try:
      async with httpx.AsyncClient() as client:
        # Create user
        resp = await client.post(
            f"{logto_endpoint}/api/users",
            headers=headers,
            json={
                "username": safe_username,
                "phoneNumber": phone_number,
                "password": session_id,  # Using session ID as password
            }
        )

        if not (200 <= resp.status_code < 300):
            print(f"❌ Failed to create user '{username}': {resp.text}")
            return False

        user_id = resp.json()["id"]
        print(f"✅ Created user: {username} (ID: {user_id})")

        # Get role ID from mapping
        if not role_id:
            print(f"❌ Role '{role_name}' not found in mapping.")
            return False

        # Assign role to user
        post_resp = await client.post(
            f"{logto_endpoint}/api/roles/{role_id}/users",
            headers=headers,
            json={"userIds": [user_id]}
        )

        if not (200 <= post_resp.status_code < 300):
            print(f"✅ Assigned role '{role_name}' ({role_id}) to user {username}")
            return True
        else:
            print(f"❌ Failed to assign role '{role_name}' to user {username}: {post_resp.text}")
            return False

    except Exception as e:
        print(f"❌ Exception while creating user '{username}': {e}")
        return False


async def get_role_id( role_name: str) -> Optional[str]:
    access_token = await fetch_access_token()
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    """
    Retrieve role ID dynamically by querying the API.

    Args:
        client: The HTTP client instance.
        headers: Headers for the request (e.g., authorization).
        role_name: The name of the role.

    Returns:
        The role ID if found, otherwise None.
    """
    try:
      async with httpx.AsyncClient() as client:
        resp = await client.get(f"{logto_endpoint}/api/roles", headers=headers)

        if resp.status_code != 200:
            print(f"❌ Failed to fetch roles: {resp.text}")
            return None

        roles = resp.json()
        for role in roles:
            if role["name"] == role_name:
                print(f"✅ Found role ID for '{role_name}': {role['id']}")
                return role["id"]

        print(f"❌ Role '{role_name}' not found.")
        return None

    except Exception as e:
        print(f"❌ Exception while retrieving role ID for '{role_name}': {e}")
        return None
