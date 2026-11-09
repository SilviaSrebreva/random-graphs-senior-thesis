from biased_coin import biased_coin_flip


# SECONDARY

def test_bias_0_always_false():
    for i in range(1000):
        assert biased_coin_flip(0) == False


def test_bias_1_always_true():
    for i in range(1000):
        assert biased_coin_flip(1) == True
