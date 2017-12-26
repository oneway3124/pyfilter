from pyfilter.timeseries import EulerMaruyma, Observable, StateSpaceModel
from pyfilter.filters import Linearized, NESS, NESSMC2, APF, UKF
from pyfilter.distributions.continuous import MultivariateNormal, Normal
import numpy as np
from pyfilter.utils.utils import dot
import pandas as pd
import matplotlib.pyplot as plt
from time import time


def finit(s, r, b):
    return [-5.91652, -5.52332, 24.5723]


def ginit(s, r, b):
    return np.sqrt(10) * np.eye(3)


def f(x, s, r, b):
    x1 = -s * (x[0] - x[1])
    x2 = r * x[0] - x[1] - x[0] * x[2]
    x3 = x[0] * x[1] - b * x[2]

    return x1, x2, x3


def g(x, s, r, b):
    return np.eye(3)


def alpha(x, ko):
    mat = np.zeros((2, x.shape[0]))
    mat[0, 0] = mat[1, 2] = ko

    return dot(mat, x)


def beta(x, ko):
    return np.eye(2) / np.sqrt(10)


if __name__ == '__main__':
    dt = 1e-2
    mvn3 = MultivariateNormal(ndim=3)
    hidden = EulerMaruyma((finit, ginit), (f, g), (10, 28, 8/3), (mvn3, mvn3), dt=dt)
    obs = Observable((alpha, beta), (0.8,), MultivariateNormal(ndim=2))

    ssm = StateSpaceModel(hidden, obs)

    x, y = ssm.sample(1500)

    fig, ax = plt.subplots(2)

    ax[0].plot(x)
    ax[1].plot(y)

    hidden = EulerMaruyma((finit, ginit), (f, g), (Normal(15, 6), Normal(20, 10), Normal(4, 2)), (mvn3, mvn3), dt=dt)
    ssm = StateSpaceModel(hidden, obs)

    start = time()
    ness = NESS(ssm, (1000,), filt=UKF).longfilter(y)
    print(time() - start)

    ax[0].plot(ness.filtermeans())

    fig, ax = plt.subplots(3)

    for i, p in enumerate(ness._model.hidden.theta):
        pd.DataFrame(p).plot(kind='kde', ax=ax[i])

    plt.show()

