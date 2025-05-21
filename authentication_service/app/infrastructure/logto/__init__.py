
import httpx
from app.core.config import settings
from app.infrastructure.logto.services import fetch_access_token
from app.infrastructure.logto.utils import load_json_part
from app.infrastructure.logto.services import create_users


logto_endpoint = settings.logto_endpoint
token_endpoint = settings.logto_token_endpoint
application_id = settings.logto_app_id
application_secret = settings.logto_app_secret
admin_api_resource = settings.admin_api_resource or "default"
logto_json_path = settings.logto_json_path






async def seed_logto_resources_and_roles(file_path: str):
    raw_resources = load_json_part(file_path, "resources")
    raw_roles = load_json_part(file_path, "roles")
    raw_users = load_json_part(file_path, "users")

    resources = [
        {
            "tenantId": "default",
            "name": res["name"],
            "indicator": res["name"],
            "accessTokenTtl": 3600,
            "scopes": [{"name": scope, "description": ""} for scope in res["scopes"]]
        }
        for res in raw_resources
    ]

    roles = [
        {
            "tenantId": "default",
            "name": role["name"],
            "description": role["description"],
            "type": role["type"],
            "isDefault": role["name"] == "mobile_user",
            "scopes": role["scopes"]
        }
        for role in raw_roles
    ]

    users = [
        {
            "username": user["username"],
            "email": user["email"],
            "primaryPhone" : user["primaryPhone"],
            "password": user["password"],
            "roles": user["roles"]
        }
        for user in raw_users
    ]
    print(f"users {users}")
    access_token = await fetch_access_token()
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient() as client:
        resource_map = {}
        scope_lookup = {}

        # Step 1: Create resources and scopes
        res_check = await client.get(f"{logto_endpoint}/api/resources", headers=headers)
        res_check.raise_for_status()
        all_resources = res_check.json()

        for resource in resources:
            existing_resource = next((r for r in all_resources if r["name"] == resource["name"]), None)

            if existing_resource:
                print(f"ℹ️ Resource '{resource['name']}' already exists.")
                resource_id = existing_resource["id"]
                resource_map[resource["name"]] = existing_resource

                # Fetch existing scopes for this resource
                existing_scopes_res = await client.get(
                    f"{logto_endpoint}/api/resources/{resource_id}/scopes",
                    headers=headers
                )
                existing_scopes_res.raise_for_status()
                existing_scopes = existing_scopes_res.json()
                existing_scope_names = {s["name"]: s for s in existing_scopes}
            else:
                # Create the resource
                res_body = {
                    "tenantId": resource["tenantId"],
                    "name": resource["name"],
                    "indicator": resource["indicator"],
                    "accessTokenTtl": resource["accessTokenTtl"]
                }

                res = await client.post(f"{logto_endpoint}/api/resources", headers=headers, json=res_body)
                res.raise_for_status()
                print(f"✅ Created resource '{resource['name']}'")

                resource_data = res.json()
                resource_id = resource_data["id"]
                resource_map[resource["name"]] = resource_data
                existing_scope_names = {}

            # Create missing scopes and populate scope_lookup
            for scope in resource["scopes"]:
                if scope["name"] in existing_scope_names:
                    scope_data = existing_scope_names[scope["name"]]
                    print(f"ℹ️ Scope '{scope['name']}' already exists in resource '{resource['name']}'")
                else:
                    scope_body = {
                        "name": scope["name"],
                        "description": scope["description"]
                    }
                    scope_res = await client.post(
                        f"{logto_endpoint}/api/resources/{resource_id}/scopes",
                        headers=headers,
                        json=scope_body
                    )
                    scope_res.raise_for_status()
                    scope_data = scope_res.json()
                    print(f"✅ Created scope '{scope['name']}' in resource '{resource['name']}'")

                scope_lookup[scope_data["name"]] = scope_data["id"]

        # Step 2: Create roles and attach scopes
        role_id_map = {}
        role_check = await client.get(f"{logto_endpoint}/api/roles", headers=headers)
        role_check.raise_for_status()
        all_roles = role_check.json()



        print("roles", roles, flush=True)

        for role in roles:
            # Check if the role already exists
            existing_role = next((r for r in all_roles if r["name"] == role["name"]), None)

            if existing_role:
                print(f"ℹ️ Role '{role['name']}' already exists.")
                role_id = existing_role["id"]
            else:
                # Create the role
                role_body = {
                    "tenantId": role["tenantId"],
                    "name": role["name"],
                    "description": role["description"],
                    "type": role["type"],
                    "isDefault": role["isDefault"],
                    "scopes": role["scopes"]
                }
                role_res = await client.post(f"{logto_endpoint}/api/roles", headers=headers, json=role_body)
                role_res.raise_for_status()
                role_data = role_res.json()
                role_id = role_data["id"]
                print(f"✅ Created role '{role['name']}'")

            # Map role name to its ID
            role_id_map[role["name"]] = role_id

            # Always attempt to attach scopes, regardless of whether the role existed
            print(f"🔍 scope lookup: {scope_lookup}")
            scope_ids = [
                scope_lookup[scope_name]
                for scope_name in role["scopes"]
                if scope_name in scope_lookup
            ]
            print(f"🔗 scope_ids: {scope_ids}")

            if scope_ids:
                attach_res = await client.post(
                    f"{logto_endpoint}/api/roles/{role_id}/scopes",
                    headers=headers,
                    json={"scopeIds": scope_ids}
                )
                attach_res.raise_for_status()
                print(f"✅ Attached scopes to role '{role['name']}'")

        # Step 3: Create users and assign roles
        user_name_to_id = {}

        user_check_resp = await client.get(f"{logto_endpoint}/api/users", headers=headers)
        user_check_resp.raise_for_status()
        all_users = user_check_resp.json()

        for user in users:
            username = user["username"]
            email = user["email"]
            password = user["password"]
            phone_number = user["primaryPhone"]
            roles = user.get("roles", [])

            existing_user = next((u for u in all_users if u["username"] == username), None)

            if existing_user:
                user_id = existing_user["id"]
                print(f"ℹ️ User '{username}' already exists.")
            else:
                user_resp = await client.post(
                    f"{logto_endpoint}/api/users",
                    headers=headers,
                    json={"username": username, "email": email, "password": password ,"primaryPhone": phone_number}
                )
                user_resp.raise_for_status()
                user_id = user_resp.json()["id"]
                print(f"✅ Created user: {username}")

            user_name_to_id[username] = user_id

            for role_name in roles:
                role_id = role_id_map.get(role_name)
                if not role_id:
                    print(f"⚠️ Role '{role_name}' not found, skipping assignment for user '{username}'.")
                    continue

                # Check if user already has this role
                role_users_resp = await client.get(
                    f"{logto_endpoint}/api/roles/{role_id}/users",
                    headers=headers
                )
                role_users_resp.raise_for_status()
                assigned_users = role_users_resp.json()
                already_assigned = any(u["id"] == user_id for u in assigned_users)

                if already_assigned:
                    print(f"ℹ️ User '{username}' already has role '{role_name}', skipping.")
                    continue


                print(f"userID {user_id}")
                print(f"roleID {role_id}")
                assign_resp = await client.post(
                    f"{logto_endpoint}/api/roles/{role_id}/users",
                    headers=headers,
                    json={"userIds": [user_id]}
                )
                print(f"role {role_name} assignment for user '{username}' .",flush=True)
                print(f"assign_resp {assign_resp.status_code}",flush=True)
                print(f"assign_resp {assign_resp.json()}",flush=True)
                assign_resp.raise_for_status()
                print(f"✅ Assigned role '{role_name}' to '{username}'")

        return {
            "resources": resource_map,
            "scopes": scope_lookup,
            "roles": role_id_map,
            "users": user_name_to_id
        }

