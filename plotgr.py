import matplotlib.pyplot as plt


# Plotting tours
def plot_lines(tours):
    for tour in tours:
        "Plot lines to connect a series of points."
        plt.plot([p[0] for p in tour[1]], [p[1] for p in tour[1]], label=tour[0])
    plt.axis('scaled');  # plt.axis('off')
    plt.ylabel('Y-Axis', fontsize=15)
    plt.xlabel('X-Axis', fontsize=15)
    plt.title('Route')
    plt.legend()
    plt.show()


def plot_tour(tours):
    "Plot the cities as circles and the tour as lines between them."
    plot_lines(list(tours))


# Fucntion to track tour points
# def TourFunction(ClusterList, Geometric_Points):
#     TourPoints = []
#     for cluster in ClusterList:
#         TourPoints.extend([Geometric_Points[0]])
#
#         currentTourPoints = []
#         for cust in cluster:
#             currentTourPoints.append(Geometric_Points[cust])
#
#         TourPoints.extend(currentTourPoints)
#
#     plot_tour(TourPoints)

# Fucntion to track tour points
def TourFunction(ClusterList, Geometric_Points):
    TourPoints = []
    for index, cluster in enumerate(ClusterList):
        currentTourPoints = [Geometric_Points[0]]

        for cust in cluster:
            currentTourPoints.append(Geometric_Points[cust])

        currentTourPoints.append(Geometric_Points[0])
        TourPoints.append(['route_' + str(index + 1), currentTourPoints])

    plot_tour(TourPoints)
