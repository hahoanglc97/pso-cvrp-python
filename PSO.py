import numpy as np
import random
import math


# -----------------Function that returns number of customers served by each vehicle------------------------------------
def customers_served_by_each_vehicle(customers, vehicle_capacity, demmatrix, cs):  # cs is current solution here

    # storing length of current solution
    sc = len(cs)
    value = 1
    # initializing empty list of served customers
    served_customers = []
    while value:
        # cap is used to check vehicle capacity constraint, initially set to zero
        cap = 0
        # serve stores number of customers served for each iteration
        serve = 0

        for j in range(sum(served_customers), sc):
            # if capacity exceeds vehicle's total capacity, get out of loop
            if demmatrix[cs[j]] + cap > vehicle_capacity:
                break
            else:
                serve = serve + 1  # increment of one more customer served
                cap = cap + demmatrix[cs[j]]
        served_customers.append(serve)

        if sum(served_customers) == customers:
            value = 0
    return served_customers


# --------------------------------------------------------------------------------------------------------------------
# Function to return minimum distance covered by all vehicle i.e fitness candidate
def min_distance_traverse(customers, demmatrix, distmatrix, vehicle_capacity, s):  # s is solution
    size = len(s)
    min_vehicle = [0] * size  # Minimum required vehicles
    min_dist_value = [0] * size  # Total travelled Distance-The total distance travelled by all vehicles

    for i in range(size):
        currentsolution = s[i]
        customer_served_count = customers_served_by_each_vehicle(customers, vehicle_capacity, demmatrix,
                                                                 currentsolution)

        min_dist_value[i] = distance_traverse(customers, distmatrix, currentsolution, customer_served_count)
        min_vehicle[i] = len(customer_served_count)  # Minimum required vehicles

    return min_dist_value


# --------------------------------------------function that computes total travelled distance by each vehicle----------
def distance_traverse(customers, distmatrix, currentsolution, customer_served_count):
    # setting lb and ub initially to zero,
    lowerbound = upperbound = 0
    vehicle_count = len(customer_served_count)
    VehDistance = [0] * vehicle_count

    customer_vehicle_set = []
    for i in range(vehicle_count):
        lowerbound = sum(customer_served_count[0:i])

        upperbound = lowerbound + customer_served_count[i]
        VehDistance[i] = customer_depot_distance(currentsolution[lowerbound:upperbound], distmatrix)

    return sum(VehDistance)


# function returning distance calculated for each cluster from depot to customers and back to depot
def customer_depot_distance(cluster, distmatrix):  # cluster defines the customer set assigned to each vehicle
    current_distance = 0
    # for calculation of distance from customer to customer and customer to depot for each vehicle
    for i in range(len(cluster)):
        if i == 0:
            # distance calculated from depot to a particular customer
            current_distance = current_distance + distmatrix[0][cluster[i]]
        else:
            current_distance = current_distance + distmatrix[cluster[i - 1]][
                cluster[i]]  # distance represented for one customer to other

    current_distance = current_distance + distmatrix[cluster[len(cluster) - 1]][
        0]  # distance for customer back to depot
    return current_distance


# ---------------------------------------------------------------------------------------------------------------------

# function that return customers by sorting the particle's position assigned to them
def sorting_customers(t1, t2):
    # zip is a tuple iterator here pairs t2 and t1 together
    pair = zip(t2, t1)
    # extracting t1 values on the basis of t2 values sorted using sorted function
    cus = [i for _, i in sorted(pair)]
    return cus


# function that gives the fitness candidate i.e., the distance calculated for each generation
def fitness_value(particleposition, customers, demmatrix, distmatrix, vehicle_capacity):
    particle_customer_list = sorting_customers(list(range(1, customers + 1)), particleposition)
    value_2 = min_distance_traverse(customers, demmatrix, distmatrix, vehicle_capacity, [particle_customer_list])

    return value_2[0]


def particle_swarm_optimization(customers, demmatrix, distmatrix, vehicle_capacity, number_of_particles,
                                number_of_iterations):
    # needed to calculate velocity and position vector
    # Clerc and Kennedy 2002, constrictor coefficient can be used to prevent velocity "explosion"
    kappa = 1
    phi1 = 2.05
    phi2 = 2.05
    phi = phi1 + phi2
    chi = (2*kappa)/(abs(2-phi-math.sqrt(abs(pow(phi, 2)-(4*phi)))))
    # W is inertia constant
    W = chi
    # C1 is cognitive acceleration constant
    C1 = chi * phi1
    # C2 is social acceleration constant
    C2 = chi * phi2

    # W = 1
    # C1 = 2
    # C2 = 2
    # creating particle position and velocity vector array
    vector_position_particle = [[] for i in range(number_of_particles)]
    vector_velocity = [[] for i in range(number_of_particles)]

    # initializing position and vector values with random values within a specific range

    for i in range(number_of_particles):
        for j in range(customers):
            # vector_position_particle[i][j] represents position of jth customer for particle number ith
            vector_position_particle[i].append(random.random() * random.randrange(-30, 30))
            vector_velocity[i].append(random.random() * random.randrange(-30, 30))
    # initially the pbest position vector will be the particle position value itself
    pb_position = vector_position_particle

    pb_fitness = [float('inf') for i in range(number_of_particles)]  # represents fitness for personal best
    gb_fitness = float('inf')  # represents fitness for global best
    # initially it is assigned particle's first position values
    gb_position = vector_position_particle[0]

    iteration_no = 0
    # iteration is for how many generation it should calculate the fitness
    while iteration_no < number_of_iterations:

        for i in range(number_of_particles):

            fitness_candidate_value = fitness_value(vector_position_particle[i], customers, demmatrix, distmatrix,
                                                    vehicle_capacity)

            # for setting personal and global best to the minimum fitness candidate value
            if pb_fitness[i] > fitness_candidate_value:
                pb_fitness[i] = fitness_candidate_value
                pb_position[i] = vector_position_particle[i]

            if gb_fitness > fitness_candidate_value:
                gb_fitness = fitness_candidate_value
                gb_position = vector_position_particle[i]

        for i in range(number_of_particles):
            for j in range(customers):
                vector_velocity[i][j] = (W * vector_velocity[i][j]) + (C1 * random.random()) * (
                            pb_position[i][j] - vector_position_particle[i][j]) + (C2 * random.random()) * (
                                                    gb_position[j] - vector_position_particle[i][j])
                vector_position_particle[i][j] = vector_velocity[i][j] + vector_position_particle[i][j]

        # print("Obtained distance (fitness value) is : ", gb_fitness, "in generation number ", iteration_no + 1)

        iteration_no = iteration_no + 1

    # particle_stochastic_position = sorting_customers(list(range(1, customers + 1)), gb_position)

    # return particle_stochastic_position  # return list of set of vehicles
    return gb_fitness
