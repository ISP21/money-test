## Tests of Money class

`bigmoney_test.py` - unit tests I used to score student work.

`doctests.py` - some doctests in a file by themselves. I didn't use this.


## Common Mistakes

### Assigning a value directly to `currency` in constructor

Incorrect:
```python
def __init__(self, value, currency='Baht'):
    self._value = value
    self.currency = currency
```

We want `currency` to be a read-only property, so that a money object
cannot be changed.  If you write `self.currency = currency` then it
creates a (read/write) attribute named `currency`.

You cannot have an attribute and a property with the same name (`self.currency`).     
The solution is to prefix the attribute name with underscore or double-underscore.

Correct:
```python
def __init__(self, value, currency='Baht'):
    self._value = value
    self._currency = currency
```
and write a `@property` for `currency`.


### Writing 'setter' properties for value and currency

Money should be *immutable*.  The assignment stated to write **only** 'getter'
properties.

```python
# CORRECT
@property
def currency(self):
    """The currency of this money object."""
    return self._currency

# WRONG - should not be able to change the currency of Money!
@currency.setter
def currency(self, new_currency):
    self._currency = new_currency

# If you wrote this, I want to change 1,000 Baht into 1,000 Dollars, please.
```

### `__add__` returns a number instead of Money

```python
    def __add__(self, money):
        """Add two money objects and return result as a new Money object."""
        if self.currency == money.currency:
            return self.value + money.value
        else:
            return False
```

There are 2 errors in this code:

1. returns a number instead of Money (the docstring even tells you this!)
2. returns False instead of raising ValueError

should be:
```python
    def __add__(self, money):
        """Add two money objects and return result as a new Money object."""
        if self.currency == money.currency:
            return Money(self.value + money.value, self.currency)
        raise ValueError("Cannot add money with different currencies.")
```

### Code Improvement: don't write useless 'if' statements

Whenever you see code like this:

```python
    if some_expression:
        return True
    else:
        return False
```
you can eliminate the `if` statement and simply write:
```python
    return some_expression
```

Here's an example from Money:
```python
def __eq__(self, other):
    """Money objects are equal if they have the same value AND same currency."""
    if not isinstance(other, Money):
        return False
    if self.value == other.value and self.currency == other.currency:
        return True
    return False
```

simplify to:
```python
def __eq__(self, other):
    """Money objects are equal if they have the same value AND same currency."""
    if not isinstance(other, Money):
        return False
    return self.value == other.value and self.currency == other.currency
```

Special case: in Python you can use *non-boolean* values in an `if` statement,
such as:
```python
    name = input("what is your name? ")
    if name:
        return True   # person input a name
    else:
        return False  # empty string
```
in that case, you'd need to rewrite it as a boolean expression.

### Testing the value instead of always using "," format option

In `__str__` some students wrote code like this:
```python
    if self._value < 1000:
       return f"{self._value:.0f} {self.currency}"
    else:
       # use ',' in value
       return f"{self._value:,.0f} {self.currency}"
```

this is not necessary. 

**Think:** Would the Python designers require the programmer to *test* the value before using the ',' format?  That would make printing a table of numbers very complicated!  We would need to test every value and choose a format.

Let's see how the ',' format option behaves:

```python
>>> x = 5.0
>>> print(f"{x:,.0f}")
5
>>> x = 999
>>> print(f"{x:,.0f}")
999
>>> x = 1000
>>> print(f"{x:,.0f}")
1,000
>>> x = 1234567890
>>> print(f"{x:,.0f}")
1,234,567,890
```

The formatter always does the right thing.

But be careful of this: it *rounds values* instead of *truncating*:

```python
>>> x = 999.99
>>> print(f"{x:,.2f}")
999.99
>>> x = 999.996
>>> print(f"{x:,.2f}")
1,000.00
```
This is usually what you want, but not always.
