import sys, re, hashlib, urllib.request, json, concurrent.futures as cf
API="https://mempool.space/api"
def get(p):
    for i in range(4):
        try:
            with urllib.request.urlopen(API+p,timeout=60) as r: return r.read()
        except Exception as e: err=e
    raise err
def varint(b,i):
    n=b[i]
    if n<0xfd: return n,i+1
    if n==0xfd: return int.from_bytes(b[i+1:i+3],'little'),i+3
    if n==0xfe: return int.from_bytes(b[i+1:i+5],'little'),i+5
    return int.from_bytes(b[i+1:i+9],'little'),i+9
TXT=re.compile(rb"[\x20-\x7e]{16,}")
def txs(b):
    i=80; n,i=varint(b,i)
    for _ in range(n):
        s=i; i+=4; seg=False
        if b[i]==0 and b[i+1]==1: seg=True; i+=2
        ns=i-(2 if seg else 0)
        nin,i=varint(b,i); scripts=[]
        for _ in range(nin):
            i+=36; l,i=varint(b,i); scripts.append(b[i:i+l]); i+=l+4
        nout,i=varint(b,i)
        for _ in range(nout):
            i+=8; l,i=varint(b,i); scripts.append(b[i:i+l]); i+=l
        we=i
        if seg:
            for _ in range(nin):
                k,i=varint(b,i)
                for _ in range(k): l,i=varint(b,i); i+=l
        i+=4
        core=b[s:s+4]+b[ns+2 if seg else ns:we]+b[i-4:i] if seg else b[s:i]
        txid=hashlib.sha256(hashlib.sha256(core).digest()).digest()[::-1].hex()
        yield txid,scripts
def scan(h):
    out=[]
    try:
        bh=get(f"/block-height/{h}").decode().strip()
        b=get(f"/block/{bh}/raw")
        for txid,sc in txs(b):
            for s in sc:
                for m in TXT.finditer(s):
                    t=m.group().decode()
                    if t.count(' ')>=2 and sum(c.isalpha() for c in t)>len(t)*.6:
                        out.append((h,txid,t))
    except Exception as e: print("ERR",h,e,file=sys.stderr)
    return out
if __name__=="__main__":
    a,z=int(sys.argv[1]),int(sys.argv[2])
    with cf.ThreadPoolExecutor(16) as ex, open(sys.argv[3],"a") as f:
        for res in ex.map(scan,range(a,z)):
            for r in res: f.write(json.dumps(r)+"\n")
            f.flush()
