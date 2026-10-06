# Korrektur der Preisprognose auf abnehmende Abstände zum Power-Law-Support:
# Zyklushochs (Preis/Support) sind historisch log-linear gefallen; der Trend wird fortgeschrieben
# und je Prognosezyklus (für Preisprognose und Ribbon-Bänder) als Obergrenze genutzt (log-Abstand wird proportional gestaucht).
import json,sys,numpy as np,pandas as pd
J=json.load(open(sys.argv[1]))
H=pd.to_datetime(['2012-11-28','2016-07-09','2020-05-11','2024-04-20','2028-04-15','2032-04-15','2036-04-15'])
h=pd.Series(np.array(J['price'])/np.array(J['pl']),index=pd.to_datetime(J['dates']))
ft=pd.to_datetime(J['fdates']);sup=np.array(J['fpl'])
peaks=[h[H[i]:H[i+1]].max() for i in range(4)]
k,c=np.polyfit(np.arange(4),np.log(peaks),1)
cap={i:float(np.exp(c+k*i)) for i in range(3,6)}; cap[3]=max(cap[3],peaks[3])
print('Hochs',np.round(peaks,2),'Faktor je Zyklus',round(np.exp(k),2),'Caps',{H[i].year:round(v,2) for i,v in cap.items()})
lm=np.log(np.array(J['fp50'])/sup); s=np.ones(len(ft))
for i in range(3,6):
    m=(ft>=H[i])&(ft<H[i+1])
    if m.any(): mx=lm[m].max(); s[m]=min(1,np.log(cap[i])/mx) if mx>0 else 1
s=pd.Series(s).rolling(365,min_periods=1,center=True).min().rolling(365,min_periods=1,center=True).mean().values
s=np.minimum(s,1)
ramp=np.clip(np.arange(len(ft))/180,0,1); s=1-(1-s)*ramp   # weicher Start ab heute
J['fp50_raw']=J['fp50'];J['dimfit']={'peaks':[round(p,2) for p in peaks],'factor':round(float(np.exp(k)),3),'caps':{str(H[i].year):round(v,2) for i,v in cap.items()}}
for key in ('fp25','fp50','fp75'):
    m=np.array(J[key])/sup; lmk=np.log(m); J[key]=[round(v,2) for v in sup*np.exp(np.where(lmk>0,lmk*s,lmk))]
# Ribbon-Bänder gleich stauchen (Abstand zum Support), damit Zonen konsistent bleiben
J['fbands']=[[round(v,2) for v in sup*np.exp(np.where(np.log(np.array(b)/sup)>0,np.log(np.array(b)/sup)*s,np.log(np.array(b)/sup)))] for b in J['fbands']]
f=pd.Series(np.array(J['fp50'])/sup,index=ft)
for i in range(3,6):
    seg=f[H[i]:H[i+1]]
    if len(seg): print('Prognose-Zyklus',H[i].year,'max',round(seg.max(),2),seg.idxmax().date())
# Zone der korrigierten Prognose neu bestimmen
B=np.array(J['fbands']).T; fp=np.array(J['fp50'])
J['fzone']=[int(np.searchsorted(B[i],fp[i])) for i in range(len(fp))]
idx={d:i for i,d in enumerate(J['fdates'])}
for r in J['ftable']:
    i=idx[r[0]];r[1],r[2],r[3],r[4]=round(J['fp25'][i]),round(J['fp50'][i]),round(J['fp75'][i]),J['fzone'][i]
    print(r[:5],'Abstand',round(J['fp50'][i]/J['fpl'][i],2))
json.dump(J,open(sys.argv[2],'w'))
