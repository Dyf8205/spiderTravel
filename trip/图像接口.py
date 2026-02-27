import requests

# cookies = {
#     'GUID': '09034038212685890828',
#     'nfes_isSupportWebP': '1',
#     'ibulanguage': 'JP',
#     'ibulocale': 'ja_jp',
#     'cookiePricesDisplayed': 'JPY',
#     'ibu_country': 'JP',
#     'ibu_cookie_strict': '0',
#     'ibusite': 'JP',
#     'ibugroup': 'trip',
#     '_resDomain': 'https%3A%2F%2Faw-s.tripcdn.com',
#     'UBT_VID': '1771297777554.9228uRV3XXVN',
#     '_bfa': '1.1771297777554.9228uRV3XXVN.1.1771297779357.1771297779357.1.1.10320668147',
#     'intl_ht1': 'h4%3D228_125202955',
# }

headers = {
    'accept': 'application/json',
    'accept-language': 'zh-CN,zh;q=0.9',
    'content-type': 'application/json',
    'cookieorigin': 'https://jp.trip.com',
    'origin': 'https://jp.trip.com',
    'priority': 'u=1, i',
    'referer': 'https://jp.trip.com/hotels/tokyo-hotel-detail-125202955/grand-hostel-ldk-tokyo-nishikasai/?curr=JPY&locale=ja_jp',
    'sec-ch-ua': '"Not:A-Brand";v="99", "Microsoft Edge";v="145", "Chromium";v="145"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36 Edg/145.0.0.0',
    # 'cookie': 'GUID=09034038212685890828; nfes_isSupportWebP=1; ibulanguage=JP; ibulocale=ja_jp; cookiePricesDisplayed=JPY; ibu_country=JP; ibu_cookie_strict=0; ibusite=JP; ibugroup=trip; _resDomain=https%3A%2F%2Faw-s.tripcdn.com; UBT_VID=1771297777554.9228uRV3XXVN; _bfa=1.1771297777554.9228uRV3XXVN.1.1771297779357.1771297779357.1.1.10320668147; intl_ht1=h4%3D228_125202955',
}

json_data = {
    'hotelId': 6070530,
    'versionControl': [
        {
            'key': 'EnableVideo',
            'value': 'T',
        },
    ],
    'head': {
        'platform': 'PC',
        'cver': '0',
        'bu': 'IBU',
        'group': 'trip',
        'aid': '',
        'sid': '',
        'ouid': '',
        'locale': 'ja-JP',
        'region': 'JP',
        'timezone': '8',
        'currency': 'JPY',
        'pageId': '10320668147',
        'guid': '',
        'isSSR': False,
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
    },
}

response = requests.post(
    'https://jp.trip.com/restapi/soa2/28820/ctgethotelalbum',
    # cookies=cookies,
    headers=headers,
    json=json_data,
)

print(response.json())