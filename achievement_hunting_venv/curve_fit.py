import numpy as np
from scipy import optimize


def logit_curve_fit(
    xy_values: list[list[float]],
) -> tuple[list[float], list[float], list[float]]:
    def logit(x: float, a: float, b: float, c: float, d: float, g: float) -> float:
        return d + ((a - d) / ((1 + ((x / c) ** b)) ** g))

    ach_constants = optimize.curve_fit(
        logit,
        xy_values[0],
        xy_values[1],
        p0=(0.1, 2.0, 50.0, 1.0, 4000.0),
        bounds=(0.0, [1.0, np.inf, np.inf, 1.0, np.inf]),
        method="trf",
    )

    ta_constants = optimize.curve_fit(
        logit,
        xy_values[0],
        xy_values[2],
        p0=(0.1, 2.0, 50.0, 1.0, 4000.0),
        bounds=(0.0, [1.0, np.inf, np.inf, 1.0, np.inf]),
        method="trf",
    )

    gs_constants = optimize.curve_fit(
        logit,
        xy_values[0],
        xy_values[3],
        p0=(0.1, 2.0, 50.0, 1.0, 4000.0),
        bounds=(0.0, [1.0, np.inf, np.inf, 1.0, np.inf]),
        method="trf",
    )

    return ach_constants[0], ta_constants[0], gs_constants[0]
