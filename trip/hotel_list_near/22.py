data = {
  "date": {
    "dateType": 1,
    "dateInfo": {
      "checkInDate": "20260323",
      "checkOutDate": "20260324"
    }
  },
  "destination": {
    "type": 1,
    "geo": {
      "cityId": cityId,
      "countryId": countryId
    },
    "keyword": {
      "word": name
    }
  },
  "extraFilter": {
    "childInfoItems": [],
    "ctripMainLandBDCoordinate": True,
    "sessionId": "",
    "extendableParams": {
      "tripWalkDriveSwitch": "T",
      "isUgcSentenceB": "",
      "multiLangHotelNameVersion": "E"
    }
  },
  "filters": [
    {
      "type": "17",
      "title": "直線距離（由近到遠）",
      "value": "5",
      "filterId": "17|5"
    },
    {
      "type": "31",
      "title": "",
      "value": str(hotelId),
      "filterId": "31|"+str(hotelId)
    },
    {
      "type": "80",
      "title": "每房每晚價格（未連稅及附加費）",
      "value": "0",
      "filterId": "80|0|1"
    },
    {
      "filterId": "29|1",
      "type": "29",
      "value": "1|2"
    }
  ],
  "roomQuantity": 1,
  "marketInfo": {
    "received": False,
    "isRechargeSuccessful": False,
    "guideBannerInfo": {
      "title": "歡迎！預訂住宿即享{0}10%{/0}優惠！",
      "subItems": [
        "獲取優惠代碼，節省高達 10%",
        "下載 App，獲取另一個優惠代碼，節省5%（最多 HK$50）"
      ],
      "bannerSubItems": [
        {
          "text": "獲取優惠代碼，節省高達 10%",
          "iconType": "yes"
        },
        {
          "text": "下載 App，獲取另一個優惠代碼，節省5%（最多 HK$50）",
          "iconType": "yes"
        },
        {
          "text": "使用您的優惠代碼",
          "iconType": "plus"
        }
      ]
    },
    "unclaimedActivityInfos": [
      {
        "strategyId": 0,
        "activityId": 349,
        "property": 5,
        "couponShowType": ""
      }
    ],
    "authInfo": {
      "isLogin": False,
      "isMember": False
    },
    "extraInfo": {
      "SpecialActivityId": "T"
    }
  },
  "paging": {
    "pageIndex": 1,
    "pageSize": 20,
    "pageCode": str(pageid)
  },
  "hotelIdFilter": {
    "hotelAldyShown": [
      "688174"
    ]
  },
  "recommend": {
    "searchType": "",
    "nearbyHotHotel": {
      "hotelId": str(hotelId),
      "hotelCityId": cityId,
      "hotelStar": 3,
      "hotelName": name,
      "nearbySubType": "TripHotelList",
      "coordinate": [
        {
          "latitude": latitude,
          "longitude": longitude,
          "coordinateType": 1
        },
        {
          "latitude": latitude,
          "longitude": longitude,
          "coordinateType": 2
        }
      ]
    }
  },
  "head": {
    "platform": "PC",
    "cver": "0",
    "cid": cid,
    "bu": "IBU",
    "group": "trip",
    "aid": "",
    "sid": "",
    "ouid": "",
    "locale": "zh-HK",
    "timezone": "8",
    "currency": "HKD",
    "pageId": pageid,
    "vid": cid,
    "guid": "",
    "isSSR": False,
    "extension": [
      {
        "name": "cityId",
        "value": ""
      },
      {
        "name": "checkIn",
        "value": "2026-03-23"
      },
      {
        "name": "checkOut",
        "value": "2026-03-24"
      },
      {
        "name": "region",
        "value": "HK"
      }
    ]
  }
}