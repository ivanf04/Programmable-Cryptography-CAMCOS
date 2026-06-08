# Programmable-Cryptography-CAMCOS
This is a library to emulate implementation of math functions within a fully homomorphic encryption system.

These scripts are written in Python and heavily reliant on the numpy library. You don't need to know what that means or have formally learned Python to contribute, although programming familiarity may help. 

Note: for the remainder of this document, "ciphertext" may be abbreviated as "ct"

## Getting Started

### Dependencies 

* Pyhthon 3.14.3
* numpy 2.4.3

### Getting Started 

* First clone the repository, run:  "git clone https://github.com/ivanf04/Programmable-Cryptography-CAMCOS"
* Next start your virtual environment, from the project directory run:source venv/bin/activate
* Then install dependencies: pip install . 

### Executing Programs 

* Functions are writen in the /src/fhelib directory, test for these functions are found in /test
* Test files names pretain to the specific function they are testing. Simply run the files in your IDE to see test reults in your terminal

## Table of contents 

### Primitives
* [addition](src/fhelib/primitives/add.py)
* [multiplication](src/fhelib/primitives/multiply.py)
* [cycle](src/fhelib/primitives/cycle.py)
* [conjugate](src/fhelib/primitives/conjugate.py)

### Low Level
* [div_newton](src/fhelib/lowlevel/div_newton.py)
* [dot_product](src/fhelib/lowlevel/dot_product.py)
* [factorial](src/fhelib/lowlevel/factorial.py)
* [matrix_multiplication](src/fhelib/lowlevel/matrix_multiplication.py)
* [power](src/fhelib/lowlevel/power.py)
* [realify](src/fhelib/lowlevel/realify.py)
* [sigmoid](src/fhelib/lowlevel/sigmoid.py)
* [sign](src/fhelib/lowlevel/sign.py)
* [sum](src/fhelib/lowlevel/sum.py)
* [tanh](src/fhelib/lowlevel/tanh.py)

### Auxiliary
* [difference](src/fhelib/auxiliary/difference.py)
* [difference_matrix](src/fhelib/auxiliary/difference_matrix.py)
* [equality](src/fhelib/auxiliary/equality.py)
* [exponential](src/fhelib/auxiliary/exponential.py)
* [index_swap](src/fhelib/auxiliary/index_swap.py)
* [max](src/fhelib/auxiliary/max.py)
* [reciprocal_adpt_guess](src/fhelib/auxiliary/reciprocal_adpt_guess.py)
* [reciprocal_univ_guess](src/fhelib/auxiliary/reciprocal_univ_guess.py)
* [softmax](src/fhelib/auxiliary/softmax.py)

### Stats
* [fhe_correlation_coefficient](src/fhelib/stats/fhe_correlation_coefficient.py)
* [fhe_mean](src/fhelib/stats/fhe_mean.py)
* [fhe_median](src/fhelib/stats/fhe_median.py)
* [mode](src/fhelib/stats/mode.py)
* [moment_generator](src/fhelib/stats/moment_generator.py)

## The Base Moves 

These are the four core functions that we assume work within our system. 

```python
cts = cta + ctb      # element-wise addition
ctm = cta * ctb      # element-wise multiplication
np.roll(ct,k)        # shift the elements in ct by k indeces with wraparound
np.conjugate(ct)     # complex conjugation of each element in ct
```

Simply replace ct* with the desired ciphertext variables to operate on (and k with an integer). 

See [internal document?] for more details.


## License 

TBD
