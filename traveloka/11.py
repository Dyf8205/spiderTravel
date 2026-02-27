# -*- coding:UTF-8 -*-
# author:dyf
# time:2026/2/11 17:02
# explain:
import requests
from awswaf.aws import AwsWaf
from urllib.parse import urlparse
from get_proxy import get_proxies
from loguru import logger
session = requests.Session()
proxies = get_proxies()


# baseUrl = 'https://www.traveloka.com/ja-jp/hotel/japan/hilton-tokyo-bay-1000000139391'
baseUrl = "https://www.traveloka.com/ja-jp/hotel/japan/hotel-nikko-osaka-1000000116979"
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'priority': 'u=0, i',
    'referer': baseUrl,
    'sec-ch-ua': '"Not(A:Brand";v="8", "Chromium";v="144", "Google Chrome";v="144"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36',
    # 'cookie': 'clientSessionId=T1-web.01KH5WZ7N2GBHJYCXV2VTX5F25; tv_cs=1; tv-repeat-visit=true; countryCode=US; tv_user={"authorizationLevel":100,"id":null}; _gcl_au=1.1.197414990.1770798436; _tt_enable_cookie=1; _ttp=01KH5WZM0NK2Z7XTGKHQSMDKDS_.tt.1; _fbp=fb.1.1770798436732.183175601700349752; _fwb=173iPz86Wiv5Po8uzjZyngc.1770798437928; __rtbh.lid=%7B%22eventType%22%3A%22lid%22%2C%22id%22%3A%22dJ91OZdDXbFUWI3rQEFv%22%2C%22expiryDate%22%3A%222027-02-11T08%3A27%3A18.103Z%22%7D; _yjsu_yjad=1770798438.daf88895-57b1-445f-bbf0-8a685186766a; _gid=GA1.2.2089500825.1770798439; _ly_su=1770798438.daf88895-57b1-445f-bbf0-8a685186766a; __lt__cid=601fd639-b7f4-4e0b-af1b-cd4f3814d0b2; __lt__sid=a380cc23-ce4d2a63; _im_vid=01KH5WZZS8H9ABX99MSK0KDM8A; _cs_ex=1760605804; _cs_c=1; ttcsid_CFNI0BRC77UEUGLEG00G=1770798436379::KTeX6X3aVyWAQiS4GRXU.1.1770798555149.1; tv_mcc_id=01KH5Y7JC385J15CPRJG13D9TX; tvl=qgdHX7GvehrD9XH5a3S4PUiOJGezXQ9yizVaSxTklwrLYY64AE4apiD1qmHRGaV8gGAQoV6xR5wi1hxtboYegx0JoHbuxL9J5IDMykh7yrn/kmgjvZe3CXlrOt5A94G1h8SGYm0D03zEW7S7g02l9zkAPbkMGQ6AJj+0Bs51j2fX+a/xpVXX1mfFc2XnX665RdYRGMOXmY1RYPoaDZe/4o2DSVZeF8aMq2g/QZhDz9Qh1nTpXB8ahggltPsIsqMqWt6/i9JHfxLSjqxr4qAqEgT/bN5a6dnZ0jubJ26U5eXM0WMA1zSky7I1/5su3gOqvpSAhyJO2AhikPTFDPLTBddLrEb4MbgzdxqXBnjWGlG/Wn6ULKMnMNfGXtA8pNESxbVWc9mUJC6U6r8wkx04c+4CDTx/jJt5ZXoEQTwGFtmvFcCuLSwzN6i0oSIN7Me1ytIbbsmHCGnz3sWzyttR7ib46UomsvnEDZSxzOI9jOxh++MojmBsBHH3jDvpun8w; tvs=qgdHX7GvehrD9XH5a3S4PXWKx93/3Xi103f/kPpnhg2NQFssR/Qj+XlD8T04Iyju+MuKvY7Pp5uHWBnQzrYzg8bNkOr6Ct4jeTn5SRRDoCrOhrxqOCt7gsYLvYv0WUC8d+gyQzq70AhHhvg65it3EHJ8QJVLDxjwhIbxYg4fKH9bPZBZuDO5H0NNMHQUyz3U1N+0NjAmWhSTtggf9gIHJIaLKSmYGn4epBOkel7pAXwVrUUSDqV1s1yuQ6nX+VjCKnVDuZT19rmz/EIO4rDOaOyULFhNd6mLmNHgg0NJunm3NsKhJDtFI1afSbeKadSyXEw2bImmv0C+7A4wSqGznc3wWdOLlzemGQX5jLyfTlyh9ECyOlH1qwRP+rV49MU6GbpHe+//A53te9f8Z0+XAFe4baf+BS5pSC/pI7mJhDwofcjPaW8QtXvU+V1RNkikDD7FUbWmLfrJuk0QzePgz4g66DeD91m56YFYfFCE8qXPNk/6vPDdeNNXYeohnKE6HcoV/fRbU4ccWy+PavoUnQ==; amp_f4354c=5R_FhCPQ0KfAABBDBdJW_F...1jh5svjcs.1jh5u7k34.0.0.0; g_state={"i_l":0,"i_ll":1770799747332,"i_b":"5QHRRiZhST4K8OHkLaoLJmP9kt332/cJpcH4R9UhWzs","i_e":{"enable_itp_optimization":17}}; cto_bundle=Vc90eV9ZcldITiUyQlU4RWoxUWdUJTJGU0lWQmlDaG5MRER2WnNldE5wdUZSZlR0TCUyQk16RmZTQ1NnU25sZkNGUGRoemdSR2JaOGoyZ3pWNmxOSFZSSnR5ZU1iSXVZemp0b3NzNERZY1RBU1FOajhSQ2RuJTJCSEV2djRGeTFUSUNtdHBoWXhwNXJU; amp_1a5adb=GuWJo3_gP4smqbFhOECTEG...1jh5svjcj.1jh5u7lb4.d.0.d; _ga_RSRSMMBH0X=GS2.1.s1770798437$o1$g1$t1770799749$j60$l0$h1212974502; _ga=GA1.1.2093526800.1770798438; wcs_bt=s_2cb982ada97c:1770799749; ttcsid=1770798436380::DQd7iBN5Kc3mN0awBDXK.1.1770799750740.0; ttcsid_CUM82PBC77U4QKJNCRL0=1770798437192::f7UMMbXmFAPRAUCE4GLM.1.1770799750740.1; tvo=L2FwaS92MS90dmxrL2V2ZW50cw==; datadome=ba~yFf4qvPJc9t5rgwLMwdjwtg~h23~dPi85DFDoc~h0Ha5Mn7HRkQvlYxZPvlC0P3HrX47Ufk1XNuPcuBV3bGo_WR~sQL1VIrCE9nQPPrIonYHD7hTf_4OenBiYryja; tv_lt=1770799776962; __smn_fid=cTRl3Ep7c110rQglL1316AiigFUQ94PA3sQzQKq4k_2r28YU; _dd_s=rum=0&expire=1770800671892&logs=1&id=f8d2de8f-2613-47dd-8ae8-f0f87b8f3b04&created=1770798433832; aws-waf-token=23b9b21b-9aa4-4a1b-8764-d7d4692ec5ed:EwoA7HQ8k0krAAAA:Gk6Z3Z2fLpKueu6ljVLbWVGn2LNeOKowSYNX31fMXQqybZaZaZsDeynNkTg57Fv2ZyP+r6hOn/LVJ4ww5fJVEn8Iv0zFfxM+aJrrwGJX2zmqIvd34Zwr/0kxZYpWTG6Il6RiEwyV8qJ+fBWuvQINBQ84EkaoiLkv/bZmkvGiRa9dVfPs3wL7unHWcH/TaUntl0CnYlnRaPAm7H6cDBt+FvI7oK+9olgNkDcpVRb+NR6GI25quADID5Ttf/AXWhWoZ2Pg',
}

