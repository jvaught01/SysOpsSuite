import json
import logging
from channels.generic.websocket import WebsocketConsumer
from Backups.models import Backup
from django.db.models import Q

# Set up logging
logger = logging.getLogger(__name__)


class SearchConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        logger.debug("WebSocket connection established.")
        print("WebSocket connection established.")  # Debug print
        self.send(
            text_data=json.dumps(
                {
                    "type": "connection_established",
                    "message": "WebSocket connection established for search.",
                }
            )
        )

    def disconnect(self, close_code):
        logger.debug(f"WebSocket connection closed with code {close_code}.")
        print(f"WebSocket connection closed with code {close_code}.")  # Debug print

    def receive(self, text_data):
        print(f"Received text_data: {text_data}")  # Debug print
        data = json.loads(text_data)
        logger.debug(f"Received data: {data}")

        if data.get("type") == "search":
            print("Received search request.")  # Debug print
            search_term = data.get("search_term", "")
            filter_by = data.get("filter", "all")

            logger.debug(
                f"Searching for term '{search_term}' with filter '{filter_by}'."
            )
            print(
                f"Searching for term '{search_term}' with filter '{filter_by}'."
            )  # Debug print

            results = self.search_backups(search_term)

            if results:
                logger.debug(f"Found {len(results)} results.")
                print(f"Found {len(results)} results.")  # Debug print
            else:
                logger.debug("No results found.")
                print("No results found.")  # Debug print

            self.send(
                text_data=json.dumps(
                    {
                        "type": "search_results",
                        "results": results,
                    }
                )
            )

    def search_backups(self, search_term):
        results = []

        # Search across all Backup objects
        for backup in Backup.objects.all():
            hostname = backup.switch_name
            config_data = backup.config_data

            # Check each section for the search term
            if "BGP" in config_data:
                for entry in config_data["BGP"].get("Networks", []):
                    if search_term in entry:
                        results.append(
                            {
                                "where": "BGP",
                                "line": f"network {entry}",
                                "hostname": hostname,
                            }
                        )

            if "StaticRoutes" in config_data.get("Routing", {}):
                for route in config_data["Routing"]["StaticRoutes"]:
                    if search_term in route.get("Destination", ""):
                        results.append(
                            {
                                "where": "Static Routes",
                                "line": f"ip route {route['Destination']} {route.get('Gateway', '')}",
                                "hostname": hostname,
                            }
                        )

            if "Interfaces" in config_data:
                for interface in config_data["Interfaces"]:
                    if search_term in interface.get("IPAddress", ""):
                        results.append(
                            {
                                "where": "Interfaces",
                                "line": f"interface {interface['Name']} ip address {interface['IPAddress']}",
                                "hostname": hostname,
                            }
                        )

            if "Vlans" in config_data:
                for vlan in config_data["Vlans"]:
                    if search_term in vlan.get("Name", ""):
                        results.append(
                            {
                                "where": "VLANs",
                                "line": f"vlan {vlan['ID']} name {vlan['Name']}",
                                "hostname": hostname,
                            }
                        )

            if "ACLs" in config_data:
                for acl in config_data["ACLs"]:
                    for rule in acl.get("Rules", []):
                        if search_term in rule:
                            results.append(
                                {
                                    "where": f"ACL {acl['Name']}",
                                    "line": rule,
                                    "hostname": hostname,
                                }
                            )

        return results
