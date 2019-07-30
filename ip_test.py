# This script reads IP subnet from a file and testing addresses. IPs response
# to PING will be examed by reverse lookup. All IPs with valid hostname will be
# placed into a file named "Discovered_items_with_hostname.csv", rests will be
# placed in file named "Discovered _items_without_hostname.csv"

import ipaddress
import socket
import csv
from subprocess import Popen, PIPE
from tqdm import tqdm


def read_ips(file):
    ip_list = []

    with open(file) as file_object:
        file_content = file_object.readlines()
        file_content.pop(0)

        for line in file_content:
            row = line.rstrip().replace('"', '').split(',')  # remove new line and quote
            ip_list.append(row[0])

    return(ip_list)


def exam_ip(ip_addresses):

    ips_reach = []
    ips_unreach = []

    total_ip = len(ip_addresses)
    print("Processing \"PING\" total IPs: " + str(total_ip))
    pbar = tqdm(total=total_ip)

    for ip in ip_addresses:
        ip = str(ip)
        toping = Popen(['ping', '-c', '2', '-i', '0.3',
                        '-W', '350', ip], stdout=PIPE)
        output = toping.communicate()[0]
        result = toping.returncode

        if result == 0:
            ips_reach.append(ip)

        else:
            ips_unreach.append(ip)

        pbar.update(1)

    pbar.close()

    return(ips_reach, ips_unreach)


def name_lookup(ips_reach):

    known_hosts = []
    unknown_hosts = []

    for ip in ips_reach:
        ip_with_dns = {}
        ip_no_dns = {}

        tkry:
            ip_with_dns['Hostname'] = socket.gethostbyaddr(ip)[0]
            ip_with_dns['Address'] = ip
            known_hosts.append(ip_with_dns)

        except socket.herror:
            ip_no_dns['Address'] = ip
            unknown_hosts.append(ip_no_dns)

    return(known_hosts, unknown_hosts)


file_path = "/Users/xxx/Downloads/"
input_file = file_path + "ip_addresses.csv"

addresses = read_ips(input_file)

ips_reach, ips_unreach = exam_ip(addresses)

result_kh, result_ukh = name_lookup(ips_reach)

csv_columns_kh = ['Hostname', 'Address']
csv_column_ukh = ['Address']
csv_khost = str(file_path) + "orphan_fqdn.csv"
csv_ukhost = str(file_path) + "orphan_noname.csv"
csv_unreach = str(file_path) + "orphan_unreach_host.csv"

try:
    with open(csv_khost, 'w') as out_csv_known:
        writer = csv.DictWriter(out_csv_known, fieldnames=csv_columns_kh)
        writer.writeheader()
        for data in result_kh:
            writer.writerow(data)
except IOError:
    print("I/O error")

try:
    with open(csv_ukhost, 'w') as out_csv_unknown:
        writer = csv.DictWriter(out_csv_unknown, fieldnames=csv_column_ukh)
        writer.writeheader()
        for data in result_ukh:
            writer.writerow(data)
except IOError:
    print("I/O error")

try:
    with open(csv_unreach, 'w') as out_csv_unreach:
        out_csv_unreach.write("Unreachable Address\n")
        for data in ips_unreach:
            out_csv_unreach.write(data + "\n")
except IOError:
    print("I/O error")
