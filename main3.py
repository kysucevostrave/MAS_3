import csv
import matplotlib.pyplot as plt
import networkx as nx

class Verts:
    def __init__(self, filename):
        self.arr = []
        self.edges = []
        self.matrix = []
        self.dist = []
        self.diameter = 0
        self.v_cnt = 0
        self.min_vert = 0
        self.max_vert = 0

        self.create(filename)

    def create(self, filename):
        with open(filename, 'r') as file:
            for line in file:
                num1, num2 = map(int, line.strip().split(';'))
                self.make_vert(num1, num2)
                self.make_vert(num2, num1)
                self.edges.append((num1, num2))
        self.v_cnt = len(self.arr)

        self.arr = sorted(self.arr, key=lambda x: x.value)

        for i in self.arr:
            i.degree = len(i.neighbors)
        self.min_vert = min(len(vert.neighbors) for vert in self.arr)
        self.max_vert = max(len(vert.neighbors) for vert in self.arr)

    def add_vert(self, vert):
        self.arr.append(vert)

    def find_vert(self, value):
        for index, vert in enumerate(self.arr):
            if vert.value == value:
                return index
        return -1

    def make_vert(self, num1, num2):
        vertIdx = self.find_vert(num1)
        if vertIdx == -1:
            self.add_vert(Vert(num1))
            self.arr[self.v_cnt-1].add_neighbor(num2)
        else:
            self.arr[vertIdx].add_neighbor(num2)

    def make_matrix(self):
        for vert in self.arr:
            tmp = []
            for i in range(0, self.v_cnt):
                if i in vert.neighbors:
                    tmp.append(1)
                else:
                    tmp.append(0)
            self.matrix.append(tmp)

    def print_matrix(self):
        for row in self.matrix:
            print(row)

    def make_dist(self):
        v = self.v_cnt

        self.dist = [[]] * v
        for i in range(0, v):
            self.dist[i] = [float("inf")] * v
            self.dist[i][i] = 0

        for vert in self.arr:
            for neigh in vert.neighbors:
                self.dist[vert.value-1][neigh-1] = 1
        for k in range(0, v):
            for i in range(0, v):
                for j in range(0, v):
                    tmp = self.dist[i][k] + self.dist[k][j]
                    if self.dist[i][j] > tmp:
                        self.dist[i][j] = tmp

        self.diameter = max(max(row) for row in self.dist)
        print("Diameter: {}".format(self.diameter))
        self.calc_avg_dist()

    def print_dist(self):
        for row in self.dist:
            print(row)

    def calc_avg_dist(self):
        tmp = 0
        for i, row in enumerate(self.dist):
            for j, value in enumerate(row):
                if j > i:
                    tmp = tmp + value
        res = 2/(self.v_cnt * (self.v_cnt-1))
        res = res * tmp
        print("Mean (average) distance: {}".format(res))

    def make_closeness(self):
        for i, row in enumerate(self.dist):
            closeness = round(len(self.dist)/sum(row), 7)
            self.arr[i].closeness = closeness

    def make_clust_coef(self):
        coef_sum = 0
        for v in self.arr:
            triangel_cnt = 0
            for ni in v.neighbors:
                n = self.arr[ni-1]
                a = set(n.neighbors)
                b = set(v.neighbors)
                triangel_cnt += len(a & b)
            v.triangel_cnt = triangel_cnt
            d = v.degree * (v.degree-1)
            if d == 0:
                v.clust_coef = 0
            else:
                v.clust_coef = round(triangel_cnt / d, 9)
            coef_sum += v.clust_coef

        trans = coef_sum/self.v_cnt

        print("Transitivity: {}".format(trans))
        for v in self.arr:
            print("{};{}".format(v.value, v.clust_coef))

    def global_coef(self):
        cc = [[]] * (self.max_vert+1)
        for i in range(0, (self.max_vert+1)):
            cc[i] = [i, 0, 0]

        for v in self.arr:
            cc[v.degree][2] += 1
            cc[v.degree][1] += v.clust_coef


        gcc_deg = []
        gcc_val = []
        for i in cc:
             if i[2] != 0:
                 gcc_deg.append(i[0])
                 gcc_val.append(i[1]/i[2])
        
        plt.scatter(gcc_deg,gcc_val)
        plt.xlabel("d")
        plt.ylabel("AVG_CC")
        plt.grid(True)
        #plt.show()


    def write_csv(self):
        with open("verts.csv", mode='w', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(['ID vrcholu', 'degree', 'closeness', 'betwenness', 'CC'])
            for vert in self.arr:
                writer.writerow([vert.value, vert.degree,vert.closeness, vert.betweenness, vert.clust_coef])

    def make_betweeness(self):
        G = nx.Graph()
        G.add_edges_from(self.edges)
        betweenness_centrality = nx.betweenness_centrality(G)
        for node, centrality in betweenness_centrality.items():
            vertIdx = self.find_vert(node)
            self.arr[vertIdx].betweenness = round(centrality,9)



    def print(self):
        for v in self.arr:
            print(v)    


class Vert:
    def __init__(self, value):
        self.value = value
        self.neighbors = []
        self.degree = 0
        self.closeness = 0
        self.triangel_cnt = 0
        self.clust_coef = 0

    def __str__(self):
        return "value = {}, neigh => {}, degree => {}, closeness => {}, coef => {}".format(self.value, self.neighbors, self.degree, self.closeness, self.clust_coef)

    def add_neighbor(self, neighbor):
        self.neighbors.append(neighbor)


def main():
    filename = 'KarateClub.csv'
    verts = Verts(filename)

    verts.make_matrix()

    verts.make_dist()
    # verts.print_dist()

    verts.make_closeness()
    verts.make_betweeness()
    print()
    verts.make_clust_coef()

    verts.global_coef()

    verts.write_csv()

    #verts.print()

    # verts.print_matrix()

    # min_vert = verts.min_vert
    # max_vert = verts.max_vert

    # total_deg = sum(len(vert.neighbors) for vert in verts.arr)
    # avg_deg = total_deg / len(verts.arr)

    # cetnost = [0] * (max_vert + 1)
    # for vert in verts.arr:
    #     cnt = len(vert.neighbors)
    #     cetnost[cnt] = cetnost[cnt] + 1

    # rel_cetnost = [round(x / len(verts.arr), 3) for x in cetnost]

    # print("Min stupeň: {}".format(min_vert))
    # print("Max stupeň: {}".format(max_vert))
    # print("Priemerný stupeň: {}".format(avg_deg))
    # print("Cetnosti sú : {}".format(cetnost))
    # print("Relativne cetnosti sú : {}".format(rel_cetnost))

    # os_x = [i for i in range(0, max_vert+1)]
    # plt.bar(os_x, cetnost)

    # plt.axvline(avg_deg, color="red")
    # plt.title('Cetnosti')
    # plt.xlabel('Stupen')
    # plt.ylabel('Pocet')
    # plt.show()


if __name__ == "__main__":
    main()
