import json,sys,numpy as np,pandas as pd
d=json.load(open(sys.argv[1]))
def ser(cid,key):
    for s in d[cid]['series']:
        if s['series_key']==key:
            df=pd.DataFrame(s['series_data']);df['ts']=pd.to_datetime(df['ts']).dt.tz_localize(None).dt.normalize()
            return df.groupby('ts')['y'].last().astype(float)
    raise KeyError(cid,key)
price=ser('118','price')
anchors={'Realized Price':('14','realized_price'),'Realized Price LTS':('116','Realized price LTS'),
 'Realized Price STS':('115','Realized price STS'),'Balanced Price':('141','balanced_price'),
 'Delta Price':('144','delta_price'),'Terminal Price':('142','terminal_price'),'Top Price':('143','top_price'),
 '200WMA':('1294','200wma'),'Realized Price 2Y':('1315','realized_price_2y'),'Realized Price 4Y':('1316','realized_price_4y')}
Q=[0.03,0.10,0.25,0.40,0.60,0.75,0.90,0.97]
idx=price.index; logb={}; used=[]
for name,(c,k) in anchors.items():
    a=ser(c,k).reindex(idx)
    a=a[(a>0)]
    r=np.log(price.reindex(a.index)/a).dropna()
    if len(r)<1000: print('skip',name,len(r)); continue
    q=np.quantile(r,Q); used.append((name,len(r),r.index.min().date()))
    logb[name]=pd.DataFrame({i:np.log(a)+q[i] for i in range(len(Q))})
# consensus: median across anchors in log space (only anchors available that day)
stack=pd.concat(logb,axis=1)
bands=pd.DataFrame({i:np.exp(stack.xs(i,axis=1,level=1).median(axis=1,skipna=True)) for i in range(len(Q))})
navail=stack.xs(0,axis=1,level=1).notna().sum(axis=1)
bands=bands[navail>=3].dropna()
bands=bands.apply(lambda col: col.rolling(7,min_periods=1,center=True).mean())  # glätten
p=price.reindex(bands.index)
# Zone of current price
def zone(i):
    v=p.iloc[i];row=bands.iloc[i].values;return int(np.searchsorted(row,v))
z=[zone(i) for i in range(len(p))]
print('anchors',used);print('range',bands.index.min().date(),bands.index.max().date())
print('last',p.index[-1].date(),p.iloc[-1],bands.iloc[-1].round(0).tolist(),'zone',z[-1])
cnt=np.bincount(z,minlength=9)/len(z);print('time share per zone',np.round(cnt,3))
out={'dates':[x.strftime('%Y-%m-%d') for x in bands.index],'price':[round(x,2) for x in p],
     'bands':[[round(x,2) for x in bands[i]] for i in range(len(Q))],'q':Q,'zone':z,
     'anchors':[u[0] for u in used],'share':[round(x,4) for x in cnt]}
json.dump(out,open(sys.argv[2],'w'))
pd.DataFrame({'price':p,**{f'q{int(Q[i]*100)}':bands[i] for i in range(len(Q))},'zone':z}).to_csv(sys.argv[3],float_format='%.2f')
