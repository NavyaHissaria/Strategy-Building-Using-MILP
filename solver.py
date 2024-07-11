from pyomo.environ import *
import math
model=ConcreteModel()
model.constraints=ConstraintList()
n=10                                          #Number of match ticks
E=[840,840,840,840,840,840,840,840,840,840]   #Enemy strength for each attack tick
E[0]=0
E[n-1]=100000
T=2500                                        #Treasure required to reach victory
V=[40,40,40,40,40,40,40,40,40,40]             #Number of jobs in each match tick
Cg=10                                         #Amount of gold one can generate in each job for one job tick
Cf=10                                         #Amount of food one can generate in each job for one job tick
Ct=10                                         #Amount of treasure one can generate in each job for one job tick
Tg=30                                         #Amount of gold required to train one soldier
Tf=40                                         #Amount of food required to train one soldier
M=10000000                                    #The big M we will be using
Wininc=100000                                 #The army winning increase, needs to be optimized for better solution
Str_Sol=84                                    #Strength of one soldier
armyV_initial=84*24                           #Initialized as needed, the initial value of army
initial_gold=700
initial_food=1000
model.food_in=Var(range(n), domain=NonNegativeIntegers)                 #Number of jobs allocated to food in each tick
model.gold_in=Var(range(n),domain=NonNegativeIntegers)                  #Number of jobs allocated to gold in each tick
model.treasure_in=Var(range(n),domain=NonNegativeIntegers)              #Number of jobs allocated to treasure in each tick
model.total_gold=Var(range(n),domain=NonNegativeIntegers)               #Represents gold before ith attack {deducting all costs}
model.total_food=Var(range(n),domain=NonNegativeIntegers)               #Represents food before ith attack {deducting all costs}
model.total_treasure=Var(range(n),domain=NonNegativeIntegers)           #Represents treasure before ith attack {deducting all costs}
model.train=Var(range(n),domain=NonNegativeIntegers)                    #Represents the number of soldiers trained before ith attack
model.army=Var(range(n),domain=NonNegativeIntegers)                     #Represents the strength of total army before ith attack
model.armyV=Var(range(n),domain=NonNegativeIntegers)                    #Represents the strength of total army after ith attack
model.W=Var(range(n),domain=Binary)                                     #Represents binary which denotes whether won at or before ith attack or not
model.r=Var(range(n),domain=[1.0000,0.3333,0.6667,0.5000,0.2000,0.8000,0.0000,0.5714])  #Represents the  fraction of army which should survive
model.x1_25=Var(range(n),domain=Binary)                                 #The next few variables sets rule for wars, the damage our army gets in attack
model.x1_5=Var(range(n),domain=Binary)
model.x1_75=Var(range(n),domain=Binary)
model.x2=Var(range(n),domain=Binary)
model.x3=Var(range(n),domain=Binary)
model.x5=Var(range(n),domain=Binary)
model.obj = Objective(expr = n-sum(model.W[i] for i in range (n)), sense = minimize)          #Gives the fastest possible win, collecting T amounts of treasure
for i in range(1,n):
    model.constraints.add(expr=model.total_gold[i]==model.total_gold[i-1]+Cg*model.gold_in[i]-Tg*model.train[i])
    model.constraints.add(expr=model.total_food[i]==model.total_food[i-1]+Cf*model.food_in[i]-Tf*model.train[i])
    model.constraints.add(expr=model.total_treasure[i]==model.total_treasure[i-1]+Ct*model.treasure_in[i])
    model.constraints.add(expr=model.army[i]==model.armyV[i-1]+Str_Sol*model.train[i]+Wininc*model.W[i])
    model.constraints.add(expr=model.armyV[i]>=0)
    model.constraints.add(expr=model.army[i]>=E[i])
    model.constraints.add(expr=model.armyV[i]==model.army[i]-E[i]*model.r[i])
    model.constraints.add(expr=model.army[i]-1.25*E[i]-1<=M*model.x1_25[i])           #x_{1.25}
    model.constraints.add(expr=model.army[i]-1.25*E[i]-1>=-M*(1-model.x1_25[i]))
    model.constraints.add(expr=model.r[i]-0.8000<=M*(1-model.x1_25[i]))
    model.constraints.add(expr=model.r[i]-0.8000>=-M*(model.x1_25[i]))
    model.constraints.add(expr=model.army[i]-1.5*E[i]-1<=M*model.x1_5[i])             #x_{1.5}
    model.constraints.add(expr=model.army[i]-1.5*E[i]-1>=-M*(1-model.x1_5[i]))
    model.constraints.add(expr=model.r[i]-0.6667<=M*(1-model.x1_5[i]))
    model.constraints.add(expr=model.r[i]-0.6667>=-M*(model.x1_5[i]))
    model.constraints.add(expr=model.army[i]-1.75*E[i]-1<=M*model.x1_75[i])           #x_{1.75}
    model.constraints.add(expr=model.army[i]-1.75*E[i]-1>=-M*(1-model.x1_75[i]))
    model.constraints.add(expr=model.r[i]-0.5714<=M*(1-model.x1_5[i]))
    model.constraints.add(expr=model.r[i]-0.5714>=-M*(model.x1_5[i]))
    model.constraints.add(expr=model.army[i]-2*E[i]-1<=M*model.x2[i])                 #x_{2}
    model.constraints.add(expr=model.army[i]-2*E[i]-1>=-M*(1-model.x2[i]))
    model.constraints.add(expr=model.r[i]-0.5000<=M*(1-model.x2[i]))
    model.constraints.add(expr=model.r[i]-0.5000>=-M*(model.x2[i]))
    model.constraints.add(expr=model.army[i]-3*E[i]-1<=M*model.x3[i])                 #x_{3}
    model.constraints.add(expr=model.army[i]-3*E[i]-1>=-M*(1-model.x3[i]))
    model.constraints.add(expr=model.r[i]-0.3333<=M*(1-model.x3[i]))
    model.constraints.add(expr=model.r[i]-0.3333>=-M*(model.x3[i]))
    model.constraints.add(expr=model.army[i]-5*E[i]-1<=M*model.x5[i])                 #x_{5}
    model.constraints.add(expr=model.army[i]-5*E[i]-1>=-M*(1-model.x5[i]))
    model.constraints.add(expr=model.r[i]-0.2000<=M*(1-model.x5[i]))
    model.constraints.add(expr=model.r[i]-0.2000>=-M*(model.x5[i]))
    model.constraints.add(expr=model.r[i]<=1-model.x5[i])
