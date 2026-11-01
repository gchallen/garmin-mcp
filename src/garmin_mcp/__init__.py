"""
Modular MCP Server for Garmin Connect Data
"""

import os

import requests
from mcp.server.fastmcp import FastMCP

from garth.exc import GarthHTTPError
from garminconnect import Garmin, GarminConnectAuthenticationError

# Import all modules
from garmin_mcp import activity_management
from garmin_mcp import health_wellness
from garmin_mcp import user_profile
from garmin_mcp import devices
from garmin_mcp import gear_management
from garmin_mcp import weight_management
from garmin_mcp import challenges
from garmin_mcp import training
from garmin_mcp import workouts
from garmin_mcp import data_management
from garmin_mcp import womens_health

def get_mfa() -> str:
    """Get MFA code from user input"""
    print("\nGarmin Connect MFA required. Please check your email/phone for the code.")
    return input("Enter MFA code: ")

# Get credentials from environment
email = os.environ.get("GARMIN_EMAIL")
password = os.environ.get("GARMIN_PASSWORD")
tokenstore = os.getenv("GARMINTOKENS") or "~/.garminconnect"
tokenstore_base64 = os.getenv("GARMINTOKENS_BASE64") or "~/.garminconnect_base64"


def init_api(email, password):
    """Initialize Garmin API with your credentials."""

    try:
        # Using Oauth1 and OAuth2 token files from directory
        print(
            f"Trying to login to Garmin Connect using token data from directory '{tokenstore}'...\n"
        )

        # Using Oauth1 and Oauth2 tokens from base64 encoded string
        # print(
        #     f"Trying to login to Garmin Connect using token data from file '{tokenstore_base64}'...\n"
        # )
        # dir_path = os.path.expanduser(tokenstore_base64)
        # with open(dir_path, "r") as token_file:
        #     tokenstore = token_file.read()

        garmin = Garmin()
        garmin.login(tokenstore)

    except (FileNotFoundError, GarthHTTPError, GarminConnectAuthenticationError):
        # Session is expired. You'll need to log in again
        print(
            "Login tokens not present, login with your Garmin Connect credentials to generate them.\n"
            f"They will be stored in '{tokenstore}' for future use.\n"
        )
        try:
            garmin = Garmin(
                email=email, password=password, is_cn=False, prompt_mfa=get_mfa
            )
            garmin.login()
            # Save Oauth1 and Oauth2 token files to directory for next login
            garmin.garth.dump(tokenstore)
            print(
                f"Oauth tokens stored in '{tokenstore}' directory for future use. (first method)\n"
            )
            # Encode Oauth1 and Oauth2 tokens to base64 string and safe to file for next login (alternative way)
            token_base64 = garmin.garth.dumps()
            dir_path = os.path.expanduser(tokenstore_base64)
            with open(dir_path, "w") as token_file:
                token_file.write(token_base64)
            print(
                f"Oauth tokens encoded as base64 string and saved to '{dir_path}' file for future use. (second method)\n"
            )
        except (
            FileNotFoundError,
            GarthHTTPError,
            GarminConnectAuthenticationError,
            requests.exceptions.HTTPError,
        ) as err:
            print(err)
            return None

    return garmin


def main():
    """Initialize the MCP server and register all tools"""

    # Initialize Garmin client
    garmin_client = init_api(email, password)
    if not garmin_client:
        print("Failed to initialize Garmin Connect client. Exiting.")
        return

    print("Garmin Connect client initialized successfully.")

    # Configure all modules with the Garmin client
    activity_management.configure(garmin_client)
    health_wellness.configure(garmin_client)
    user_profile.configure(garmin_client)
    devices.configure(garmin_client)
    gear_management.configure(garmin_client)
    weight_management.configure(garmin_client)
    challenges.configure(garmin_client)
    training.configure(garmin_client)
    workouts.configure(garmin_client)
    data_management.configure(garmin_client)
    womens_health.configure(garmin_client)

    # Create the MCP app
    app = FastMCP("Garmin Connect v1.0")

    # Register tools from all modules
    app = activity_management.register_tools(app)
    app = health_wellness.register_tools(app)
    app = user_profile.register_tools(app)
    app = devices.register_tools(app)
    app = gear_management.register_tools(app)
    app = weight_management.register_tools(app)
    app = challenges.register_tools(app)
    app = training.register_tools(app)
    app = workouts.register_tools(app)
    app = data_management.register_tools(app)
    app = womens_health.register_tools(app)

    # Add activity listing tool directly to the app
    @app.tool(structured_output=False)
    async def list_activities(limit: int = 5, offset: int = 0, summary_only: bool = False) -> str:
        """List recent Garmin activities with pagination support

        Args:
            limit: Maximum number of activities to return (default 5, max 100)
            offset: Number of activities to skip (for pagination)
            summary_only: If True, return only basic info (name, type, date, ID) without detailed metrics
        """
        try:
            # Cap the limit to prevent excessive data
            limit = min(limit, 100)
            activities = garmin_client.get_activities(offset, limit)

            if not activities:
                return f"No activities found at offset {offset}."

            result = f"Activities {offset + 1} to {offset + len(activities)}:\n\n"
            for idx, activity in enumerate(activities, 1):
                result += f"--- Activity {offset + idx} ---\n"
                result += f"Activity: {activity.get('activityName', 'Unknown')}\n"
                result += (
                    f"Type: {activity.get('activityType', {}).get('typeKey', 'Unknown')}\n"
                )
                result += f"Date: {activity.get('startTimeLocal', 'Unknown')}\n"
                result += f"ID: {activity.get('activityId', 'Unknown')}\n"

                if not summary_only:
                    # Add key metrics when not in summary mode
                    if 'distance' in activity:
                        result += f"Distance: {activity.get('distance', 0) / 1000:.2f} km\n"
                    if 'duration' in activity:
                        duration_sec = activity.get('duration', 0)
                        hours = int(duration_sec // 3600)
                        minutes = int((duration_sec % 3600) // 60)
                        seconds = int(duration_sec % 60)
                        result += f"Duration: {hours:02d}:{minutes:02d}:{seconds:02d}\n"
                    if 'averageHR' in activity:
                        result += f"Avg HR: {activity.get('averageHR')} bpm\n"
                    if 'calories' in activity:
                        result += f"Calories: {activity.get('calories')}\n"

                result += "\n"

            # Add pagination info
            result += f"\nShowing {len(activities)} activities starting from position {offset + 1}\n"
            if len(activities) == limit:
                result += f"Use offset={offset + limit} to see the next {limit} activities."

            return result
        except Exception as e:
            return f"Error retrieving activities: {str(e)}"

    # Run the MCP server
    app.run()


if __name__ == "__main__":
    main()
