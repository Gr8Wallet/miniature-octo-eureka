# 4-Jahres-Prognose aus allen KPIs:
# 1) Jede KPI wird per Halving-Zyklus-Analogie fortgeschrieben (Median der Verläufe ab gleicher Zyklusphase 2012/2016/2020).
# 2) Die 10 Preismodelle (Anker) liefern so das prognostizierte Ribbon.
# 3) Jede KPI wird (zyklisch bereinigt) per historischer Zuordnung in eine Ribbon-Position übersetzt;
#    gewichteter Median aller KPIs = Konsens-Position -> Preisprognose (+ 25/75 %-Spanne).
import json,sys,numpy as np,pandas as pd
d=json.load(open(sys.argv[1])); R=json.load(open(sys.argv[2]))
H=pd.to_datetime(['2012-11-28','2016-07-09','2020-05-11','2024-04-20'])
N=4*365
def ser(s):
    df=pd.DataFrame(s['series_data']);df['ts']=pd.to_datetime(df['ts']).dt.tz_localize(None).dt.normalize()
    return pd.to_numeric(df.groupby('ts')['y'].last(),errors='coerce').dropna().asfreq('D').interpolate(limit=30)
price=ser([s for s in d['118']['series'] if s['series_key']=='price'][0])
T0=price.index[-1]; fidx=pd.date_range(T0+pd.Timedelta(days=1),periods=N,freq='D')
phase=(T0-H[-1]).days
def analog(x,islog):
    v=np.log(x) if islog else x
    paths=[]
    for h in H[:-1]:
        s=h+pd.Timedelta(days=phase); w=v.reindex(pd.date_range(s,periods=N+1,freq='D'))
        if w.isna().mean()>0.05 or np.isnan(w.iloc[0]): continue
        w=w.interpolate().bfill().ffill(); paths.append((w.values[1:]-w.values[0]))
    if not paths: return None,0
    p=np.median(np.array(paths),0)
    last=v.dropna().iloc[-1]; out=last+p
    return (np.exp(out) if islog else out),len(paths)
kpis={}; meta=[]
for cid,c in d.items():
    ss=[s for s in c['series'] if s['series_key']!='price' and s.get('series_data')]
    if not ss: continue
    x=ser(ss[0]); x=x[x.index<=T0]
    if len(x)<1500 or x.index[-1]<T0-pd.Timedelta(days=10): continue
    x=x.reindex(pd.date_range(x.index[0],T0,freq='D')).interpolate().ffill()
    islog=bool((x>0).all() and x.max()/max(x.min(),1e-12)>20)
    f,n=analog(x,islog)
    if f is None: continue
    kpis[cid]=(c['name'].strip(),x,pd.Series(f,index=fidx),islog,n)
print('KPIs prognostiziert:',len(kpis))
# --- Ribbon-Prognose aus prognostizierten Anker-Modellen
dates=pd.to_datetime(R['dates']);B=pd.DataFrame(np.array(R['bands']).T,index=dates)
anchors={'14':0,'116':0,'115':0,'141':0,'144':0,'142':0,'143':0,'1294':0,'1315':0,'1316':0}
Q=R['q'];lb=[]
for cid in anchors:
    if cid not in kpis: continue
    _,x,f,_,_=kpis[cid]; r=np.log(price.reindex(x.index)/x).dropna(); q=np.quantile(r,Q)
    lb.append(np.log(f.values)[None,:]+q[:,None])
fB=np.exp(np.median(np.array(lb),0))
fB=pd.DataFrame(fB.T,index=fidx).rolling(15,min_periods=1,center=True).mean()
# Übergang ohne Sprung: Abweichung zum letzten Ist-Ribbon auslaufen lassen (90 Tage)
gap=np.log(B.iloc[-1].values)-np.log(fB.iloc[0].values); dec=np.exp(-np.arange(N)/90)
fB=np.exp(np.log(fB.values)+gap[None,:]*dec[:,None])
# --- Position im Ribbon (0..8, kontinuierlich)
def position(lp,bands):
    lb_=np.log(bands); e=np.column_stack([lb_[:,0]-(lb_[:,1]-lb_[:,0]),lb_,lb_[:,-1]+(lb_[:,-1]-lb_[:,-2])])
    return np.array([np.interp(v,row,np.arange(-0.5,9.5,1.0) if False else np.linspace(0,9,10)) for v,row in zip(lp,e)])
