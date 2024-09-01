import re
import logging
import json

# Initialize logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def parse_switch_config(config_text):
    config_data = {
        "Hostname": "",
        "Vlans": [],
        "Interfaces": [],
        "Routing": {"StaticRoutes": [], "OSPF": {}, "EIGRP": {}, "BGP": {}},
        "ACLs": [],
    }

    try:
        # Parse hostname
        hostname_match = re.search(r"hostname (\S+)", config_text)
        if hostname_match:
            config_data["Hostname"] = hostname_match.group(1)

        # Parse VLANs
        vlan_pattern = re.compile(r"vlan (\d+)(?:\n +name (.+))?")
        vlans = vlan_pattern.findall(config_text)
        for vlan in vlans:
            vlan_id, vlan_name = vlan
            if vlan_name:
                config_data["Vlans"].append({"ID": vlan_id, "Name": vlan_name.strip()})
            else:
                config_data["Vlans"].append({"ID": vlan_id, "Name": "Unnamed"})

        # Parse Interfaces
        interface_pattern = re.compile(
            r"interface (\S+)(?:\n +description (.+?))?(?:\n +switchport (.+?))?(?:\n +channel-group (\d+) mode (.+?))?(?:\n +ip address (\S+))?",
            re.MULTILINE,
        )
        interfaces = interface_pattern.findall(config_text)
        for intf in interfaces:
            config_data["Interfaces"].append(
                {
                    "Name": intf[0],
                    "Description": intf[1].strip() if intf[1] else "N/A",
                    "Switchport": intf[2].strip() if intf[2] else "N/A",
                    "ChannelGroup": intf[3] if intf[3] else "N/A",
                    "ChannelMode": intf[4] if intf[4] else "N/A",
                    "IPAddress": intf[5] if intf[5] else "N/A",
                }
            )

        # Parse Static Routes
        static_route_pattern = re.compile(r"ip route (\S+) (\S+)")
        static_routes = static_route_pattern.findall(config_text)
        for route in static_routes:
            config_data["Routing"]["StaticRoutes"].append(
                {"Destination": route[0], "Gateway": route[1]}
            )

        # Parse OSPF Configuration
        ospf_pattern = re.compile(
            r"router ospf (\d+)([\s\S]*?)(?=^router|\n\n|$)", re.MULTILINE
        )
        ospf_match = ospf_pattern.search(config_text)
        if ospf_match:
            config_data["Routing"]["OSPF"]["ProcessID"] = ospf_match.group(1)
            networks = re.findall(r"network (\S+) area (\S+)", ospf_match.group(2))
            config_data["Routing"]["OSPF"]["Networks"] = [
                {"Network": net[0], "Area": net[1]} for net in networks
            ]

        # Parse EIGRP Configuration
        eigrp_pattern = re.compile(
            r"router eigrp (\d+)([\s\S]*?)(?=^router|\n\n|$)", re.MULTILINE
        )
        eigrp_match = eigrp_pattern.search(config_text)
        if eigrp_match:
            config_data["Routing"]["EIGRP"]["ProcessID"] = eigrp_match.group(1)
            networks = re.findall(r"network (\S+)", eigrp_match.group(2))
            config_data["Routing"]["EIGRP"]["Networks"] = [
                {"Network": net} for net in networks
            ]

        # Parse BGP Configuration
        bgp_pattern = re.compile(
            r"router bgp (\d+)([\s\S]*?)(?=^router|\n\n|$)", re.MULTILINE
        )
        bgp_match = bgp_pattern.search(config_text)
        if bgp_match:
            config_data["Routing"]["BGP"]["ProcessID"] = bgp_match.group(1)
            logger.debug(f"BGP Match found with process ID: {bgp_match.group(1)}")

            # Parse Address Family within BGP
            address_family_pattern = re.compile(
                r"^ {2}address-family ipv4 unicast([\s\S]*?)(?=^\S|\n{2}|^!)",
                re.MULTILINE,
            )
            address_family_match = address_family_pattern.search(bgp_match.group(2))
            if address_family_match:
                logger.debug(f"Address Family Match found in BGP configuration.")

                # Parse Networks within Address Family
                networks = re.findall(
                    r"^ {4}network (\S+)", address_family_match.group(1), re.MULTILINE
                )
                logger.debug(f"Networks found: {networks}")

                config_data["Routing"]["BGP"]["Networks"] = [
                    {"Network": net} for net in networks
                ]
            else:
                logger.debug("No Address Family found in BGP configuration.")
        else:
            logger.debug("No BGP configuration found.")

        # Parse all ACLs
        acl_pattern = re.compile(r"(ip access-list \S+)((?:\n\s+.+)+)", re.MULTILINE)
        acls = acl_pattern.findall(config_text)
        for acl_name, acl_rules in acls:
            acl_rules_list = acl_rules.strip().split("\n")
            acl_rules_cleaned = [
                rule.strip() for rule in acl_rules_list if rule.strip()
            ]
            config_data["ACLs"].append(
                {"Name": acl_name.strip(), "Rules": acl_rules_cleaned}
            )

    except Exception as e:
        logger.error(f"Failed to parse configuration: {e}")
        raise

    return config_data


# Optional utility function to convert parsed data to JSON (if needed)
def config_to_json(config_data):
    return json.dumps(config_data, indent=4)
