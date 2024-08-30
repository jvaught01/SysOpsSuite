import re
import json

def parse_switch_config(config_text):
    config_data = {
        "Hostname": "",
        "Vlans": [],
        "Interfaces": [],
        "Routing": {
            "StaticRoutes": [],
            "OSPF": {}
        }
    }

    # Parse hostname
    hostname_match = re.search(r'hostname (\S+)', config_text)
    if hostname_match:
        config_data["Hostname"] = hostname_match.group(1)

    # Parse VLANs
    vlan_pattern = re.compile(r'vlan (\d+)(?:\n +name (.+))?')
    vlans = vlan_pattern.findall(config_text)
    for vlan in vlans:
        vlan_id, vlan_name = vlan
        config_data["Vlans"].append({"ID": vlan_id, "Name": vlan_name.strip() if vlan_name else ""})

    # Parse Interfaces
    interface_pattern = re.compile(r'interface (\S+)(?:\n +description (.+))?(?:\n +switchport (.+))?(?:\n +channel-group (\d+) mode (.+))?(?:\n +ip address (\S+))?', re.MULTILINE)
    interfaces = interface_pattern.findall(config_text)
    for intf in interfaces:
        config_data["Interfaces"].append({
            "Name": intf[0],
            "Description": intf[1].strip() if intf[1] else "",
            "Switchport": intf[2].strip() if intf[2] else "",
            "ChannelGroup": intf[3] if intf[3] else "",
            "ChannelMode": intf[4] if intf[4] else "",
            "IPAddress": intf[5] if intf[5] else ""
        })

    # Parse Static Routes
    static_route_pattern = re.compile(r'ip route (\S+) (\S+)')
    static_routes = static_route_pattern.findall(config_text)
    for route in static_routes:
        config_data["Routing"]["StaticRoutes"].append({"Destination": route[0], "Gateway": route[1]})

    # Parse OSPF Configuration
    ospf_pattern = re.compile(r'router ospf (\d+)\n +network (\S+) area (\S+)\n +max-lsa (\d+)', re.MULTILINE)
    ospf_match = ospf_pattern.search(config_text)
    if ospf_match:
        config_data["Routing"]["OSPF"] = {
            "ProcessID": ospf_match.group(1),
            "Network": ospf_match.group(2),
            "Area": ospf_match.group(3),
            "MaxLSA": ospf_match.group(4)
        }

    return config_data

# Optional utility function to convert parsed data to JSON (if needed)
def config_to_json(config_data):
    return json.dumps(config_data, indent=4)
