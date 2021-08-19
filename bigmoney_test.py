"""
Tests of Money class using pytest.
To run:  python3 -m pytest bigmoney_test.py
"""
import pytest
from money import Money


def test_init():
    """Test the constructor."""
    m = Money(10.5)  # use default currency
    assert m._value == 10.5
    assert m._currency == "Baht"
    m = Money(1, "USD")
    assert m._value == 1
    assert m._currency == "USD"

def test_currency_property():
    """Money should have properties for currency and value.

    Since the value property was given, only test currency."""
    m = Money(5.0)  # use default currency
    #assert m.value == 5.0
    assert m.currency == "Baht"
    # explicit currency
    m = Money(10, "Bananas")
    #assert m.value == 10
    assert m.currency == "Bananas"
    # property should be read-only
    with pytest.raises(AttributeError):
        m.currency = "Ringgit"

def test_str_int():
    """String form should print value as int if no fractional value."""
    m = Money(12, "BTC")
    assert str(m) == "12 BTC"

def test_str_float():
    """String form has exactly 2 decimal digits if value is not int."""
    m = Money(1.2, "Dogecoin")
    assert str(m) == "1.20 Dogecoin"
    m = Money(1.2345, "Ether")
    assert str(m) == "1.23 Ether"

def test_str_has_comma():
    """Values 1000 or larger should include comma."""
    m = Money(999, "Doge")
    assert str(m) == "999 Doge"
    m = Money(1000, "Doge")
    assert str(m) == "1,000 Doge"
    m = Money(12345678, "Ether")
    assert str(m) == "12,345,678 Ether"

def test_eq():
    """Money is equal only if value and currency are same."""
    m1 = Money(3, "Baht")
    m2 = Money(3.1, "Baht")
    assert not m1 == m2
    m2 = Money(3, "Baht")
    assert m1 == m2
    m2 = Money(3, "Bath")
    assert not m1 == m2
    # should not change the args
    assert m1.value == 3 and m1.currency == "Baht", "should not modify args"
    assert m2.value == 3 and m2.currency == "Bath", "should not modify args"
    # edge case
    z1 = Money(0)
    z2 = Money(0)
    assert z1 == z2
    # trivial case
    assert m1 == m1

def test_add():
    """Add money objects with same currency."""
    m1 = Money(3, "Baht")
    m2 = Money(5, "Baht")
    m  = m1 + m2
    assert m.value == 8
    assert m.currency == "Baht"
    assert m1.value == 3, "Add should not modify the arguments"
    assert m2.value == 5, "Add should not modify the arguments"

def test_add_different_currency():
    """Add money with different currency should raise exception."""
    m1 = Money(3, "Baht")
    m2 = Money(5, "Bird")
    with pytest.raises(ValueError):
        m = m1 + m2

def test_greater_than():
    """Test that m1 > m2 orders Money by currency, then by value."""
    m1 = Money(3, "Baht")
    m2 = Money(4, "Baht")
    m3 = Money(3, "Dollar")
    assert not m1 > m1
    assert not m1 > m2
    assert m2 > m1
    assert m3 > m1, "Dollar is after Baht, compare currency first"
    assert m3 > m2, "should compare currency first"
    assert not m2 > m3
   
# This test is disabled, but you might want to write __ge__ and enable it.
def optional_test_greater_equal():
    """Test that m1 >= m2 works.  Implement __ge__ in Money."""
    m1 = Money(3, "Baht")
    m2 = Money(4, "Baht")
    m3 = Money(3, "Bat")
    assert m1 >= m1
    assert not m1 >= m2
    assert m2 >= m1
    assert m3 >= m2

if __name__ == '__main__':
    # this will execute all your *_test.py files, not just this one.
    pytest.main()
