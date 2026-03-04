# Fully Homomorphic Encryption 

This is an attempt at building a library to emulate implementation of math functions within a fully homomorphic encryption system.

These scripts are written in Python and heavily reliant on the numpy library. You don't need to know what that means or have formally learned Python to contribute, although programming familiarity may help. 

Note: for the remainder of this document, "ciphertext" may be abbreviated as "ct"

## The Primitive Moves 

These are the four core functions that we assume work within our system. 

```python
ctc = cta + ctb      # element-wise addition
ctab = cta * ctb     # element-wise multiplication
np.roll(ct,k)        # shift the elements in ct by k indeces with wraparound
np.conjugate(ct)     # complex conjugation of each element in ct
```

Simply replace ct* with the desired ciphertext variables to operate on (and k with an integer). 

See [internal document?] for more details.

## Quickstart Guide for Limited Programming Background

To create a new function, use roughly the following format:

```python
def function_name(user_ct):
    local_ct = np.copy(user_ct)
    # sequence of primitive moves (and helper functions)
    return local_ct 
```

"function_name" is the name of your function. Be descriptive of what you're trying to achieve! 
"user_ct" is the ciphertext provided by the user, or you when you call the function elsewhere.
"local_ct" is a new ciphertext to be used within the function. In this case, local_ct is a copy of user_ct.
"\#" marks the start of a comment (code that won't get executed).
"return" ends the function and returns what follows to where the function was called. 

If developing a function within a separate .py file, include the following line at the top of the file to use the functions within fhe_lib: 

```python
import fhe_lib as fhel
```

To use a function from fhe_lib in a separate .py file, call it like so:

```python
fhel.sum(cta, ctb)
```

## License 

TBD