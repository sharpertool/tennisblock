

class Player:

    def __init__(self, p=None):
        self._id = None
        self._gender = None
        self._ntrp = 2.5
        self._microntrp = 2.5
        self._phone = None
        self._name = None

        if p:
            self._id = p.pk
            self._gender = p.gender
            self._ntrp = p.ntrp
            self._microntrp = p.microntrp
            self._phone = p.phone
            self._name = p.Name()

    @property
    def gender(self):
        return self._gender

    @property
    def Name(self):
        return self._name

    @property
    def ntrp(self):
        return self._ntrp

    @property
    def microntrp(self):
        return self._ntrp


