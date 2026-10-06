# Prognose des Ribbons für 4 Jahre: Power-Law-Trend (Fit ab 2018) für die Ribbon-Mitte,
# heutige Abweichung klingt mit 2 Jahren Halbwertszeit ab, Bandbreiten gleiten auf den 4-Jahres-Median.
import json,sys,numpy as np,pandas as pd
D=json.load(open(sys.argv[1]))
t=pd.to_datetime(D['dates']);B=np.log(np.array(D['bands']));mid=(B[3]+B[4])/2
g=pd.Timestamp('2009-01-03');x=np.log((t-g).days.values)
m=t>='2018-01-01';b,a=np.polyfit(x[m],mid[m],1);r0=mid[-1]-(a+b*x[-1])
off_now=B[:,-1]-mid[-1];off_tgt=np.median((B-mid)[:,t>=t[-1]-pd.Timedelta(days=1461)],1)
ft=pd.date_range(t[-1]+pd.Timedelta(days=1),t[-1]+pd.Timedelta(days=4*365),freq='D')
dt=(ft-t[-1]).days.values/365.25;fx=np.log((ft-g).days.values)
fmid=a+b*fx+r0*0.5**(dt/2);k=1-0.5**(dt/1)
fB=np.exp(fmid[None,:]+off_now[:,None]*(1-k)+off_tgt[:,None]*k)
D['fdates']=[d.strftime('%Y-%m-%d') for d in ft];D['fbands']=[[round(v,2) for v in r] for r in fB]
D['fit']={'a':a,'b':b,'r0':r0}
yr=[i for i,d in enumerate(ft) if d.month==10 and d.day==1]
D['ftable']=[[ft[i].strftime('%Y-%m-%d')]+[round(v) for v in fB[:,i]] for i in yr]
print(D['ftable'])
json.dump(D,open(sys.argv[2],'w'))
pd.DataFrame(fB.T,index=ft,columns=[f'q{int(q*100)}' for q in D['q']]).to_csv(sys.argv[3],float_format='%.2f')
