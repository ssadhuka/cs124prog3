#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 17:13:56 2020

@author: shuvomsadhuka
"""
import sys
import math
import random
import numpy as np
from typing import List

MAX_ITER = 25000
MAX_VAL = 1e12
LIST_LENGTH = 100

# cooling schedule for simulated annealing
COOLING = lambda t : 1e10 * 0.8 ** math.floor(t / 300)

# unseeded generator for test inputs
list_generator = random.Random()
# seeded generator for randomized algorithms
searcher = random.Random()
searcher.seed(0)


class MaxHeap(object):
        def __init__(self, array=[]):
                self.heap = array
                
        def __len__(self):
                return len(self.heap)
                
        def max_heapify(self, v):
                #for v in range(n/2, -1, -1):
                left = 2*v + 1
                right = left + 1
                if (left < len(self.heap)) and (self.heap[left] > self.heap[v]):
                        largest = left
                else:
                        largest = v
                
                if (right < len(self.heap)) and (self.heap[right] > self.heap[largest]):
                        largest = right
                
                if (largest != v):
                        self.heap[v], self.heap[largest] = self.heap[largest], self.heap[v]
                        self.max_heapify(largest)
        
        def build_heap(self):
                # print('BUILDING HEAP')
                for i in range(len(self.heap)//2, -1, -1):
                        self.max_heapify(i)
        
        def extract_max(self):
                maximum = self.heap[0]
                self.heap[0] = self.heap[len(self.heap)-1]
                del(self.heap[len(self.heap) - 1])
                self.max_heapify(0)
                return maximum
        
        def insert(self, v):
                self.heap.append(v)
                parent = math.ceil(len(self.heap)/2) - 1
                n = len(self.heap) - 1
                
                while (n > 0) and (self.heap[n] > self.heap[parent]):
                        self.heap[n], self.heap[parent] = self.heap[parent], self.heap[n]
                        n = parent
                        parent = math.ceil(n/2) - 1
                
        
def Karmarkar_Karp(inputs) -> int:
        assert(isinstance(inputs, MaxHeap)), "Input KK as a MaxHeap object!"
        #heaped_inputs = MaxHeap(inputs)
        #heaped_inputs.max_heapify()
        
        while len(inputs.heap) > 1:
                R1 = inputs.extract_max()
                R2 = inputs.extract_max()
                residue = R1 - R2
                
                if residue != 0:
                        inputs.insert(residue)
        
        if len(inputs.heap) == 1:
                return inputs.heap[0]
        else:
                return 0
    
# Karmarkar-Karp that takes in a list to simplify later code
def kk_list(inputs : MaxHeap, prepartitioned=False) -> int:
    heaped_inputs = MaxHeap(inputs)
    heaped_inputs.build_heap()
    return Karmarkar_Karp(heaped_inputs)

def prepartition(a : List[int], pre : List[int]) -> List[int]:
    new_list = [0] * len(a)
    for i in range(len(a)):
        assert(pre[i] in range(len(a)))
        new_list[pre[i]] += a[i]
    return new_list

def repeated_random(a : List[int], prepartitioned=True) -> int:
    # print("Repeated random")
    res = sum(a)
    population = range(len(a)) if prepartitioned else [-1,1]
    value = (lambda s : kk_list(prepartition(a, s))) if prepartitioned \
        else lambda s : abs(sum([x * y for x, y in zip(a,s)]))
    for _ in range(MAX_ITER):
        test_soln = searcher.choices(population,k=len(a))
        new_res = value(test_soln)
        # print(test_soln, new_res)
        if abs(new_res) < res:
            res = abs(new_res)
    return res

def hill_climbing(a: List[int], prepartitioned=False) -> int:
    # print("Hill climbing")
    population = range(len(a)) if prepartitioned else [-1,1]
    value = (lambda s : kk_list(prepartition(a, s))) if prepartitioned \
        else lambda s : abs(sum([x * y for x, y in zip(a,s)]))
    soln = searcher.choices(population,k=len(a))
    res = value(soln)
    for _ in range(MAX_ITER):
        test_soln = soln
        i = searcher.randrange(len(soln))
        test_soln[i] = searcher.choice(population)
        new_res = value(test_soln)
        if abs(new_res) < res:
            soln = test_soln
            res = abs(new_res)
            # print(soln, new_res)
    return res

def sim_annealing(a: List[int], prepartitioned=False, cool=COOLING) -> int:
    # print("Simulated annealing")
    population = range(len(a)) if prepartitioned else [-1,1]
    value = (lambda s : kk_list(prepartition(a, s))) if prepartitioned \
        else lambda s : abs(sum([a * b for a, b in zip(a,s)]))
    current_soln = searcher.choices(population,k=len(a))
    current_soln_res = value(current_soln)
    # best_soln = current_soln
    best_res = current_soln_res
    for t in range(MAX_ITER):
        test_soln = current_soln
        i = searcher.randrange(len(current_soln))
        test_soln[i] = searcher.choice(population)
        test_res = value(test_soln)
        if abs(test_res) < current_soln_res \
            or searcher.random() < math.exp(-(abs(test_res) - current_soln_res) / cool(t)):
            current_soln = test_soln
            current_soln_res = abs(test_res)
            # print(current_soln_res)
        if current_soln_res < best_res:
            # best_soln = current_soln
            best_res = current_soln_res
    return best_res

def main():       
        # configure for autograder             
        if len(sys.argv) == 4:
                assert(sys.argv[1] == "0")
                inputfile = open(sys.argv[3],'r')
                lst = [int(inputfile.readline()) for _ in range(LIST_LENGTH)]
                algs = [kk_list, repeated_random, hill_climbing, sim_annealing]
                alg_number = int(sys.argv[2])
                print(algs[alg_number % 10](lst, alg_number > 10))
                return
        
        
        # test_example = [1, 1, 1, 2]        
        test_example = list(np.random.randint(int(1e12), size=100))
        best_residue = 1e12
        
        # repeated random, no prepartition
        for _ in range(MAX_ITER):
                R1, R2 = 0, 0
                random.shuffle(test_example)
                for j in range(len(test_example)):
                        if random.randint(0,1) == 0:
                                R1 += test_example[j]
                        else:
                                R2 += test_example[j]
                
                random_residue = abs(R1-R2)
                if random_residue < best_residue:
                        best_residue = random_residue
                        
        #print("Repeated Random, no prepartition, ", best_residue)
        #print("Repeated Random, no prepartition, ", repeated_random(test_example, prepartitioned=False))
        #print("Simulated Annealing, no prepartition, ", sim_annealing(test_example))
        #print("Hill Climbing, no prepartition, ", hill_climbing(test_example))
        
        #print("Repeated Random, prepartition, ", repeated_random(test_example))
        #print("Simulated Annealing, prepartition, ", sim_annealing(test_example, prepartitioned=True))
        #print("Hill Climbing, prepartition, ", hill_climbing(test_example, prepartitioned=True))
        
        
        test = MaxHeap(test_example)
        test.build_heap()
        #print("Karmarkar-Karp, ", Karmarkar_Karp(test))

if __name__ == '__main__':
        main()


'''
#print(test.heap)
test.extract_max()
#print(test.heap)
test.insert(10)
test.insert(11)
test.insert(12)
test.insert(100)
test.insert(1000)
print(test.heap)

print(Karmarkar_Karp(test))
'''