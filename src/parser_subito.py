import asyncio
import aiohttp

from bs4 import BeautifulSoup


class SubitoParser:
    __COOKIES = {
        'kppid': 'B80A0CC706E56FD7C9B41C99',
        'didomi_token': 'eyJ1c2VyX2lkIjoiMThkZmYzOWQtOTBmMi02MDdjLTk2ZGEtZTFiN2VlNDExZjkwIiwiY3JlYXRlZCI6IjIwMjQtMDMtMDJUMTI6NTM6MTcuNzM0WiIsInVwZGF0ZWQiOiIyMDI0LTAzLTAyVDEyOjUzOjIxLjE0NFoiLCJ2ZW5kb3JzIjp7ImVuYWJsZWQiOlsiZ29vZ2xlIiwiYzphbXBsaXR1ZGUiLCJjOm1pY3Jvc29mdC1vbmVkcml2ZS1saXZlLXNkayIsImM6YXBwc2ZseWVyLTlqY3duaVk5IiwiYzpiaW5nLWFkcyIsImM6ZGlkb21pIiwiYzprcnV4LWRpZ2l0YWwiLCJjOnF1YW50Y2FzdC1tZWFzdXJlbWVudCIsImM6b21uaXR1cmUtYWRvYmUtYW5hbHl0aWNzIiwiYzpncmFwZXNob3QiLCJjOnF1YW50dW0tYWR2ZXJ0aXNpbmciLCJjOngxIiwiYzp0dWJlbW9ndWwiLCJjOnNlZ21lbnQiLCJjOmFkbW9iIiwiYzptZWRhbGxpYS1paHpyeUZMWSIsImM6c2FsZXNmb3JjZS1DUEJGRWZIUCIsImM6b3B0aW1pemVseS1FTlFFaWlaVCIsImM6YWthY2Rvcm9kLVdBRDdpWHRoIiwiYzptaWNyb3NvZnQtYW5hbHl0aWNzIiwiYzphdGludGVybmUtY1dRS0hlSloiLCJjOnBhbmdsZWRzcC1aQnhMaGdDVyIsImM6Ymx1ZWthaSIsImM6Z29vZ2xlYW5hLTRUWG5KaWdSIiwiYzpzb2Npb21hbnRpLW1NVEc4eGc0IiwiYzphd3MtY2xvdWRmcm9udCIsImM6c3VibGltZXNrLXBaN0FueTdHIiwiYzptZWV0cmljc2ctTmRFTjhXeFQiLCJjOmNlbnRyby1pVVdWbU40TiIsImM6bWljcm9zb2Z0IiwiYzpwaW50ZXJlc3QiXX0sInB1cnBvc2VzIjp7ImVuYWJsZWQiOlsiY29va2llYW5hLWtDQ1JHejRtIiwiY29va2llZGktbk5lMjNRamQiLCJjb29raWV0ZWMtOXFmQUVWd2siLCJhdWRpZW5jZW0teGVkZVUyZ1EiLCJnZW9sb2NhdGlvbl9kYXRhIl19LCJ2ZW5kb3JzX2xpIjp7ImVuYWJsZWQiOlsiZ29vZ2xlIiwiYzpwYW5nbGVkc3AtWkJ4TGhnQ1ciLCJjOnNvY2lvbWFudGktbU1URzh4ZzQiLCJjOmNlbnRyby1pVVdWbU40TiJdfSwidmVyc2lvbiI6MiwiYWMiOiJEQmVBV0FGa0JKWUVvZ0pZZ1VWQkxHQ2VjRkNJTFJ3WG9nd1guREJlQVdBRmtCSllFb2dKWWdVVkJMR0NlY0ZDSUxSd1hvZ3dYIn0=',
        '_pulse2data': '6839195a-da88-4b5a-851b-c7809e640b70^%^2Cv^%^2C^%^2C1709384898353^%^2CeyJpc3N1ZWRBdCI6IjIwMjQtMDMtMDJUMTI6NTM6MzJaIiwiZW5jIjoiQTEyOENCQy1IUzI1NiIsImFsZyI6ImRpciIsImtpZCI6IjIifQ..nUuXZY5DOchC7odwsJQYBQ.cCKIe1pZE3WyZwk8oT1vcVl-79JlWGdc8thNXP5xkb_yeIrx4PQvcvfFp-z2uNDKKIaqLi8vodoihthjo6zJtrGJrV2wERdX1cRAhJcPFCWppx-bK6EUrDqq8MAzMHZBJVhLFslfLe2dVKVHbpYykj8fhhj3x5o8x__jDG2UDArtHvBesTpMFAq_G6btkAPPXuP0Mo9058uxSWQvXvRvBA.lXL0L-t_A-qpWLXS0Mjnuw^%^2C^%^2C^%^2Ctrue^%^2C^%^2CeyJraWQiOiIyIiwiYWxnIjoiSFMyNTYifQ..OibO4XCKu9A3PdFM4U4jHtohyjA9K8Ua8D_Lpv8BIFc',
        '_ga_D72SGH4DYJ': 'GS1.1.1709384000.1.1.1709384676.0.0.0',
        '_ga': 'GA1.1.2098639722.1709384000',
        'euconsent-v2': 'CP62DgAP62DgAAHABBENApEoAP_gAELgABCYI3wPAABQAKAAwACAAFYALgAwABwADwAIAAWwAxADIAGkARABFACZAFsAXIAwgDEAGYAOQAeAA9QCAAIEAQgAjABHAChAFIAMEAZQA0gBxADrAHiAP0AhABEACJgEcAJaAWkAuoBfYDAAMCAZ0A4QB7QELAI1ATEAsMBZgC8wGMgMnAZYA5gBzQD9wICgQHAjMBG8Eb4EEACgALAAqABcADgAHgAQQAxADIAGgARAAmQBbAFwAMQAZgA9AB-AEIAI4AZQA_QCEAEWAI4AXUAvoB7QExALzAYIAycBlgD9wI3gBEIAMAARBqEAAYAAiDUA.f_wACFwAAAAA',
        '_gcl_au': '1.1.1044411882.1709384001',
        'displayCookieConsent': 'y',
        'FPID': 'FPID2.2.dTIIck0JwPkGq5O6GAgK^%^2BChtR94h8enFhlAyON15QUk^%^3D.1709384000',
        'FPLC': 'iucMJHF7jHdWld9A7RKctLX^%^2BYiKNtNjSBnPdrJah4Kes86MzU9NZv9AAfbbYsfzehTewLwWZNlb9dzRNy7W6v1FJqjKh51YK8fGSHuHBMQC8dS1m7kDziOs1lV4mNA^%^3D^%^3D',
        'FPAU': '1.1.1044411882.1709384001',
        '__gads': 'ID=ae009f9d49545acb:T=1709384015:RT=1709384681:S=ALNI_MakTdnFL75jnfWsILhQ1kwWp_qWmg',
        '__gpi': 'UID=00000d3aa456b6b1:T=1709384015:RT=1709384681:S=ALNI_MZlEjrqSnLyP_uYNmgPMxijq4niAw',
        '__eoi': 'ID=22fa2e304b2c3c59:T=1709384015:RT=1709384681:S=AA-AfjbOlFclylniq6rkbXt1wiT4',
        '_pin_unauth': 'dWlkPU1HTXlZbVU0TXpRdFl6aG1NQzAwTmpGbUxXSTVaRFV0WWprMk9UZzBOakE1WXpSbA',
        '__rtbh.lid': '^%^7B^%^22eventType^%^22^%^3A^%^22lid^%^22^%^2C^%^22id^%^22^%^3A^%^22npKRsxnENopILmrcuicE^%^22^%^7D',
        '_fbp': 'fb.1.1709384003316.1110197362',
        'crto_is_user_optout': 'false',
        'akacd_orodha': '2177452799~rv=11~id=f42363da4b3432fd7e23ff31965371b9',
        '_pbjs_userid_consent_data': '2273866697984331',
        '_pubcid': 'e4e8c4f3-1b3c-467a-bc8e-e002790ec00c',
        '__gsas': 'ID=52ee4447818f55ad:T=1709384345:RT=1709384345:S=ALNI_MZlZjuUfoApJSrE_BuqiTQnzZldsw',
        'mdLogger': 'false',
        'kampyle_userid': '854d-8674-c27b-c8bc-6092-2e2a-18e9-71c5',
        'kampyleUserSession': '1709384335768',
        'kampyleSessionPageCounter': '1',
        'kampyleUserSessionsCount': '1',
        'kampyleUserPercentile': '49.880684222250906',
    }
    __HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Connection': 'keep-alive',
        # 'Cookie': 'kppid=B80A0CC706E56FD7C9B41C99; didomi_token=eyJ1c2VyX2lkIjoiMThkZmYzOWQtOTBmMi02MDdjLTk2ZGEtZTFiN2VlNDExZjkwIiwiY3JlYXRlZCI6IjIwMjQtMDMtMDJUMTI6NTM6MTcuNzM0WiIsInVwZGF0ZWQiOiIyMDI0LTAzLTAyVDEyOjUzOjIxLjE0NFoiLCJ2ZW5kb3JzIjp7ImVuYWJsZWQiOlsiZ29vZ2xlIiwiYzphbXBsaXR1ZGUiLCJjOm1pY3Jvc29mdC1vbmVkcml2ZS1saXZlLXNkayIsImM6YXBwc2ZseWVyLTlqY3duaVk5IiwiYzpiaW5nLWFkcyIsImM6ZGlkb21pIiwiYzprcnV4LWRpZ2l0YWwiLCJjOnF1YW50Y2FzdC1tZWFzdXJlbWVudCIsImM6b21uaXR1cmUtYWRvYmUtYW5hbHl0aWNzIiwiYzpncmFwZXNob3QiLCJjOnF1YW50dW0tYWR2ZXJ0aXNpbmciLCJjOngxIiwiYzp0dWJlbW9ndWwiLCJjOnNlZ21lbnQiLCJjOmFkbW9iIiwiYzptZWRhbGxpYS1paHpyeUZMWSIsImM6c2FsZXNmb3JjZS1DUEJGRWZIUCIsImM6b3B0aW1pemVseS1FTlFFaWlaVCIsImM6YWthY2Rvcm9kLVdBRDdpWHRoIiwiYzptaWNyb3NvZnQtYW5hbHl0aWNzIiwiYzphdGludGVybmUtY1dRS0hlSloiLCJjOnBhbmdsZWRzcC1aQnhMaGdDVyIsImM6Ymx1ZWthaSIsImM6Z29vZ2xlYW5hLTRUWG5KaWdSIiwiYzpzb2Npb21hbnRpLW1NVEc4eGc0IiwiYzphd3MtY2xvdWRmcm9udCIsImM6c3VibGltZXNrLXBaN0FueTdHIiwiYzptZWV0cmljc2ctTmRFTjhXeFQiLCJjOmNlbnRyby1pVVdWbU40TiIsImM6bWljcm9zb2Z0IiwiYzpwaW50ZXJlc3QiXX0sInB1cnBvc2VzIjp7ImVuYWJsZWQiOlsiY29va2llYW5hLWtDQ1JHejRtIiwiY29va2llZGktbk5lMjNRamQiLCJjb29raWV0ZWMtOXFmQUVWd2siLCJhdWRpZW5jZW0teGVkZVUyZ1EiLCJnZW9sb2NhdGlvbl9kYXRhIl19LCJ2ZW5kb3JzX2xpIjp7ImVuYWJsZWQiOlsiZ29vZ2xlIiwiYzpwYW5nbGVkc3AtWkJ4TGhnQ1ciLCJjOnNvY2lvbWFudGktbU1URzh4ZzQiLCJjOmNlbnRyby1pVVdWbU40TiJdfSwidmVyc2lvbiI6MiwiYWMiOiJEQmVBV0FGa0JKWUVvZ0pZZ1VWQkxHQ2VjRkNJTFJ3WG9nd1guREJlQVdBRmtCSllFb2dKWWdVVkJMR0NlY0ZDSUxSd1hvZ3dYIn0=; _pulse2data=6839195a-da88-4b5a-851b-c7809e640b70^%^2Cv^%^2C^%^2C1709384898353^%^2CeyJpc3N1ZWRBdCI6IjIwMjQtMDMtMDJUMTI6NTM6MzJaIiwiZW5jIjoiQTEyOENCQy1IUzI1NiIsImFsZyI6ImRpciIsImtpZCI6IjIifQ..nUuXZY5DOchC7odwsJQYBQ.cCKIe1pZE3WyZwk8oT1vcVl-79JlWGdc8thNXP5xkb_yeIrx4PQvcvfFp-z2uNDKKIaqLi8vodoihthjo6zJtrGJrV2wERdX1cRAhJcPFCWppx-bK6EUrDqq8MAzMHZBJVhLFslfLe2dVKVHbpYykj8fhhj3x5o8x__jDG2UDArtHvBesTpMFAq_G6btkAPPXuP0Mo9058uxSWQvXvRvBA.lXL0L-t_A-qpWLXS0Mjnuw^%^2C^%^2C^%^2Ctrue^%^2C^%^2CeyJraWQiOiIyIiwiYWxnIjoiSFMyNTYifQ..OibO4XCKu9A3PdFM4U4jHtohyjA9K8Ua8D_Lpv8BIFc; _ga_D72SGH4DYJ=GS1.1.1709384000.1.1.1709384676.0.0.0; _ga=GA1.1.2098639722.1709384000; euconsent-v2=CP62DgAP62DgAAHABBENApEoAP_gAELgABCYI3wPAABQAKAAwACAAFYALgAwABwADwAIAAWwAxADIAGkARABFACZAFsAXIAwgDEAGYAOQAeAA9QCAAIEAQgAjABHAChAFIAMEAZQA0gBxADrAHiAP0AhABEACJgEcAJaAWkAuoBfYDAAMCAZ0A4QB7QELAI1ATEAsMBZgC8wGMgMnAZYA5gBzQD9wICgQHAjMBG8Eb4EEACgALAAqABcADgAHgAQQAxADIAGgARAAmQBbAFwAMQAZgA9AB-AEIAI4AZQA_QCEAEWAI4AXUAvoB7QExALzAYIAycBlgD9wI3gBEIAMAARBqEAAYAAiDUA.f_wACFwAAAAA; _gcl_au=1.1.1044411882.1709384001; displayCookieConsent=y; FPID=FPID2.2.dTIIck0JwPkGq5O6GAgK^%^2BChtR94h8enFhlAyON15QUk^%^3D.1709384000; FPLC=iucMJHF7jHdWld9A7RKctLX^%^2BYiKNtNjSBnPdrJah4Kes86MzU9NZv9AAfbbYsfzehTewLwWZNlb9dzRNy7W6v1FJqjKh51YK8fGSHuHBMQC8dS1m7kDziOs1lV4mNA^%^3D^%^3D; FPAU=1.1.1044411882.1709384001; __gads=ID=ae009f9d49545acb:T=1709384015:RT=1709384681:S=ALNI_MakTdnFL75jnfWsILhQ1kwWp_qWmg; __gpi=UID=00000d3aa456b6b1:T=1709384015:RT=1709384681:S=ALNI_MZlEjrqSnLyP_uYNmgPMxijq4niAw; __eoi=ID=22fa2e304b2c3c59:T=1709384015:RT=1709384681:S=AA-AfjbOlFclylniq6rkbXt1wiT4; _pin_unauth=dWlkPU1HTXlZbVU0TXpRdFl6aG1NQzAwTmpGbUxXSTVaRFV0WWprMk9UZzBOakE1WXpSbA; __rtbh.lid=^%^7B^%^22eventType^%^22^%^3A^%^22lid^%^22^%^2C^%^22id^%^22^%^3A^%^22npKRsxnENopILmrcuicE^%^22^%^7D; _fbp=fb.1.1709384003316.1110197362; crto_is_user_optout=false; akacd_orodha=2177452799~rv=11~id=f42363da4b3432fd7e23ff31965371b9; _pbjs_userid_consent_data=2273866697984331; _pubcid=e4e8c4f3-1b3c-467a-bc8e-e002790ec00c; __gsas=ID=52ee4447818f55ad:T=1709384345:RT=1709384345:S=ALNI_MZlZjuUfoApJSrE_BuqiTQnzZldsw; mdLogger=false; kampyle_userid=854d-8674-c27b-c8bc-6092-2e2a-18e9-71c5; kampyleUserSession=1709384335768; kampyleSessionPageCounter=1; kampyleUserSessionsCount=1; kampyleUserPercentile=49.880684222250906',
        'If-None-Match': 'W/bo0xifs8b0723u',
        # Requests doesn't support trailers
        # 'TE': 'trailers',
    }
    __PARAMS = {
        'shp': 'true',
    }
    __PROXY = 'http://user164993:21perz@181.215.227.162:2363'

    def __init__(self, bot):
        self.__DOMEN = 'https://www.subito.it'  # Домен сайта
        self.__AD_URL = 'https://www.subito.it/annunci-italia/vendita/casa-e-persona/?shp=true&o='
        self.__bot = bot
        self.__run = False

    async def start(self, user_id):
        self.__run = True
        page_num = 1
        while self.__run:
            try:
                await self.__get_products_links(user_id, page_num)
            except aiohttp.client_exceptions.ClientProxyConnectionError:
                pass
            page_num += 1

    def stop(self):
        self.__run = False

    def is_running(self):
        return self.__run

    async def __get_products_links(self, user_id, page_num):
        url = f'{self.__AD_URL}{page_num}'
        print(page_num)
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    url=url,
                    params=self.__PARAMS,
                    cookies=self.__COOKIES,
                    headers=self.__HEADERS,
                    proxy=self.__PROXY
            ) as response:
                html = await response.text()

        soup = BeautifulSoup(html, 'lxml')
        ads = soup.find_all("div", class_="items__item item-card item-card--small")

        tasks = [self.__get_user_url(url) for url in ads]
        results = await asyncio.gather(*tasks)
        for result in results:
            if result[0]:
                ad_url = f'<a href="{result[1]}">Ссылка на объявление</a>'
                user_url = f'<a href="{self.__DOMEN + result[2]}">Ссылка на продавца</a>'
                time_ = result[3]
                text = f'{ad_url}\n{user_url}\n{time_}'

                await self.__bot.send_message(user_id, text, parse_mode="HTML")

    async def __get_user_url(self, ad) -> tuple:
        ad_url = ad.find_next()['href']

        async with aiohttp.ClientSession() as session:
            async with session.get(
                url=ad_url,
                params=self.__PARAMS,
                cookies=self.__COOKIES,
                headers=self.__HEADERS,
                proxy=self.__PROXY
            ) as response:
                html = await response.text()
                soup = BeautifulSoup(html, 'lxml')
                page_not_found = soup.find('div', class_='__410_title-text__JMfJE')
                if page_not_found:
                    return False, '', '', ''

                time_ = soup.find('div', class_='AdInfo_ad-info__listing-info__D44kO').find_next().text.split(' ')
                user = soup.find('div', class_='PrivateUserProfileBadge-module_buttonAndContainer__ciDlV')
                if user is None:
                    return False, '', '', ''
                if time_[0] != 'Oggi':
                    return False, '', '', ''

                link = user.find('h6').find('a')['href']
                return await self.__get_user_data(link), ad_url, link, f'Сегодня в {time_[-1]}'

    async def __get_user_data(self, url) -> bool:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                url=self.__DOMEN + url,
                params=self.__PARAMS,
                cookies=self.__COOKIES,
                headers=self.__HEADERS,
                proxy=self.__PROXY
            ) as response:
                html = await response.text()
                soup = BeautifulSoup(html, 'lxml')
                user_data = soup.find('div', class_='UserData_trust_info_box___ef6s')

                ads = user_data.find_all('p', class_='index-module_sbt-text-atom__ed5J9 index-module_token-body__GXE1P index-module_size-small__XFVFl index-module_weight-book__WdOfA UserData_ads_info_text__Zm2Vo')
                if ads is None:
                    return False

                ads_count = ads[0].next.text
                ads_online_count = ads[1].next.text

                if int(ads_count) == 1 and int(ads_online_count) == 1:
                    return True
                return False


