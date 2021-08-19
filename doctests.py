# Additional doctest for money.py
# I did not use these in scoring the student submissions.

def runtests():
    """
    Doctests for money, as a separate file.
    
    Examples:
    >>> from money import Money
    >>> m = Money(1000)
    >>> m.value
    1000
    >>> m.currency
    'Baht'
    >>> str(m)            # don't print decimal part if value is an integer
    '1,000 Baht'
    >>> m2 = Money(1000)
    >>> m == m2
    True
    >>> m2 = Money(100)
    >>> m == m2
    False
    >>> sum = m + m2
    >>> str(sum)
    '1,100 Baht'
    >>> m > m2
    True
    >>> m2 > m
    False
    >>> m3 = Money(101, "AUD")
    >>> m3 > m2
    False
    >>> d = Money(0.5, "USD")
    >>> str(d)                # value is not integer, so print 2 decimal digits
    '0.50 USD'
    >>> str(d + d)            # value is 1.0. value is integer but float datatype 
    '1 USD'
    >>> d2 = Money(100, 'USD')
    >>> m2 == d2              # value is same but currencies are different
    False
    """
    pass

if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=1)
