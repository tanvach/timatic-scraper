import urllib

import re
from os import listdir
import time
import socket
import socks

# Uncomment the lines below if tor proxy server is available (details in README)
# Must install SocksiPy library from http://socksipy.sourceforge.net/

# socks.set_default_proxy(socks.SOCKS5, "localhost", 9050)
# socket.socket = socks.socksocket

# Set where to dump the HTML files
folder_path = "/tmp/"


timatic_url = "https://www.timaticweb.com/"

# Country codes 
country_codes = ["AF","AL","DZ","AS","AD","AO","AI","AQ","AG","AR","AM","AW","AU","AT","AZ","BS","BH","BD","BB","BY","BE","BZ","BJ","BM","BT","BO","BA","BW","BV","BR","IO","BN","BG","BF","BI","KH","CM","CA","CV","OU","KY","CF","TD","CL","CN","CX","CC","CO","KM","CG","CD","CK","CR","CI","HR","CU","CY","CZ","DK","DJ","DM","DO","TP","EC","EG","SV","GQ","ER","EE","ET","FK","FO","FJ","FI","FR","GF","PF","TF","GA","GM","GE","DE","GH","GI","GR","GL","GD","GP","GU","GT","GG","GN","GW","GY","HT","HM","HN","HK","HU","IS","IN","ID","IR","IQ","IE","IM","IL","IT","JM","JP","JE","JO","KZ","KE","KA","KI","KR","KP","KW","KG","LA","LV","LB","LS","LR","LY","LI","LT","LU","MO","MK","MG","MW","MY","MV","ML","MT","MH","MQ","MR","MU","YT","MX","FM","MD","MC","MN","ME","MS","MA","MZ","MM","NA","NR","NP","NL","AN","NC","NZ","NI","NE","NG","NU","NF","MP","NO","ND","OM","PK","PW","PS","PA","PG","PY","PE","PH","PN","PL","PT","PR","QA","RE","RO","RU","RW","LC","WS","SM","ST","SA","CB","SN","RS","SC","SL","SG","SK","SI","SB","SO","ZA","GS","SS","ES","LK","SH","KN","SX","PM","VC","SD","SR","SJ","SZ","SE","CH","SY","TW","TJ","TZ","TH","TG","TK","TO","TT","TN","TR","TM","TC","TV","UG","UA","AE","GB","US","UM","UX","UY","UZ","VU","VA","VE","VN","VG","VI","WF","EH","YE","ZR","ZM","ZW"]
skip_cc = {}

file_names = listdir(folder_path)

# Loop through the country codes and obtain all the combinations
# Also checks if files have already been downloaded
# Note: This will generate LOTS of files (around 50,000)

for cc1 in country_codes:
    for cc2 in country_codes:
        if cc1 != cc2 and (cc1 not in skip_cc) and (cc2 not in skip_cc):
            file_name = cc1 + "_" + cc2
            if any(file_name in s for s in file_names):
                pass
                #print("Already Downloaded " + cc1 + " to " + cc2)
            else:
                url = "https://www.timaticweb.com/cgi-bin/tim_website_client.cgi?SpecData=1&VISA=&page=visa&NA="+cc1+"&AR=00&PASSTYPES=PASS&DE="+cc2+"&user=EK&subuser=EMIRATES"
                f = urllib.request.urlopen(url)
                page = f.read().decode("utf-8")
                if page.find("NOT IN AIRPORT OR CITY TABLE") > -1:
                    bad_national = page.split("NOT IN AIRPORT OR CITY TABLE")[1].strip().split("\r")[0]
                    skip_cc[bad_national] = True
                    print(bad_national)
                    continue
                with open( folder_path + file_name +".html", "w") as output_file:
                    output_file.write(page)
                time.sleep(1)
            