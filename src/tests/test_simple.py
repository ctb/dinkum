import pytest

import dinkum
from dinkum.vfg import Gene
from dinkum.vfn import Tissue
from dinkum import Timecourse
from dinkum import observations


def test_maternal():
    dinkum.reset()

    x = Gene(name='X')
    m = Tissue(name='M')
    x.is_present(where=m, start=1, duration=1)

    # set observations
    observations.check_is_present(gene='X', time=1, tissue='M')
    observations.check_is_not_present(gene='X', time=2, tissue='M')

    # run time course
    dinkum.run(1, 5)


def test_maternal_fail():
    dinkum.reset()

    x = Gene(name='X')
    m = Tissue(name='M')
    x.is_present(where=m, start=1, duration=1)

    # set observations
    observations.check_is_present(gene='X', time=1, tissue='M')
    observations.check_is_present(gene='X', time=2, tissue='M')

    with pytest.raises(dinkum.DinkumObservationFailed):
        dinkum.run(1, 5)


def test_activation():
    dinkum.reset()

    # set it all up!
    x = Gene(name='X')
    y = Gene(name='Y')

    y.activated_by(source=x)
    x.activated_by(source=y)

    m = Tissue(name='M')
    x.is_present(where=m, start=1)

    # set observations
    observations.check_is_present(gene='X', time=1, tissue='M')
    observations.check_is_not_present(gene='Y', time=1, tissue='M')
    observations.check_is_present(gene='X', time=2, tissue='M')
    observations.check_is_present(gene='Y', time=2, tissue='M')

    # run!
    dinkum.run(start=1, stop=5)


def test_simple_repression():
    dinkum.reset()

    # establish preconditions
    observations.check_is_present(gene='X', time=1, tissue='M')
    observations.check_is_not_present(gene='Y', time=1, tissue='M')

    observations.check_is_present(gene='X', time=2, tissue='M')
    observations.check_is_present(gene='Y', time=2, tissue='M')
    observations.check_is_present(gene='Z', time=2, tissue='M')

    observations.check_is_not_present(gene='Z', time=3, tissue='M')

    # set it all up!
    x = Gene(name='X')
    y = Gene(name='Y')
    z = Gene(name='Z')

    y.activated_by(source=x)
    x.activated_by(source=y)

    z.and_not(activator=x, repressor=y)

    m = Tissue(name='M')
    x.is_present(where=m, start=1, duration=1)

    # run!
    dinkum.run(1, 5)


def test_simple_multiple_tissues():
    dinkum.reset()

    ## tissue M
    observations.check_is_present(gene='X', time=1, tissue='M')
    observations.check_is_not_present(gene='Y', time=1, tissue='M')

    observations.check_is_present(gene='X', time=2, tissue='M')
    observations.check_is_present(gene='Y', time=2, tissue='M')
    observations.check_is_present(gene='Z', time=2, tissue='M')

    observations.check_is_not_present(gene='Z', time=3, tissue='M')

    ## tissue N
    observations.check_is_present(gene='Y', time=1, tissue='N')
    observations.check_is_not_present(gene='X', time=1, tissue='N')
    observations.check_is_present(gene='X', time=2, tissue='N')
    observations.check_is_present(gene='Y', time=2, tissue='N')

    # set it all up!

    ## VFG
    x = Gene(name='X')
    y = Gene(name='Y')
    z = Gene(name='Z')

    y.activated_by(source=x)
    x.activated_by(source=y)

    z.and_not(activator=x, repressor=y)

    ## VFN
    m = Tissue(name='M')
    x.is_present(where=m, start=1, duration=1)

    n = Tissue(name='N')
    y.is_present(where=n, start=1, duration=1)

    # run!
    dinkum.run(1, 5)


def test_simple_positive_feedback():
    dinkum.reset()

    # establish preconditions
    observations.check_is_present(gene='X', time=1, tissue='M')
    observations.check_is_not_present(gene='Y', time=1, tissue='M')

    observations.check_is_present(gene='X', time=2, tissue='M')
    observations.check_is_present(gene='Y', time=2, tissue='M')

    observations.check_is_present(gene='X', time=3, tissue='M')
    observations.check_is_present(gene='Y', time=3, tissue='M')

    # set it all up!
    x = Gene(name='X')
    y = Gene(name='Y')

    y.activated_by(source=x)
    x.activated_by(source=y)

    m = Tissue(name='M')
    x.is_present(where=m, start=1, duration=1)

    # run!
    dinkum.run(1, 5)


