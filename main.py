import matplotlib.pyplot as plt


class Verts:
    def __init__(self, filename):
        self.arr = []
        self.matrix = []

        self.create(filename)
        self.make_matrix()

    def create(self, filename):
        with open(filename, 'r') as file:
            for line in file:
                num1, num2 = map(int, line.strip().split(';'))
                self.make_verts(num1, num2)

    def add_vert(self, vert):
        self.arr.append(vert)

    def find_vert(self, value):
        for index, vert in enumerate(self.arr):
            if vert.value == value:
                return index
        return -1

    def make_verts(self, num1, num2):
        vertIdx = self.find_vert(num1)
        if vertIdx == -1:
            self.add_vert(Vert(num1))
            self.arr[len(self.arr)-1].add_neighbor(num2)
        else:
            self.arr[vertIdx].add_neighbor(num2)

        vertIdx = self.find_vert(num2)
        if vertIdx == -1:
            self.add_vert(Vert(num2))
            self.arr[len(self.arr)-1].add_neighbor(num1)
        else:
            self.arr[vertIdx].add_neighbor(num1)

    def make_matrix(self):
        for vert in self.arr:
            tmp = []
            for i in range(0, len(self.arr)):
                if i in vert.neighbors:
                    tmp.append(1)
                else:
                    tmp.append(0)
            self.matrix.append(tmp)

    def print_matrix(self):
        for row in self.matrix:
            print(row)

    def print(self):
        for a in self.arr:
            print(a)


class Vert:
    def __init__(self, value):
        self.value = value
        self.neighbors = []

    def __str__(self):
        return "value = {}, neigh => {}".format(self.value, self.neighbors)

    def add_neighbor(self, neighbor):
        self.neighbors.append(neighbor)


def main():
    filename = 'KarateClub.csv'
    verts = Verts(filename)

    verts.print()
    verts.print_matrix()
    min_vert = min(len(vert.neighbors) for vert in verts.arr)
    max_vert = max(len(vert.neighbors) for vert in verts.arr)
    print("Min stupeň: {}".format(min_vert))

    print("Max stupeň: {}".format(max_vert))

    total_deg = sum(len(vert.neighbors) for vert in verts.arr)
    avg_deg = total_deg / len(verts.arr)
    print("Priemerný stupeň: {}".format(avg_deg))

    cetnost = [0] * (max_vert + 1)
    for vert in verts.arr:
        cnt = len(vert.neighbors)
        cetnost[cnt] = cetnost[cnt] + 1

    rel_cetnost = [round(x / len(verts.arr), 3) for x in cetnost]

    print("Cetnosti sú : {}".format(cetnost))
    print("Relativne cetnosti sú : {}".format(rel_cetnost))

    os_x = [i for i in range(0, max_vert+1)]
    plt.bar(os_x, cetnost)

    plt.axvline(avg_deg, color="red")
    plt.title('Cetnosti')
    plt.xlabel('Stupen')
    plt.ylabel('Pocet')
    plt.show()


if __name__ == "__main__":
    main()
