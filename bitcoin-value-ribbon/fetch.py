import json,gzip,hashlib,urllib.request,sys
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
K="sb_publishable_RYSDy8FrvWsClNWT9WWg8A_Mb9eCdp9"
key=hashlib.pbkdf2_hmac('sha256',b"your-32-char-secret-key-here!!!",b"salt",100000,32)
charts=json.load(open(sys.argv[1]))
ids=[int(c['id']) for c in charts]
out={}
for i in range(0,len(ids),10):
    req=urllib.request.Request("https://api.blockhorizon.io/functions/v1/metric_handler/charts-batch",
      data=json.dumps({"chartIds":ids[i:i+10],"includeFullData":True}).encode(),
      headers={"Content-Type":"application/json","apikey":K,"Authorization":"Bearer "+K})
    r=json.load(urllib.request.urlopen(req,timeout=120))
    b=bytes.fromhex(r['data'])
    res=json.loads(gzip.decompress(AESGCM(key).decrypt(b[:12],b[12:],None)))
    for m in res:
        if m.get('success'): out[str(m['data'].get('id'))]=m['data']
        else: print('fail',m)
    print(i,len(out),flush=True)
json.dump(out,open(sys.argv[2],'w'))
