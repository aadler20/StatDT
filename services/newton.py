import numpy as np
from scipy import misc
from scipy import optimize
from sympy import diff, evalf, symbols
from decimal import Decimal
from math import sin, cos, exp
import matplotlib.pyplot as plt

# method 1
def f(x):
    return x**2 - 5*x + 6
x0 = 4
x = optimize.newton(f, x0, fprime=None, args=(), tol=1e-08, maxiter=50, fprime2=None)
print('Method 1')
print('x0: ', x0)
print('x: ', x)
print("f(x) = ", (x**2 - 5*x + 6))


# method 2
def NewtonsMethod2(f, x, tol=1e-08):
    while True:
        x1 = x - f(x) / misc.derivative(f, x)
        t = abs(x1 - x)
        if t < tol:
            break
        x = x1
    return x

def f(x):
    return x**2 - 5*x + 6

x0 = 4

x = NewtonsMethod2(f, x0)

print('Method 2')
print('x0: ', x0)
print('x: ', x)
print("f(x) = ", (x**2 - 5*x + 6))

# method 3
def f(x):
    return x**2 - 5*x + 6


def dx(x):
    return 2*x - 5


def NewtonsMethod3(x, tol=1e-08):
    h = f(x) / dx(x)
    while abs(h) >= tol:
        h = f(x) / dx(x)
        x = x - h
    return x

x0 = 4

x = NewtonsMethod3(x0)

print('Method 3')
print('x0: ', x0)
print('x: ', x)
print("f(x) = ", (x**2 - 5*x + 6))

# method 4 using diff
def f(x):
    return x**2 - 5*x + 6

def NewtonsMethod4(f, x0, tol=1e-8):
    x = symbols('x')
    dx = diff(f(x), x)
    print("First Derivative : {}".format(dx))
    while True:
        x1 = x0 - f(x0) / float(dx.subs(x, x0))
        if abs(x1 - x0) < tol:
            break
        x0 = x1
    return x1

x0 = 4
x = NewtonsMethod4(f, x0)
print('Method 4')
print('x0: ', x0)
print('x: ', x)
print("f(x) = ", (f(x)))

# method 5 (recursion)
f = lambda x: x**2 - 5*x + 6
dx = lambda x: 2*x - 5

def NewtonsMethod5(f, df, x0, tol=1e-8):
    if abs(f(x0)) < tol:
        return x0
    else:
        return NewtonsMethod5(f, df, x0 - f(x0)/dx(x0), tol)

x0 = 4
x = NewtonsMethod5(f, dx, x0)
print('Method 5')
print('x: ', x0)
print('x: ', x)
print("f(x) = ", (x**2 - 5*x + 6))