response = session.get(
    baseUrl,
    headers=headers,
    proxies=proxies

)
print("详情页")
print(response.status_code)
goku, host = AwsWaf.extract(response.text)
token = AwsWaf(goku, host, urlparse(baseUrl).netloc, proxies)()

with open(baseUrl.split("/")[-1],"w",encoding="utf-8") as f:
    f.write(response.text)

headers = {
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'origin': 'https://www.traveloka.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': baseUrl,
    'sec-ch-ua': '"Not(A:Brand";v="8", "Chromium";v="144", "Google Chrome";v="144"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    # 't-a-v': '262277',
    # 'tv-clientsessionid': 'T1-web.01KH5WZ7N2GBHJYCXV2VTX5F25',
    'tv-country': 'EN',
    'tv-currency': 'USD',
    'tv-language': 'en_EN',
    # 'tv-mcc-id': '01KH5Y7JC385J15CPRJG13D9TX',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36',
    # 'www-app-version': 'release_webacd_20260205-9e27d5b142',
    # 'x-client-interface': 'desktop',
    # 'x-did': 'MDFLSDVXWkhIQUc1RURBRUQ4QjVOTVIxQ1c=',
    'x-domain': 'accomRoom',
    # 'x-route-prefix': 'ja-jp',
    # 'cookie': 'clientSessionId=T1-web.01KH5WZ7N2GBHJYCXV2VTX5F25; tv_cs=1; tv-repeat-visit=true; countryCode=US; tv_user={"authorizationLevel":100,"id":null}; _gcl_au=1.1.197414990.1770798436; _tt_enable_cookie=1; _ttp=01KH5WZM0NK2Z7XTGKHQSMDKDS_.tt.1; _fbp=fb.1.1770798436732.183175601700349752; _fwb=173iPz86Wiv5Po8uzjZyngc.1770798437928; __rtbh.lid=%7B%22eventType%22%3A%22lid%22%2C%22id%22%3A%22dJ91OZdDXbFUWI3rQEFv%22%2C%22expiryDate%22%3A%222027-02-11T08%3A27%3A18.103Z%22%7D; _yjsu_yjad=1770798438.daf88895-57b1-445f-bbf0-8a685186766a; _gid=GA1.2.2089500825.1770798439; _ly_su=1770798438.daf88895-57b1-445f-bbf0-8a685186766a; __lt__cid=601fd639-b7f4-4e0b-af1b-cd4f3814d0b2; __lt__sid=a380cc23-ce4d2a63; _im_vid=01KH5WZZS8H9ABX99MSK0KDM8A; _cs_ex=1760605804; _cs_c=1; ttcsid_CFNI0BRC77UEUGLEG00G=1770798436379::KTeX6X3aVyWAQiS4GRXU.1.1770798555149.1; tv_mcc_id=01KH5Y7JC385J15CPRJG13D9TX; tvl=qgdHX7GvehrD9XH5a3S4PUiOJGezXQ9yizVaSxTklwrLYY64AE4apiD1qmHRGaV8gGAQoV6xR5wi1hxtboYegx0JoHbuxL9J5IDMykh7yrn/kmgjvZe3CXlrOt5A94G1h8SGYm0D03zEW7S7g02l9zkAPbkMGQ6AJj+0Bs51j2fX+a/xpVXX1mfFc2XnX665RdYRGMOXmY1RYPoaDZe/4o2DSVZeF8aMq2g/QZhDz9Qh1nTpXB8ahggltPsIsqMqWt6/i9JHfxLSjqxr4qAqEgT/bN5a6dnZ0jubJ26U5eXM0WMA1zSky7I1/5su3gOqvpSAhyJO2AhikPTFDPLTBddLrEb4MbgzdxqXBnjWGlG/Wn6ULKMnMNfGXtA8pNESxbVWc9mUJC6U6r8wkx04c+4CDTx/jJt5ZXoEQTwGFtmvFcCuLSwzN6i0oSIN7Me1ytIbbsmHCGnz3sWzyttR7ib46UomsvnEDZSxzOI9jOxh++MojmBsBHH3jDvpun8w; tvs=qgdHX7GvehrD9XH5a3S4PXWKx93/3Xi103f/kPpnhg2NQFssR/Qj+XlD8T04Iyju+MuKvY7Pp5uHWBnQzrYzg8bNkOr6Ct4jeTn5SRRDoCrOhrxqOCt7gsYLvYv0WUC8d+gyQzq70AhHhvg65it3EHJ8QJVLDxjwhIbxYg4fKH9bPZBZuDO5H0NNMHQUyz3U1N+0NjAmWhSTtggf9gIHJIaLKSmYGn4epBOkel7pAXwVrUUSDqV1s1yuQ6nX+VjCKnVDuZT19rmz/EIO4rDOaOyULFhNd6mLmNHgg0NJunm3NsKhJDtFI1afSbeKadSyXEw2bImmv0C+7A4wSqGznc3wWdOLlzemGQX5jLyfTlyh9ECyOlH1qwRP+rV49MU6GbpHe+//A53te9f8Z0+XAFe4baf+BS5pSC/pI7mJhDwofcjPaW8QtXvU+V1RNkikDD7FUbWmLfrJuk0QzePgz4g66DeD91m56YFYfFCE8qXPNk/6vPDdeNNXYeohnKE6HcoV/fRbU4ccWy+PavoUnQ==; amp_f4354c=5R_FhCPQ0KfAABBDBdJW_F...1jh5svjcs.1jh5u7k34.0.0.0; g_state={"i_l":0,"i_ll":1770799747332,"i_b":"5QHRRiZhST4K8OHkLaoLJmP9kt332/cJpcH4R9UhWzs","i_e":{"enable_itp_optimization":17}}; cto_bundle=Vc90eV9ZcldITiUyQlU4RWoxUWdUJTJGU0lWQmlDaG5MRER2WnNldE5wdUZSZlR0TCUyQk16RmZTQ1NnU25sZkNGUGRoemdSR2JaOGoyZ3pWNmxOSFZSSnR5ZU1iSXVZemp0b3NzNERZY1RBU1FOajhSQ2RuJTJCSEV2djRGeTFUSUNtdHBoWXhwNXJU; amp_1a5adb=GuWJo3_gP4smqbFhOECTEG...1jh5svjcj.1jh5u7lb4.d.0.d; _ga_RSRSMMBH0X=GS2.1.s1770798437$o1$g1$t1770799749$j60$l0$h1212974502; _ga=GA1.1.2093526800.1770798438; wcs_bt=s_2cb982ada97c:1770799749; ttcsid=1770798436380::DQd7iBN5Kc3mN0awBDXK.1.1770799750740.0; ttcsid_CUM82PBC77U4QKJNCRL0=1770798437192::f7UMMbXmFAPRAUCE4GLM.1.1770799750740.1; tvo=L2FwaS92MS90dmxrL2V2ZW50cw==; tv_lt=1770799776962; __smn_fid=cTRl3Ep7c110rQglL1316AiigFUQ94PA3sQzQKq4k_2r28YU; datadome=tBjyPDUmORe18gW~9CD1iEu15RMG8oZx_dl_jcFdWGyDyAnsG7GRxeY_Y0QRg39XQRfjdoGrxf_unjcdNCo4yiLWSO9vC2gg5GSxQ6FoE5fhqJ02sQ5Dtc2nY6kXCqJz; aws-waf-token=23b9b21b-9aa4-4a1b-8764-d7d4692ec5ed:EwoAngo+CY4GAAAA:a+liawAb0A2wg3s40EKsh3UVocqB0RBgm0h6JxxxUlgZoM0oj3ey/DuszlIHThccSazFVmvGvKkKaJl8pSfniK0HUGR3cYAJ4GoH58aaQhWgBW7VXLPFbIdBn1F8Kr2uX+TPAqzG7wDUIspDmt7tjgki5GJcQ8Svke8OkN17xvK/CALlIIv8xbpCQwu7F/EAL3tlOKfqjJwykepJf/hNrbpT9ma5jSW2rVKa/0NztL3Vd9G3hbroLjiFkFQL4yalnfqE; _dd_s=rum=0&expire=1770800772243&logs=1&id=f8d2de8f-2613-47dd-8ae8-f0f87b8f3b04&created=1770798433832',
}

