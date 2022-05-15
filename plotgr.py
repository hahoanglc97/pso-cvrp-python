import matplotlib.pyplot as plt


# Plotting tours
def plot_lines(points, style='bo-'):
    "Plot lines to connect a series of points."
    plt.plot([p[0] for p in points], [p[1] for p in points], style)
    plt.axis('scaled');  # plt.axis('off')
    plt.ylabel('Y-Axis', fontsize=15)
    plt.xlabel('X-Axis', fontsize=15)
    plt.title('Route')
    plt.show()


def plot_tour(tour):
    "Plot the cities as circles and the tour as lines between them."
    plot_lines(list(tour) + [tour[0]])


# Fucntion to track tour points
def TourFunction(ClusterList, Geometric_Points):
    TourPoints = []
    for cluster in ClusterList:
        TourPoints.extend([Geometric_Points[0]])

        currentTourPoints = []
        for cust in cluster:
            currentTourPoints.append(Geometric_Points[cust])

        TourPoints.extend(currentTourPoints)

    plot_tour(TourPoints)
