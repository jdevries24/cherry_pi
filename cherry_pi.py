import math
import multiprocessing
from fraction import *

class maths:
   #class to hold all the mathmatics
   
   def string_divide(n,d,pers = 200):
      #this method takes in a numerator and denominator interger
      #then divides them to compleation or untill the number of decimals is meet
      or_n = n
      acm = str(n//d) + "."
      i = n//d
      s = 0
      while ((n != 0) and (s < pers)):
         s += 1
         n = n - (i * d)
         if (n == 0) or (n == or_n):
            break
         n = n * 10
         i = n // d
         acm += str(i)
      return acm
   
   def factorial(n):
      #returns the factoral of n
      if n == 0:
         return 1
      result = 1
      for i in range(n):
         result = result * (n - i)
      return result
   
   def sqrt_10005(start,end,base = None,terminal = None):
      #as the Chudnovsky algorithm uses the sqrt(10005) a method is needed
      #this method simply calculates the continues fraction that is sqrt(10005)
      operators = (200,40)
      result = fraction(operators[(end) % 2],1)
      if base != None:
         result = result + base.inverse()
      for i in range(end,start,-1):
         #run it backwards
         result = fraction(operators[i % 2],1) + result.inverse()
         if (i % 100 == 0):
            print("Sqrt",end,"to",start,"is at",i)
      print("#####Sqrt",end,"to",start,"is Done!#####")
      if terminal != None:
         terminal.send(result)
         terminal.close()
      return result
   
   def Chudnovsky_algorithm(start,end):
      #this is where the magic happens the algorthem is pi=C(sum((M*L)/X),0,infinity)^-1
      #in this method all that is generated is sum((M*L)/X),start,end)
      L = (545140134 * start) + 13591409
      X = pow(-262537412640768000,start)
      M_num = maths.factorial(6*start)
      M_dnm = maths.factorial(3*start) * pow(maths.factorial(start),3)
      M = fraction(M_num,M_dnm)
      K = (12 * start) + 6
      #hold onto your buts cuz its going to get complicated
      result = fraction(0,1) #start with the fraction at zero
      for q in range(start,end):
         result = result + fraction(M.n * L,M.d * X) #thats all there is too it kinda next up descreatly move up our vars
         #each one of the vars can be stepped up dont wan't to calculate a factoral every time
         L = L + 545140134
         X = X * -262537412640768000
         M = M * fraction(pow(K,3) - (16 * K),pow(q+1,3))
         K = K + 12
         if (q % 100) == 0:
            print("  Pi",start,"to",end,"is at",q)
      print("######  Pi",start,"to",end,"is done#####")
      return result
   
   def sum_seq_fraction(fractions):
      #add a squence of fractions together
      result = fraction(0,1)
      for f in fractions:
         result = result + f
      return result
   
class cherry_pi:
   #actual program class
   
   def add_file_seq(file_names,file_base = "pi/pi"):
      #this method is for adding a number of files together
      result = fraction(0,1)
      for names in file_names:
         result = result + pi_tools.open_fraction(file_base+names)
      return result
   
   def run_Chudnovsky_round(start,end,threads,name = '0',file_base = "pi/pi"):
      #runs a descrete round of the Chudnovsky algorithm multi_treaded then saves the 
      #result to disk
      aguments = pi_tools.split_up_iteration_even(start,end,threads)#get the points that we wan't to run to
      thread_pool = multiprocessing.Pool(threads) #set it up as a pool of tasks
      fraction_seq = list(thread_pool.starmap(maths.Chudnovsky_algorithm,aguments))#this blocks exacution so we dont need to worry about missing anything
      sum_fraction = maths.sum_seq_fraction(fraction_seq)#add up the parts 
      pi_tools.save_fraction(file_base + name,sum_fraction) #and save it free up some memory
      thread_pool.close()#and always thread safe!!!
      print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
      print("$ Done with Chudnovsky round",name,"$")
      print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
      
   def Find_C(rounds):
      #the C part of the algorithm is 426880 * SQRT(10005) this is where we get that fraction
      m_sqrt = maths.sqrt_10005(0,rounds)
      m_sqrt = fraction(100,1) + m_sqrt.inverse() #the sqrt_10005 method only gets us the fraction part of the 
      #sqrt and comes in inverted we need to add the integer part and save it. 
      m_sqrt = fraction(m_sqrt.n*426880,m_sqrt.d)
      pi_tools.save_fraction("SQRT_10005",m_sqrt)#as of now the implentation is use SQRT as a constent. Its easer to compute
      #don't wan't to compute it every run ya know
      
   def check_precision(pi_string):
      #runs through what your pi string 
      #and compares it to a known pi string 
      #then returns how meany digits you got right and 
      #prints a message
      pi_f = open("PiDigits.txt")
      real_pi = pi_f.read()
      for i in range(len(pi_string)):
         if (i > len(real_pi)):
            print("Holy shit!")#pardon my French
            return i
         if pi_string[i] != real_pi[i]:
            print("error at:",i+1)
            return i
      print("all",len(pi_string)-2,"digits correct")
      return len(pi_string)-1
   
   def run(Chudnovsky_limit,Chudnovsky_rounds,threads = 1,digits = 100,save_file = "1000"):
      args = pi_tools.split_up_iteration_even(0,Chudnovsky_limit,Chudnovsky_rounds)
      files = [] #files range from 0 to number of Chudnovsky rounds
      for i in range(Chudnovsky_rounds):
         cherry_pi.run_Chudnovsky_round(args[i][0],args[i][1],threads,str(i),"pi/pi") #for your own system you should set "pi/pi" to
         #your own path so your home folder doesn't get swamped with pi0d and so on
         files.append(str(i))
      print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
      print("$ Done with all Chudnovsky $")
      print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
      print("doing final calculations")
      pi_fraction = cherry_pi.add_file_seq(files,"pi/pi") #see above
      pi_fraction = pi_tools.open_fraction("SQRT_10005") * pi_fraction.inverse() #times the sqrt_fraction to the inverse of the pi fraction
      pi_tools.save_string("Pi_fraction_of_"+save_file,pi_fraction) # save the pi fraction because we may be able to use more of it
      pi_decimal = maths.string_divide(pi_fraction.n,pi_fraction.d,digits) # get the decimal part by doing old school division
      good_to = cherry_pi.check_precision(pi_decimal) #see if we nailed it
      pi_tools.save_string("Pi_of_"+save_file,pi_decimal[:good_to])
      print("attempted to calcualate",digits,"digits")
   
if __name__ == "__main__":
   import os
   program_treads = os.cpu_count() #defult is to everthing avil
   Chudnovsky_l = 1000 #this is a small limit will only get about 1444 good digits
   rounds = 5 #the higher the Chudnovsky_l the higher the rounds. In theory this could be the same but that alot of read writes
   digits = 1000 #not how much digits you wan't how much digits are going to get estracted from the final fraction
   save_file = str(Chudnovsky_l) #what the postfix off all the save files for this run
   cherry_pi.run(Chudnovsky_l,rounds,program_treads,digits,save_file)
   
