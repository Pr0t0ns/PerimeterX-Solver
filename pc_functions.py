def L(key: str) -> list: # L(t)
    n = None
    e = []
    for i in range(len(key) >> 2):
        e.append(0)
    n = 0
    for n in range(0, 8 * len(key), 8):
        try:
            e[n >> 5] |= (255 & ord(key[n // 8])) << (n % 32)
        except:
            e.append(0)
            e[n >> 5] |= (255 & ord(key[n // 8])) << (n % 32)
    return e

## START XOR funcs ##
def O(t, n):
    if t is None:
        return n
    t = t & 0xFFFFFFFF
    n = n & 0xFFFFFFFF
    e = (t & 0xFFFF) + (n & 0xFFFF)
    upper = ((t >> 16) + (n >> 16) + (e >> 16)) & 0xFFFF
    result = (upper << 16) | (e & 0xFFFF)
    if result >= 0x80000000:
        result -= 0x100000000
    return result

def j(t, n):
    t = t & 0xFFFFFFFF
    result = ((t << n) | (t >> (32 - n))) & 0xFFFFFFFF
    if result >= 0x80000000:
        result -= 0x100000000
    return result

def N(t, n, e, r, o, i):
    return O(j(O(O(n, t), O(r, i)), o), e)

def P(t, n, e, r, o, i, a):
    _c = (n & e | ~n & r)
    return N(_c, t, n, o, i, a)

def R(t, n, e, r, o, i, a):
    _abc = (n & r | e & ~r)
    return N(_abc, t, n, o, i, a)

def _(t, n, e, r, o, i, a):
    return N(n ^ e ^ r, t, n, o, i, a)

def F(t, n, e, r, o, i, a):
    return N(e ^ (n | ~r), t, n, o, i, a)

def G(t):
    e = ""
    for n in range(0, 32 * len(t), 8):
        e += chr((t[n >> 5] >> (n % 32)) & 0xFF)
    return e

### END XOR Funcs ###

def U(t: list, n: int) -> list: # Original U(t, n)
    try:
        t[n >> 5] |= 128 << (n % 32)
    except:
        t.append(128)
    try:
        t[14 + ((n + 64) >> 9 << 4)] = n
    except IndexError:
        for _ab in range(14 + ((n + 64) >> 9 << 4) - len(t) + 1):
            t.append(0)
        t[14 + ((n + 64) >> 9 << 4)] = n
    c = 1732584193
    u = -271733879
    l = -1732584194
    f = 271733878
    for e in range(0, len(t), 16):
        r = c
        o = u
        i = l
        a = f
        c = P(c, u, l, f, t[e], 7, -680876936)
        f = P(f, c, u, l, t[e + 1], 12, -389564586)
        l = P(l, f, c, u, t[e + 2], 17, 606105819)
        u = P(u, l, f, c, t[e + 3], 22, -1044525330)
        c = P(c, u, l, f, t[e + 4], 7, -176418897)
        f = P(f, c, u, l, t[e + 5], 12, 1200080426)
        l = P(l, f, c, u, t[e + 6], 17, -1473231341)
        u = P(u, l, f, c, t[e + 7], 22, -45705983)
        c = P(c, u, l, f, t[e + 8], 7, 1770035416)
        f = P(f, c, u, l, t[e + 9], 12, -1958414417)
        l = P(l, f, c, u, t[e + 10], 17, -42063)
        u = P(u, l, f, c, t[e + 11], 22, -1990404162)
        c = P(c, u, l, f, t[e + 12], 7, 1804603682)
        f = P(f, c, u, l, t[e + 13], 12, -40341101)
        l = P(l, f, c, u, t[e + 14], 17, -1502002290)
        try:
            u = P(u, l, f, c, t[e + 15], 22, 1236535329)
        except:
            u = P(u, l, f, c, None, 22, 1236535329)
        c = R(c, u, l, f, t[e + 1], 5, -165796510)
        f = R(f, c, u, l, t[e + 6], 9, -1069501632)
        l = R(l, f, c, u, t[e + 11], 14, 643717713)
        u = R(u, l, f, c, t[e], 20, -373897302)
        c = R(c, u, l, f, t[e + 5], 5, -701558691)
        f = R(f, c, u, l, t[e + 10], 9, 38016083)
        try:
            l = R(l, f, c, u, t[e + 15], 14, -660478335)
        except:
            l = R(l, f, c, u, None, 14, -660478335)
        u = R(u, l, f, c, t[e + 4], 20, -405537848)
        c = R(c, u, l, f, t[e + 9], 5, 568446438)
        f = R(f, c, u, l, t[e + 14], 9, -1019803690)
        l = R(l, f, c, u, t[e + 3], 14, -187363961)
        u = R(u, l, f, c, t[e + 8], 20, 1163531501)
        c = R(c, u, l, f, t[e + 13], 5, -1444681467)
        f = R(f, c, u, l, t[e + 2], 9, -51403784)
        l = R(l, f, c, u, t[e + 7], 14, 1735328473)
        u = R(u, l, f, c, t[e + 12], 20, -1926607734)
        c = _(c, u, l, f, t[e + 5], 4, -378558)
        f = _(f, c, u, l, t[e + 8], 11, -2022574463)
        l = _(l, f, c, u, t[e + 11], 16, 1839030562)
        u = _(u, l, f, c, t[e + 14], 23, -35309556)
        c = _(c, u, l, f, t[e + 1], 4, -1530992060)
        f = _(f, c, u, l, t[e + 4], 11, 1272893353)
        l = _(l, f, c, u, t[e + 7], 16, -155497632)
        u = _(u, l, f, c, t[e + 10], 23, -1094730640)
        c = _(c, u, l, f, t[e + 13], 4, 681279174)
        f = _(f, c, u, l, t[e], 11, -358537222)
        l = _(l, f, c, u, t[e + 3], 16, -722521979)
        u = _(u, l, f, c, t[e + 6], 23, 76029189)
        c = _(c, u, l, f, t[e + 9], 4, -640364487)
        f = _(f, c, u, l, t[e + 12], 11, -421815835)
        try:
            l = _(l, f, c, u, t[e + 15], 16, 530742520)
        except:
            l = _(l, f, c, u, None, 16, 530742520)
        u = _(u, l, f, c, t[e + 2], 23, -995338651)
        c = F(c, u, l, f, t[e], 6, -198630844)
        f = F(f, c, u, l, t[e + 7], 10, 1126891415)
        l = F(l, f, c, u, t[e + 14], 15, -1416354905)
        u = F(u, l, f, c, t[e + 5], 21, -57434055)
        c = F(c, u, l, f, t[e + 12], 6, 1700485571)
        f = F(f, c, u, l, t[e + 3], 10, -1894986606)
        l = F(l, f, c, u, t[e + 10], 15, -1051523)
        u = F(u, l, f, c, t[e + 1], 21, -2054922799)
        c = F(c, u, l, f, t[e + 8], 6, 1873313359)
        try:
            f = F(f, c, u, l, t[e + 15], 10, -30611744)
        except:
            f = F(f, c, u, l, None, 10, -30611744)
        l = F(l, f, c, u, t[e + 6], 15, -1560198380)
        u = F(u, l, f, c, t[e + 13], 21, 1309151649)
        c = F(c, u, l, f, t[e + 4], 6, -145523070)
        f = F(f, c, u, l, t[e + 11], 10, -1120210379)
        l = F(l, f, c, u, t[e + 2], 15, 718787259)
        u = F(u, l, f, c, t[e + 9], 21, -343485551)
        c = O(c, r)
        u = O(u, o)
        l = O(l, i)
        f = O(f, a)
    return [c,u,l,f]