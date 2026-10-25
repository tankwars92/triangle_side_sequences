"""Refined closed forms: S = sum over pieces I of [ a0*dQ0(I) + a1*dQ1(I) + s*dM(I) ],
   dQp(I)=Qp(R)-Qp(L-1), dM(I)=M(R)-M(L-1), M = M0+M1 (total first moment); nu = n mod 2."""
from fractions import Fraction as F
from family import pieces, Sqfree, Coprime, factor
ce=lambda a,b:-(-a//b)
def coeffs(side,n):
    H=(n-1)//2; nu=n%2; k0=ce(n-H,2); top=n//3; be=ce(n,3)
    out=[]
    for (L,R) in pieces(side,n):
        if L>R: continue
        if side=='max':
            a0=1-F(n+nu,2); a1=1-F(n+1-nu,2); s=F(3,2)
        elif side=='min':
            if R<k0 or (L<k0): a0=H+1-F(n+nu,2); a1=H+1-F(n+1-nu,2); s=F(1,2)
            else: a0=F(n-nu,2)+1; a1=F(n-1+nu,2)+1; s=F(-3,2)
        else:
            if R<be or (L<be): a0=a1=F(H-n+1); s=F(2)
            else: a0=a1=F(H+1); s=F(-1)
        out.append((L,R,a0,a1,s))
    return out
def S_refined(side,n,orc):
    tot=F(0)
    for L,R,a0,a1,s in coeffs(side,n):
        q0=orc.pref(R,0)[0]-orc.pref(L-1,0)[0]
        q1=orc.pref(R,1)[0]-orc.pref(L-1,1)[0]
        dm=sum(orc.pref(R,p)[1]-orc.pref(L-1,p)[1] for p in (0,1))
        tot+=a0*q0+a1*q1+s*dm
    assert tot.denominator==1; return int(tot)
