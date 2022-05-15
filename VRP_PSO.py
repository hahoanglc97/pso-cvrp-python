import math
import numpy as np
import random as r
import matplotlib.pyplot as plt
import plotgr
import copy
import PSO


# --------------------------------------[Reading data set values through function]------------------------------------------------------------------------
def readdata(name_of_file):
    a1 = open(name_of_file, 'r')
    # reading content of a1 and storing in a2
    a2 = a1.read()
    # splitting contents in a2 into list from where newline is started
    a2 = a2.split('\n')
    # For reading number of customers, splitting values in third index of a2 list into new list
    temp_customer = a2[3].split()
    # converting a list value to integer which gives total customers
    no_of_customers = int(temp_customer[2])
    # reading vehicle capacity which is in five index of list b2
    temp_capacity = a2[5].split()
    vehicle_total_capacity = int(temp_capacity[2])

    a1.close()
    length = no_of_customers
    # initializing array matrices of demand of customers, X coordinate , Y coordinate using compact for loop
    x = [0 for j in range(no_of_customers)]
    y = [0 for j in range(no_of_customers)]
    customer_demand = [0 for j in range(length)]
    # -----------reading values of x,y nodes of customers as well as their demand by splitting into lists from the respective indices of their start-----
    for j in range(0, length):
        x_y_values = a2[j + 7].split()
        customer_demand[j] = int(float(a2[no_of_customers + 8 + j].split()[1]))
        x[j] = int(float(x_y_values[1]))
        y[j] = int(float(x_y_values[2]))

    # ------------------------------[calculating distance between nodes and computing the distance matrix]--------------------------------------------

    # initializing 2-d distance matrix that computes distance between customers and customer & depot
    matrix_distance = [[0 for i in range(no_of_customers)] for j in range(no_of_customers)]
    for i in range(no_of_customers):
        for j in range(no_of_customers):
            if i == j:
                matrix_distance[i][j] = 0
            elif i > j:  # since this matrix is symmetrical
                matrix_distance[i][j] = matrix_distance[j][i]
            else:
                matrix_distance[i][j] = math.sqrt((x[j] - x[i]) ** 2 + (y[j] - y[i]) ** 2)

    return vehicle_total_capacity, no_of_customers - 1, matrix_distance, customer_demand, x, y


# -------------------------------------[calling dataset function to read values]-----------------------------------------------


capacity_of_vehicle, total_customers, distance_matrix, demand_matrix, X, Y = readdata('data-test/A/A-n32-k5.vrp')

coordinates_of_customers = [[X[i], Y[i]] for i in range(len(X))]
print("Coordinates of customer:  ", coordinates_of_customers)

print("Demand Matrix : ", demand_matrix, "VehicleCapacity : ", capacity_of_vehicle)
print("Distance Matrix: ", distance_matrix)

# number_of_particles = int(input("Enter Number of generations for finding the fitness value on every iteration: "))
# number_of_iterations = int(input("Enter Number of generations for finding the fitness value on every iteration: "))

# Calling PSO
Sol = PSO.particle_swarm_optimization(total_customers, demand_matrix, distance_matrix, capacity_of_vehicle,
                                      80, 50000)

customer_count_serve = PSO.customers_served_by_each_vehicle(total_customers, capacity_of_vehicle, demand_matrix, Sol)

total_required_vehicles = len(customer_count_serve)

print("required vehicles for the journey : ", total_required_vehicles)
Cluster_Customers = []
for j in range(total_required_vehicles):
    LB = sum(customer_count_serve[0:j])
    UB = LB + customer_count_serve[j]
    temp = Sol[LB:UB]
    Cluster_Customers.append(temp)

print("Network Routes of Customer cluster formed vehiclewise: ", Cluster_Customers)

# Ploting tours for SRC solutions
plotgr.TourFunction(Cluster_Customers, coordinates_of_customers)
