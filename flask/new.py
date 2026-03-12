# import sys
# def process(v):
#     st=",".join(v)
#     return st
# v=sys.argv
# print(process(v[1:]))
# print(len(v))

# k=2
# for i in range(k,k**k+1,k):
#     print(i)

# nums=[2,2,4,1,5]
# e=[i for i in nums if i%2==0 and i not in e]
# print(e)


# def longestBalanced(nums):
#     e=[]
#     o=[]
#     for i in nums:
#         if i%2==0 and i not in e:
#             e.append(i)
#         elif i%2!=0 and i not in o:
#             o.append(i)
#     # print(nums,e,o)
#     if len(e)==len(o):
#         return len(nums)
# print(longestBalanced([1,2,3,4]))

# a=[1,2,3,4,5]
# a.remove(1)
# print(a)

class Multiset:
    multiset=[2,3]
    result=[]

    def add(self, val):
        # adds one occurrence of val from the multiset, if any
        self.multiset.append(val)
        print(self.multiset)
        pass

    def remove(self, val):
        # removes one occurrence of val from the multiset, if any
        if val in self.multiset:
            self.multiset.remove(val)
        pass

    def __contains__(self, val):
        # returns True when val is in the multiset, else returns False
        if val in self.multiset:
            self.result.append(True)
        return False
    
    def __len__(self):
        # returns the number of elements in the multiset
        self.result.append(len(self.multiset))
        return 0
    
    def query(self,val):
        if val in self.multiset:
            self.result.append(True)
        else:
            self.result.append(False)
    def p(self):
        print(self.multiset)
        print(self.result)
a=Multiset()
print(len(a))
# a.add(2)
# a.add(4)
# a.remove(5)
# a.__len__()
# a.__contains__(4)
# a.query(6)
# a.p()