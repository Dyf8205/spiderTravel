import requests
import json


headers = {
    "accept": "application/json",
    "accept-language": "zh-CN,zh;q=0.9",
    "cache-control": "no-cache",
    "content-type": "application/json",
    "cookieorigin": "https://hk.trip.com",
    "origin": "https://hk.trip.com",
    # "phantom-token": "1004-common-LZFKmQIA4EhFEM4RLUJHfJo4WLNemBwLHj0ZyfpwlpjaBWDTK1LJNOvh5iUlws4Eg6wqLvbzioPJtXw5OJ49EzSiZsjzpyopiT6Y0oIAFJpSinXitDrmY3qEHcvaGwTbRLSysSw4Qw35JTfw1pjkQWQSRL1i7Zv08EbTjS7ehzi0hWLY5PKnzj4BW8aK0ZYdFjNzEopyQEU8iqAYFEB5YpByAEZfYkpytfK4tr5lI1fjF7wUkegcEGfIM9wPDiLbRSE6kYnSydLKDQi8pj9PjoNWSPyHEzBYLtypXyXDjZzjatE58e3XWkEl5Y93y4ES5iDQyS4w3PeGBjkXIkFw1HYFaW8LEk8Rd1jpEFoih8JlbWSXiqkeknylSEDEPtY9kwtXwHaetBjSgIpkxDqyoEq3inmJdOi7Ow47R5LYX6E4Em1YSZwUsKMtiqAjTAjkFWGpxT1yhEZXiaXJmNR4LRPpvh5YX5E9sYZ1iA9vnLYFEhlYOpwb1wX0KnpjmOwoPrfpxGhYUEOaiAzJfaY3BWflYUQwaDetoWs6RhHeFcR9PvTEaMYl3wGQwbDKDljzpwtnrLgRbmvXFjaEXPiqnJ4UY3fWt6YfHwPle9XWh9RQGe7MYmSWAEalYHGwZBEnUy18vc6WZOjHE8AiQdJ4oYbEHPY95w04wLFKH6emLWzky4TwLzjN7YPE1UioFJdXW1E1lY3Bwz1wo4wkbYAEdbiqsJO3R5EB6YkQwGmEgbxBZj03y7EOAiDdJsEDPYXhwZ3wbnvUOw3LwgEX4imBJfFvkXePfJSES3YcBwbPJMDEOqwdFwQ1vDFwA8woENoindJFUv9HetZJ7E8pYzNwlGKsTiGajbljpaW1OvB5YgkeTzJBMvqFjtXrDUj8mIgE3hitoJDBvnsEqFyS4xGQYAgYa3YXHYD7YzLYZ6YGJ8XyXj4YOzI9bvOQizQRLay96wDpwMLJUMwmdjO9WShRHpWB5RUPvXPWt8IXzvnQEp7JOtjLhKmljOmespE49rtzjAGRXhJbNj1tR9ybYllxXTe6GY7QRPFyXhRbTJpBikGyN6WbtJnpeUqiXqW5cEH3y84eM4EStJo4vszvUOeq9vOBw8pJh5jkUeQnED8Ealv4nyfLyQ3ELOJoOvzUjXpY1nJOfJUdezqYbJhYNbI6AjDbeonRZ9JM9YTqwtFEO7vh8Yq8wUEhXIhaEmYT1w3DRqnRkAYgLEtvSNw7Nv6YHjm8xlFeqmvHBeM8YOSilgYFOjm5r4SxNYTpyBlEk5YXLeH7EFZj7lWhmW9fKFSifYMnjP7i61jltrMzKhmeaSEZ8WSHELGI9MykY4dJ9aWglEUDRs8iBMwHLwdMek9yOUw6OjmMY4LEMhRoYfNe9QWo7WLdRkdi17wSOws7e5HylhYDojcpyfkymkw9Y88x4QR0gKDZi1liD9wc4JNdwlDvqYcAr5svlEoOYtLiGtwbXRGpEsHWtQw6qR0UKHYHSRHTwq4Y6hJmXElHiBJSYNBxDhvklv4Gjd3whcvQ0jl5iXBRDnKnYmpRPXY5qyXmYO3w6nIBEUYPhWU8KAXemHjn7wzNvGnjzOxDLW5XEMYsQr0nvGGxPSR9zJmTWT1i0J6awBYSae36yO6ifljbfianiQpxacWMsjtr8cx1gY09wkPIzrTy1fxzmYb9jBFjf4WAjQqYPBybnRAYhpvaqi45Jk7RabWgliFfYcpWZAwaPwl6j8FRQFEXmy8Ajg1yP6",
    "pragma": "no-cache",
    "priority": "u=1, i",
    # "referer": "https://hk.trip.com/",
    "sec-ch-ua": "\"Google Chrome\";v=\"135\", \"Not-A.Brand\";v=\"8\", \"Chromium\";v=\"135\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
}

