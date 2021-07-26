

# This file was *autogenerated* from the file hilbert.sage
from sage.all_cmdline import *   # import sage library

_sage_const_3 = Integer(3); _sage_const_100 = Integer(100); _sage_const_2 = Integer(2); _sage_const_18 = Integer(18); _sage_const_0p5 = RealNumber('0.5'); _sage_const_4p2 = RealNumber('4.2'); _sage_const_1 = Integer(1)
from sage.modular.local_comp.liftings import lift_matrix_to_sl2z
from all import *
from shimura import *
from modular import *

N = _sage_const_3   # level of our modular function gamma_2
prec = _sage_const_100   # We do our complex calculations with 100 bits of precision
R = PolynomialRing(ZZ, names=('X',)); (X,) = R._first_ngens(1)
K = NumberField(x**_sage_const_2  + x + _sage_const_18 , embedding=-_sage_const_0p5 +_sage_const_4p2 *I, names=('theta',)); (theta,) = K._first_ngens(1)
O = K.maximal_order()
Omod3 = O.quotient_ring(N, 'b')
J = Ideles(K)


print("=============================================================")
print("================= Finding a class invariant =================")
Omod3star = K.ideal(N).idealstar(flag=_sage_const_2 )
for x in Omod3star.gens_values():
    print("=============================================================")
    print("Found generator x = {} of (O/{}O)^*".format(x, N))

    u = J._from_modulo_element(Omod3(x))
    print("Corresponding idèle u is\n{}".format(u))

    B, A = factored_shimura_connecting_homomorphism(u, output_prec=N)
    print("Factorization g_theta(u) = B*A is given by:\n{}\n*\n{}".format(B, A))

    A = A.change_ring(ZZ) # u lies in Ohat^*, hence A lies in SL_2(ZZ)
    B_N = matrix_modulo(B, N)
    d = det(B_N)
    STs = ST_factor(diagonal_matrix([_sage_const_1 , _sage_const_1 /d]) * B_N * A)
    print("It follows that g_theta(u)_N = iota({})*{}".format(d, STs))

    print("Hence the action of {} on gamma_2 is given by".format(x))
    print_action_on_gamma_2(STs)
    print("And the action of {} on zeta_{} is given by".format(x, N))
    print("  zeta_{} ]--> zeta_{}^{}".format(N, N, d))



print("=============================================================")
print()
print("=============================================================")
print("============= Computing the minimal polynomial ==============")
CC = ComplexField(prec=prec)
conjugates = [] # In this list we will collect the conjugates of our class invariant
Cl = ray_class_group(K, Modulus(K.ideal(_sage_const_1 ))) # i.e. the ideal class group of K
for ideal_class in Cl:
    print("=============================================================")
    print("Found class of the ideal {}".format(ideal_class.ideal()))

    v = J(ideal_class)
    print("Corresponding idèle v is:\n{}".format(v))

    B, A = factored_shimura_connecting_homomorphism(v, output_prec=_sage_const_3 )
    print("Factorization g_theta(v) = B*A is given by:\n{}\n*\n{}".format(B, A))

    B_N = matrix_modulo(B, N)
    d = det(B_N).lift()
    U = diagonal_matrix([_sage_const_1 , _sage_const_1 /det(B_N)]) * B_N
    B_N_lift = SL2Z(lift_matrix_to_sl2z(U.list(), N))
    V = B_N_lift * A
    print("Hence this ideal class acts on QQ(zeta_{}) by {}".format(N, d))
    print("and with a fractional linear transformation given by\n{}".format(V))

    tau = apply_fractional_linear_transformation(V, theta)
    conjugate = CC.zeta(N)**d * gamma_2(tau, prec)
    conjugates.append(conjugate)
    print("The corresponing conjugate of our class invariant is approximately\n{}".format(conjugate))

print("=============================================================")
print("================ Recognizing the polynomial =================")
print("=============================================================")
R = PolynomialRing(CC, names=('Y',)); (Y,) = R._first_ngens(1)
approx_polynomial = prod([Y - conjugate for conjugate in conjugates])
coefficients = [round(c.real()) + round(c.imag())*I for c in approx_polynomial.coefficients()]
R = PolynomialRing(ZZ, names=('X',)); (X,) = R._first_ngens(1)
try:
    f = R(coefficients)
    print("Hilbert class polynomial:")
    print(f)
except TypeError:
    raise ValueError("Precision of our numerical complex computations ({} bits) is too low!".format(CF.prec()))

