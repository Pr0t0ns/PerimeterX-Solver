import tls_client
import uuid
import time
import json
import re
from fingerprint import fingerprint_1, fingerprint_2
from mods import encrypt_payload, generate_pc
import urllib.parse
class PX:
    def __init__(self, app_id: str, ft: int, collector_uri: str, host: str, sid: str, vid: str, cts: str, proxy: str=None):
        self.session = tls_client.Session(client_identifier="chrome_127", random_tls_extension_order=True)
        if proxy != None:
            self.session.proxies = {
                'https': f'http://{proxy}',
                'http': f'http://{proxy}'
            }
        self.collector_url = collector_uri
        self.app_id = app_id
        self.vid = vid
        self.cts = cts
        self.host = host
        self.sid = sid
        self.ft = ft
        self.session.headers = {
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'content-type': 'application/x-www-form-urlencoded',
            'origin': host,
            'priority': 'u=1, i',
            'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
        }
        self.st = int(time.time()) * 1000
        self.site_uuids = {
            "sid": sid,
            "vid": vid,
            "cts": cts
        }
        self.uuid = str(uuid.uuid4())
        self.pc_key = f"{self.uuid}:v6.7.9:{ft}"
        self.rsc = 1

    @staticmethod
    def parse_for_cookie(response: dict) -> str:

        try:
            return str(response['do']).split("bake|_px3|330|")[1].split("|")[0]
        except:
            return None
        

    def request_1(self):
        self.raw_payload = fingerprint_1(self.host, self.uuid, self.st)
        payload = {
            "payload": encrypt_payload(self.raw_payload),
            "appId": self.app_id,
            "tag": "v6.7.9",
            "uuid": self.uuid,
            "ft": self.ft,
            "seq": (self.rsc - 1),
            "en": "NTA",
            "pc": generate_pc(self.pc_key, self.raw_payload),
            "sid": self.sid,
            "rsc": self.rsc
        }
        i = 0
        for site_key in self.site_uuids:
            if self.site_uuids[site_key] != None:
                payload[site_key] = self.site_uuids[site_key]
            i += 1
        self.rsc += 1
        self.resp_1 = self.session.post(self.collector_url, data=urllib.parse.urlencode(payload, safe="=")).json()
        return

    def solve_request(self):
        self.fp_2 = fingerprint_2(json.loads(self.raw_payload), self.resp_1, self.site_uuids)
        payload_data = {
            "payload": encrypt_payload(self.fp_2),
            "appId": self.app_id,
            "tag": "v6.7.9",
            "uuid": self.uuid,
            "ft": self.ft,
            "seq": self.rsc - 1,
            "en": "NTA",
            "cs": f"{str(self.resp_1['do']).split("cs|")[1].split("',")[0]}",
            "pc": generate_pc(self.pc_key, self.fp_2),
            "sid": self.site_uuids['sid'],
            "vid": self.site_uuids['vid'],
            "cts": self.site_uuids['cts'],
            "rsc": self.rsc
        }
        self.resp_2 = self.session.post(self.collector_url, data=urllib.parse.urlencode(payload_data, safe="=")).json()
        return
    def solve(self):
        self.request_1()
        token = PX.parse_for_cookie(self.resp_1)
        if token != None:
            return token
        self.solve_request()
        token = PX.parse_for_cookie(self.resp_2)
        return token

if __name__ == "__main__":
    token = PX(
        app_id="PX0OZADU9K",
        ft=221,
        collector_uri="https://collector-px0ozadu9k.px-cloud.net/api/v2/collector",
        host="https://airtable.com/login",
        sid="474b6227-54f2-11ef-a959-cc2d2dcd99ae󠄱󠄷󠄲󠄳󠄳󠄲󠄶󠄷󠄹󠄴󠄵󠄵󠄳",
        vid="49bf0cb5-5697-11ef-84ed-4e092214a776",
        cts="49bf1545-5697-11ef-84ed-422d064a3602"
    ).solve()
    
    if token != None:
        print(f"Solved PX: {token}")
    else:
        print('Failed to solve PX')