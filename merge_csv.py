# Read IP addresses from csv file than PING them one by one.

file_path = "/Users/scui/Downloads/NOC_mgnt_scan/fqdn/"
# file = ['adm12_DC9_fw_noname.csv', 'mgnt_DC8_priv_log_noname.csv',
#        'mgnt_DC7_priv_log_noname.csv', 'mgnt_CC78_noname.csv',
#        'mgnt_CN_priv_log_noname.csv', 'mgnt_DC6_priv_log_fw_noname.csv',
#        'mgnt_DC5_priv_log_fw_noname.csv', 'mgnt_DC9_ADC_fw_noname.csv',
#        'mgnt_DC8_ADC_fw_noname.csv', 'mgnt_DC7_ADC_fw_noname.csv',
#        'mgnt_CN_ADC_fw_noname.csv'
#        ]
f_fqdn = ['adm13_DC9_fw_fqdn.csv', 'adm12_DC9_fw_fqdn.csv',
          'mgnt_DC8_access_fw_fqdn.csv', 'mgnt_DC8_priv_log_fqdn.csv',
          'mgnt_DC7_access_fw_fqdn.csv', 'mgnt_DC7_priv_log_fqdn.csv',
          'mgnt_CC78_fqdn.csv', 'mgnt_CN_priv_log_fqdn.csv',
          'mgnt_DC6_access_fw_fqdn.csv', 'mgnt_DC5_access_fw_fqdn.csv',
          'mgnt_DC5_priv_log_fw_fqdn.csv', 'mgnt_DC8_fw_fqdn.csv',
          'mgnt_DC7_fw_fqdn.csv', 'mgnt_DC7_ADC_fw_fqdn.csv',
          'mgnt_DC6_fw_fqdn.csv', 'mgnt1_DC5_fw_fqdn.csv'
          ]

with open('/Users/scui/Downloads/NOC_mgnt_scan/fqdn_host.csv', 'w') as outfile:
  for fname in f_fqdn:
    in_file = file_path + fname
    with open(in_file) as in_file_object:
      outfile.write(fname + ' ')
      outfile.write(in_file_object.read())
