class VersionNumber():

    def __init__(self, version_str=None):
        self.numbers = {0: 0, 1: 0, 2: 0}

        if version_str is not None:
            self.from_string(version_str)

    def __str__(self):
        return(f'VersionNumber[{self.to_string(3)}]')

    def from_string(self, version_str):
        parts = version_str.split('.')
        for i in range(3):
            try:
                part = parts[i]
                try:
                    self.numbers[i] = int(part)
                except Whatever:
                    self.numbers[i] = 0
            except IndexError:
                self.numbers[i] = 0

    def to_string(self, lvl=3):
        result = f'{self.numbers[0]}'
        if lvl > 1:
            result += f'.{self.numbers[1]}'
        if lvl > 2:
            result += f'.{self.numbers[2]}'
        return result

    def to_integer(self):
        result = 0
        result += self.numbers[0] * 10000
        result += self.numbers[1] * 100
        result += self.numbers[2]
        return result
    
    def round(self, lvl=1):
        if lvl < 3:
            self.numbers[2] = 0
        if lvl < 2:
            self.numbers[1] = 0

    def __eq__(self, other):
        if not isinstance(other, VersionNumber):
            return False
        return self.to_integer() == other.to_integer()

    def __lt__(self, other):
        return self.to_integer() < other.to_integer()

    def __le__(self, other):
        return self.to_integer() <= other.to_integer()

    def __gt__(self, other):
        return self.to_integer() > other.to_integer()

    def __ge__(self, other):
        return self.to_integer() >= other.to_integer()


if __name__ == '__main__':
    print('Running tests...')
    vn0 = VersionNumber()
    assert str(vn0) == 'VersionNumber[0.0.0]'
    assert vn0.to_integer() == 0

    vn1 = VersionNumber('3.28.01')
    assert str(vn1) == 'VersionNumber[3.28.1]'

    assert vn1.to_string() == '3.28.1'
    assert vn1.to_string(1) == '3'
    assert vn1.to_string(2) == '3.28'
    assert vn1.to_string(3) == '3.28.1'
    assert vn1.to_string(4) == '3.28.1'
    assert vn1.to_integer() == 32801

    vn2 = VersionNumber('3.22.7')
    assert vn1 != vn2
    assert not vn1 == vn2
    assert vn1 > vn2
    assert not vn1 < vn2
    assert vn1 >= vn2
    assert not vn1 <= vn2
    assert not vn2 > vn1
    assert vn2 < vn1
    assert not vn2 >= vn1
    assert vn2 <= vn1

    vn3 = VersionNumber('3.28')

    assert not vn1 == vn3

    vn1.round(2)
    assert vn1.to_string() == '3.28.0'

    assert vn1 == vn3