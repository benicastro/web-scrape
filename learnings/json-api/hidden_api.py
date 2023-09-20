import requests
import pandas as pd
import time

url = "https://www.sunglasshut.com/wcs/resources/plp/10152/byCategoryId/3074457345626651837"
result = []

for page_num in range(1, 15):
    querystring = {
        "isProductNeeded": "true",
        "isChanelCategory": "false",
        "pageSize": "100",
        "responseFormat": "json",
        "currency": "USD",
        "cvosrc": "yext.4270",
        "viewTaskName": "CategoryDisplayView",
        "storeId": "10152",
        "DM_PersistentCookieCreated": "true",
        "pageView": "image",
        "catalogId": "20602",
        "top": "Y",
        "beginIndex": "0",
        "langId": "-1",
        "categoryId": "3074457345626651837",
        "cid": "yext.1142442",
        "orderBy": "default",
        "currentPage": f"{page_num}",
    }

    payload = ""
    headers = {
        "cookie": "aka-cc=PH; aka-ct=SALCEDOVILLAGE; aka-zp=; bm_sz=A1EA813062E0140475738348C96BD760~YAAQdwdaaKHamI+KAQAAzz/xsBVvZl0Hoa+DgTlimhBx5J++zgfAl/oEJ6d0i3MFeCFTyN/efaeplJi/xImy0gwnyM/TEOTz7UiYhQ4dtErLzlSWZsgqxJYTcqdY75yURbsf8TEDuM3F6A31jxwHOZYvMZ9uAtnsn7E/goimunRAyU/myeA8JtAubjPbYS6rCpt3+AhowXBmD9e88ao5oTIYPNGU+mLw3V72o47bKLtDubKN3fMj6G850mU6F1AnpKs2GzLldR9M0dcIdMxO5w+ziz/txpXn7SU1r5OYHnw7xu3Pc3nS1w==~3425346~3556148; mt.v=2.1591009368.1695185715181; dtCookie=v_4_srv_-2D40_sn_8NGE7HOLK696DAEEGCDF441FCC6JVPE7; rxVisitor=1695185715246B6LR8E60V98CI7KLDK6J635AV6IIAOMG; _ALGOLIA=anonymous-27f9d98f-fcff-4449-ae97-a2d12232d9a3; sgh-desktop-facet-state-search=; ftr_ncd=6; JSESSIONID=0000MAywAvqYS-bEWlKh4beFRkL:1c7qtpec2; __wid=853260388; ftr_blst_1h=1695185716620; ak_bmsc=42135AC0EC540A82DB8241E679052DE4~000000000000000000000000000000~YAAQdwdaaAfbmI+KAQAAhknxsBUYrnVeSNguxASDcO8h751oS0hbOrGFnr6tsrWT/R2TBnlp6tMh7am7i12LFthHTuIHslcVQMeVnROn3m/mIIR8g2hN8WIL9iLxI2pCSDf/BJLfME/+V/wQJ9Frd5SgCyrYJ8DJtBxt3u8VwY4t7k1lJCXw+J46zjKzMBjRXBLh8sPBYPSXCE/3EOJmSXdYwkEdHRi66s5pMqCWZAQ0SCdXdyYB7sEFbavCQzrYsxVpL2lUTqycUqBq7GzWAgHGalJ3CgbE45JIpjxD2NFSQHlJooKp879BMtKARtr4TSbJYN87rKpTRzo/wcTCdfb2BVt918h6n3cLYTZTl4ucowoeNWrhFl/eojlvqmNlNsXrJJ3zRVdFparsQXnztjzG3YIGfsSQ4C1EAGOgymevg28PIhO33XuvLwVPj6h3w7rZmEv55y7c1MlOTiXw3kSTflr1S1D6ldCJtM+wA/mvwvxJAIJCyxbEzxXaYg==; tealium_data2track_Tags_AdobeAnalytics_TrafficSourceMid_ThisHit=direct; tealium_data_tags_adobeAnalytics_trafficSourceMid_thisSession=direct; tealium_data_session_timeStamp=1695185717524; userToken=undefined; TrafficSource_Override=1; tiktok_click_id=undefined; AMCVS_125138B3527845350A490D4C^%^40AdobeOrg=1; s_ecid=MCMID^%^7C46734388428539416654465857272385236108; AMCV_125138B3527845350A490D4C^%^40AdobeOrg=-1303530583^%^7CMCIDTS^%^7C19621^%^7CMCMID^%^7C46734388428539416654465857272385236108^%^7CMCAAMLH-1695790518^%^7C3^%^7CMCAAMB-1695790518^%^7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y^%^7CMCOPTOUT-1695192918s^%^7CNONE^%^7CMCAID^%^7CNONE^%^7CvVersion^%^7C3.3.0; _abck=487E047E177414DB0DC92F2BA453886A~0~YAAQdwdaaDzbmI+KAQAAilDxsAo1h8cktP/RK1Iyz1hySXoEGHQTm2TX82RQ0gJ8t29Iu63U7vgscQ51Pc+GU1Z7HYpy5q/n4yVHsVLrCpVaxmkkzv5jlSOjUI0yXykVcBLfFNT0pTnB+ONl3hZydhSeYBiivyi1QMp75oHfMKU/Vs4A9h+i03D+RvXKnQdnHqRJKmebGrqYnNwHgiWDU4eqH4jaF7Cb3BalkyfRl4bBzu+HvcTXE1Dd2RYYJxh6zUtEY5+uiT+fyTbuNnVVAPmM2XvbKWKtcqHal5elHz/bnYJ50T9dDY8Bn74Tyz8mOM90Zwaz6y9PWVh3NRt+O0+RRSreBsgvBbqCi/CZRDbHl+ouZaxODM7u4ghpMIusDg9MyUaBe09ifF9qaKmMUW4tKEvTcjcrpyY3koI=~-1~^|^|-1^|^|~-1; s_fid=041230894DA4B735-3CF90E115FF415CD; UserTrackingProducts=0; CONSENTMGR=consent:true^%^7Cts:1695185724345; _cs_mk_aa=0.22191805177975588_1695185726590; _cs_c=1; _gcl_au=1.1.63269743.1695185731; _ga=GA1.1.1220315301.1695185731; _pin_unauth=dWlkPU16UXdaVGs0T0dZdFlUQm1PUzAwWkRKbUxXRm1ORFF0WW1Wa056azJaV0V6TjJVMw; _scid=18bfa885-9250-4fdc-992a-2ab1449e08a9; __pdst=bd3810cedfe8484d9785b9809877b27f; __rtbh.lid=^%^7B^%^22eventType^%^22^%^3A^%^22lid^%^22^%^2C^%^22id^%^22^%^3A^%^22duysYDOeUI5qZBnIPdVF^%^22^%^7D; _fbp=fb.1.1695185736781.1318257380; _tt_enable_cookie=1; _ttp=a3mgpLf7a3dYNMDqlMuxLThP6f6; tfpsi=5d54c688-25d2-4b96-b06a-bb4af04c9fb3; smc_uid=1695185744174797; smc_tag=eyJpZCI6Njc4LCJuYW1lIjoic3VuZ2xhc3NodXQuY29tIn0=; smc_session_id=dmKvEAbVm9sRN9OBsr6844orpzOAcoaw; _sctr=1^%^7C1695139200000; smc_refresh=24860; smc_sesn=1; smc_not=default; s_cc=true; TS011f624f=015966d2925ab7c2756734f5d1131ccbea100db9cd9c6f1aefa92a29dc1a8d6813dec9c399b5326c1de40b2b62c2b05c06bd84979e45a089b0994b17c083be577559b2f2cc; SGPF=32N0GL5ePVU98TCRH-6MWxzGvKNbBKJMhufmTjEJDlPFeNnm-uunTYQ; tealium_data2track_Tags_AdobeAnalytics_TrafficSourceJid_ThisHit=309202REF; tealium_data_tags_adobeAnalytics_trafficSourceJid_stackingInSession=309201DIR-309202REF; outbrain_cid_fetch=true; dtSa=-; sgh-desktop-facet-state-plp=categoryid:undefined^|gender:true^|brands:partial^|polarized:true^|price:true^|frame-shape:partial^|color:true^|face-shape:false^|fit:false^|materials:false^|lens-treatment:false; bm_sv=9A51FC3DD350A4A2F6E7AEA671C1B49F~YAAQdwdaaAocmY+KAQAAqnv6sBWpi3H8cRzdqNr+3nZMRCgJuuQJue3GMIxo0/lND+90udheeGtB3JKTLAWrCfkrCKNNGH/eaLAn8VTMlX0MlRGDHM6QNoF6Z/G1eX1se76o6xb+ZAKW2s2qq+9awVyq7/nXHVMqnH0aDypq7lXlGruFPBgwo9YaLiFxZvNla4Lr4rty/ZaFUOafGQO4h5aUW6ugDe784d2o1vUhiPTriD6ZKnnE8UjaxmqoxNTsmpXcHtg5~1; s_sq=^%^5B^%^5BB^%^5D^%^5D; _cs_id=f5a7942c-d544-a9a9-bd8f-e7dccc0a5a5a.1695185726.1.1695186321.1695185726.1.1729349726808; _cs_s=3.0.0.1695188121473; forterToken=28b6ad584b8a43feb6b222462aa1ab98_1695186318741__UDF43-m4_6; _scid_r=18bfa885-9250-4fdc-992a-2ab1449e08a9; _uetsid=efe74240577111eeacdde1ead1cfe63e; _uetvid=efe7b7f0577111eeab01dd6343787ce3; _derived_epik=dj0yJnU9WFp5Y0RXOHY0MlY0bzk0bXVyakVSQ0EtS3BCa3kydF8mbj05NVRfakVSY1dMN2JLTmNYQllub2NnJm09MSZ0PUFBQUFBR1VLZlpNJnJtPTEmcnQ9QUFBQUFHVUtmWk0mc3A9Mg; cto_bundle=CFC0rl91U0tDRVhBNXZtSU5qaWJ0bUJUeUtDNiUyRjlocWRITGNqOGp5aExLOTNxSGVNYndjOGs1MEJNQmZXVHR5czQwJTJGRCUyQlNiMjI3UllzMGFMYnc4bjZraU44cERDOFJzYmVzVyUyRnU5R1hDRkNyNkdVdUxXcFNNRllDOUVlank3aGphY3ZJZDlpWDhzbWNOcktHcVZuSTl1V294UWFUWkxTYWolMkZJMTdFWnhRSk50b2xwbDNMMzljZWlXSkFrc3g5JTJCbXh5QnlEeHhZMExpWGhHR2lPZkVrT2RJdDZBJTNEJTNE; rxvt=1695188130235^|1695185715248; dtPC=-40^-vBHDLWFQFVPRDGHHMGMLQPAEHCBPMDEVK-0e0; _ga_6P80B86QTY=GS1.1.1695185731.1.1.1695186330.25.0.0; smc_tpv=5; smc_spv=5; smct_session=^{^\^s^^:1695185746695,^\^l^^:1695186340881,^\^lt^^:1695186340881,^\^t^^:526,^\^p^^:67^}; utag_main=v_id:018ab0f148fe007835a9ae7ef6580506f003c06700a9d^n:1^e:18^s:0^t:1695188141538^:1695185717503^%^3Bexp-session^n:3^%^3Bexp-session^:sunglasshut.com^:1^:3^%^3Bexp-session^:ap-east-1^%^3Bexp-session; tealium_data_action_lastAction=Men:Sun:Plp-Editorial click ^[sgh-load-more  button^]^[Loadmoresunglasses^]; tealium_data_action_lastEvent=click ^[sgh-load-more  button^]^[Loadmoresunglasses^]",
        "authority": "www.sunglasshut.com",
        "accept": "application/json, text/plain, */*",
        "accept-language": "en-US,en;q=0.9",
        "referer": "https://www.sunglasshut.com/us/mens-sunglasses",
        "sec-ch-ua": "^\^Chromium^^;v=^\^116^^, ^\^Not",
    }

    response = requests.request(
        "GET", url, data=payload, headers=headers, params=querystring
    )

    data = response.json()

    for p in data["plpView"]["prodcuts"]["products"]["product"]:
        result.append(p)

df = pd.json_normalize(result)

df.to_csv("first_results.csv")