pos=pd.Series(position(np.log(price.reindex(dates).values),B.values),index=dates)
def inv_position(p,bands):
    lb_=np.log(bands); e=np.column_stack([lb_[:,0]-(lb_[:,1]-lb_[:,0]),lb_,lb_[:,-1]+(lb_[:,-1]-lb_[:,-2])])
    return np.exp([np.interp(v,np.linspace(0,9,10),row) for v,row in zip(p,e)])
# --- KPI -> Position
def feat(full,islog):
    v=np.log(full) if islog else full
    return v-v.rolling(1461,min_periods=365).mean() if islog else v
rows=[];P=[];W=[]
for cid,(name,x,f,islog,n) in kpis.items():
    if cid in ('128',):pass
    full=pd.concat([x,f]); z=feat(full,islog)
    zh=z.reindex(pos.index); m=zh.notna()&pos.notna()
    if m.sum()<1000: continue
    a=zh[m];p=pos[m]
    rho=pd.Series(a.values).rank().corr(pd.Series(p.values).rank())
    if not np.isfinite(rho) or abs(rho)<0.2: rows.append((name,round(rho,2) if np.isfinite(rho) else None,'zu schwach',n));continue
    # Zuordnung über Quantil-Bins: KPI-Wert -> mittlere Position
    qs=np.unique(np.quantile(a,np.linspace(0,1,21)));bi=np.clip(np.searchsorted(qs,a,side='right')-1,0,len(qs)-2)
    centers=[a[bi==i].median() for i in range(len(qs)-1)];vals=[p[bi==i].median() for i in range(len(qs)-1)]
    o=np.argsort(centers);centers=np.array(centers)[o];vals=np.array(vals)[o]
    zf=z.reindex(fidx).values; pf=np.interp(zf,centers,vals)
    # Kalibrierung: heute muss die KPI die heutige Position treffen -> Offset klingt in 1 Jahr aus
    p_now=np.interp(z.reindex([T0]).values[0],centers,vals); off=pos.iloc[-1]-p_now
    pf=pf+off*np.exp(-np.arange(N)/365)
    P.append(pf);W.append(rho**2);rows.append((name,round(rho,2),'genutzt',n))
P=np.array(P);W=np.array(W)
def wq(col,q):
    o=np.argsort(col);c=np.cumsum(W[o])/W.sum();return col[o][np.searchsorted(c,q)]
cons=np.array([[wq(P[:,t],q) for q in (0.25,0.5,0.75)] for t in range(N)])
cons=pd.DataFrame(cons,index=fidx).rolling(30,min_periods=1,center=True).mean().values
fp={k:inv_position(cons[:,i],fB) for i,k in enumerate(['p25','p50','p75'])}
used=[r for r in rows if r[2]=='genutzt']
print('genutzt',len(used),'von',len(rows))
R['fdates']=[t.strftime('%Y-%m-%d') for t in fidx];R['fbands']=[[round(v,2) for v in fB[:,i]] for i in range(fB.shape[1])]
for k,v in fp.items(): R['f'+k]=[round(x,2) for x in v]
R['fzone']=[int(min(8,max(0,np.floor(c)))) for c in cons[:,1]]
R['kpis']=sorted([[r[0],r[1],r[2]] for r in rows],key=lambda r:-abs(r[1] or 0))
R['nk']=len(kpis);R['nused']=len(used);R['phase']=phase
yr=[i for i,t in enumerate(fidx) if t.month==10 and t.day==1]
R['ftable']=[[fidx[i].strftime('%Y-%m-%d'),round(fp['p25'][i]),round(fp['p50'][i]),round(fp['p75'][i]),R['fzone'][i]]+[round(v) for v in fB[i]] for i in yr]
for r in R['ftable']:print(r[:5])
mx=np.argmax(fp['p50']);mn=np.argmin(fp['p50'][mx:])+mx
print('peak',fidx[mx].date(),round(fp['p50'][mx]),'low after',fidx[mn].date(),round(fp['p50'][mn]))
R.pop('fit',None)
json.dump(R,open(sys.argv[3],'w'))
pd.DataFrame({'p25':fp['p25'],'p50':fp['p50'],'p75':fp['p75'],'zone':R['fzone'],**{f'q{int(Q[i]*100)}':fB[:,i] for i in range(8)}},index=fidx).to_csv(sys.argv[4],float_format='%.2f')
pd.DataFrame(rows,columns=['kpi','spearman_rho','status','analog_cycles']).to_csv(sys.argv[5],index=False)
