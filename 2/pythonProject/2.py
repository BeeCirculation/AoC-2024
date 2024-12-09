import copy
from math import *
SafeCount = 0
def Split(n):
   return n.split(' ')
def ReportSafe(replst = [1, 3, 9]):
   High = -100000
   Low = 100000
   for i in range(len(replst) - 1):
       Diff = replst[i+1] - replst[i]
       if Diff > High:
           High = Diff
       if Diff < Low:
           Low = Diff
   if 1 <= abs(High) <= 3 and 1 <= abs(Low) <= 3:
       if High/Low > 0:
           return True
       else:
           return False
   else:
       return False


with open('input.txt') as f:
   input = list(map(Split, list(f.read().split('\n'))))[:-1]


for i in input:
    if i:
        SafeCount += int(ReportSafe(list(map(int, i))))


print('Safe reports without dampener: ' + str(SafeCount))


SafeCount = 0


for i in input:
    if i:
       Loopt = False
       for j in range(len(i)+1):
           Loopi = copy.copy(i)
           if j < len(i):
               Loopi.pop(j)
           if ReportSafe(list(map(int, Loopi))):
               Loopt = True
       SafeCount += int(Loopt)


print('Safe reports with dampener: ' + str(SafeCount))