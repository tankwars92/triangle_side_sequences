"""Checks of the explicit weight formulas (Lemmas 3-5 and Table 1) used in the paper."""
from fractions import Fraction as F
from family import weight,pieces
ce=lambda a,b:-(-a//b)
bad=0
for n in range(3,600):
    H=(n-1)//2
    for side in ('min','mid','max'):
        w=weight(side,n)
        for (L,R) in pieces(side,n):
            for k in range(L,R+1):
                e=(n-k)%2
                if side=='min':
                    k0=ce(n-H,2)
                    f=F(H+1)-F(n,2)-F(e,2)+F(k,2) if k<k0 else F(n-e,2)+1-F(3*k,2)
                elif side=='mid':
                    f=F(H-n+1+2*k) if k<ce(n,3) else F(H+1-k)
                else: f=F(3*k,2)+1-F(n+e,2)
                bad+= (f!=w(k))
print("T1 explicit affine forms: mismatches =",bad,"(n=3..599)")
for n in range(3,300):
    m=n*n if n%2==0 else (n+3)**2
    alc=(2*m+48)//96
    for side in ('min','mid','max'):
        w=weight(side,n); assert sum(w(k) for L,R in pieces(side,n) for k in range(L,R+1))==alc
print("T2 sum of weights = nearest integer to n^2/48 (n even) or (n+3)^2/48 (n odd), n=3..299, all three sides")
for n in range(3,200):
    for side in ('min','mid','max'):
        sup={}
        for a in range(1,n):
            for b in range(a,n):
                c=n-a-b
                if c>=b and a+b>c:
                    s={'min':a,'mid':b,'max':c}[side]; sup[s]=sup.get(s,0)+1
        w=weight(side,n); cov={k for L,R in pieces(side,n) for k in range(L,R+1)}
        assert set(sup)<=cov and all(w(k)==sup.get(k,0) for k in cov),(n,side)
print("T3 W_n equals the brute-force count of triangles on the whole piece range; pieces cover the support, n=3..199")
