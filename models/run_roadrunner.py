"""
Simulate LASSIE example model with libroadrunner.

See https://github.com/aresio/LASSIE
and 


"""

from __future__ import absolute_import, print_function, division
import time
import roadrunner


if __name__ == "__main__":
    model_file = "./copasi_test_4096x4096.xml"

    # timepoints = [10, 50, 100, 500, 1000]  # called samples in LASSIE
    timepoints = [10]
    tmax = 50
    abs_tol = 1E-12
    rel_tol = 1E-6

    # load model
    print('Load model:', model_file, '\n')
    r = roadrunner.RoadRunner(model_file)

    # set the tolerances
    r.setIntegratorSetting('cvode', 'absolute_tolerance', abs_tol)
    r.setIntegratorSetting('cvode', 'relative_tolerance', rel_tol)
    print(r, '\n')

    timings = []
    for Nt in timepoints:
        # reset model before simulation
        r.reset()

        # time the simulation
        print('Start simulation: Nt={}'.format(Nt))
        t_start = time.time()
        r.simulate(start=0, end=tmax, steps=Nt)
        t_duration = time.time() - t_start
        timings.append(t_duration)

        print('-'*80)
        print('{}, samples={}, duration={} [s]', model_file, Nt, t_duration)
        print('-'*80)

    for Nt, t in dict(zip(timepoints, timings)):
        print('{} : {}', Nt, t)
