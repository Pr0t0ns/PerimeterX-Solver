import json
import base64
import urllib.parse
import re
from pc_functions import L, U, G


def encode_string(t):
    url_encoded = urllib.parse.quote(t, safe='')
    def replace_func(match):
        return chr(int(match.group(1), 16))
    decoded = re.sub(r'%([0-9A-F]{2})', replace_func, url_encoded)
    base64_encoded = base64.b64encode(decoded.encode('utf-8')).decode('utf-8')
    return base64_encoded

def calculate_hash_from_xored_value(value: str) -> str:
    n = "0123456789abcdef"
    e = ""
    for o in range(len(value)):
        r = ord(value[o])
        e += n[(r >> 4) & 0xF] + n[r & 0xF]
    return e

def hash_to_full_pc(hash: str) -> int:
    n = ""
    e = ""
    for r in range(len(hash)):
        o = ord(hash[r])
        if 48 <= o <= 57: 
            n += hash[r]
        else:
            e += str(o % 10)  
    return n + e

def generate_pc(key: str, fingerprint: str, pc_generation: bool=True) -> int: # Original Function W(t, n)
    e = None
    r = L(key)
    o = []
    i = []
    for _abcd in range(15):
        o.append(0)
        i.append(0)
    o.append(None)
    i.append(None)
    if len(r) > 16:
        r = U(r, 8 * len(key))
    for e in range(16):
        try:
            o[e] = 909522486 ^ r[e]
        except:
            o[e] = 909522486
        try:
            i[e] = 1549556828 ^ r[e]
        except:
            i[e] = 1549556828
    for val in L(fingerprint):
        o.append(val)
    a = U(o, 512 + 8 * len(fingerprint))
    for int_val in a:
        i.append(int_val)
    _v = G(U(i, 640))
    calculated_hash = calculate_hash_from_xored_value(_v)
    if not pc_generation:
        return calculated_hash
    r = (hash_to_full_pc(calculated_hash))
    o = ""
    for i in range(0, len(r), 2):
        o += r[i]
    return o
    

def fn(t, n):
    e = ""
    for char in t:
        e += chr(ord(char) ^ n)
    return e

def encrypt_payload(payload: str) -> str:
    return encode_string(fn(payload, 50))