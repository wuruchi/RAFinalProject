import random
import numpy
import math
import copy
import time
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 10 11:39:37 2018

@author: BleuDChan
"""

#Class that generates the array with random data for the experiments
class Generator(object):
    def __init__(self, numrandom, numworse, numbest):
        self.samplerandom = numrandom
        self.sampleworse = numworse
        self.samplebest = numbest
        #number of items per vector
        self.numberItems = 50001
        
    def generate(self):
        
        total = self.samplerandom + self.sampleworse + self.samplebest
        
        
        assert(total == 200)
        
        #dataL = []
        dataL = ""
        for i in range(self.samplerandom):
            new = []
            for j in range(self.numberItems):
                new.append(random.randint(100,999))
                #ew = str(random.randint(100,999)) + " "
            dataL += " ".join(str(x) for x in new) + "\n"
        for i in range(self.sampleworse):
            new = []
            for j in range(self.numberItems):
                new.append(random.randint(100,999))
            new.sort()
            dataL += " ".join(str(x) for x in new) + "\n"
            
        for i in range(self.samplebest):
            new = []
            for j in range(self.numberItems):
                new.append(random.randint(100,999))
            new.sort(reverse = True)
            dataL += " ".join(str(x) for x in new) + "\n"
        #Saves data into a file in the same directory as the code
        print(dataL,  file=open('data.txt', 'w'))
        
        return 'Ok'
    
class RandomTests(object):
    def __init__(self):
        self.data = numpy.loadtxt('data.txt', numpy.int32)
    

    # Python program for implementation of Quicksort Sort 
    # Taken from https://www.geeksforgeeks.org/quick-sort/
    # This function takes last element as pivot, places 
    # the pivot element at its correct position in sorted 
    # array, and places all smaller (smaller than pivot) 
    # to left of pivot and all greater elements to right 
    # of pivot 
    def partition(self,arr,low,high): 
        i = ( low-1 )         # index of smaller element 
        pivot = arr[high]     # pivot 
      
        for j in range(low , high): 
      
            # If current element is smaller than or 
            # equal to pivot 
            if   arr[j] <= pivot: 
              
                # increment index of smaller element 
                i = i+1 
                arr[i],arr[j] = arr[j],arr[i] 
      
        arr[i+1],arr[high] = arr[high],arr[i+1] 
        return ( i+1 ) 
    
    # The main function that implements QuickSort 
    # arr[] --> Array to be sorted, 
    # low  --> Starting index, 
    # high  --> Ending index 
      
    # Function to do Quick sort 
    def quickSort(self,arr,low,high): 
        if low < high: 
      
            # pi is partitioning index, arr[p] is now 
            # at right place 
            pi = self.partition(arr,low,high) 
      
            # Separately sort elements before 
            # partition and after partition 
            self.quickSort(arr, low, pi-1) 
            self.quickSort(arr, pi+1, high) 
    
    # Modified Random version of the quicksort algorithm
    # Picks a random pivot according to what was explained at class
    def partitionR(self,arr,low,high):
        r = random.randint(low,high)
        arr[r],arr[high] = arr[high],arr[r]
        return self.partition(arr,low,high)
    
    def quickSortR(self,arr,low,high):
        if low < high:
            r = self.partitionR(arr,low,high)
            self.quickSortR(arr,low,r-1)
            self.quickSortR(arr,r+1,high)
    
    #Finds the median using quickSortR
    def medianQuickSortR(self,arr):
        startEvalTime = time.time()
        self.quickSortR(arr,0,len(arr) -1)       
        return arr[math.ceil(len(arr)/2)], time.time() - startEvalTime
    
    #Select function for the quickSelect
    #Partly adapted from kodedojo.com
    def select(self,lst, l, r, index):
        if r == l:
            return lst[l]
        # choose random pivot
        pivot_index = random.randint(l, r)
        # move pivot to beginning of list
        lst[l], lst[pivot_index] = lst[pivot_index], lst[l]
        i = l
        for j in range(l+1, r+1):
            if lst[j] < lst[l]:
                i += 1
                lst[i], lst[j] = lst[j], lst[i]
        # move pivot to correct location
        lst[i], lst[l] = lst[l], lst[i]
        # recursively partition one side only
        if index == i:
            return lst[i]
        elif index < i:
            return self.select(lst, l, i-1, index)
        else:
            return self.select(lst, i+1, r, index)
        
         
    def quickselect(self,items):
        startEvalTime = time.time()
        item_index = math.ceil(len(items)/2)
        if items is None or len(items) < 1:
            return None
    
        if item_index < 0 or item_index > len(items) - 1:
            raise IndexError()
    
        return self.select(items, 0, len(items) - 1, item_index), time.time() - startEvalTime
       
    #Coded from the pseucocode in the Mitzenmacher Upfal book         
    def rMedian(self,arr):
        startEvalTime = time.time()
        n = len(arr)
        sizesample = math.ceil(math.pow(n,3/4))

        sortedR = []
        for i in range(sizesample):
            sortedR.append(random.choice(arr))
        sortedR.sort()

        index_d = math.floor(math.pow(n,3/4)/2 - math.sqrt(n))
        index_u = math.floor(math.pow(n,3/4)/2 + math.sqrt(n))

        value_d = sortedR[index_d]
        value_u = sortedR[index_u]

        listC = []
        listD = []
        listU = []
        for i in range(0,n):
            if arr[i] < value_d:
                listD.append(arr[i])
            if (arr[i] >= value_d and arr[i] <= value_u):
                listC.append(arr[i])
            if arr[i] > value_u:
                listU.append(arr[i])
    
        if (len(listD) > int(n/2)) or (len(listU) > int(n/2)):
            return 'FAIL'
        if (len(listC) <= 4*math.pow(n,3/4)):
            listC.sort()
        else:
            return 'FAIL'

        m = listC[math.floor(n/2) - len(listD)]
      
        return [m, time.time() - startEvalTime]
        
    #Performs the experiment
    def experiment(self):
        #output = 'Array,Exp,Result,time\n'
        output = 'Array,timeQSort,timeQSelect,timeRMedian,RMedianSuccess\n'
        #outputAsc = 'Array,timeQSort,timeQSelect,timeRMedian\n'
        #outputDesc = 'Array,timeQSort,timeQSelect,timeRMedian\n'
        for i in range(200):
            tempvector = copy.deepcopy(self.data[i])
            Qsort = self.medianQuickSortR(tempvector)
            tempvector = []
            tempvector = copy.deepcopy(self.data[i])
            Qselect = self.quickselect(tempvector)
            tempvector = []
            tempvector = copy.deepcopy(self.data[i])
            RMedian = self.rMedian(tempvector)
            print(Qsort[0],Qselect[0],RMedian[0])
            #if i < 50:
            #    output += str(i) + ',' + str(Qsort[1]) + ',' + str(Qselect[1]) + ',' + str(RMedian[1]) + '\n'
            #elif i < 100 and i >= 50:
            #    outputAsc += str(i) + ',' + str(Qsort[1]) + ',' + str(Qselect[1]) + ',' + str(RMedian[1]) + '\n'
            #else:
            #    outputDesc += str(i) + ',' + str(Qsort[1]) + ',' + str(Qselect[1]) + ',' + str(RMedian[1]) + '\n'
            #output += str(i) + ',Qsort,' + str(Qsort[0]) + ',' + str(Qsort[1]) + '\n'
            #output += str(i) + ',Qselect,' + str(Qselect[0]) + ',' + str(Qselect[1]) + '\n'
            #output += str(i) + ',RMedian,' + str(RMedian[0]) + ',' + str(RMedian[1]) + '\n'
            output += str(i) + ',' + str(Qsort[1]) + ',' + str(Qselect[1]) + ',' + str(RMedian[1]) + ',' + str(RMedian[0]) + '\n'
            print(i)
        
        print(output,  file=open('resultsExperiment.txt', 'w'))
        
        
    

        
            

#gen = Generator(100,50,50)
#gen.generate()

#rand = Gromacs()
#rand.exp()
#rand.experiment()


#print(rand.quickselect(rand.data[3]))
#print(rand.rMedian(rand.data[3]))
#print(rand.medianQuickSortR(rand.data[3]))
#print(rand.data[2])
#print(rand.data[0])




