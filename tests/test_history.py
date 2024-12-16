from history.tracker import History

def test_add_entry():
    history = History()
    history.add_entry("Add 2 and 3", 5)
    assert history.get_all() == ["Add 2 and 3 = 5"]

def test_get_all():
    history = History()
    history.add_entry("Multiply 4 and 5", 20)
    history.add_entry("Divide 10 by 2", 5)
    assert history.get_all() == ["Multiply 4 and 5 = 20", "Divide 10 by 2 = 5"]
