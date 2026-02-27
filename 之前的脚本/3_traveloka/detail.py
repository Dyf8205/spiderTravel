import requests


headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "zh-CN,zh;q=0.9",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "priority": "u=0, i",
    "sec-ch-ua": "\"Google Chrome\";v=\"135\", \"Not-A.Brand\";v=\"8\", \"Chromium\";v=\"135\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
}
cookies = {
    # "clientSessionId": "T1-mweb.01KCRVCTVC6TGSS8C5G4Q5R2XD",
    # "tv_cs": "1",
    # "tv-repeat-visit": "true",
    # "countryCode": "HK",
    # "tv_user": "{\"authorizationLevel\":100,\"id\":null}",
    # "g_state": "{\"i_l\":0,\"i_ll\":1766065607564,\"i_b\":\"TsagOGGGdZ2zUTIxvo+h27DEuigBQ8WmZ6/T1H6wTGI\",\"i_e\":{\"enable_itp_optimization\":8}}",
    # "amp_f4354c": "-QqqB24nH3R9_1J9MIxqFK...1jcord57l.1jcord57l.0.0.0",
    # "_gcl_au": "1.1.226873146.1766065608",
    # "tv_lt": "1766065609730",
    # "_ga_RSRSMMBH0X": "GS2.1.s1766065610$o1$g0$t1766065610$j60$l0$h432708830",
    # "datadome": "uLP4u_Sn2LgHXqR2ap5NlvbmcxJNN~eJPpVrKGKf1LrWxrnJnpunG~aTKx~cdqn7ekwaLPXhUgIxmtcHv9nnCDyQY4bw8vkYB6gh8pZJTtM2j926qplQjfGIQP~wth4M",
    # "_ga": "GA1.2.1023487150.1766065610",
    # "_gid": "GA1.2.50355628.1766065610",
    # "__lt__cid": "7fcc1b96-9d72-42b3-b685-5c7914ff4045",
    # "__lt__sid": "ea2d7f54-17579922",
    # "_fwb": "226DnMObBTA4P4hOh0XvEM5.1766065610904",
    # "wcs_bt": "s_2cb982ada97c:1766065610",
    # "_ly_su": "1766065610.4a5462cc-f8d1-4351-b57f-81a6df85ab65",
    # "_yjsu_yjad": "1766065610.0c839bd5-4bb0-4b82-a5b5-684787e26ed4",
    # "_fbp": "fb.1.1766065610978.845280797480932066",
    # "cto_bundle": "V4eMal9BNEJxVmViMTBFaWxtN0pmN1dZdUNZNHQzaTZrVnpnJTJCZGxCYiUyRkJHJTJCQVZEbG1lb0hNaGc5NVpidFR2eldOcGpqQ2wzM0dRbElQRGdDT3c5SFNuT0dTaW9FM0NSWkV1clclMkIyMXl5cHolMkZjYk8lMkZwWUdxc1h3bXlpMFUwZnJZOVFFeg",
    # "_tt_enable_cookie": "1",
    # "_ttp": "01KCRVD9GPVQK2PETJYWBHT6SB_.tt.1",
    # "_im_vid": "01KCRVDBN3722ENVRC4WGYZHMJ",
    # "ttcsid_CFNI0BRC77UEUGLEG00G": "1766065612321::5UTBw7uCHDhOso2aT-Uy.1.1766065622605.1",
    # "__smn_fid": "DS7-Gl_76GY9XMhgUHYLzAjN7wQQv4_bjbMzQJal6omG28EU",
    "aws-waf-token": "13757b6d-c81c-49e7-a5f5-b98e1e7448b2:AAoAaERgdl4GAAAA:9FYMN/DhsaE4BTIinqcPG/3Uh2/h9R9sAjytdwI1caIJCW7cFhyg9J0Qh6WTOcvfViK5YWaTivHTO7YX5gFw9etRAHK4mQIYANfNXk/TcVc/w5gXXxvex3K0QFPN9uyEXXetetk+23/tMTfQ7PNPgjSSwWMXAqryyXdwjL9nBfHjKtrQ2gDcq63wWC8NCI/IIpt9XCGMhkLZuh8=",
    # "tvl": "qgdHX7GvehrD9XH5a3S4PUiOJGezXQ9yizVaSxTklwrLYY64AE4apiD1qmHRGaV8gGAQoV6xR5wi1hxtboYegx0JoHbuxL9J5IDMykh7yrn/kmgjvZe3CXlrOt5A94G1h8SGYm0D03zEW7S7g02l9zkAPbkMGQ6AJj+0Bs51j2fcC/wcXzrA2lKPP780WiI8Xz5EgYPs5OIMqRi768TBaL8lk5uk1KkfQ8XT9/QoMZsqlOXuSPv5hBz7G+5gUdtU0BQwIo4lavlQjCnh4UeyQVgvYCKUnpuZZKSXcOQbdkjM0WMA1zSky7I1/5su3gOqHTlWHDRqn/CXAqCXFSBDwbRp3O1DCVG+GIpDagMispXC2ApRmNcP0A8FksXVQlLUxbVWc9mUJC6U6r8wkx04c+4CDTx/jJt5ZXoEQTwGFtmvFcCuLSwzN6i0oSIN7Me1ytIbbsmHCGnz3sWzyttR7kqE06sQuTSTPgKq6wDGoh8=",
    # "tvs": "qgdHX7GvehrD9XH5a3S4PXWKx93/3Xi103f/kPpnhg3I3knVJoWxdYuhF/SFxrBjhERB089Yu/lBibC//8ur+wT9+yPDKAJ2/2UATOaPOrhzhR9Shq9evKfuDnzob04Id+gyQzq70AhHhvg65it3EHJ8QJVLDxjwhIbxYg4fKH9bPZBZuDO5H0NNMHQUyz3U1N+0NjAmWhSTtggf9gIHJIaLKSmYGn4epBOkel7pAXxlmH6SQDIbVMhUICxHSon0bVRRxIZSiHCI/zwJ/H/kKHK1VHMOf2lFjczfUzWfM663NsKhJDtFI1afSbeKadSyXEw2bImmv0C+7A4wSqGznc3wWdOLlzemGQX5jLyfTlyh9ECyOlH1qwRP+rV49MU6GbpHe+//A53te9f8Z0+XAD+gyitqyBUMXlUUBhL1p/5QizIevN0ItfDV9YiCBd8d9PYN0ZKIJPnbcbKDEaRR23wpMY91AYFzJ6h8za/vSrnqDlY26eY/bwMK2Y7r9t1q",
    # "ttcsid": "1766065612323::Z5UXUbipjPMD3I-2aUUX.1.1766065777544.0",
    # "ttcsid_CUM82PBC77U4QKJNCRL0": "1766065661523::1yCQ_hpY6Ay-vyiPpj75.1.1766065777544.0",
    # "amp_1a5adb": "fZU8TKJG1WI_EmuszpDyqM...1jcord56k.1jcoriau4.5.0.5",
    # "tvo": "L2FwaS92MS90dmxrL2V2ZW50cw==",
    # "_dd_s": "rum=0&expire=1766066677510&logs=1&id=18478c34-ed64-41a1-bbb5-90924e5939ff&created=1766065601820"
}
url = "https://www.traveloka.com/zh-en/hotel/indonesia/tanjung-sari-inn--1000000440952"
response = requests.get(url, headers=headers, cookies=cookies)

print(response.text)
print(response)