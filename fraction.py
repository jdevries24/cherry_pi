import math
class fraction:
   
   #class for representing rational numbers. Allows for the four basic operations 
   def __init__(self,N,D,cannon = True):
      if (N == 0):
         self.n = 0
         self.d = 1
         return
      if cannon:
         g = math.gcd(N,D)
         N = N // g
         D = D // g
      self.n = N
      self.d = D
      
   def __str__(self):
      #usefull for looking at what a fraction looks like
      return str(self.n) + "/" + str(self.d)
   
   def __add__(self,o):
      #find the denominators least common multiple set both fractions to it and then add
      #return self.add_method_a(o)
      g = math.gcd(self.d,o.d)
      if g == 1:
         lcm = (self.d*o.d)
         return fraction((o.d*self.n) + (self.d*o.n),lcm,False)
      else:
         num = (self.n*o.d) + (o.n * self.d)
         return fraction(num,self.d*o.d)
   
   def __sub__(self,o):
      #same as above only subtract
      num = (self.n * o.d) - (o.n * self.n)
      return fraction(num,self.d*o.d,False)
   
   def __mul__(self,o):
      #easyst of all operations just multiply the numerator and denominator
      return fraction(self.n * o.n,self.d * o.d)
   
   def __truediv__(self,o):
      #not sure if this is ever used
      return fraction(self.n * o.d,self.d * o.n)
   
   def __float__(self):
      return self.n/self.d
   
   def inverse(self):
      return fraction(self.d,self.n)
   
   
class pi_tools:
   #collection of useful algorthms for the program
   
   
   def split_up_iteration_even(start,end,split_amount):
      split_num = (end - start)//split_amount
      splits = []
      for i in range(split_amount):
         splits.append((start,start+split_num))
         start += split_num
      splits[-1] = (splits[-1][0],end)
      return splits
   
   def split_up_iteration(start,end,split_amount):
      task_num = end - start
      splits = []
      starting_point = start
      for i in range(split_amount):
         task_num -= task_num//2
         splits.append((starting_point,task_num+starting_point))
         starting_point += task_num
      splits[-1] = (splits[-1][0],end)
      return splits
      
   
   def save_string(file_name,string):
      #just a method to save a string to a file
      f = open(file_name,'w')
      f.write(str(string))
      f.close()
      
   def int_to_bytes(a_int):
      min_bits = int(math.log2(a_int)) + 1
      min_bytes = (min_bits//8) + 2
      return a_int.to_bytes(min_bytes,'big',signed=True)
      
   def save_fraction(file_name,fract):
      #saves a fraction as two binnary files
      f = open(file_name+"n",'wb')
      f.write(pi_tools.int_to_bytes(fract.n))
      f.close()
      f = open(file_name+"d",'wb')
      f.write(pi_tools.int_to_bytes(fract.d))
      f.close()
      
   def open_fraction(file_name):
      #loads a fraction from two binnary files
      f = open(file_name+"n",'rb')
      num = int.from_bytes(f.read(),'big',signed=True)
      f.close()
      f = open(file_name+"d",'rb')
      den = int.from_bytes(f.read(),'big',signed=True)
      f.close()
      frac = fraction(0,1) #skip over the intilizer no need to check for gcd assume fraction is reduced allredy
      frac.n = num 
      frac.d = den
      return frac
   