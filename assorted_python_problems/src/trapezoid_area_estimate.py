"""
Estimate the area of a curve given two arrays of X and Y coordinates of
points on the curve.
"""


def trapezoid_area(base1: float, base2: float, height: float) -> float:
    return (base1 + base2) * height / 2


def solution(X, Y):
    """
    https://www.cuemath.com/trapezoidal-rule-formula/
    Area = (h/2) [y0 + 2 (y1 + y2 + y3 + ..... + yn-1) + yn]
    ^ above case is for equally spaced trapezoids
    """
    if not X or not Y or len(X) != len(Y):
        raise ValueError(f"Wrong inputs!\n{X}\n{Y}")
    area = 0
    x0, y0 = X[0], Y[0]
    for x1, y1 in zip(X[1:], Y[1:]):
        # the trapezoid is laid out vertically and has height x1-x0, with the
        # two bases being y0 and y1
        area += trapezoid_area(y0, y1, x1 - x0)
        x0 = x1
        y0 = y1
    return round(area, 9)


assert solution([0, 1], [0, 1]) == 0.5, "simple case"
# note the original problem statement was rambling about ROC curves and AUROC
# saying X and Y were guaranteed to start with 0, end with 1, and be
# monotonic increasing. I decided to ignore all that and just provide a more
# generic solution that works regardless
assert solution([0, 2], [1, 5]) == 6, "another one interval case"
assert (
    solution(
        [0.00, 0.2, 0.33, 0.43, 0.63, 0.66, 1.00],
        [0.00, 0.25, 0.25, 0.50, 0.50, 1.00, 1.00],
    )
    == 0.5575
), "From problem statement"
