import re

ipv4 = re.compile('[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}')

print(re.match(ipv4, '1.2.3.2'))
