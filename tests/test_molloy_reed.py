from molloy_reed import molloy_reed_criterion, critical_fraction


# PRIMARY

def test_critical_fraction_kappa_at_most_2():
    # kappa <= 2 means no giant component, so there is nothing to remove
    assert critical_fraction(2) == 0
    assert critical_fraction(1.5) == 0


# SECONDARY

def test_critical_fraction_kappa_1():
    # with kappa = 1 the formula would divide by zero, the if should catch it first
    assert critical_fraction(1) == 0


def test_molloy_reed_empty_raises():
    try:
        molloy_reed_criterion([])
        assert False, "should have raised ValueError"
    except ValueError:
        pass
