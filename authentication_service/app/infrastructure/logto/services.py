import uuid
from importlib import resources

from fastapi import FastAPI, HTTPException
import httpx
import time

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


async def create_users(client: httpx.AsyncClient, headers: dict, users: list) -> dict:
    user_name_to_id = {}
    for user in users:
        username = user["username"]
        phone = user["primaryPhone"]

        if username.isdigit():
            username = f"user_{username}"

        try:
            resp = await client.get(f"{logto_endpoint}/api/users?username={username}", headers=headers)
            existing_users = resp.json()
            if existing_users:
                user_id = existing_users[0]["id"]
            else:
                resp = await client.post(
                    f"{logto_endpoint}/api/users",
                    json={"username": username, "primaryPhone": phone},
                    headers=headers
                )
                if resp.status_code != 201:
                    print(f"❌ Failed to create user '{username}': {resp.text}")
                    continue
                user_id = resp.json()["id"]
                print(f"✅ Created user: {username}")
        except Exception as e:
            print(f"❌ Exception while creating user '{username}': {e}")
            continue

        user_name_to_id[username] = user_id
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


async def seed_roles_and_users(access_token: str, seed_data: dict):
    if not all(k in seed_data for k in ("resource", "permissions", "roles", "users")):
        raise ValueError("Seed data must include 'resource', 'permissions', 'roles', and 'users'.")

    headers = {
        "Authorization": f"Bearer {access_token}",
        "scope": "all",
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient() as client:
        await create_resource_if_missing(client, headers, seed_data["resource"])
        role_name_to_id = await create_roles_and_assign_permissions(client, headers, seed_data["roles"])
        user_name_to_id = await create_users(client, headers, seed_data["users"])
        await assign_roles_to_users(client, headers, seed_data["users"], role_name_to_id, user_name_to_id)


# def create_resources(access_token, resources) :
#     headers = {
#         "Authorization": f"Bearer {access_token}",
#         "Content-Type": "application/json"
#     }
#
#     with httpx.Client() as client:
#         for resource in resources:
#             res_data = {
#                 "name": resource["name"],
#                 "indicator": resource.get("indicator", resource["name"]),
#                 "isDefault": False,
#                 "accessTokenTtl": 3600,
#                 "scopes": [
#                     {
#                         "name": scope,
#                         "description": f"Permission to {scope.replace(':', ' ')}"
#                     }
#                     for scope in resource["scopes"]
#                 ]
#             }
#             response = client.post(f"{logto_endpoint}/api/resources", json=res_data, headers=headers)
#             response.raise_for_status()
#             print(f"Created resource: {resource['name']} ✅")
#
#
#     return "success"


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




def create_roles_logto(access_token, roles):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    with httpx.Client() as client:
        for role in roles:
            # Create the role
            response = client.post(f"{logto_endpoint}/api/roles", json=role, headers=headers)
            response.raise_for_status()
            role_data = response.json()
            role_id = role_data.get("id")  # Assuming the API returns the resource ID
            print(f"Created role: {role['name']} ✅")

            # Wrap permissions into the expected payload shape
            permissions = role.get("permissions", [])
            scope_payload = {"scopeIds": permissions}
            print(f"Assigning scopes: {scope_payload} to role {role_id} ✅")

            # Assign scopes to the role
            scope_response = client.post(
                f"{logto_endpoint}/api/roles/{role_id}/scopes",
                json=scope_payload,
                headers=headers
            )
            scope_response.raise_for_status()
            print(f"Added scopes to role {role_id}: {scope_response.status_code} ✅")

    return "Roles created successfully and permissions assigned"