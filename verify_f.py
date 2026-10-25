import random
from family import *
random.seed(77)
big=[720720,510510,2*3*5*7*11*13*17*19,999999,1048576]+[random.randint(10**5,10**6) for _ in range(8)]
small=[random.randint(1000,30000) for _ in range(40)]+[27720,30030,32768,29999]
for s,(side,kind) in SEQ.items():
    prop=prop_sqfree if kind=='sqfree' else prop_coprime
    for n in (small if kind=='sqfree' else big): assert a(s,n)==a_linear(n,side,prop),(s,n)
    print(s,"ok",flush=True)
print("fast == linear: squarefree sequences on 44 values n<=3e4, coprime sequences on 13 composite/random n<=1e7")
