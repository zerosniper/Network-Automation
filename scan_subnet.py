import ipaddress
import socket
import csv
from subprocess import Popen, PIPE
from tqdm import tqdm


def read_networks(file):
    network_list = {}
    net_name = []
    ip_net = []

    with open(file) as file_object:
        file_content = file_object.readlines()
        file_content.pop(0)

        for line in file_content:
            row = line.rstrip().replace('"', '').split(',')  # remove new line and quote
            net_name.append(row[0])
            ip_net.append(row[1])

        network_list['name'] = net_name
        network_list['subnet'] = ip_net

    return(network_list)


def exam_ip(network_name, network):

    ips_reach = []
    known_hosts = []
    unknown_hosts = []

    ips = ipaddress.ip_network(network)
    total_ip = int(len(list(ips.hosts())))

    print("Processing IP subnet: " + network_name)
    pbar = tqdm(total=total_ip)

    for ip in ips.hosts():
        ip = str(ip)
        toping = Popen(['ping', '-c', '2', '-i', '0.1',
                        '-W', '230', ip], stdout=PIPE)
        output = toping.communicate()[0]
        result = toping.returncode

        if result == 0:
            ips_reach.append(ip)

        pbar.update(1)

    pbar.close()

    for count in range(len(ips_reach)):
        addr = ips_reach[count]
        ip_with_dns = {}
        ip_no_dns = {}

        try:
            ip_with_dns['Hostname'] = socket.gethostbyaddr(addr)[0]
            ip_with_dns['Address'] = addr
            known_hosts.append(ip_with_dns)

        except socket.herror:
            ip_no_dns['Address'] = addr
            unknown_hosts.append(ip_no_dns)

    return(known_hosts, unknown_hosts)


file_path = "/Users/scui/Downloads/"
input_file = file_path + "noc_mgnt_segment_10.csv"

networks = read_networks(input_file)

subnet_name = networks['name']
subnet = networks['subnet']

if len(subnet_name) != len(subnet):
    print("The subnet name and IP subnet is mismaching, something wrong in the file")

else:
    for i in range(len(subnet)):

        result_kh, result_ukh = exam_ip(subnet_name[i], subnet[i])

        csv_columns_kh = ['Hostname', 'Address']
        csv_column_ukh = ['Address']
        csv_khost = str(file_path) + str(subnet_name[i]) + "_fqdn.csv"
        csv_ukhost = str(file_path) + str(subnet_name[i]) + "_noname.csv"

        if result_kh:
            try:
                with open(csv_khost, 'w') as out_csv_known:
                    writer = csv.DictWriter(
                        out_csv_known, fieldnames=csv_columns_kh)
                    writer.writeheader()
                    for data in result_kh:
                        writer.writerow(data)
            except IOError:
                print("I/O error")
        if result_ukh:
            try:
                with open(csv_ukhost, 'w') as out_csv_unknown:
                    writer = csv.DictWriter(
                        out_csv_unknown, fieldnames=csv_column_ukh)
                    writer.writeheader()
                    for data in result_ukh:
                        writer.writerow(data)
            except IOError:
                print("I/O error")
