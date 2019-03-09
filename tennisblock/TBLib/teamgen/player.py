from dataclasses import dataclass


@dataclass
class Player:

    pk: int
    gender: str
    ntrp: float
    microntrp: float
    phone: str
    name: str

    @property
    def Name(self):
        return self.name