model.constraints.add(expr=model.total_treasure[0]==0)
model.constraints.add(expr=model.armyV[0]==armyV_initial)
model.constraints.add(expr=model.total_gold[0]==initial_gold)
model.constraints.add(expr=model.total_food[0]==initial_food)
for i in range(n):
    model.constraints.add(expr=model.total_gold[i]>=0)
    model.constraints.add(expr=model.total_food[i]>=0)
    model.constraints.add(expr=model.food_in[i]+model.gold_in[i]+model.treasure_in[i]==V[i])
    model.constraints.add(expr=model.total_treasure[i]<=M*model.W[i]+T-1)
    model.constraints.add(expr=model.total_treasure[i]>=-M*(1-model.W[i])+T-1)
    model.constraints.add(expr=model.r[i]<=1)
    model.constraints.add(expr=model.r[i]>=0)
    model.constraints.add(expr=model.W[i]>=0)
    model.constraints.add(expr=model.W[i]<=1)
opt = SolverFactory('cbc')
result=opt.solve(model)
file_name='best_strategy.txt'
with open(file_name,'w') as file:
  file.write("enemy.txt\njobs.txt\n2016\n")
  for i in range (1,n):
    file.write(str(int(model.food_in[i]()))+'\n')
    file.write(str(int(model.gold_in[i]()))+'\n')
    file.write(str(int(model.train[i]()))+'\n')