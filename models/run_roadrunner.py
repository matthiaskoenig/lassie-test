"""
Simulate LASSIE example model with libroadrunner.

See https://github.com/aresio/LASSIE
and 


"""

from __future__ import absolute_import, print_function, division
import time
import roadrunner
import pandas as pd
from six import iteritems


if __name__ == "__main__":
    model_file = "./copasi_test_4096x4096.xml"

    # timepoints = [10, 50, 100, 500, 1000]  # called samples in LASSIE
    timepoints = [20, 100]  # LSODA ~250[s], LASSIE ~17.4 [s], roadrunner ???
    tmax = 9.06
    abs_tol = 1E-12
    rel_tol = 1E-6

    # load model
    print('Load model:', model_file, '\n')
    t_start = time.time()
    r = roadrunner.RoadRunner(model_file)
    t_load = time.time() - t_start
    print('loading: {:3.2f} [s]'.format(t_load))

    # set the tolerances
    r.setIntegratorSetting('cvode', 'absolute_tolerance', abs_tol)
    r.setIntegratorSetting('cvode', 'relative_tolerance', rel_tol)
    # print(r)

    timings = []
    for Nt in timepoints:
        # reset model before simulation
        r.reset()

        # time the simulation
        print('Start simulation: Nt={}'.format(Nt))
        t_start = time.time()
        s = r.simulate(start=0, end=tmax, steps=Nt)
        t_duration = time.time() - t_start
        timings.append(t_duration)


        df = pd.DataFrame(data=s, columns=r.timeCourseSelections)
        df.to_csv('./test_{}.tsv'.format(Nt), sep="\t")

        print('-'*80)
        print('{}, samples={}, duration={:3.2f} [s]'.format(model_file, Nt, t_duration))
        print('-'*80)

    for Nt, t in iteritems(dict(zip(timepoints, timings))):
        print('{} : {:3.2f}'.format(Nt, t))
