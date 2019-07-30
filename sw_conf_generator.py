def svi_conf_core(vlan_id, network_name, host_addr, network_mask, dhcp_relay, dhcp_relay2, network_gateway):
    """Build SVI configuration"""
    svi_int = "interface Vlan" + vlan_id
    svi_des = " description " + network_name
    ip_addr = " ip address " + host_addr + " " + network_mask
    ip_redir = " no ip redirects"
    ip_proxy = " no ip proxy-arp"
    arp_time = " arp timeout 295"
    stby_ip = " standby " + vlan_id + " ip " + network_gateway
    stby_time = " standby " + vlan_id + " timers 1 3"
    stby_auth = " standby " + vlan_id + " authentication md5 key-string " + vlan_id
    conf_end = "!"

    int_conf = [
        svi_int,
        svi_des,
        ip_addr,
        ip_redir,
        ip_proxy,
        stby_ip,
        stby_time,
        stby_auth,
        arp_time,
    ]

    if dhcp_relay:
        ip_helper = " ip helper-address " + dhcp_relay
        int_conf.append(ip_helper)

    if dhcp_relay2:
        ip_helper2 = " ip helper-address " + dhcp_relay2
        int_conf.append(ip_helper2)

    int_conf.append(conf_end)

    return int_conf


def svi_conf_acc(vlan_id, network_name, host_addr, network_mask):
    """Build SVI configuration"""
    svi_int = "interface Vlan" + vlan_id
    svi_des = " description " + network_name
    ip_addr = " ip address " + host_addr + " " + network_mask
    ip_redir = " no ip redirects"
    ip_proxy = " no ip proxy-arp"
    conf_end = "!"

    int_conf = [
        svi_int,
        svi_des,
        ip_addr,
        ip_redir,
        ip_proxy,
        conf_end,
    ]

    return int_conf


core_sw = {
    'host_name': 'SWEx-TEST888-STO-01.ikea.com',
    'host_addr': '10.0.43.253',
    'function': 'Switch',
    'mgnt_ip': 'No',
    'device_type': 'x',
    'subnet_info': {
        'network_id': '53052',
        'start_ip': '10.0.43.0',
        'end_ip': '10.0.43.255',
        'network_mask': '255.255.255.0',
        'network_name': 'WirelessAP_VLAN210',
        'vlan_id': '210',
        'vlan_name': "Wireless AP's",
        'network_gateway': '10.0.43.254',
        'dhcp_relay': ['1.1.1.1', '']
    }
}


core_sw_mgt = {
    'host_name': 'SWEx-TEST888-STO-02.ikea.com',
    'host_addr': '10.0.47.124',
    'function': 'Switch',
    'mgnt_ip': 'No',
    'device_type': 'x',
    'subnet_info': {
        'network_id': '53059',
        'start_ip': '10.0.47.64',
        'end_ip': '10.0.47.127',
        'network_mask': '255.255.255.192',
        'network_name': 'ServerManagement_VLAN151',
        'vlan_id': '151',
        'vlan_name': 'ServerManagement',
        'network_gateway': '10.0.47.126',
        'dhcp_relay': ['1.1.1.1', '2.2.2.2']
    }
}

acc_sw = {
    'host_name': 'SWEs-TEST888-STO-03.ikea.com',
    'host_addr': '10.0.47.3',
    'mgnt_ip': 'Yes',
    'function': 'Switch',
    'device_type': 's',
    'serial_nr': 'FFFFFFFFFFF%20',
    'subnet_info': {
        'network_id': '53058',
        'start_ip': '10.0.47.0',
        'end_ip': '10.0.47.63',
        'network_mask': '255.255.255.192',
        'network_name': 'NetworkManagement_VLAN150',
        'vlan_id': '150',
        'vlan_name': 'NetworkManagement',
        'network_gateway': '10.0.47.62'
    }
}
vlan_id = core_sw_mgt['subnet_info']['vlan_id']
network_name = core_sw_mgt['subnet_info']['network_name']
network_mask = core_sw_mgt['subnet_info']['network_mask']
network_gateway = core_sw_mgt['subnet_info']['network_gateway']
dhcp_relay = core_sw_mgt['subnet_info']['dhcp_relay'][0]
dhcp_relay2 = core_sw_mgt['subnet_info']['dhcp_relay'][1]
host_addr = core_sw_mgt['host_addr']

int_conf = svi_conf_core(vlan_id, network_name, host_addr,
                         network_mask, dhcp_relay, dhcp_relay2, network_gateway)
filename = "port_conf.txt"
with open(filename, 'a') as file_object:
    for int_conf_item in int_conf:
        file_object.write(int_conf_item + "\n")
