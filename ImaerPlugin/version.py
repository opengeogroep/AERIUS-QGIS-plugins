class VersionNumber():

    def __init__(self, version_str=None):
        self.numbers = {0: 0, 1: 0, 2: 0}

        if version_str is not None:
            self.from_string(version_str)

    def __str__(self):
        return(f'VersionNumber[{self.numbers[0]}.{self.numbers[1]}.{self.numbers[2]}]')

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

    def to_string(self):
        return(f'{self.numbers[0]}.{self.numbers[1]}.{self.numbers[2]}')

    def to_integer(self):
        result = 0
        result += self.numbers[0] * 10000
        result += self.numbers[1] * 100
        result += self.numbers[2]
        return result

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
    vn = VersionNumber()
    print(vn)
    vn = VersionNumber('3.28.01')
    print(vn)
    print(vn.to_integer())

    vn2 = VersionNumber('3.22.7')
    print(vn != vn2)
    print(vn == vn2)
    print(vn > vn2)
    print(vn < vn2)
    print(vn >= vn2)
    print(vn <= vn2)
    print(vn2 > vn)
    print(vn2 < vn)
    print(vn2 >= vn)
    print(vn2 <= vn)

    vn = VersionNumber('3.28')
    print(vn)