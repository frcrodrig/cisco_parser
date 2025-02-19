import textfsm
from regparsers import *


def get_cdp_neighbours(config, curr_path, file, devinfo):
    nei_template = open(curr_path + '\\nrt_cdp_nei.template')
    fsm = textfsm.TextFSM(nei_template)

    fsm.Reset()
    neighbours = fsm.ParseText(config)
    all_neighbours = []
    lastindex = 0
    i = 0

    if devinfo[2] == "Not set":
        dev_id = devinfo[0]
    else:
        dev_id = devinfo[0] + '.' + devinfo[2]

    for i in range(lastindex, len(neighbours)):
        all_neighbours.append([])
        all_neighbours[len(all_neighbours) - 1].append(file)
        all_neighbours[len(all_neighbours) - 1].append(dev_id)
        all_neighbours[len(all_neighbours) - 1].append(devinfo[3])
        all_neighbours[len(all_neighbours) - 1].append(devinfo[1])
        all_neighbours[len(all_neighbours) - 1].append(neighbours[i][4])
        all_neighbours[len(all_neighbours) - 1].append(neighbours[i][1])
        all_neighbours[len(all_neighbours) - 1].append(strip_cisco_from_cdp_name(neighbours[i][3]))
        all_neighbours[len(all_neighbours) - 1].append(neighbours[i][2])
        all_neighbours[len(all_neighbours) - 1].append(neighbours[i][5])
    if i != 0:
        lastindex = i + 1

    nei_template.close()

    return all_neighbours


def get_vrfs(config, curr_path, file, devinfo):
    nei_template = open(curr_path + '\\nrt_cdp_nei.template')
    fsm = textfsm.TextFSM(nei_template)

    fsm.Reset()
    neighbours = fsm.ParseText(config)
    all_neighbours = []
    lastindex = 0
    i = 0

    for i in range(lastindex, len(neighbours)):
        all_neighbours.append([])
        all_neighbours[len(all_neighbours) - 1].append(file)
        all_neighbours[len(all_neighbours) - 1].append(devinfo[0] + '.' + devinfo[2])
        all_neighbours[len(all_neighbours) - 1].append(devinfo[3])
        all_neighbours[len(all_neighbours) - 1].append(devinfo[1])
        all_neighbours[len(all_neighbours) - 1].append(neighbours[i][4])
        all_neighbours[len(all_neighbours) - 1].append(neighbours[i][1])
        all_neighbours[len(all_neighbours) - 1].append(neighbours[i][3])
        all_neighbours[len(all_neighbours) - 1].append(neighbours[i][2])
        all_neighbours[len(all_neighbours) - 1].append(neighbours[i][5])
    if i != 0:
        lastindex = i + 1

    nei_template.close()

    return all_neighbours


