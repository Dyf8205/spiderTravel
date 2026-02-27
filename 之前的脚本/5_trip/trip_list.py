# -*- coding:utf-8 -*-
import requests
import json


headers = {
    "accept": "application/json",
    "accept-language": "zh-CN,zh;q=0.9",
    "cache-control": "no-cache",
    "content-type": "application/json",
    "currency": "USD",
    "locale": "en-XX",
    "origin": "https://www.trip.com",
    # "p": "60676774416",
    "phantom-token": "1004-common-aHTWadY4TIDPxpaY8FwA7RDcvBpw1dv76vBDJopyl1iA9ysowpDWqQy80JNgRmBw1dYspJBUjfqwzPiUXyU5EPAEUpy9Hi7QRZSvnDwO6ycJpgRHMWgY4PeoXKFAYsXRz9y3cwTsw3zY8qj4Gw5qWp0inDWSXJsNRm5YTneqProfx3YpcYPoIfcRSzKAHjnTj51EaBysEs4iH5YgE9BY4nyHEZ8YsSyaDKBTKboKMgIgOjDzwOaeDpE4zIpowkZiopRZEdSYSQybzKNai1BjSTj7aWdOyPEsSYgUyUFWm4eZXyaBjNEcfi0MyDcwaoe16jBqIzEnHiP5JZzYMkY81jfE6gYhQwQbw5sKscj0Xwd7rGneqXYzETQig4JfsYsqW1XYO4JPEPQYMgyXPR58Y0En0Y4byfOY7ORNEATYk8wOfwAmKcNjZqwFPrXQi7cvt9jfESqin3JOUYMTWO4Yk8JzEAsYD0yl0R8XYgEP3YQPyXzYlkY4GjcBEAqvTY8HR88KqPwThRHnyQDwHBYnGYOXw43ySBwGkja5RlhRLbvhswSMIFAwPdjglv5ailqILdxGXvtTJZZxNgxFSW7dIlMJdpjq0jnYANiMDKmNy0XyOpWQmv1Zy1PYnhJkBwZ3joMeMSiq0EtUYG0yBpekzEQTwtSJ0Nv3gesTEO1j35wstRdteB9yH9YPTJXbJkFEL3EbhJ51Y1bEhAv7hvN0EHHxsMIzjcYb8yHkWqPY3cRgDJk0YQowXLEcmvnXYAnwDfid9rlgegYLBWA1yS9IZMY6pEO6ilv6LW5Y9kEFLekHidzv5SeoZYNtif4Yqcj7nrohwMY7nIq3Jh9v3FeZPE1hjDhWZ5JkkxtEdYpE5gyffxdarMlKgBeQXE6FWOUJ5XIkHYSYX7e8FiNZrf3RSNi35wk8w0geZLy0Fw9Xj3mIamwocW3YNgv97ykax4kR0ni3Dwg8waMedkyXzYHAj1NJHcimDE8YLOrqoEt7v0TiqBvZUETUwPMvDlj7YakrMoIoqrtoYaUi1DwS5RnpEUFWpkylHitSYXYb7wt7YSwFLJT1J3hEbXwmYpOefaeZqJl9jOnwT8vX5jslegmK3BJtYM8x9mESgYL6YSUYhSxpJ1YU1J0yMNwzajfNwDMvtMjnDynLwG3xzYpfwPnj0arcXY3zWsMWUBYQzWzNYfYGPiqAKm9iN6jzLiUnitkxFgWM7jmrL1xFNYpfwLkI6r5ykMxdUYU8jH4jlpWmjLJsMyGXYmY9ZKnHyHgrhARMDWgDimoYaOWNpwfXwSajaTRgLEs1j3BK1beLl",
    # "pid": "fa12d936-6014-4c2b-b6e1-8c297754bccb",
    "pragma": "no-cache",
    "priority": "u=1, i",
    "referer": "https://www.trip.com/hotels/list?city=228&checkin=2025/12/21&checkout=2025/12/22",
    "sec-ch-ua": "\"Google Chrome\";v=\"135\", \"Not-A.Brand\";v=\"8\", \"Chromium\";v=\"135\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    # "trip-trace-id": "1762267681196.6ef3LgHqXvNL-1766286030561-1458429102",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
    # "x-traceid": "1762267681196.6ef3LgHqXvNL-1766286030561-1458429102"
}

url = "https://www.trip.com/htls/getHotelList"
params = {
    "x-traceID": "1762267681196.6ef3LgHqXvNL-1766286030561-1458429102"
}
data = {
    "guideLogin": "T",
    "search": {
        "checkIn": "20251221",
        "checkOut": "20251222",
        "sourceFromTag": "",
        "filters": [
            {
                "filterId": "29|1",
                "value": "1|2",
                "type": "29"
            },
            {
                "filterId": "17|1",
                "type": "17",
                "value": "1",
                "subType": "2"
            },
            {
                "filterId": "80|0|1",
                "type": "80",
                "value": "0",
                "subType": "2"
            }
        ],
        "location": {
            "geo": {
                "countryID": 0,
                "provinceID": 0,
                "cityID": 228,
                "districtID": 0,
                "oversea": True
            },
            "coordinates": []
        },
        "pageIndex": 4,
        "pageSize": 20,
        "needTagMerge": "T",
        "roomQuantity": 1,
        "orderFieldSelectedByUser": False,
        "hotelId": 0,
        "hotelIds": [],
        "lat": 35.698333,
        "lng": 139.783652,
        "tripWalkDriveSwitch": "T",
        "resultType": "",
        "nearbyHotHotel": {},
        "recommendTimes": 0,
        "crossPromotionId": "",
        "travellingForWork": False
    },
    "batchRefresh": {
        "batchId": "",
        "batchSeqNo": 0
    },
    "queryTag": "NORMAL",
    "mapType": "MAPBOX",
    "extends": {
        "crossPriceConsistencyLog": "",
        "NewTaxDescForAmountshowtype0": "B",
        "TaxDescForAmountshowtype2": "T",
        "MealTagDependOnMealType": "T",
        "MultiMainHotelPics": "T",
        "enableDynamicRefresh": "T",
        "isFirstDynamicRefresh": "T",
        "ExposeBedInfos": "F",
        "TaxDescRemoveRoomNight": "",
        "priceMaskLoginTip": "",
        "singleSearchMergeListB": "F",
        "needSpecialHotelUnSatisfyText": "F",
        "NeedHotelHighLight": "T",
        "NeedNewHighLightModule": "",
        "NeedBanCommentTag": "",
        "needEntireSetRoomDesc": "T"
    },
    "head": {
        "platform": "PC",
        "bu": "ibu",
        "group": "TRIP",
        "locale": "en-XX",
        "timeZone": "8",
        "currency": "USD",
        "p": "60676774416",
        "pageID": "10320668148",
        "deviceID": "PC",
        "clientVersion": "0",
        "frontend": {
            "sessionID": "11",
            "pvid": "11"
        },
        "extension": [
            {
                "name": "cityId",
                "value": "228"
            },
            {
                "name": "checkIn",
                "value": "2025/12/21"
            },
            {
                "name": "checkOut",
                "value": "2025/12/22"
            },
            {
                "name": "region",
                "value": "XX"
            }
        ],
        "tripSub1": "",
        "ticket": "",
        "href": "https://www.trip.com/hotels/list?city=228&checkin=2025/12/21&checkout=2025/12/22",
        "deviceConfig": "L"
    }
}
data = json.dumps(data, separators=(',', ':'))
response = requests.post(url, headers=headers, params=params, data=data)

print(response.text)
print(response)