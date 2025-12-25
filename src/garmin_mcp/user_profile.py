"""
User Profile functions for Garmin Connect MCP Server
"""
import datetime
from typing import Any, Dict, List, Optional, Union

# The garmin_client will be set by the main file
garmin_client = None


def configure(client):
    """Configure the module with the Garmin client instance"""
    global garmin_client
    garmin_client = client


def register_tools(app):
    """Register all user profile tools with the MCP server app"""
    
    @app.tool()
    async def get_full_name() -> str:
        """Get user's full name from profile"""
        try:
            full_name = garmin_client.get_full_name()
            return full_name
        except Exception as e:
            return f"Error retrieving user's full name: {str(e)}"

    @app.tool()
    async def get_unit_system() -> str:
        """Get user's preferred unit system from profile"""
        try:
            unit_system = garmin_client.get_unit_system()
            return unit_system
        except Exception as e:
            return f"Error retrieving unit system: {str(e)}"
    
    @app.tool()
    async def get_user_profile() -> str:
        """Get user profile information"""
        try:
            profile = garmin_client.get_user_profile()
            if not profile:
                return "No user profile information found."
            return profile
        except Exception as e:
            return f"Error retrieving user profile: {str(e)}"

    @app.tool()
    async def get_userprofile_settings() -> str:
        """Get user profile settings"""
        try:
            settings = garmin_client.get_userprofile_settings()
            if not settings:
                return "No user profile settings found."
            return settings
        except Exception as e:
            return f"Error retrieving user profile settings: {str(e)}"

    @app.tool()
    async def get_heart_rate_zones() -> str:
        """Get user's heart rate zones and max heart rate setting

        Returns the configured max heart rate and heart rate zone boundaries
        used for training zone calculations. Includes resting HR and lactate
        threshold HR if available.
        """
        try:
            # Use the biometric service endpoint for HR zones
            hr_zones = garmin_client.connectapi("/biometric-service/heartRateZones")

            if not hr_zones:
                return "No heart rate zone data found."

            # Handle list response (may contain sport-specific zones)
            if isinstance(hr_zones, list):
                # Find DEFAULT sport zones, or return all if no default
                default_zones = next(
                    (z for z in hr_zones if z.get("sport") == "DEFAULT"),
                    hr_zones[0] if hr_zones else None
                )
                if default_zones:
                    return {
                        "maxHeartRate": default_zones.get("maxHeartRateUsed"),
                        "restingHeartRate": default_zones.get("restingHeartRateUsed"),
                        "lactateThresholdHeartRate": default_zones.get("lactateThresholdHeartRateUsed"),
                        "trainingMethod": default_zones.get("trainingMethod"),
                        "zones": {
                            "zone1Floor": default_zones.get("zone1Floor"),
                            "zone2Floor": default_zones.get("zone2Floor"),
                            "zone3Floor": default_zones.get("zone3Floor"),
                            "zone4Floor": default_zones.get("zone4Floor"),
                            "zone5Floor": default_zones.get("zone5Floor"),
                        },
                        "sport": default_zones.get("sport"),
                        "allSportZones": hr_zones if len(hr_zones) > 1 else None
                    }

            return hr_zones

        except Exception as e:
            return f"Error retrieving heart rate zones: {str(e)}"

    return app