# -*- coding: utf-8 -*-
"""
Created on Tue Sep 20 16:57:24 2022

@author: vatsa
"""

# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import time
start = time.time()

import random

global best_route
global best_route_distance
global sum_of_fitness
  
# EARLY STOPPING
global early_stopping_count
  
def create_dictionary_on_cities(cities):
    dict_cities = {}
    for i in range(len(cities)):
        dict_cities[i] = cities[i];
    return dict_cities

def dist(tuple1,tuple2):
    return (tuple1[0]-tuple2[0])**2 + (tuple1[1]-tuple2[1])**2 + (tuple1[2]-tuple2[2])**2

def create_distance_matrix(no_of_cities,dict_cities):
    distance_matrix = [[0 for x in range(no_of_cities)] for y in range(no_of_cities)] 
    for i in range(no_of_cities):
        for j in range(i+1,no_of_cities):
            tmp = dist(dict_cities[i],dict_cities[j])
            distance_matrix[i][j] = tmp
            distance_matrix[j][i] = tmp
    #print(distance_matrix)
    return distance_matrix
    
def create_initial_population(no_of_cities,population_size):
    initial_population = []
    order = list(range(no_of_cities))
    for i in range(population_size):
        #Create a random order for cities\
        temp_order = order.copy()
        random.shuffle(temp_order)
        temp_order.append(temp_order[0])
        initial_population.append(temp_order)
    return initial_population
    
def create_RankList(population,dict_cities,distance_matrix):
    rankList = []
    sum_dist = 0
    for order in population:
        distance = 0
        for i in range(len(order)-1):
            distance += distance_matrix[order[i]][order[i+1]]
            #distance += dist(dict_cities[order[i]], dict_cities[order[i+1]])
        rankList.append([distance,tuple(order)])    
        sum_dist += distance 
    # Update best route    
    rankList = sorted(rankList, key = lambda x: x[0])
    global best_route
    global best_route_distance
    global early_stopping_count
    if(rankList[0][0]<best_route_distance):
        best_route = rankList[0][1]
        best_route_distance = rankList[0][0]
        early_stopping_count = 0
    else:
        early_stopping_count += 1
    
    global sum_of_fitness
    sum_of_fitness = 0
    for i in range(len(rankList)):
        rankList[i][0] = sum_dist/rankList[i][0]
        sum_of_fitness += rankList[i][0]
    
    return rankList

def Roulette_Selection(rankList):    
    #p = random.randint(0,sum_of_fitness)
    p = random.random()*sum_of_fitness
    i = 0
    while(p<sum_of_fitness):
        p += rankList[i][0]
        i += 1
        if(i==len(rankList)):
            i=0
    return rankList[i-1][1];

def crossover(parent1,parent2,startInd,endInd):
    child = []
    bool_available = [True]*len(parent1)
    for i in range(startInd,endInd+1):
        child.append(parent1[i]);
        bool_available[parent1[i]] = False;
    for i in parent2:
        if(bool_available[i]):
            child.append(i)
            bool_available[i] = False
    if(len(child)+1==len(parent1)):
        child.append(child[0])
    if(len(child)!=len(parent1)):
        print("*************************FLAG******************************")
        print(parent1, parent2, startInd, endInd)
    return tuple(child)
    

def create_new_population(population,rankList,no_elite):
    #print("No of elite: ",no_elite)
    new_population = []
    #print("Elite Adding")
    for i in range(no_elite):
        new_population.append(rankList[i][1])
    #print(new_population)
    n = int((len(population) - no_elite)/2)
    #print("Elite Added")
    for i in range(n):
        #print("Roulette Started")
        parent1 = Roulette_Selection(rankList)
        parent2 = Roulette_Selection(rankList)
        startInd = random.randint(0, len(parent1)-2)
        endInd = random.randint(startInd+1, len(parent1)-1)
        #print("Roulette Ended")
        #print("Crossover Started")
        child = crossover(parent1, parent2, startInd, endInd)
        new_population.append(child)
        child = crossover(parent2, parent1, startInd, endInd)
        new_population.append(child)
        #print("Crossover Ended")
    return new_population
 
def calc_final_ans(distance_matrix,best_route):
    ans = 0    
    for i in range(0,len(best_route)-1):
        ans += distance_matrix[best_route[i]][best_route[i+1]]
    return ans


#tmp = pd.read_csv('input1.txt', delimiter=' ', dtype=int)
got_cities = False
cities = []
with open('input.txt') as f:
    lines = f.readlines()
    
#print(lines)
no_of_cities = int(lines[0][:-1])
population_size = 0
no_of_populations = 0

if(no_of_cities<100):
    population_size = 450
    no_of_populations = 2000
elif(no_of_cities<200):
    population_size = 450
    no_of_populations = 1500
elif(no_of_cities<=500):
    population_size = 500
    no_of_populations = 1200
else:
    population_size = 500
    no_of_populations = 750

for i in range(1,len(lines)-1):
    cities.append(tuple(map(int,lines[i][:-1].split(" "))))
cities.append(tuple(map(int,lines[-1].split(" "))))

#print(cities)

#cities = create_city_location(no_of_cities)
dict_cities = create_dictionary_on_cities(cities)

distance_matrix = create_distance_matrix(no_of_cities, dict_cities)

population = create_initial_population(no_of_cities,population_size)

best_route = population[0]
best_route_distance = calc_final_ans(distance_matrix,best_route)
rankList = create_RankList(population,dict_cities,distance_matrix)
#rankList = create_RankList(population,dict_cities)
no_elite = int(0.2*len(population))

#print("START")
#print("No of Cities : ", len(cities))
#print("Dictionary of Cities: ", len(dict_cities), dict_cities)
#print("Initial Population Size: ", len(population))
#print("Initial Best Route distance: ", best_route_distance)
#print("Initial Best Route: ",best_route)
#print("Initial RankList: ", rankList)

early_stopping_count = 0
for i in range(no_of_populations):  
    if(time.time() - start > 195):
        break
    
    new_population = create_new_population(population, rankList, no_elite)
    #print("POPULATION    CREATED")
    population = new_population
    rankList = create_RankList(population,dict_cities,distance_matrix)
        
    if(early_stopping_count>250):
        print("EARLY STOPPED")
        break
        
    #print("POPULATION RANKED")
    print(" For",i+1,"iteration: ")
    #print("New Population Size: ", len(new_population))
    print("New Best Route distance: ", best_route_distance)
    #print("New Best Route: ",best_route)
    #print("New RankList: ", rankList)
    #print("\n")

#print("Final Best Distance:",best_route_distance)
#print("Final Best Route:",best_route)
#print("Wei Men shen's Answer:",calc_final_ans(distance_matrix,[1,0,5,2,6,4,3,1]))

# Storing Output
file = open("output.txt", "w") 
for city in best_route[:-1]:
    tuple_x = dict_cities[city]
    tmp = str(tuple_x[0]) + " " + str(tuple_x[1]) + " " + str(tuple_x[2]) + "\n"
    file.write(tmp)
tuple_x = dict_cities[best_route[-1]]
tmp = str(tuple_x[0]) + " " + str(tuple_x[1]) + " " + str(tuple_x[2])
file.write(tmp)
file.close()
#print(time.time()-start)