class SubitoDebug:
    __COOKIES = {
        'kppid': 'B80A0CC706E56FD7C9B41C99',
        'didomi_token': 'eyJ1c2VyX2lkIjoiMThkZmYzOWQtOTBmMi02MDdjLTk2ZGEtZTFiN2VlNDExZjkwIiwiY3JlYXRlZCI6IjIwMjQtMDMtMDJUMTI6NTM6MTcuNzM0WiIsInVwZGF0ZWQiOiIyMDI0LTAzLTAyVDEyOjUzOjIxLjE0NFoiLCJ2ZW5kb3JzIjp7ImVuYWJsZWQiOlsiZ29vZ2xlIiwiYzphbXBsaXR1ZGUiLCJjOm1pY3Jvc29mdC1vbmVkcml2ZS1saXZlLXNkayIsImM6YXBwc2ZseWVyLTlqY3duaVk5IiwiYzpiaW5nLWFkcyIsImM6ZGlkb21pIiwiYzprcnV4LWRpZ2l0YWwiLCJjOnF1YW50Y2FzdC1tZWFzdXJlbWVudCIsImM6b21uaXR1cmUtYWRvYmUtYW5hbHl0aWNzIiwiYzpncmFwZXNob3QiLCJjOnF1YW50dW0tYWR2ZXJ0aXNpbmciLCJjOngxIiwiYzp0dWJlbW9ndWwiLCJjOnNlZ21lbnQiLCJjOmFkbW9iIiwiYzptZWRhbGxpYS1paHpyeUZMWSIsImM6c2FsZXNmb3JjZS1DUEJGRWZIUCIsImM6b3B0aW1pemVseS1FTlFFaWlaVCIsImM6YWthY2Rvcm9kLVdBRDdpWHRoIiwiYzptaWNyb3NvZnQtYW5hbHl0aWNzIiwiYzphdGludGVybmUtY1dRS0hlSloiLCJjOnBhbmdsZWRzcC1aQnhMaGdDVyIsImM6Ymx1ZWthaSIsImM6Z29vZ2xlYW5hLTRUWG5KaWdSIiwiYzpzb2Npb21hbnRpLW1NVEc4eGc0IiwiYzphd3MtY2xvdWRmcm9udCIsImM6c3VibGltZXNrLXBaN0FueTdHIiwiYzptZWV0cmljc2ctTmRFTjhXeFQiLCJjOmNlbnRyby1pVVdWbU40TiIsImM6bWljcm9zb2Z0IiwiYzpwaW50ZXJlc3QiXX0sInB1cnBvc2VzIjp7ImVuYWJsZWQiOlsiY29va2llYW5hLWtDQ1JHejRtIiwiY29va2llZGktbk5lMjNRamQiLCJjb29raWV0ZWMtOXFmQUVWd2siLCJhdWRpZW5jZW0teGVkZVUyZ1EiLCJnZW9sb2NhdGlvbl9kYXRhIl19LCJ2ZW5kb3JzX2xpIjp7ImVuYWJsZWQiOlsiZ29vZ2xlIiwiYzpwYW5nbGVkc3AtWkJ4TGhnQ1ciLCJjOnNvY2lvbWFudGktbU1URzh4ZzQiLCJjOmNlbnRyby1pVVdWbU40TiJdfSwidmVyc2lvbiI6MiwiYWMiOiJEQmVBV0FGa0JKWUVvZ0pZZ1VWQkxHQ2VjRkNJTFJ3WG9nd1guREJlQVdBRmtCSllFb2dKWWdVVkJMR0NlY0ZDSUxSd1hvZ3dYIn0=',
        '_pulse2data': '6839195a-da88-4b5a-851b-c7809e640b70^%^2Cv^%^2C^%^2C1709384898353^%^2CeyJpc3N1ZWRBdCI6IjIwMjQtMDMtMDJUMTI6NTM6MzJaIiwiZW5jIjoiQTEyOENCQy1IUzI1NiIsImFsZyI6ImRpciIsImtpZCI6IjIifQ..nUuXZY5DOchC7odwsJQYBQ.cCKIe1pZE3WyZwk8oT1vcVl-79JlWGdc8thNXP5xkb_yeIrx4PQvcvfFp-z2uNDKKIaqLi8vodoihthjo6zJtrGJrV2wERdX1cRAhJcPFCWppx-bK6EUrDqq8MAzMHZBJVhLFslfLe2dVKVHbpYykj8fhhj3x5o8x__jDG2UDArtHvBesTpMFAq_G6btkAPPXuP0Mo9058uxSWQvXvRvBA.lXL0L-t_A-qpWLXS0Mjnuw^%^2C^%^2C^%^2Ctrue^%^2C^%^2CeyJraWQiOiIyIiwiYWxnIjoiSFMyNTYifQ..OibO4XCKu9A3PdFM4U4jHtohyjA9K8Ua8D_Lpv8BIFc',
        '_ga_D72SGH4DYJ': 'GS1.1.1709384000.1.1.1709384676.0.0.0',
        '_ga': 'GA1.1.2098639722.1709384000',
        'euconsent-v2': 'CP62DgAP62DgAAHABBENApEoAP_gAELgABCYI3wPAABQAKAAwACAAFYALgAwABwADwAIAAWwAxADIAGkARABFACZAFsAXIAwgDEAGYAOQAeAA9QCAAIEAQgAjABHAChAFIAMEAZQA0gBxADrAHiAP0AhABEACJgEcAJaAWkAuoBfYDAAMCAZ0A4QB7QELAI1ATEAsMBZgC8wGMgMnAZYA5gBzQD9wICgQHAjMBG8Eb4EEACgALAAqABcADgAHgAQQAxADIAGgARAAmQBbAFwAMQAZgA9AB-AEIAI4AZQA_QCEAEWAI4AXUAvoB7QExALzAYIAycBlgD9wI3gBEIAMAARBqEAAYAAiDUA.f_wACFwAAAAA',
        '_gcl_au': '1.1.1044411882.1709384001',
        'displayCookieConsent': 'y',
        'FPID': 'FPID2.2.dTIIck0JwPkGq5O6GAgK^%^2BChtR94h8enFhlAyON15QUk^%^3D.1709384000',
        'FPLC': 'iucMJHF7jHdWld9A7RKctLX^%^2BYiKNtNjSBnPdrJah4Kes86MzU9NZv9AAfbbYsfzehTewLwWZNlb9dzRNy7W6v1FJqjKh51YK8fGSHuHBMQC8dS1m7kDziOs1lV4mNA^%^3D^%^3D',
        'FPAU': '1.1.1044411882.1709384001',
        '__gads': 'ID=ae009f9d49545acb:T=1709384015:RT=1709384681:S=ALNI_MakTdnFL75jnfWsILhQ1kwWp_qWmg',
        '__gpi': 'UID=00000d3aa456b6b1:T=1709384015:RT=1709384681:S=ALNI_MZlEjrqSnLyP_uYNmgPMxijq4niAw',
        '__eoi': 'ID=22fa2e304b2c3c59:T=1709384015:RT=1709384681:S=AA-AfjbOlFclylniq6rkbXt1wiT4',
        '_pin_unauth': 'dWlkPU1HTXlZbVU0TXpRdFl6aG1NQzAwTmpGbUxXSTVaRFV0WWprMk9UZzBOakE1WXpSbA',
        '__rtbh.lid': '^%^7B^%^22eventType^%^22^%^3A^%^22lid^%^22^%^2C^%^22id^%^22^%^3A^%^22npKRsxnENopILmrcuicE^%^22^%^7D',
        '_fbp': 'fb.1.1709384003316.1110197362',
        'crto_is_user_optout': 'false',
        'akacd_orodha': '2177452799~rv=11~id=f42363da4b3432fd7e23ff31965371b9',
        '_pbjs_userid_consent_data': '2273866697984331',
        '_pubcid': 'e4e8c4f3-1b3c-467a-bc8e-e002790ec00c',
        '__gsas': 'ID=52ee4447818f55ad:T=1709384345:RT=1709384345:S=ALNI_MZlZjuUfoApJSrE_BuqiTQnzZldsw',
        'mdLogger': 'false',
        'kampyle_userid': '854d-8674-c27b-c8bc-6092-2e2a-18e9-71c5',
        'kampyleUserSession': '1709384335768',
        'kampyleSessionPageCounter': '1',
        'kampyleUserSessionsCount': '1',
        'kampyleUserPercentile': '49.880684222250906',
    }
    __HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Connection': 'keep-alive',
        # 'Cookie': 'kppid=B80A0CC706E56FD7C9B41C99; didomi_token=eyJ1c2VyX2lkIjoiMThkZmYzOWQtOTBmMi02MDdjLTk2ZGEtZTFiN2VlNDExZjkwIiwiY3JlYXRlZCI6IjIwMjQtMDMtMDJUMTI6NTM6MTcuNzM0WiIsInVwZGF0ZWQiOiIyMDI0LTAzLTAyVDEyOjUzOjIxLjE0NFoiLCJ2ZW5kb3JzIjp7ImVuYWJsZWQiOlsiZ29vZ2xlIiwiYzphbXBsaXR1ZGUiLCJjOm1pY3Jvc29mdC1vbmVkcml2ZS1saXZlLXNkayIsImM6YXBwc2ZseWVyLTlqY3duaVk5IiwiYzpiaW5nLWFkcyIsImM6ZGlkb21pIiwiYzprcnV4LWRpZ2l0YWwiLCJjOnF1YW50Y2FzdC1tZWFzdXJlbWVudCIsImM6b21uaXR1cmUtYWRvYmUtYW5hbHl0aWNzIiwiYzpncmFwZXNob3QiLCJjOnF1YW50dW0tYWR2ZXJ0aXNpbmciLCJjOngxIiwiYzp0dWJlbW9ndWwiLCJjOnNlZ21lbnQiLCJjOmFkbW9iIiwiYzptZWRhbGxpYS1paHpyeUZMWSIsImM6c2FsZXNmb3JjZS1DUEJGRWZIUCIsImM6b3B0aW1pemVseS1FTlFFaWlaVCIsImM6YWthY2Rvcm9kLVdBRDdpWHRoIiwiYzptaWNyb3NvZnQtYW5hbHl0aWNzIiwiYzphdGludGVybmUtY1dRS0hlSloiLCJjOnBhbmdsZWRzcC1aQnhMaGdDVyIsImM6Ymx1ZWthaSIsImM6Z29vZ2xlYW5hLTRUWG5KaWdSIiwiYzpzb2Npb21hbnRpLW1NVEc4eGc0IiwiYzphd3MtY2xvdWRmcm9udCIsImM6c3VibGltZXNrLXBaN0FueTdHIiwiYzptZWV0cmljc2ctTmRFTjhXeFQiLCJjOmNlbnRyby1pVVdWbU40TiIsImM6bWljcm9zb2Z0IiwiYzpwaW50ZXJlc3QiXX0sInB1cnBvc2VzIjp7ImVuYWJsZWQiOlsiY29va2llYW5hLWtDQ1JHejRtIiwiY29va2llZGktbk5lMjNRamQiLCJjb29raWV0ZWMtOXFmQUVWd2siLCJhdWRpZW5jZW0teGVkZVUyZ1EiLCJnZW9sb2NhdGlvbl9kYXRhIl19LCJ2ZW5kb3JzX2xpIjp7ImVuYWJsZWQiOlsiZ29vZ2xlIiwiYzpwYW5nbGVkc3AtWkJ4TGhnQ1ciLCJjOnNvY2lvbWFudGktbU1URzh4ZzQiLCJjOmNlbnRyby1pVVdWbU40TiJdfSwidmVyc2lvbiI6MiwiYWMiOiJEQmVBV0FGa0JKWUVvZ0pZZ1VWQkxHQ2VjRkNJTFJ3WG9nd1guREJlQVdBRmtCSllFb2dKWWdVVkJMR0NlY0ZDSUxSd1hvZ3dYIn0=; _pulse2data=6839195a-da88-4b5a-851b-c7809e640b70^%^2Cv^%^2C^%^2C1709384898353^%^2CeyJpc3N1ZWRBdCI6IjIwMjQtMDMtMDJUMTI6NTM6MzJaIiwiZW5jIjoiQTEyOENCQy1IUzI1NiIsImFsZyI6ImRpciIsImtpZCI6IjIifQ..nUuXZY5DOchC7odwsJQYBQ.cCKIe1pZE3WyZwk8oT1vcVl-79JlWGdc8thNXP5xkb_yeIrx4PQvcvfFp-z2uNDKKIaqLi8vodoihthjo6zJtrGJrV2wERdX1cRAhJcPFCWppx-bK6EUrDqq8MAzMHZBJVhLFslfLe2dVKVHbpYykj8fhhj3x5o8x__jDG2UDArtHvBesTpMFAq_G6btkAPPXuP0Mo9058uxSWQvXvRvBA.lXL0L-t_A-qpWLXS0Mjnuw^%^2C^%^2C^%^2Ctrue^%^2C^%^2CeyJraWQiOiIyIiwiYWxnIjoiSFMyNTYifQ..OibO4XCKu9A3PdFM4U4jHtohyjA9K8Ua8D_Lpv8BIFc; _ga_D72SGH4DYJ=GS1.1.1709384000.1.1.1709384676.0.0.0; _ga=GA1.1.2098639722.1709384000; euconsent-v2=CP62DgAP62DgAAHABBENApEoAP_gAELgABCYI3wPAABQAKAAwACAAFYALgAwABwADwAIAAWwAxADIAGkARABFACZAFsAXIAwgDEAGYAOQAeAA9QCAAIEAQgAjABHAChAFIAMEAZQA0gBxADrAHiAP0AhABEACJgEcAJaAWkAuoBfYDAAMCAZ0A4QB7QELAI1ATEAsMBZgC8wGMgMnAZYA5gBzQD9wICgQHAjMBG8Eb4EEACgALAAqABcADgAHgAQQAxADIAGgARAAmQBbAFwAMQAZgA9AB-AEIAI4AZQA_QCEAEWAI4AXUAvoB7QExALzAYIAycBlgD9wI3gBEIAMAARBqEAAYAAiDUA.f_wACFwAAAAA; _gcl_au=1.1.1044411882.1709384001; displayCookieConsent=y; FPID=FPID2.2.dTIIck0JwPkGq5O6GAgK^%^2BChtR94h8enFhlAyON15QUk^%^3D.1709384000; FPLC=iucMJHF7jHdWld9A7RKctLX^%^2BYiKNtNjSBnPdrJah4Kes86MzU9NZv9AAfbbYsfzehTewLwWZNlb9dzRNy7W6v1FJqjKh51YK8fGSHuHBMQC8dS1m7kDziOs1lV4mNA^%^3D^%^3D; FPAU=1.1.1044411882.1709384001; __gads=ID=ae009f9d49545acb:T=1709384015:RT=1709384681:S=ALNI_MakTdnFL75jnfWsILhQ1kwWp_qWmg; __gpi=UID=00000d3aa456b6b1:T=1709384015:RT=1709384681:S=ALNI_MZlEjrqSnLyP_uYNmgPMxijq4niAw; __eoi=ID=22fa2e304b2c3c59:T=1709384015:RT=1709384681:S=AA-AfjbOlFclylniq6rkbXt1wiT4; _pin_unauth=dWlkPU1HTXlZbVU0TXpRdFl6aG1NQzAwTmpGbUxXSTVaRFV0WWprMk9UZzBOakE1WXpSbA; __rtbh.lid=^%^7B^%^22eventType^%^22^%^3A^%^22lid^%^22^%^2C^%^22id^%^22^%^3A^%^22npKRsxnENopILmrcuicE^%^22^%^7D; _fbp=fb.1.1709384003316.1110197362; crto_is_user_optout=false; akacd_orodha=2177452799~rv=11~id=f42363da4b3432fd7e23ff31965371b9; _pbjs_userid_consent_data=2273866697984331; _pubcid=e4e8c4f3-1b3c-467a-bc8e-e002790ec00c; __gsas=ID=52ee4447818f55ad:T=1709384345:RT=1709384345:S=ALNI_MZlZjuUfoApJSrE_BuqiTQnzZldsw; mdLogger=false; kampyle_userid=854d-8674-c27b-c8bc-6092-2e2a-18e9-71c5; kampyleUserSession=1709384335768; kampyleSessionPageCounter=1; kampyleUserSessionsCount=1; kampyleUserPercentile=49.880684222250906',
        'If-None-Match': 'W/bo0xifs8b0723u',
        # Requests doesn't support trailers
        # 'TE': 'trailers',
    }
    __PARAMS = {
        'shp': 'true',
    }
    __PROXY = 'http://user164993:21perz@181.215.227.162:2363'

    def __init__(self):
        self.__DOMEN = 'https://www.subito.it'  # Домен сайта

    async def start(self):
        await self.__get_products_links()

    async def __get_products_links(self):
        url = f'/annunci-italia/vendita/casa-e-persona/?shp=true&o={1}'
        print(url)
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    url=self.__DOMEN + url,
                    params=self.__PARAMS,
                    cookies=self.__COOKIES,
                    headers=self.__HEADERS,
                    proxy=self.__PROXY
            ) as response:
                html = await response.text()

        soup = BeautifulSoup(html, 'lxml')
        ads = soup.find_all("div", class_="items__item item-card item-card--small")

        tasks = [self.__get_user_url(url) for url in ads]
        results = await asyncio.gather(*tasks)
        for result in results:
            if result[0]:
                print(result)
                # await self.__bot.send_message(user_id, result[1])

    async def __get_user_url(self, ad) -> tuple:
        ad_url = ad.find_next()['href']

        async with aiohttp.ClientSession() as session:
            async with session.get(
                    url=ad_url,
                    params=self.__PARAMS,
                    cookies=self.__COOKIES,
                    headers=self.__HEADERS,
                    proxy=self.__PROXY
            ) as response:
                html = await response.text()
                soup = BeautifulSoup(html, 'lxml')
                page_not_found = soup.find('div', class_='__410_title-text__JMfJE')
                if page_not_found:
                    return False, '', ''

                time_ = soup.find('div', class_='AdInfo_ad-info__listing-info__D44kO').find_next().text.split(' ')
                user = soup.find('div', class_='PrivateUserProfileBadge-module_buttonAndContainer__ciDlV')
                if user is None:
                    return False, '', ''
                if time_[0] != 'Oggi':
                    return False, '', ''

                link = user.find('h6').find('a')['href']
                return await self.__get_user_data(link), link, f'Сегодня в {time_[-1]}'

    async def __get_user_data(self, url) -> bool:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    url=self.__DOMEN + url,
                    params=self.__PARAMS,
                    cookies=self.__COOKIES,
                    headers=self.__HEADERS,
                    proxy=self.__PROXY
            ) as response:
                html = await response.text()
                soup = BeautifulSoup(html, 'lxml')
                user_data = soup.find('div', class_='UserData_trust_info_box___ef6s')

                ads = user_data.find_all('p', class_='index-module_sbt-text-atom__ed5J9 index-module_token-body__GXE1P index-module_size-small__XFVFl index-module_weight-book__WdOfA UserData_ads_info_text__Zm2Vo')
                if ads is None:
                    return False

                ads_count = ads[0].next.text
                ads_online_count = ads[1].next.text

                if int(ads_count) == 1 and int(ads_online_count) == 1:
                    return True
                return False


if __name__ == '__main__':
    subito = SubitoDebug()
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(subito.start())
