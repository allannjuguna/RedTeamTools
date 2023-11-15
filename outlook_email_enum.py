#! /usr/bin/python3
# -*- coding: utf-8 -*-
#  @author: zerofrost🦊
#  @date: 2023-11-14
#  @description: This script enumerates outlook emails ; checks for valid from a list

white="\033[0m"
red="\033[91m"
green="\033[92m"
bold="\033[01m"
yellow="\033[93m"
blue="\033[94m"
success=f"{bold}{green}[+]{white} - "
alert=f"{bold}{yellow}[!]{white} - "
progress=f"{bold}{blue}[*]{white} - "
fail=f"{bold}{red}[*]{white} - "
end=f"{white}"

import argparse
import requests
import time
from concurrent.futures import ThreadPoolExecutor

parser=argparse.ArgumentParser()
parser.add_argument('-f','--file',help='File containing emails to check',required=True)
parser.add_argument('-v','--verbose',help='Enable verbose mode',required=False,default=False,action='store_true')
parser.add_argument('-s','--silent',help='Show minimal info, only show valid emails',required=False,default=False,action='store_true')
parser.add_argument('-t','--threads',help='Number of threads to use ',required=False,default=10,type=int)
args=parser.parse_args()


def reademails(filename):
	try:
		with open(filename,'r',encoding="latin-1") as r:
			emails=r.readlines()
			r.close()
		return emails
	except Exception as e:
		print(f"{fail} Unable to read file '{args.file}'. Error {e}")
		exit()


def banner():
	string=r"""
	   ____        __  __            __       ______                    
	  / __ \__  __/ /_/ /___  ____  / /__    / ____/___  __  ______ ___ 
	 / / / / / / / __/ / __ \/ __ \/ //_/   / __/ / __ \/ / / / __ `__ \
	/ /_/ / /_/ / /_/ / /_/ / /_/ / ,<     / /___/ / / / /_/ / / / / / /
	\____/\__,_/\__/_/\____/\____/_/|_|   /_____/_/ /_/\__,_/_/ /_/ /_/ 
	                                                                                       
	                                                                 v1
	"""
	print(f"{yellow}{string}{white}")


cookies = {
    'buid': '0.AQ8AMe_N-B6jSkuT5F9XHpElWgIAAAAAAPEPzgAAAAAAAAABAAA.AQABAAEAAAAmoFfGtYxvRrNriQdPKIZ-FHnoSKlL_IBhSwMDeyo4T8haM33AhtlOpUYvbxDzxR9cSHdQzJSfqwJdGEz2aZjmeOfBhtq2CJgj5UH4D8eBdNOag8zjnf9xO01htREGfU4gAA',
    'esctx': 'PAQABAAEAAAAmoFfGtYxvRrNriQdPKIZ-_io83mu_6rtEG1wmMHiu7IyaiRc7uRNCFS8BmhUtoZImzIs6qUlK8rJVvUVfyMwUVRhiyAlACxszMR0c6IZzp6H74Ok9xpa6G3puZAsBBafOx966bQ7lSreBZv-qD6JM1vUdARWtOqPDTO3FGSa98xTHmLHa9NecQKlW-uzM0e0gAA',
    'esctx-9S11laNwNdU': 'AQABAAEAAAAmoFfGtYxvRrNriQdPKIZ-ESg8Ts3dEj4aUc0kjrSn457oaWF_Vn6D7Ea-qhWAICEPIt80q8FZ8X6i4E44XO1uh9PqgpMrkfV8wt8aHJR9W_n9Yp0sJwaRNrm6CFAyjBVm0Q9fn1Q4S5y_ZHGHv0B2MObrg6WzwsmX2QiCfX0HRSAA',
    'fpc': 'AqSKE2JV11pEmBNWkpIOCGaerOTJAQAAANlB5dwOAAAA',
    'x-ms-gateway-slice': 'estsfd',
    'stsservicecookie': 'estsfd',
    'brcap': '0',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
    'Accept': 'application/json',
    'Accept-Language': 'en-US,en;q=0.5',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://login.microsoftonline.com/common/oauth2/authorize?client_id=00000002-0000-0ff1-ce00-000000000000&redirect_uri=https%3a%2f%2foutlook.office.com%2fowa%2f&resource=00000002-0000-0ff1-ce00-000000000000&response_mode=form_post&response_type=code+id_token&scope=openid&msafed=1&msaredir=1&client-request-id=f22d0139-3a57-3d49-3fbd-acf36387b27c&protectedtoken=true&claims=%7b%22id_token%22%3a%7b%22xms_cc%22%3a%7b%22values%22%3a%5b%22CP1%22%5d%7d%7d%7d&nonce=638355542595287901.e4dcec58-6200-44af-92e6-09e8515a3bea&state=DcsxFoAgDARR0OdxIiGwEI4TMbaWXl-KP93EEMK-bEvkldBb0QKgCgZE--B8er2nTyg1YaZa7aEh3oiHKzKsXG5xvUd6P0s_',
    'hpgid': '1104',
    'hpgact': '1800',
    'canary': 'PAQABAAEAAAAmoFfGtYxvRrNriQdPKIZ-R4_yFxcfwMN8BE2nY-y8zZzm_5xEE29c9oyYmgCwWjML0StodoORbsaKcNQl-Ktz6K7mZlocRaLOUtabd6S62cEB_ZxzfNPbTPGXB30ZnfPElkeMQXz5sHjmMm4pn7hRnoTk_StaUeQ874zBELudqGTGb9X5q_bOOCCXl_H5dZyfB2ZOAvkOW1dxT3d_xWi5YNI3j4dwMyJTpUswjegFtSAA',
    'client-request-id': 'f22d0139-3a57-3d49-3fbd-acf36387b27c',
    'hpgrequestid': '903be2c4-81a0-47a7-9f78-c66f6af56001',
    'Content-type': 'application/json; charset=utf-8',
    'Origin': 'https://login.microsoftonline.com',
    'Connection': 'keep-alive',
}