import time
import random
def ue():
    e = random.randint(0, 999999988)
    t = random.randint(0, 999999988)
    return f"{e}{t}"


wait_time = random.uniform(1, 2)
time.sleep(wait_time)

fbp = f"fb.1.{int(time.time() * 1000)}.{ue()}"
print(f"随机等待 {wait_time:.2f} 秒... 获取{fbp}")


wait_time = random.uniform(1, 2)
print(f"随机等待 {wait_time:.2f} 秒...")
time.sleep(wait_time)

timestamp = str(int(time.time() * 1000))
json_data = {
    'fields': [],
    'data': {
        'contexts': {
            'hotelDetailURL': baseUrl,
            'bookingId': None,
            'sourceIdentifier': 'HOTEL_DETAIL',
            'shouldDisplayAllRooms': False,
            'marketingContextCapsule': {
                'fb_browser_id_fbp': fbp,
                'timestamp': timestamp,
                'initial_page_full_url': 'https://www.traveloka.com/ja-jp/hotel',
                'initial_timestamp': timestamp,
                'page_full_url': baseUrl,
                'client_user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36',
            },
        },
        'prevSearchId': 'undefined',
        'numInfants': 0,
        'ccGuaranteeOptions': {
            'ccInfoPreferences': [
                'CC_TOKEN',
                'CC_FULL_INFO',
            ],
            'ccGuaranteeRequirementOptions': [
                'CC_GUARANTEE',
            ],
        },
        'rateTypes': [
            'PAY_NOW',
            'PAY_AT_PROPERTY',
        ],
        'isJustLogin': False,
        'isReschedule': False,
        'monitoringSpec': {
            'referrer': '',
        },
        'hotelId': baseUrl.split("/")[-1].split("-")[-1],
        'currency': 'USD',
        'labelContext': {},
        'isExtraBedIncluded': False,
        'hasPromoLabel': False,
        'supportedRoomHighlightTypes': [
            'ROOM',
        ],
        'checkInDate': {
            'day': '14',
            'month': '3',
            'year': '2026',
        },
        'checkOutDate': {
            'day': '19',
            'month': '3',
            'year': '2026',
        },
        'numOfNights': 1,
        'numAdults': 1,
        'numRooms': 1,
        'numChildren': 0,
        'childAges': [],
        # 'tid': 'ae75aca7-5e60-4239-ae57-529d8fc4ab7f',
    },
    'clientInterface': 'desktop',
}





