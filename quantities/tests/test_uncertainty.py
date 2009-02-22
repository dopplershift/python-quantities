# -*- coding: utf-8 -*-

import unittest

from nose.tools import *
from numpy.testing import *
from numpy.testing.utils import *

import numpy as np
import quantities as q


def test_uncertainquantity_creation():
    a = q.UncertainQuantity(1, q.m)
    assert_equal(str(a), '1.0 m\n±0.0 m (1σ)')
    a = q.UncertainQuantity([1, 1, 1], q.m)
    assert_equal(str(a), '[ 1.  1.  1.] m\n±[ 0.  0.  0.] m (1σ)')
    a = q.UncertainQuantity(a)
    assert_equal(str(a), '[ 1.  1.  1.] m\n±[ 0.  0.  0.] m (1σ)')
    a = q.UncertainQuantity([1, 1, 1], q.m, [.1, .1, .1])
    assert_equal(str(a), '[ 1.  1.  1.] m\n±[ 0.1  0.1  0.1] m (1σ)')
    assert_raises(ValueError, q.UncertainQuantity, [1, 1, 1], q.m, 1)
    assert_raises(ValueError, q.UncertainQuantity, [1, 1, 1], q.m, [1, 1])

def test_uncertainquantity_rescale():
    a = q.UncertainQuantity([1, 1, 1], q.m, [.1, .1, .1])
    b = a.rescale(q.ft)
    assert_equal(
        str(b),
        '[ 3.2808399  3.2808399  3.2808399] ft'
        '\n±[ 0.32808399  0.32808399  0.32808399] ft (1σ)'
    )

def test_uncertainquantity_simplified():
    a = 1000*q.constants.electron_volt
    assert_equal(
        str(a.simplified),
        '1.602176487e-16 kg·m²/s²\n±4e-24 kg·m²/s² (1σ)'
    )

def test_uncertainquantity_set_uncertainty():
    a = q.UncertainQuantity([1, 2], 'm', [.1, .2])
    assert_equal(
        str(a),
        '[ 1.  2.] m\n±[ 0.1  0.2] m (1σ)'
    )
    a.uncertainty = [1., 2.]
    assert_equal(
        str(a),
        '[ 1.  2.] m\n±[ 1.  2.] m (1σ)'
    )
    def set_u(q, u):
        q.uncertainty = u
    assert_raises(ValueError, set_u, a, 1)

def test_uncertainquantity_multiply():
    a = q.UncertainQuantity([1, 2], 'm', [.1, .2])
    assert_equal(
        str(a*a),
        '[ 1.  4.] m²\n±[ 0.14142136  0.56568542] m² (1σ)'
    )
    assert_equal(
        str(a*2),
        '[ 2.  4.] m\n±[ 0.2  0.4] m (1σ)'
    )

def test_uncertainquantity_divide():
    a = q.UncertainQuantity([1, 2], 'm', [.1, .2])
    assert_equal(
        str(a/a),
        '[ 1.  1.] dimensionless\n±[ 0.14142136  0.14142136] '
        'dimensionless (1σ)'
    )
    assert_equal(
        str(a/2),
        '[ 0.5  1. ] m\n±[ 0.05  0.1 ] m (1σ)'
    )