params = {'mkt': 'en-US'}


def debug(string):
	if args.verbose == True:
		print(string)

def checkemail(email):
	json_data = {
	    'username': f'{email}',
	    'isOtherIdpSupported': True,
	    'checkPhones': False,
	    'isRemoteNGCSupported': True,
	    'isCookieBannerShown': False,
	    'isFidoSupported': True,
	    'originalRequest': 'rQQIARAAjVE7b9NgAMwXp6Ypj0b9A0gWU8GJn3FsFKG0NUlwojqRaUsQSh37i2Ni57Ni50FKBlhgzMxSxIIUMaBOqBKIATF0ypwJMVWVkFARatlIxMIGN5xuutPdrWJ0nJauUX_AkHMmqXqdJg04V3-hvbIUEwF5ui3l07fev_lhPDt4PAZXG0Hg-VIigTqBg1Azjup124BxA7kJ1NMT7wCYAHAMwDgsJNkUy_M8x_Aiz6QEkaLjkDMNaPApMsnM4jhOr5MiA5MkJcIUT_M6W4P6NLy8mekEDWZOqG0P4Gk4Wkdtt-ohP3iB7W4Yfv82ylgbmXKZ2jT7eTvbk_OcVqzp2zsOqagiK8tFhazJ3aZjrtWokmKtWxWZJNdSsM20tEcWfU-v6IIuN1hk55SB4u9k-X73rplUKb86xv5roAMMn7V2UesIw5EHW7Y5iYAvEXASCVOL5xHwamG24KevN0cvn7zO7vc_o4c_d8HRQqJRKhTySuuOW-YLoqYZlqMy0BUsT73uUIjNqZ5TkV0t34NUWpToEQ5GOH6IRxexWIjA1lX6GAffcfD8Qugw-q87JhfB9BK3hBuObrv-yuoeYZvVADVhi5D2iL7rVw1jrrq604E-Id0nZv7Eg-Fw-PFy6PzK2fTs6Yf9X99yJ8s3xCKn2IyuCHSj1ldrHrslZPnBlsYhRm5yQr7gZZgyNEsD1kq_jYV-Aw2',
	    'country': 'US',
	    'forceotclogin': False,
	    'isExternalFederationDisallowed': False,
	    'isRemoteConnectSupported': False,
	    'federationFlags': 0,
	    'isSignup': False,
	    'flowToken': 'AQABAAEAAAAmoFfGtYxvRrNriQdPKIZ-dSrDzOI1sadrPQFeW3_eIKPcQ4sMHR-qIIcsmhA24JiPT3Az6hL5k_Fb5vxULN9dAmkPvFYdGHZGZNi2Jam_UBKOqpICbq6Z1lDlnEttQXuO4J6Q5Xb7Hqn2mx8y3TMeMZkac_wGQ75w3MkoMOe4bbvh9dWjqPlv9TOADzDXuopjPBBKvup5kYAq3Sia_4cpeF4F4HxaEmroq2Oq0vbD_9p6srtLoQ65zgR7qfeivVhcGQjnErK5EHC_C9AqFazewgOPgeUgmujm05lIU-pP_KYH_FGKi-rCmScREaQ1kxlovml1Y2dqp1XMONqQsej33ezuyWs1ECOI0gP_N7J5UOfQ5jBsXHV7qSwZCKg0ey_QCOhVi6mGG8CRUXrbVBr0C7nca-x_VDEkgCO1BYJZFMumvsspeqSoIUfbFLy2bd1HUKcpK-IEBqwQLb7PCkeSj2uv6dDCdRP7MYM-slAxgyK4Vx94e2nC48sn1Y2CQJXt_CHLpI2ID6CRZzQglek85Bx3FW-EzvQX_RbAOMGSvHKy99q-cW0Xvic-02ognND9Xg3L7JXigQscS8Ix4zF15aFC1m-qhUKLdCLseCFOgbmdmToOzSmLgl6aKp2UUlW28KM2nimufRq0A3Z4SlYWtgIoQeijO5dsyTsNWQWEwSAA',
	    'isAccessPassSupported': True,
	}
	response = requests.post('https://login.microsoftonline.com/common/GetCredentialType',params=params,cookies=cookies,headers=headers,json=json_data)
	content=response.text

	if '"IfExistsResult":0'.lower() in content.lower():
		if args.silent == False:
			print(f"{success} Found valid email : {email} ")
			return
		else:
			print(f"{email}")
	elif '"IfExistsResult":1'.lower() in content.lower():
		debug(f"{progress} Invalid email : {email} ")
	else:
		print(f"{fail} An error occurred while checking email : {email}")
		# print(content)
		exit()
	return


if __name__ == '__main__':
	emails=[i.strip() for i in reademails(args.file) if len(i.strip()) > 1 ]
	if args.silent == False:
		banner()
		print(f"{success} Starting Enumeration")
		print(f"{progress} Using {args.threads} threads")
		print(f"{progress} Checking {len(emails)} emails")
		print("")

	with ThreadPoolExecutor(max_workers=args.threads) as pool:
	    try:
	        response_list = list(pool.map(checkemail,emails))
	    except:
	        time.sleep(10)
	        print(f"Sleeping")
	        response_list = list(pool.map(checkemail,emails))