session.cookies.update({
   "aws-waf-token" :token})
response = session.post('https://www.traveloka.com/api/v2/hotel/search/rooms',  headers=headers, json=json_data,proxies=proxies)
print(response.status_code)
print(response.text)
with open("room.json", "w",encoding="utf-8") as outfile:
    outfile.write(response.text)



headers = {
    'accept': '*/*',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'origin': 'https://www.traveloka.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://www.traveloka.com/ja-jp/hotel/japan/hotel-nikko-osaka-1000000116979',
    'sec-ch-ua': '"Not(A:Brand";v="8", "Chromium";v="144", "Microsoft Edge";v="144"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    't-a-v': '262268',
    'tv-clientsessionid': 'T1-web.01KH7ZDTK6EMV8QTRMVFATE7SA',
    'tv-country': 'JP',
    'tv-currency': 'JPY',
    'tv-language': 'ja_JP',
    'tv-mcc-id': '01KH7ZDQWXENMH7V41AGRVZKK7',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36 Edg/144.0.0.0',
    'www-app-version': 'release_webacd_20260205-9e27d5b142',
    'x-client-interface': 'desktop',
    'x-did': 'MDFLSDdaRFIwMlhYMzRTR1pYNzE1SjJXWEE=',
    'x-domain': 'content',
    'x-route-prefix': 'ja-jp',
    # 'cookie': 'datadome=mwpualz3uRBoI2Xe64~g5yB2Sy1Yy2fBCpiY9Hz0qexmuAs8mogrUMNB8~RH8ZSwS9jNrOIZXA7ZTpgi~pZ_ASsCAKzDAdXKDkq08fnZdRw_KrwOkDLPWIqLui1WzWAj; tv-repeat-visit=true; tv_mcc_id=01KH7ZDQWXENMH7V41AGRVZKK7; countryCode=JP; clientSessionId=T1-web.01KH7ZDTK6EMV8QTRMVFATE7SA; tv_cs=1; _fbp=fb.1.1770868110084.563310523528227809; amp_f4354c=LGOKxDr39OuRmf2whAZ9Ic...1jh7vdstd.1jh7vdstd.0.0.0; _gcl_au=1.1.2036065022.1770868111; _tt_enable_cookie=1; _ttp=01KH7ZDYEJ6EVXD142G8J2QA40_.tt.1; __rtbh.lid=%7B%22eventType%22%3A%22lid%22%2C%22id%22%3A%22DTnGNeEjYo5bMgNEBIPw%22%2C%22expiryDate%22%3A%222027-02-12T03%3A48%3A32.615Z%22%7D; _ga_RSRSMMBH0X=GS2.1.s1770868112$o1$g0$t1770868112$j60$l0$h1222283564; _fwb=75olTxPOZpVmW5689zkfqC.1770868112772; wcs_bt=s_2cb982ada97c:1770868112; _yjsu_yjad=1770868113.336efc3f-0c2b-453b-a1fb-4c56d149ae33; _ga=GA1.2.1647905844.1770868113; _gid=GA1.2.76914534.1770868113; _ly_su=1770868113.336efc3f-0c2b-453b-a1fb-4c56d149ae33; cto_bundle=Kdsm4l9oNGtVdHRDbkt3NFdHUWhreEFmMWdVRWlwcXd3UXlHZXNIWnlKd2JWQmZCY1Z5UkdjWHIlMkZSMHVJQlBRYklic0Rhc3JkTzNDUiUyRmdBVWY0NUlxd09oZTFYaWh3d1NxNkJmUlNBQ3k5VG1zRTV5QURhRDZlSFBpV29WaGZzTVIwZm8; __lt__cid=30c2fd55-cdfc-45e4-92ee-7bd7f8bc43c1; __lt__sid=3c68d9ce-f7b8ba1a; _im_vid=01KH7ZE2VZXPRNPG2V99P6SJ08; ttcsid_CFNI0BRC77UEUGLEG00G=1770868111835::a_b13NNDwh7C1nUmkvIJ.1.1770868121869.1; tv_lt=1770868141054; g_state={"i_l":0,"i_ll":1770868198174,"i_b":"PGRbsu615boryNX8xM7GKqyyTyduFIi3MzPbhbIHh00","i_e":{"enable_itp_optimization":0}}; __smn_fid=DZq6A9882QvYkbeT6fjbFwiw8gQQ_djc_8QzQJj8vpLN28sU; aws-waf-token=5c7433c4-197f-447a-851d-dcd13dbd57d9:AQoAjv4Z98aJAAAA:0080RoRRTHVJjG1EpwKhxH6qI/+cU1Qar/8CP4NepSS/GzHFsyGrqy5A63on56INuL1OgqDCCzFQQVYnya6EZeuLME/Fmwq6/EBWE/QnP8twAtz/5H4zoiX5ItGxx2nEhEizUHm1mQznXUeE4Wofs/L8kJRxsXb/jjdYryA6Z6aT6oABRpDpylZu26cMUS/vubQ=; amp_1a5adb=ihtV6NniCjsOgpybuOYUQr...1jh7vdst4.1jh7vig5n.c.0.c; ttcsid=1770868111838::-bAjSSQwT6tiXPrJPeRq.1.1770868263324.0; ttcsid_CUM82PBC77U4QKJNCRL0=1770868125048::vuR0DZT_44qy_FojfGx7.1.1770868263325.0; _dd_s=rum=0&expire=1770869161040&logs=1&id=76da548a-e86f-4550-8572-7d8088cc780b&created=1770868105209',
}

json_data = {
    'fields': [],
    'data': {
        'productId':  baseUrl.split("/")[-1].split("-")[-1],
        'productType': 'ACCOMMODATION',
        'productSubtype': None,
        'filters': None,
        'subFilters': None,
        'page': 2,
        'size': 10,
        'sort': None,
    },
    'clientInterface': 'desktop',
}

response = session.post(
    'https://www.traveloka.com/api/v2/explore/media-gallery/traveler',
    headers=headers,
    json=json_data,
)
print(response.status_code)
print(response.text)
with open("traverler.json", "w",encoding="utf-8") as outfile:
    outfile.write(response.text)