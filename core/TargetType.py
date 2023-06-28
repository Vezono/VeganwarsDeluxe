from enum import Enum


class TargetType:
    def __init__(self, distance=0, team=0, aliveness=1, own=2):
        """
        Filters targets.
        :param distance:  0 - any, 1 - nearby only, 2 - distant only
        :param team:      0 - any, 1 - allies only, 2 - enemies only
        :param aliveness: 0 - any, 1 - alive only, 2 - dead only
        :param own: 0 - any (self included), 1 - self only, 2 - self excluded
        """
        self.distance = distance
        self.team = team
        self.aliveness = aliveness
        self.own = own

    def __str__(self):
        return f"D: {self.distance} | T: {self.team} | A: {self.aliveness} | O: {self.own}"


class Distance(Enum):
    ANY = 0
    NEARBY_ONLY = 1
    DISTANT_ONLY = 2


class Team(Enum):
    ANY = 0
    ALLIES_ONLY = 1
    ENEMIES_ONLY = 2


class Aliveness(Enum):
    ANY = 0
    ALIVE_ONLY = 1
    DEAD_ONLY = 2


class Own(Enum):
    ANY = 0
    SELF_ONLY = 1
    SELF_EXCLUDED = 2


class Allies(TargetType):
    def __init__(self, distance=0, aliveness=1):
        super().__init__(distance=distance, team=1, aliveness=aliveness, own=0)


class Enemies(TargetType):
    def __init__(self, distance=0, aliveness=1):
        super().__init__(distance=distance, team=2, aliveness=aliveness, own=2)


class Everyone(TargetType):
    def __init__(self, distance=0, aliveness=1):
        super().__init__(distance=distance, team=0, aliveness=aliveness, own=0)


class OwnOnly(TargetType):
    def __init__(self):
        super().__init__(distance=0, team=0, aliveness=1, own=1)
