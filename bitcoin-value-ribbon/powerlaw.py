# Power-Law-Support: log10(Preis) = a + b*log10(Tage seit Genesis), OLS-Fit ab 2011,
# danach nach unten verschoben, sodass nur 1 % der Tage darunter lagen (Boden).
import json,sys,numpy as np,pandas as pd
R=json.load(open(sys.argv[1]));g=pd.Timestamp('2009-01-03')
t=pd.to_datetime(R['dates']);p=np.array(R['price'],float);m=(t>='2011-01-01')&(p>0)
x=np.log10((t-g).days.values);b,a=np.polyfit(x[m],np.log10(p[m]),1)
r=np.log10(p[m])-(a+b*x[m]);s=np.quantile(r,0.01)
ft=pd.to_datetime(R['fdates']);fx=np.log10((ft-g).days.values)
R['pl']=[round(10**(a+s+b*v),2) for v in x];R['fpl']=[round(10**(a+s+b*v),2) for v in fx]
R['plfit']={'a':round(a+s,4),'b':round(b,4)}
print('b',b,'a',a+s,'heute',R['pl'][-1],'2030',R['fpl'][-1],'Tage unter Support',int((r<s).sum()))
json.dump(R,open(sys.argv[2],'w'))