url = "https://hk.trip.com/restapi/soa2/28820/ctGetNearbyHotelList"
data = {
    "searchCondition": {
        "adult": 2,
        "child": 0,
        "age": "",
        "hotelId": 119242392,
        "cityId": 36124,
        "checkIn": "20260119",
        "checkOut": "20260120",
        "roomQuantity": 1,
        "pageSize": 20,
        "priceType": "1",
        "mapType": "mb",
        # "url": "https://hk.trip.com/hotels/v2/detail/?cityEnName=Noida&cityId=36124&hotelId=119242392&checkIn=2026-01-19&checkOut=2026-01-20&adult=2&children=0&crn=1&ages=&curr=HKD&barcurr=HKD&hoteluniquekey=H4sIAAAAAAAA_-M6zsTFJMEkdYCJY8bWf51sQsyGBmYae_kMnjBarI92fBO4Q671cJ2DZ6Et1_XFag0OATwzGGf8fWuxgpFxI2NM_6GvGnMsHHYwsp1g3MuygOnbl7cWp1hYOVaKSrBcYtnJGF2tlJ1aqWRloqNUklmSk6pkpfR00bynDXuer2hV0lFKSS1OBgoBWYm5-aV5JUC2kbmekSVQoCSxwjMFrDE5MSe5NCexJDWksgBogJGOUmaxc0lRZkFQam5mSUkqUFVaYk5xKkg8KLUYKJMMFgQZWwTlZ-bnQXQboIiFJeaUpkJUAu1zS4VaYVgb-4iFKTr2Bctevk8sDL9YGJpYGbpYGSaxsnHc3s8swbKLlS8wwCjCLFLXMELXyV_X9QLrQRYpeUMDAwNTQ2NTU12DREsLC8PUZF0TSwNzQ2NdYwNjc1ONDx-m_91ibCR7ilHK0NzMyMjM3MzC0NDSTM8sNc3YJ92jMKLMz8eDMYjNycLY0M05yoaL2dMvSLBP-dqjYIYt9lLMHt4uipVyd-Zuvf3GXgskZwiTC0x_u437bOkB-0iYfBJrVYauh3dGv0gBYwMjYxcjtwCjB2MEYwWIt4qRnYvZwMxQgG0DI-MOxv8wwPiKEWQJADnw6OUVAgAA&masterhotelid_tracelogid=100051355-0a9881ec-490713-30375&detailFilters=17%7C5%7E17%7E5*131%7C0%7E131%7E28.6170798%7C77.373961%7CTownhouse+The+Madhav+Sector+58+Noida+Near+ISKCON+Temple+Noida%7C0*80%7C1%7C0%7E80%7E1*29%7C1%7E29%7E1%7C2&hotelType=normal&display=inctotal&subStamp=1035&isCT=true&isFlexible=F&locale=zh-HK&isRightClick=T"
    },
    "filterCondition": {
        "rate": 0,
        "priceRange": {
            "highPrice": -1,
            "lowPrice": 0
        }
    },
    "nearbyHotHotel": {
        "hotelId": 119242392,
        "hotelCityId": 36124,
        "nearbySubType": "TripHotelDetail"
    },
    "abResultEntities": [],
    "head": {
        "platform": "PC",
        "cver": "0",
        "cid": "1766568010190.f4beh8Zaz81S",
        "bu": "IBU",
        "group": "trip",
        "aid": "",
        "sid": "",
        "ouid": "",
        "locale": "zh-HK",
        "region": "HK",
        "timezone": "8",
        "currency": "HKD",
        # "pageId": "10320668147",
        "pageId": "11111111111",
        # "vid": "1766568010190.f4beh8Zaz81S",
        "guid": "",
        "isSSR": False,
        "extension": [
            {
                "name": "cityId",
                "value": ""
            },
            {
                "name": "checkIn",
                "value": "2026-01-19"
            },
            {
                "name": "checkOut",
                "value": "2026-01-20"
            }
        ]
    }
}

proxies = {
    "http": "http://127.0.0.1:7890",
    "https": "http://127.0.0.1:7890"
}
data = json.dumps(data, separators=(',', ':'))
response = requests.post(url, headers=headers, data=data)

print(response.text)
print(response)