def get_interfaces_config(config, curr_path, file, devinfo):
    interfaces = []
    int_template = open(curr_path + '\\nrt_interfaces_config.template')
    fsm = textfsm.TextFSM(int_template)
    fsm.Reset()
    interfaces = fsm.ParseText(config)

    interfaces_configuration = []
    lastindex = 0
    i = 0
    j = 0
    vlan_id = 0

    # interfaces_configuration
    # [0] - file
    # [1] - hostname
    # [2] - type of switch (asw, dsw, csw, undefined)
    # [3] - number of physical interfaces
    # [4] - number of SVI interfaces
    # [5] - number of access interfaces
    # [6] - number of trunk interfaces
    # [7] - number of access ports with dot1x
    # [8] - number of ip addresses
    # [9] - list of access vlan(s)
    # [10] - list of native vlan(s)
    # [11] - list of voice vlan(s)
    # [12] - list of vlan(s) on trunks
    # [13] - all vlan from vlan database
    # [14] - vlan id of users vlan
    # [15] - vlan id of iot_toro vlan
    # [16] - vlan id of media_equip vlan
    # [17] - vlan id of off_equip vlan
    # [18] - vlan id of admin vlan

    interfaces_configuration.append(file)
    interfaces_configuration.append(devinfo[0])
    interfaces_configuration.append(get_type_of_sw_from_hostname(devinfo[0]))
    interfaces_configuration.append(get_num_of_physical_ints(interfaces))
    interfaces_configuration.append(get_num_of_svi_ints(interfaces))
    interfaces_configuration.append(get_num_of_access_int_from_interface_list(interfaces))
    interfaces_configuration.append(get_num_of_trunk_int_from_interface_list(interfaces))
    interfaces_configuration.append(get_num_of_dot1x_interfaces(interfaces))
    interfaces_configuration.append(get_num_of_ints_with_ip(interfaces))
    interfaces_configuration.append(get_access_vlan_ids(interfaces))
    interfaces_configuration.append(get_native_vlan_ids(interfaces))
    interfaces_configuration.append(get_voice_vlan_ids(interfaces))
    interfaces_configuration.append(get_trunk_vlan_ids(interfaces))

    vlans_from_config = get_vlan_config(config, curr_path)
    interfaces_configuration.append(vlans_from_config)

    """
    fill vlan id for vlans with names   
     - users
     - iot_toro
     - media_equip
     - off_equip
     - admin
    """

    vlan_id = "0"
    for j in range(0, len(vlans_from_config)):
        if vlans_from_config[j][1] == 'users':
            vlan_id = vlans_from_config[j][0]

    if vlan_id !="0":
        interfaces_configuration.append(vlan_id)
    else:
        interfaces_configuration.append("")

    vlan_id = "0"

    for j in range(0, len(vlans_from_config)):
        if vlans_from_config[j][1] == 'iot_toro':
            vlan_id = vlans_from_config[j][0]

    if vlan_id != "0":
        interfaces_configuration.append(vlan_id)
    else:
        interfaces_configuration.append("")

    vlan_id = "0"

    for j in range(0, len(vlans_from_config)):
        if vlans_from_config[j][1] == 'media_equip':
            vlan_id = vlans_from_config[j][0]

    if vlan_id != "0":
        interfaces_configuration.append(vlan_id)
    else:
        interfaces_configuration.append("")

    vlan_id = "0"

    for j in range(0, len(vlans_from_config)):
        if vlans_from_config[j][1] == 'off_equip':
            vlan_id = vlans_from_config[j][0]

    if vlan_id != "0":
        interfaces_configuration.append(vlan_id)
    else:
        interfaces_configuration.append("")

    vlan_id = "0"

    for j in range(0, len(vlans_from_config)):
        if vlans_from_config[j][1] == 'admin':
            vlan_id = vlans_from_config[j][0]

    if vlan_id != "0":
        interfaces_configuration.append(vlan_id)
    else:
        interfaces_configuration.append("")

    return interfaces_configuration


def get_vlan_config(config, curr_path):
    # Extract vlan information (id, name) from configuration

    vlan_template = open(curr_path + '\\nrt_vlans_config.template')
    fsm = textfsm.TextFSM(vlan_template)
    fsm.Reset()
    vlans = fsm.ParseText(config)

    vlans_configuration = []

    i: int = 0
    j: int = 0
    w: int = 0

    for i in range(0, len(vlans)):
        if vlans[i][0] != "internal":
            if vlans[i][0].find(',') != -1:
                vlans_list =vlans[i][0].split(',')
                for j in range(0, len(vlans_list)):
                    vlans_configuration.append([])
                    vlans_configuration[w].append(vlans_list[j])
                    vlans_configuration[w].append("")
                    w = w +1
            else:
                vlans_configuration.append([])
                vlans_configuration[w].append(vlans[i][0])
                vlans_configuration[w].append(vlans[i][1])
                w = w + 1

    vlan_template.close()
    return vlans_configuration


