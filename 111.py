# -*- coding:UTF-8 -*-
# author:dyf
# time:2026/3/4 14:07
# explain:
a ={
"Name":"Jerk Chicken",
"Address":"132 S Fraser St, Georgetown, SC 29440, USA",
"Category":"Chicken Joint",
"Location":"""{"lat": "33.370355","lng": "-79.291349"}""",
"Open/Closed StatusOpen Hour":"""{"__typename": "OperationHourInfo","description": "The store's actual hours of operation","operationSchedule": [{"__typename": "OperationHours","dayOfWeek": "MONDAY","timeSlotList": []},{"__typename": "OperationHours","dayOfWeek": "TUESDAY","timeSlotList": []},{"__typename": "OperationHours","dayOfWeek": "WEDNESDAY","timeSlotList": []},{"__typename": "OperationHours","dayOfWeek": "THURSDAY","timeSlotList": ["11 AM - 6 PM"]},{"__typename": "OperationHours","dayOfWeek": "FRIDAY","timeSlotList": ["11 AM - 6 PM"]},{"__typename": "OperationHours","dayOfWeek": "SATURDAY","timeSlotList": ["11 AM - 6 PM"]},{"__typename": "OperationHours","dayOfWeek": "SUNDAY","timeSlotList": ["11 AM - 6 PM"]}]}""",
"Phone Number":"+18433252725",
"Average price per person":"$$",
"head Image & Album":"26",
"Reviews":"623",
"Rating Score":"4.4",
}

import json
print(json.dumps(a))
