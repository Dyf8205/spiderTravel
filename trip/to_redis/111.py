import requests

cookies = {
    'UBT_VID': '1771079563708.1bc27j67lyto',
    '_fwb': '6711gAXhIEgqJEzciOXidZ.1771079567889',
    '_RGUID': '7164722f-0725-458f-abcb-79ce9012c52a',
    'GUID': '09034178112323024667',
    'GUID.sig': 'Uy1n6DZDCMW7ZxXdLaDPjFEINF3cTBe_JsV5RopaXpQ',
    '_abtest_userid': '5ded0f42-f257-40cc-899e-7a46719319df',
    'ibu_online_jump_site_result': '{"isShowSuggestion":false}',
    '_gcl_au': '1.1.2106473264.1771465257',
    'ibu_pwa_insvisit': '%7B%22vid%22%3A%221771079563708.1bc27j67lyto%22%2C%22time%22%3A1771465321473%7D',
    'ibu_online_home_language_match': '%7B%22isFromTWNotZh%22%3Afalse%2C%22isFromIPRedirect%22%3Afalse%2C%22isFromLastVisited%22%3Afalse%2C%22isRedirect%22%3Atrue%2C%22isShowSuggestion%22%3Afalse%2C%22lastVisited%22%3A%22https%3A%2F%2Fid.trip.com%3Flocale%3Did_id%22%7D',
    'ibu_country': 'TH',
    'ibu_cookie_strict': '0',
    '_tp_search_latest_channel_name': 'hotels',
    '_gid': 'GA1.2.446010147.1771635640',
    'ubtc_trip_pwa': '0',
    'x-ctx-user-recognize': 'NON_EU',
    'ibu_online_permission_cls_ct': '3',
    'ibu_online_permission_cls_gap': '1771635718620',
    '_ga': 'GA1.2.2022414444.1771465290',
    '_ga_37RNVFDP1J': 'GS2.2.s1771635639$o1$g1$t1771635729$j60$l0$h0',
    '_ga_X437DZ73MR': 'GS2.1.s1771635672$o2$g1$t1771635733$j60$l0$h0',
    '_uetsid': 'bd963d000ec011f1a718a947fc16d521',
    '_uetvid': 'aa442ca00d3411f19623e5b72d95ae64',
    'GUID': '09034178112323024667',
    'nfes_isSupportWebP': '1',
    'ibulanguage': 'TH',
    'ibulocale': 'th_th',
    'cookiePricesDisplayed': 'THB',
    'ibusite': 'TH',
    'ibugroup': 'trip',
    '_resDomain': 'https%3A%2F%2Faw-s.tripcdn.com',
    '_bfa': '1.1771079563708.1bc27j67lyto.1.1771638250637.1771638798201.5.2.10320668147',
    'intl_ht1': 'h4%3D6898_12486039',
}

headers = {
    'accept': 'application/json',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'currency': 'THB',
    'locale': 'th-TH',
    'origin': 'https://th.trip.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'sec-ch-ua': '"Not(A:Brand";v="8", "Chromium";v="144", "Google Chrome";v="144"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36',

  }



json_data = {
    'hotelId': 12486039,
    'versionControl': [
        {
            'key': 'EnableVideo',
            'value': 'F',
        },
    ],
    'head': {

        'ctok': '',
        'cver': '0',
        'lang': '01',
        'sid': '',
        'syscode': '09',
        'auth': '',
        'xsid': '',
        'extension': [
            {
                'name': 'cityId',
                'value': '',
            },
            {
                'name': 'checkIn',
                'value': '',
            },
            {
                'name': 'checkOut',
                'value': '',
            },
        ],
        'Locale': 'th-TH',
        'Language': 'th',
        'Currency': 'THB',

        'platform': 'PC',
        'bu': 'IBU',
        'group': 'trip',
        'aid': '',
        'ouid': '',
        'locale': 'th-TH',
        'region': 'TH',
        'timezone': '8',
        'currency': 'THB',
        'pageId': '111111',

        'guid': '',
        'isSSR': False,
    },
}

response = requests.post(
    'https://th.trip.com/restapi/soa2/28820/ctgethotelalbum',
    # params=params,
    # cookies=cookies,
    headers=headers,
    json=json_data,
)
print(response.json())
# Note: json_data will not be serialized by requests
# exactly as it was in the original request.
#data = '{"hotelId":12486039,"versionControl":[{"key":"EnableVideo","value":"F"}],"head":{"cid":"1771079563708.1bc27j67lyto","ctok":"","cver":"0","lang":"01","sid":"","syscode":"09","auth":"","xsid":"","extension":[{"name":"cityId","value":""},{"name":"checkIn","value":""},{"name":"checkOut","value":""}],"Locale":"th-TH","Language":"th","Currency":"THB","ClientID":"09034178112323024667","platform":"PC","bu":"IBU","group":"trip","aid":"","ouid":"","locale":"th-TH","region":"TH","timezone":"8","currency":"THB","pageId":"10320668147","vid":"1771079563708.1bc27j67lyto","guid":"","isSSR":false}}'
#response = requests.post(
#    'https://th.trip.com/restapi/soa2/28820/ctgethotelalbum',
#    params=params,
#    cookies=cookies,
#    headers=headers,
#    data=data,
#)