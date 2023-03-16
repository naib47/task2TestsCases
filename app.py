import numpy as np
import math
from fractions import Fraction
from flask import Flask, render_template
# create an API
app = Flask(__name__)


def solution(m):
    if len(m) < 2:
        return [1, 1]

    # Split the matrix into R and Q submatrices
    absorbing = set()
    for row_i in range(len(m)):
        if sum(m[row_i]) == 0:
            absorbing.add(row_i)
    r_subm = []
    q_subm = []
    for row_i in range(len(m)):
        if row_i not in absorbing:
            row_total = float(sum(m[row_i]))
            r_temp = []
            q_temp = []
            for col_i in range(len(m[row_i])):
                if col_i in absorbing:
                    r_temp.append(m[row_i][col_i] / row_total)
                else:
                    q_temp.append(m[row_i][col_i] / row_total)
            r_subm.append(r_temp)
            q_subm.append(q_temp)

    # Calculate the fundamental matrix F
    f_subm = np.linalg.inv(np.subtract(np.identity(len(q_subm)), q_subm))

    # Calculate the expected number of steps using F and R
    fr_subm = np.dot(f_subm, r_subm)
    return dec_to_frac_with_lcm(fr_subm[0])


def dec_to_frac_with_lcm(l):
    ret_arr = []
    denoms = []
    for num in l:
        frac = Fraction(num).limit_denominator()
        ret_arr.append(frac.numerator)
        denoms.append(frac.denominator)
    lcd = 1
    for denom in denoms:
        lcd = lcm(lcd, denom)
    for num_i in range(len(ret_arr)):
        ret_arr[num_i] *= int(lcd / denoms[num_i])
    ret_arr.append(lcd)
    return ret_arr


def lcm(a, b):
    return abs(a * b) // math.gcd(a, b)


@app.route('/')
def index():
    m = np.array([[0, 1, 0, 0, 0, 1],
                  [4, 0, 0, 3, 2, 0],
                  [0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0]])
    expected_steps = solution(m)
    return render_template('index.html', expected_steps=expected_steps)


# apI Calling
if __name__ == '__main__':
    app.run(debug=True)