def test_simple_feed_forward():
    dinkum.reset()

    # establish preconditions
    observations.check_is_present(gene='X', time=1, tissue='M')
    observations.check_is_not_present(gene='Y', time=1, tissue='M')
    observations.check_is_not_present(gene='Z', time=1, tissue='M')

    observations.check_is_present(gene='X', time=2, tissue='M')
    observations.check_is_present(gene='Y', time=2, tissue='M')
    observations.check_is_not_present(gene='Z', time=2, tissue='M')

    observations.check_is_present(gene='X', time=3, tissue='M')
    observations.check_is_present(gene='Y', time=3, tissue='M')
    observations.check_is_present(gene='Z', time=3, tissue='M')

    # set it all up!
    x = Gene(name='X')
    y = Gene(name='Y')
    z = Gene(name='Z')

    y.activated_by(source=x)
    z.activated_by_and(sources=[x, y])

    m = Tissue(name='M')
    x.is_present(where=m, start=1)

    # run!
    dinkum.run(1, 5)


def test_simple_incoherent_feed_forward():
    dinkum.reset()

    # establish preconditions
    observations.check_is_present(gene='X', time=1, tissue='M')
    observations.check_is_not_present(gene='Y', time=1, tissue='M')
    observations.check_is_not_present(gene='Z', time=1, tissue='M')

    observations.check_is_present(gene='X', time=2, tissue='M')
    observations.check_is_present(gene='Y', time=2, tissue='M')
    observations.check_is_present(gene='Z', time=2, tissue='M')

    observations.check_is_present(gene='X', time=3, tissue='M')
    observations.check_is_present(gene='Y', time=3, tissue='M')
    observations.check_is_not_present(gene='Z', time=3, tissue='M')

    observations.check_is_present(gene='X', time=4, tissue='M')
    observations.check_is_present(gene='Y', time=4, tissue='M')
    observations.check_is_not_present(gene='Z', time=4, tissue='M')

    # set it all up!
    x = Gene(name='X')
    y = Gene(name='Y')
    z = Gene(name='Z')

    y.activated_by(source=x)
    z.and_not(activator=x, repressor=y)

    m = Tissue(name='M')
    x.is_present(where=m, start=1)

    # run!
    dinkum.run(1, 5)


def test_simple_incoherent_feed_forward_2_tissues():
    dinkum.reset()

    # establish preconditions
    observations.check_is_not_present(gene='Z', time=1, tissue='M')
    observations.check_is_present(gene='Z', time=2, tissue='M')
    observations.check_is_present(gene='Z', time=3, tissue='M')
    observations.check_is_present(gene='Z', time=4, tissue='M')

    observations.check_is_never_present(gene='Y', tissue='M')

    observations.check_is_not_present(gene='Z', time=1, tissue='N')
    observations.check_is_present(gene='Z', time=2, tissue='N')
    observations.check_is_not_present(gene='Z', time=3, tissue='N')
    observations.check_is_not_present(gene='Z', time=4, tissue='N')

    # set it all up!
    x = Gene(name='X')
    y = Gene(name='Y')
    z = Gene(name='Z')
    s = Gene(name='S')          # switches spec states b/t tissues M and N

    y.activated_by_and(sources=[x, s])
    z.and_not(activator=x, repressor=y)

    m = Tissue(name='M')
    x.is_present(where=m, start=1)

    m = Tissue(name='N')
    x.is_present(where=m, start=1)
    s.is_present(where=m, start=1)

    # run!
    dinkum.run(1, 5)


def test_simple_mutual_repression():
    dinkum.reset()

    # establish preconditions
    observations.check_is_never_present(gene='X', tissue='N')
    observations.check_is_never_present(gene='Y', tissue='M')

    # set it all up!
    x = Gene(name='X')
    y = Gene(name='Y')
    a = Gene(name='A')
    b = Gene(name='B')

    x.and_not(activator=a, repressor=y)
    y.and_not(activator=b, repressor=x)

    m = Tissue(name='M')
    a.is_present(where=m, start=1)

    n = Tissue(name='N')
    b.is_present(where=n, start=1)

    # run!
    dinkum.run(1, 5)


def test_simple_toggle_switch():
    dinkum.reset()

    # establish preconditions
    observations.check_is_not_present(gene='X', tissue='M', time=1)
    observations.check_is_present(gene='X', tissue='M', time=2)

    observations.check_is_never_present(gene='X', tissue='N')

    # set it all up!
    x = Gene(name='X')          # target of toggle switch
    t = Gene(name='T')          # toggle switch t.f.
    cofactor = Gene(name='cofactor')    # janus factor

    x.toggle_repressed(tf=t, cofactor=cofactor)

    # tissue M: t is present, cofactor is not; activate.
    m = Tissue(name='M')
    t.is_present(where=m, start=1)

    # tissue N: t is present, along with cofactor; repress.
    n = Tissue(name='N')
    t.is_present(where=n, start=1)
    cofactor.is_present(where=n, start=1)

    # run!
    dinkum.run(1, 5)
