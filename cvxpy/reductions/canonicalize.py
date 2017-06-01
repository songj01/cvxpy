"""
Copyright 2013 Steven Diamond, 2017 Robin Verschueren

This file is part of CVXPY.

CVXPY is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

CVXPY is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with CVXPY.  If not, see <http://www.gnu.org/licenses/>.
"""

from cvxpy.atoms.affine.add_expr import AddExpression
from cvxpy.expressions.constants import Constant
from cvxpy.expressions.variables import Variable


# TODO this assumes all possible constraint sets are cones:
def canonicalize_constr(constr, canon_methods):
    arg_exprs = []
    constrs = []
    for a in constr.args:
        e, c = canonicalize_tree(a, canon_methods)
        constrs += c
        arg_exprs += [e]
    # Feed the linear expressions into a constraint of the same type (assumed a cone):
    constr = type(constr)(*arg_exprs)
    return constr, constrs


def canonicalize_tree(expr, canon_methods):
    canon_args = []
    constrs = []
    for arg in expr.args:
        canon_arg, c = canonicalize_tree(arg, canon_methods)
        canon_args += [canon_arg]
        constrs += c
    canon_expr, c = canonicalize_expr(expr, canon_args, canon_methods)
    constrs += c
    return canon_expr, constrs


def canonicalize_expr(expr, args, canon_methods):
    if isinstance(expr, Variable):
        return expr, []
    elif isinstance(expr, Constant):
        return expr, []
    elif expr.is_atom_convex() and expr.is_atom_concave():
        if isinstance(expr, AddExpression):
            expr = type(expr)(args)
        else:
            expr = type(expr)(*args)
        return expr, []
    else:
        return canon_methods[type(expr)](expr, args)
