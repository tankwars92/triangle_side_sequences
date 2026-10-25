import time,random
from family import *
def tm(fn):
    t=time.perf_counter(); r=fn(); return r,time.perf_counter()-t
print("seq,n,value,t_double,t_linear,t_fast,agree",flush=True)
for s in ['A308453','A308455','A308454','A308202','A308209']:
    side,kind=SEQ[s]; prop=prop_sqfree if kind=='sqfree' else prop_coprime
    for e in range(2,15):
        n=10**e+7 if kind=='coprime' else 10**e
        if kind=='sqfree' and e>13: break
        rf,tf=tm(lambda:a(s,n)); vals=[rf]; td=tl=""
        if e<=4: r,t=tm(lambda:a_double(n,side,prop)); td="%.4f"%t; vals.append(r)
        if e<=6 and kind=='sqfree' or e<=7 and kind=='coprime': r,t=tm(lambda:a_linear(n,side,prop)); tl="%.4f"%t; vals.append(r)
        print("%s,%d,%d,%s,%s,%.5f,%s"%(s,n,rf,td,tl,tf,len(set(vals))==1),flush=True)
# coprime sequences at huge n (no baseline possible)
for s in ['A308202','A308209']:
    for n in [10**18+9, 2**61-1, 10**24+7, 3*5*7*11*13*17*19*23*29*31*37*41*43*47]:
        r,t=tm(lambda:a(s,n)); print("%s,%d,%d,,,%.5f,huge"%(s,n,r,t),flush=True)
