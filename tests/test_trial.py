from home.trymockito import mocker

def answer():
    mocke = mocker()
    re = mocke.func(4)
    assert re == 5