import pandas as pd
import requests
import urllib.request
from time import sleep
from colorama import init, Fore


init()


def check_proxy(isHttps, proxy, country, anon):
    try:
        proxy_handler = urllib.request.ProxyHandler({isHttps: proxy})
        opener = urllib.request.build_opener(proxy_handler)
        opener.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0')]
        urllib.request.install_opener(opener)      
        urllib.request.urlopen(isHttps+'://www.google.com')
        print(Fore.GREEN + f"Good Proxy {proxy}, {country}, {anon}, {isHttps}")
        result = open("proxy_list.txt", "a")
        result.write(f"{proxy}\n{country}\n{anon}\n{isHttps}\n\n")
        result.close
    except Exception as detail:
        print(Fore.RED + "Bad Proxy " + proxy)
        print(detail)

#Grab Proxy
url = 'https://free-proxy-list.net/'
req = requests.get(url)

raw_data = pd.read_html(req.text)
df_proxy = raw_data[0][["IP Address", "Port", "Country", "Anonymity", "Https"]]

proxy_list = df_proxy.values.tolist()

for each_proxy in proxy_list:
    try:
        ip_addr = each_proxy[0]
        port = int(each_proxy[1])
        port = str(port)
        country = each_proxy[2]
        anon = each_proxy[3]
        https = each_proxy[4]
        address = ip_addr + ":" + port

        if https == "yes":
            check_proxy("https", address, country=country, anon=anon)
        elif https == "no":
            check_proxy("http", address, country=country, anon=anon)

    except Exception as detail:
        print(detail)