def get_access_config(config, curr_path):
    # Extract vty device access parameters

    access_template = open(curr_path + '\\nrt_dev_access.template')
    fsm = textfsm.TextFSM(access_template)
    fsm.Reset()
    access = fsm.ParseText(config)

    access_config = []

    for i in range(0, len(access)):
        access_config.append([])
        access_config[i] = access[i]

    if (len(access) == 0):
        access_config.append([])
        access_config[0].append("Not set")
        access_config[0].append("Not set")
        access_config[0].append("Not set")
        access_config[0].append("Not set")
        access_config[0].append("Not set")

        access_config.append([])
        access_config[1].append("Not set")
        access_config[1].append("Not set")
        access_config[1].append("Not set")
        access_config[1].append("Not set")
        access_config[1].append("Not set")

    if (len(access) == 1):
        access_config.append([])
        access_config[1].append("Not set")
        access_config[1].append("Not set")
        access_config[1].append("Not set")
        access_config[1].append("Not set")
        access_config[1].append("Not set")

    if (access_config[0][0] == ""):
        access_config[0][0] = "Not set"

    if (access_config[0][1] == ""):
        access_config[0][1] = "Not set"

    if (access_config[0][2] == ""):
        access_config[0][2] = "Not set"

    if (access_config[0][3] == ""):
        access_config[0][3] = "Not set"

    if (access_config[0][4] == ""):
        access_config[0][4] = "Not set"

    if (access_config[1][0] == ""):
        access_config[1][0] = "Not set"

    if (access_config[1][1] == ""):
        access_config[1][1] = "Not set"

    if (access_config[1][2] == ""):
        access_config[1][2] = "Not set"

    if (access_config[1][3] == ""):
        access_config[1][3] = "Not set"

    if (access_config[1][4] == ""):
        access_config[1][4] = "Not set"

    access_template.close()
    return access_config

def get_con_access_config(config, curr_path):
    # Extract console device access parameters
    access_template = open(curr_path + '\\nrt_dev_con_access.template')
    fsm = textfsm.TextFSM(access_template)
    fsm.Reset()
    access = fsm.ParseText(config)

    access_config = []

    for i in range(0, len(access)):
        access_config.append([])
        access_config[i] = access[i]

    if (len(access) == 0):
        access_config.append([])
        access_config[0].append("Not set")
        access_config[0].append("Not set")
        access_config[0].append("Not set")
        access_config[0].append("Not set")
        access_config[0].append("Not set")

    if (access_config[0][0] == ""):
        access_config[0][0] = "Not set"

    if (access_config[0][1] == ""):
        access_config[0][1] = "Not set"

    if (access_config[0][2] == ""):
        access_config[0][2] = "Not set"

    if (access_config[0][3] == ""):
        access_config[0][3] = "Not set"

    if (access_config[0][4] == ""):
        access_config[0][4] = "Not set"

    access_template.close()
    return access_config


def get_tacacs_server_ips(config, curr_path):
    '''
    Get tacacs server IPs
    '''

    if ("N9K" in obtain_model(config)):
        match = re.findall('^tacacs-server\shost\s([0-9]+.[0-9]+.[0-9]+.[0-9]+)', config, re.MULTILINE)
        if match:
            s = ""
            for i in range(len(match)):
                s = s + " "+match[i]+","
            return s[:-1]
        else:
            return "Fail"
    else:
        # Extract vlan information (id, name) from configuration
        tacacs_template = open(curr_path + '\\nrt_tacacs_servers.template')
        fsm = textfsm.TextFSM(tacacs_template)
        fsm.Reset()
        ips = fsm.ParseText(config)
        tacacs_template.close()

        if ips:
            s = ""
            for i in range(len(ips)):
                s = s + " "+ips[i][1]+","
            return s[:-1]
        else:
            match = re.findall('^tacacs-server\shost\s([0-9]+.[0-9]+.[0-9]+.[0-9]+)', config, re.MULTILINE)
            if match:
                s = ""
                for i in range(len(match)):
                    s = s + " " + match[i] + ","
                return s[:-1]
            else:
                return "Fail"