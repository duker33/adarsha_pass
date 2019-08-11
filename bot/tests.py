from bot import Guest


def test_guest_assembles_fio():
    guest = Guest('Ivanoff', 'Ivan', 'Ivanovich')
    assert guest.fio == 'Ivanoff Ivan Ivanovich'
