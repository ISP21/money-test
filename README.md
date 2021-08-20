## Tests of Money class

`bigmoney_test.py` - unit tests I used to score student work.

`doctests.py` - some doctests in a file by themselves. I didn't use this.


## Common Errors

### 1. Assigning a value directly to `currency` in constructor

Incorrect:
```python
def __init__(self, value, currency='Baht'):
    self._value = value
    self.currency = currency
```

We want `currency` to be a read-only property, so that a money object
cannot be changed.  If you write `self.currency = currency` then you are creating a publicly modifiable attribute named `currency`.

You cannot have an attribute and a property with the same name (`self.currency`).     

The solution is to prefix the attribute name with underscore or double-underscore.

Correct:
```python
def __init__(self, value, currency='Baht'):
    self._value = value
    self._currency = currency
```
and write a `@property` for `currency`.


### 2. Writing 'setter' properties for value and currency

Money should be *immutable*.  You should write **only** 'getter' properties, **not** 'setter' properties.  The assignment stated this.

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

### 3. `__add__` returns a number instead of Money

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

### 4. Method Returns Inconsistent Data Type or Nothing at All

A method should always return the same type of value, or always return nothing.
(An exception is polymorphic methods that *by design* return different types based on context, such as `max`.)
You should not write a method that sometimes returns a value and other times returns nothing.  

The `__add__` method above is example of this.

Python is very tolerant of this; as a result it won't warn you of
programming errors.  To find possible errors, run a "linter" such as `pylint` 
or `flake8` (flake8 also does static type checking).
The checking is even better if you also use *type hints* 
(to be covered in this course).

### 5. Testing the value instead of always using "," format option

In `__str__` some students wrote code like this:
```python
    if self._value < 1000:
       return f"{self._value:.0f} {self.currency}"
    else:
       # use ',' in value
       return f"{self._value:,.0f} {self.currency}"
```

this is not necessary. 

**Think:** Would the Python designers require the programmer to *test* the value before using the ',' format option?  That would make printing a table of numbers very complicated!  We would need to test every value and choose a format.

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

But be aware of this: it *rounds values* instead of *truncating*.    
This is usually what you want, but not always.

```python
>>> x = 999.992
>>> print(f"{x:,.2f}")
999.99
>>> x = 999.996
>>> print(f"{x:,.2f}")
1,000.00
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

Here is an example from Money:

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
in that case, you need to rewrite it as a boolean expression, such as:
```python
   return name.strip() != ""
```

### Fundamentals Everyone Should Know Already

These are things that everyone **should know after Programming 2**.

* Purpose of a constructor and how to write one.
* Good encapsulation gives us freedom to change the implementation of a class without effecting other code, and avoids errors.
  - Prefer **private** attributes.  
  - Python doesn't enforce private attributes, but has a *convention* that variable names beginning with underscore or double-underscore should be treated as private.
  - Provide read access to attributes by writing a "getter" property.
  - Provide modify access ("setter" property) only when truly necessary.
* How to write a good equals (`__eq__`) method:
  ```python
  def __eq__(self, other) -> bool:
     """Two objects are equal if they have same type and same [specify what]"""
     if not isinstance(other, self.__class__):
         return False
     # now compare objects in whatever way makes sense for this class
     return self.value == other.value and self.currency == other.currency
  ```
* How to write `__str__` and `__repr__`, and the difference between them.
* How to write common "magic methods" such as `__gt__` and `__len__`.
  - When Python sees `len(x)` in code it invokes `x.__len__()`, when it sees `a > b` it invokes `a.__gt__(b)`, etc.
* Know the difference between **instance methods** and **class methods**.
  - **Instance methods** are behavior that is performed by an object.  An instance method has a `self` attribute that provides access to an object's members.
  - **Class methods** are behavior provided by the class. A class method has access to class attributes, but not instance attributes. A class method has a `cls` attribute that refers to the class.
  - **Static methods** are functions that are written inside a class, but do not have access to either class or instance members.
  - Use the annotations `@classmethod` and `@staticmethod` to indicate those methods.
* The meaning of inheritance, how to use it, and when to use it.
