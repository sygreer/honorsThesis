#!/usr/bin/env python2

from triOp import *
from numpy import zeros, matmul, identity
from numpy.linalg import norm, matrix_rank
def main():
    print('Generic systems solver')
    print('functions include...')
    print('    conjGrad(A, b, tol, maxItr)')
    print('    irls(A, b, tol, maxItr, nliter)')
    print('    lsConjGrad(A, b, tol, maxItr)')
    print('    regLsConjGrad(A, b, alpha, tol, maxItr)')

def conjGrad(A, b, tol=1e-8, maxItr=1500, x=0):
    '''
    conjugate gradients solver
    does NOT check if A is SPD
    '''
    n = len(b)

    if norm(x) == 0:
        x = zeros(n)

    r = b - A.dot(x)
    p = r

    res0 = norm(r)
    for i in range(1,maxItr):
        Ap = A.dot(p)
        pAp = p.dot(Ap)
        alpha = r.dot(p)/pAp

        x += alpha*p
        r -= alpha*Ap

        if norm(r)/res0 <= tol:
            break

        beta = -Ap.dot(r)/pAp
        p = r + beta * p
    return x

def irls(A, b, nrm=1, tol=1e-8, maxItr=1500, nliter=10):
    # find L2 solution
    At = A.transpose()
    A = matmul(A,At)
    b = At.dot(b)
    psinv = conjGrad(A,b,tol,maxItr)

    # find nrm solution
    for i in range (1,nliter):
        print("IRLS nliter # %i"%i)
        r = b - A.dot(psinv)
        R = zeros((len(b),len(b)))
        for j in range(1,len(r)):
            R[j,j] = abs(r[i]**(nrm-2));

        A = matmul(matmul(At,R),A)
        b = matmul(At,R).dot(b)
        psinv = conjGrad(A,b,tol,maxItr)

    return psinv

def lsConjGrad(A, b, tol=1e-8, maxItr=1500):
    At = A.transpose()
    Als = matmul(At,A) 
    bls = At.dot(b)
    print ("Matrix rank: %i" %matrix_rank(Als))
    print ("Full rank: %i" %len(bls))
    return conjGrad(Als, bls, tol, maxItr)

def regLsConjGrad(A, b, alpha=0.5, tol=1e-8, maxItr=1500):
    At = A.transpose()
    Als = matmul(At,A) + alpha*identity(len(b))
    bls = At.dot(b)
    return conjGrad(Als, bls, tol, maxItr)

def shaping(A, b, alpha=0.5, tol=1e-8, maxItr=1500, nliter=5, sz=30, tp="bp"):
    At = A.transpose()
    Als = matmul(At,A) + alpha*identity(len(b))
    bls = At.dot(b)

    x = zeros(len(bls))

    if tp=="tri":
        tri=triOper(sz)
        for i in range(0, nliter):
            x = foldConv(x, tri)
            x = conjGrad(Als, bls, tol, maxItr, x)
            print("Iter: %i"%i)

    elif tp=="bp":
        for i in range(0, nliter):
            x = lowPassFilter(x, sz, 1/0.001, plot=True)
            x = conjGrad(Als, bls, tol, maxItr, x)
            print("Iter: %i"%i)

        #plt.show()

    return x

if __name__ == "__main__":
    main()
