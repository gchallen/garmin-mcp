"""
Health & Wellness Data functions for Garmin Connect MCP Server
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
    """Register all health and wellness tools with the MCP server app"""
    
    @app.tool(structured_output=False)
    async def get_stats(date: str) -> str:
        """Get daily activity stats
        
        Args:
            date: Date in YYYY-MM-DD format
        """
        try:
            stats = garmin_client.get_stats(date)
            if not stats:
                return f"No stats found for {date}"
            
            return stats
        except Exception as e:
            return f"Error retrieving stats: {str(e)}"

    @app.tool(structured_output=False)
    async def get_user_summary(date: str) -> str:
        """Get user summary data (compatible with garminconnect-ha)
        
        Args:
            date: Date in YYYY-MM-DD format
        """
        try:
            summary = garmin_client.get_user_summary(date)
            if not summary:
                return f"No user summary found for {date}"
            
            return summary
        except Exception as e:
            return f"Error retrieving user summary: {str(e)}"

    @app.tool(structured_output=False)
    async def get_body_composition(start_date: str, end_date: str = None) -> str:
        """Get body composition data for a single date or date range
        
        Args:
            start_date: Date in YYYY-MM-DD format or start date if end_date provided
            end_date: Optional end date in YYYY-MM-DD format for date range
        """
        try:
            if end_date:
                composition = garmin_client.get_body_composition(start_date, end_date)
                if not composition:
                    return f"No body composition data found between {start_date} and {end_date}"
            else:
                composition = garmin_client.get_body_composition(start_date)
                if not composition:
                    return f"No body composition data found for {start_date}"
            
            return composition
        except Exception as e:
            return f"Error retrieving body composition data: {str(e)}"

    @app.tool(structured_output=False)
    async def get_stats_and_body(date: str) -> str:
        """Get stats and body composition data
        
        Args:
            date: Date in YYYY-MM-DD format
        """
        try:
            data = garmin_client.get_stats_and_body(date)
            if not data:
                return f"No stats and body composition data found for {date}"
            
            return data
        except Exception as e:
            return f"Error retrieving stats and body composition data: {str(e)}"

    @app.tool(structured_output=False)
    async def get_steps_data(date: str, hourly_only: bool = False) -> str:
        """Get steps data with optional hourly aggregation

        Args:
            date: Date in YYYY-MM-DD format
            hourly_only: If True, return hourly totals instead of detailed interval data
        """
        try:
            steps_data = garmin_client.get_steps_data(date)
            if not steps_data:
                return f"No steps data found for {date}"

            if hourly_only and isinstance(steps_data, list):
                # Aggregate data by hour
                from collections import defaultdict
                hourly_data = defaultdict(int)

                for entry in steps_data:
                    if isinstance(entry, dict) and 'startGMT' in entry:
                        # Extract hour from timestamp
                        timestamp = entry.get('startGMT', '')
                        hour = timestamp[:13] if len(timestamp) >= 13 else timestamp  # Get up to hour
                        if 'steps' in entry:
                            hourly_data[hour] += entry['steps']

                # Convert to sorted list
                hourly_list = [{"hour": hour, "steps": steps} for hour, steps in sorted(hourly_data.items())]

                return {"date": date, "hourly_steps": hourly_list, "total_steps": sum(hourly_data.values())}

            return steps_data
        except Exception as e:
            return f"Error retrieving steps data: {str(e)}"

    @app.tool(structured_output=False)
    async def get_daily_steps(start_date: str, end_date: str) -> str:
        """Get steps data for a date range
        
        Args:
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
        """
        try:
            steps_data = garmin_client.get_daily_steps(start_date, end_date)
            if not steps_data:
                return f"No daily steps data found between {start_date} and {end_date}"
            
            return steps_data
        except Exception as e:
            return f"Error retrieving daily steps data: {str(e)}"

    @app.tool(structured_output=False)
    async def get_training_readiness(date: str) -> str:
        """Get training readiness data
        
        Args:
            date: Date in YYYY-MM-DD format
        """
        try:
            readiness = garmin_client.get_training_readiness(date)
            if not readiness:
                return f"No training readiness data found for {date}"
            
            return readiness
        except Exception as e:
            return f"Error retrieving training readiness data: {str(e)}"

    @app.tool(structured_output=False)
    async def get_body_battery(start_date: str, end_date: str) -> str:
        """Get body battery data
        
        Args:
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
        """
        try:
            battery_data = garmin_client.get_body_battery(start_date, end_date)
            if not battery_data:
                return f"No body battery data found between {start_date} and {end_date}"
            
            return battery_data
        except Exception as e:
            return f"Error retrieving body battery data: {str(e)}"

    @app.tool(structured_output=False)
    async def get_body_battery_events(date: str) -> str:
        """Get body battery events data
        
        Args:
            date: Date in YYYY-MM-DD format
        """
        try:
            events = garmin_client.get_body_battery_events(date)
            if not events:
                return f"No body battery events found for {date}"
            
            return events
        except Exception as e:
            return f"Error retrieving body battery events: {str(e)}"

    @app.tool(structured_output=False)
    async def get_blood_pressure(start_date: str, end_date: str) -> str:
        """Get blood pressure data
        
        Args:
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
        """
        try:
            bp_data = garmin_client.get_blood_pressure(start_date, end_date)
            if not bp_data:
                return f"No blood pressure data found between {start_date} and {end_date}"
            
            return bp_data
        except Exception as e:
            return f"Error retrieving blood pressure data: {str(e)}"

    @app.tool(structured_output=False)
    async def get_floors(date: str) -> str:
        """Get floors climbed data
        
        Args:
            date: Date in YYYY-MM-DD format
        """
        try:
            floors_data = garmin_client.get_floors(date)
            if not floors_data:
                return f"No floors data found for {date}"
            
            return floors_data
        except Exception as e:
            return f"Error retrieving floors data: {str(e)}"

    @app.tool(structured_output=False)
    async def get_training_status(date: str) -> str:
        """Get training status data
        
        Args:
            date: Date in YYYY-MM-DD format
        """
        try:
            status = garmin_client.get_training_status(date)
            if not status:
                return f"No training status data found for {date}"
            
            return status
        except Exception as e:
            return f"Error retrieving training status data: {str(e)}"

    @app.tool(structured_output=False)
    async def get_rhr_day(date: str) -> str:
        """Get resting heart rate data
        
        Args:
            date: Date in YYYY-MM-DD format
        """
        try:
            rhr_data = garmin_client.get_rhr_day(date)
            if not rhr_data:
                return f"No resting heart rate data found for {date}"
            
            return rhr_data
        except Exception as e:
            return f"Error retrieving resting heart rate data: {str(e)}"

    @app.tool(structured_output=False)
    async def get_heart_rates(date: str, hourly_only: bool = False) -> str:
        """Get heart rate data with optional hourly aggregation

        Args:
            date: Date in YYYY-MM-DD format
            hourly_only: If True, return hourly averages instead of detailed minute-by-minute data
        """
        try:
            hr_data = garmin_client.get_heart_rates(date)
            if not hr_data:
                return f"No heart rate data found for {date}"

            if hourly_only and isinstance(hr_data, list):
                # Aggregate data by hour
                from collections import defaultdict
                hourly_data = defaultdict(list)

                for entry in hr_data:
                    if isinstance(entry, dict) and 'timestampLocal' in entry:
                        # Extract hour from timestamp
                        timestamp = entry['timestampLocal']
                        hour = timestamp[:13] if len(timestamp) >= 13 else timestamp  # Get up to hour
                        if 'value' in entry:
                            hourly_data[hour].append(entry['value'])

                # Calculate averages
                hourly_avg = {}
                for hour, values in hourly_data.items():
                    if values:
                        hourly_avg[hour] = {
                            "avg": round(sum(values) / len(values), 1),
                            "min": min(values),
                            "max": max(values),
                            "count": len(values)
                        }

                return {"date": date, "hourly_heart_rate": hourly_avg}

            return hr_data
        except Exception as e:
            return f"Error retrieving heart rate data: {str(e)}"

    @app.tool(structured_output=False)
    async def get_hydration_data(date: str) -> str:
        """Get hydration data
        
        Args:
            date: Date in YYYY-MM-DD format
        """
        try:
            hydration_data = garmin_client.get_hydration_data(date)
            if not hydration_data:
                return f"No hydration data found for {date}"
            
            return hydration_data
        except Exception as e:
            return f"Error retrieving hydration data: {str(e)}"

    @app.tool(structured_output=False)
    async def get_sleep_data(date: str, part: str = "full") -> str:
        """Get sleep data with options for retrieving specific parts or summary

        Args:
            date: Date in YYYY-MM-DD format
            part: Which part to retrieve:
                - "full": Complete data (default, may be large)
                - "summary": Only summary metrics (sleep totals, scores, etc.)
                - "levels": Sleep level transitions throughout the night
                - "metrics": Heart rate, SpO2, and stress data during sleep
                - "metadata": Basic info about the sleep session
                - "page_1", "page_2", etc.: For paginated time-series data
        """
        try:
            sleep_data = garmin_client.get_sleep_data(date)
            if not sleep_data:
                return f"No sleep data found for {date}"

            if not isinstance(sleep_data, dict):
                return sleep_data

            # Handle different parts
            if part == "summary":
                # Extract only the summary metrics
                summary = {
                    "date": date,
                    "sleepTimeSeconds": sleep_data.get("sleepTimeSeconds"),
                    "napTimeSeconds": sleep_data.get("napTimeSeconds"),
                    "unmeasurableSleepSeconds": sleep_data.get("unmeasurableSleepSeconds"),
                    "deepSleepSeconds": sleep_data.get("deepSleepSeconds"),
                    "lightSleepSeconds": sleep_data.get("lightSleepSeconds"),
                    "remSleepSeconds": sleep_data.get("remSleepSeconds"),
                    "awakeSleepSeconds": sleep_data.get("awakeSleepSeconds"),
                    "sleepStartTimestampGMT": sleep_data.get("sleepStartTimestampGMT"),
                    "sleepEndTimestampGMT": sleep_data.get("sleepEndTimestampGMT"),
                    "averageSpO2Value": sleep_data.get("averageSpO2Value"),
                    "lowestSpO2Value": sleep_data.get("lowestSpO2Value"),
                    "highestSpO2Value": sleep_data.get("highestSpO2Value"),
                    "avgSleepStress": sleep_data.get("avgSleepStress"),
                    "restlessMomentsCount": sleep_data.get("restlessMomentsCount"),
                    "overallScore": sleep_data.get("dailySleepDTO", {}).get("overallScore") if "dailySleepDTO" in sleep_data else None
                }
                # Remove None values
                summary = {k: v for k, v in summary.items() if v is not None}
                return summary

            elif part == "metadata":
                # Basic metadata about the sleep session
                metadata = {
                    "date": date,
                    "sleepStartTimestampGMT": sleep_data.get("sleepStartTimestampGMT"),
                    "sleepEndTimestampGMT": sleep_data.get("sleepEndTimestampGMT"),
                    "sleepWindowConfirmed": sleep_data.get("sleepWindowConfirmed"),
                    "calendarDate": sleep_data.get("calendarDate"),
                    "id": sleep_data.get("id"),
                    "userProfilePK": sleep_data.get("userProfilePK"),
                    "sleepTimeSeconds": sleep_data.get("sleepTimeSeconds"),
                    "napTimeSeconds": sleep_data.get("napTimeSeconds")
                }
                return {k: v for k, v in metadata.items() if v is not None}

            elif part == "levels":
                # Sleep level transitions
                result = {
                    "date": date,
                    "sleepLevels": sleep_data.get("sleepLevels", [])
                }
                # Also include validation if available
                if "validation" in sleep_data:
                    result["validation"] = sleep_data.get("validation")
                return result

            elif part == "metrics":
                # Physiological metrics during sleep
                metrics = {
                    "date": date,
                    "timeOffsetSleepSpo2": sleep_data.get("timeOffsetSleepSpo2", {}),
                    "timeOffsetSleepRespiration": sleep_data.get("timeOffsetSleepRespiration", {}),
                    "remData": sleep_data.get("remData", {}),
                    "sleepStress": sleep_data.get("sleepStress", []),
                    "sleepMotion": sleep_data.get("sleepMotion", []),
                    "bodyBatteryChange": sleep_data.get("bodyBatteryChange"),
                    "restlessMomentsCount": sleep_data.get("restlessMomentsCount"),
                    "avgSleepStress": sleep_data.get("avgSleepStress"),
                    "averageSpO2Value": sleep_data.get("averageSpO2Value"),
                    "lowestSpO2Value": sleep_data.get("lowestSpO2Value"),
                    "highestSpO2Value": sleep_data.get("highestSpO2Value"),
                    "averageRespirationValue": sleep_data.get("averageRespirationValue"),
                    "lowestRespirationValue": sleep_data.get("lowestRespirationValue"),
                    "highestRespirationValue": sleep_data.get("highestRespirationValue")
                }
                return {k: v for k, v in metrics.items() if v is not None and v != {} and v != []}

            elif part.startswith("page_"):
                # Paginated access to time-series data
                try:
                    page_num = int(part.split("_")[1]) - 1  # Convert to 0-based index
                    items_per_page = 100

                    # Collect all time-series arrays
                    time_series = {}

                    # Get sleep levels if they exist
                    if "sleepLevels" in sleep_data and isinstance(sleep_data["sleepLevels"], list):
                        levels = sleep_data["sleepLevels"]
                        start_idx = page_num * items_per_page
                        end_idx = start_idx + items_per_page
                        time_series["sleepLevels"] = levels[start_idx:end_idx]
                        time_series["sleepLevels_total"] = len(levels)
                        time_series["sleepLevels_page"] = page_num + 1
                        time_series["sleepLevels_total_pages"] = (len(levels) + items_per_page - 1) // items_per_page

                    # Get sleep stress if it exists
                    if "sleepStress" in sleep_data and isinstance(sleep_data["sleepStress"], list):
                        stress = sleep_data["sleepStress"]
                        start_idx = page_num * items_per_page
                        end_idx = start_idx + items_per_page
                        time_series["sleepStress"] = stress[start_idx:end_idx]
                        time_series["sleepStress_total"] = len(stress)

                    # Get sleep motion if it exists
                    if "sleepMotion" in sleep_data and isinstance(sleep_data["sleepMotion"], list):
                        motion = sleep_data["sleepMotion"]
                        start_idx = page_num * items_per_page
                        end_idx = start_idx + items_per_page
                        time_series["sleepMotion"] = motion[start_idx:end_idx]
                        time_series["sleepMotion_total"] = len(motion)

                    if not time_series or all(not v for k, v in time_series.items() if not k.endswith("_total") and not k.endswith("_page") and not k.endswith("_total_pages")):
                        return f"No data available for page {page_num + 1}"

                    time_series["date"] = date
                    time_series["page_info"] = {
                        "current_page": page_num + 1,
                        "items_per_page": items_per_page,
                        "has_more": any(v for k, v in time_series.items() if k.endswith("_total") and v > (page_num + 1) * items_per_page)
                    }

                    return time_series

                except (ValueError, IndexError):
                    return f"Invalid page number. Use 'page_1', 'page_2', etc."

            else:  # "full" or any other value
                return sleep_data

        except Exception as e:
            return f"Error retrieving sleep data: {str(e)}"

    @app.tool(structured_output=False)
    async def get_stress_data(date: str, hourly_only: bool = False) -> str:
        """Get stress data with optional hourly aggregation

        Args:
            date: Date in YYYY-MM-DD format
            hourly_only: If True, return hourly averages instead of detailed minute-by-minute data
        """
        try:
            stress_data = garmin_client.get_stress_data(date)
            if not stress_data:
                return f"No stress data found for {date}"

            if hourly_only and isinstance(stress_data, list):
                # Aggregate data by hour
                from collections import defaultdict
                hourly_data = defaultdict(list)

                for entry in stress_data:
                    if isinstance(entry, dict) and 'timestampLocal' in entry:
                        # Extract hour from timestamp
                        timestamp = entry['timestampLocal']
                        hour = timestamp[:13] if len(timestamp) >= 13 else timestamp  # Get up to hour
                        if 'value' in entry:
                            hourly_data[hour].append(entry['value'])

                # Calculate averages
                hourly_avg = {}
                for hour, values in hourly_data.items():
                    if values:
                        hourly_avg[hour] = {
                            "avg": round(sum(values) / len(values), 1),
                            "min": min(values),
                            "max": max(values),
                            "count": len(values)
                        }

                return {"date": date, "hourly_stress": hourly_avg}

            return stress_data
        except Exception as e:
            return f"Error retrieving stress data: {str(e)}"

    @app.tool(structured_output=False)
    async def get_respiration_data(date: str) -> str:
        """Get respiration data
        
        Args:
            date: Date in YYYY-MM-DD format
        """
        try:
            respiration_data = garmin_client.get_respiration_data(date)
            if not respiration_data:
                return f"No respiration data found for {date}"
            
            return respiration_data
        except Exception as e:
            return f"Error retrieving respiration data: {str(e)}"

    @app.tool(structured_output=False)
    async def get_spo2_data(date: str) -> str:
        """Get SpO2 (blood oxygen) data
        
        Args:
            date: Date in YYYY-MM-DD format
        """
        try:
            spo2_data = garmin_client.get_spo2_data(date)
            if not spo2_data:
                return f"No SpO2 data found for {date}"
            
            return spo2_data
        except Exception as e:
            return f"Error retrieving SpO2 data: {str(e)}"

    @app.tool(structured_output=False)
    async def get_all_day_stress(date: str, hourly_only: bool = False) -> str:
        """Get all-day stress data with optional hourly aggregation

        Args:
            date: Date in YYYY-MM-DD format
            hourly_only: If True, return hourly averages instead of detailed data
        """
        try:
            stress_data = garmin_client.get_all_day_stress(date)
            if not stress_data:
                return f"No all-day stress data found for {date}"

            if hourly_only and isinstance(stress_data, list):
                # Aggregate data by hour
                from collections import defaultdict
                hourly_data = defaultdict(list)

                for entry in stress_data:
                    if isinstance(entry, dict) and 'timestampLocal' in entry:
                        # Extract hour from timestamp
                        timestamp = entry['timestampLocal']
                        hour = timestamp[:13] if len(timestamp) >= 13 else timestamp  # Get up to hour
                        if 'value' in entry:
                            hourly_data[hour].append(entry['value'])

                # Calculate averages
                hourly_avg = {}
                for hour, values in hourly_data.items():
                    if values:
                        hourly_avg[hour] = {
                            "avg": round(sum(values) / len(values), 1),
                            "min": min(values),
                            "max": max(values),
                            "count": len(values)
                        }

                return {"date": date, "hourly_all_day_stress": hourly_avg}

            return stress_data
        except Exception as e:
            return f"Error retrieving all-day stress data: {str(e)}"

    @app.tool(structured_output=False)
    async def get_all_day_events(date: str) -> str:
        """Get daily wellness events data
        
        Args:
            date: Date in YYYY-MM-DD format
        """
        try:
            events = garmin_client.get_all_day_events(date)
            if not events:
                return f"No daily wellness events found for {date}"
            
            return events
        except Exception as e:
            return f"Error retrieving daily wellness events: {str(e)}"

    return app