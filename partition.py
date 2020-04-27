#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Apr 25 17:13:56 2020

@author: shuvomsadhuka
"""
import math
import random
import numpy as np

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
                
        
def Karmarkar_Karp(inputs):
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
    
def main():                    
        # test_example = [1, 1, 1, 2]   
        max_iter = 5         
        test_example = list(np.random.randint(int(1e12), size=100))
        best_residue = 1e12
        max_iter = 25000
        
        for i in range(max_iter):
                R1, R2 = 0, 0
                for j in range(len(test_example)):
                        if random.randint(0,1) == 0:
                                R1 += test_example[j]
                        else:
                                R2 += test_example[j]
                
                random_residue = abs(R1-R2)
                if random_residue < best_residue:
                        best_residue = random_residue
        print("Repeated Random, no prepartition, ", best_residue)
        
        test = MaxHeap(test_example)
        test.build_heap()
        print("Karmarkar-Karp, ", Karmarkar_Karp(test))
        
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