from array import *
import random
import csv


global blockchain
blockchain = []
block_time = 20
next_block = []

stat = []
block_time_counter = 0
transaction_counter = 0

limit_on_number_of_events = 1000
list_of_events = []

#one byte password
password = 120
new_hash = 23

# Set a credit limit, that is a percentage of customer’s current balance. 
credit_limit = .2

# Customers A, B, C, D, Balance 
customers_Balance = [0,0,0,0]


# functions
#---------------------------

def Transaction_Type_Gen():
    prob = random.random()

    #T0, T1, T2 , and T3 , for each customer is 0.25, 0.25, 0.1, and 0.4.
    if prob >= .75:
        return 0
    elif prob >= .5:
        return 1
    elif prob >= .4:
        return 2
    elif prob >= 0:
        return 3

#Picks a customer at random
def Pick_A_Customer():
    prob = random.random()
    if prob >= .75:
        return "A"
    elif prob >= .5:
        return "B"
    elif prob >= .25:
        return "C"
    elif prob >= 0:
        return "D"

#Customer to numb
def customer_to_numb(customer):
    if customer == "A":
        return 0
    if customer == "B":
        return 1
    if customer == "C":
        return 2
    if customer == "D":
        return 3

#update Customer balance
def update_Balance(customer, amount):
    customer = customer_to_numb(customer)
    customers_Balance[customer] += amount
    customers_Balance[customer] = round(customers_Balance[customer], 2)


#check block time
def is_block_time_full(time):
    global block_time_counter
    block_time_counter += time
    if block_time_counter <= block_time:
        return False
    else:
        return True

# checks validity of request
def validity(customer, dollar):
    customer = customer_to_numb(customer)
    if customers_Balance[customer] < dollar:
        return False
    else:
        return True

# "Miner" mining the blocks
def publish_block():
    global block_time_counter, transaction_counter, password, new_hash

    print("Next Block")
    stat.append(transaction_counter)
    print(next_block)

    blockchain.append(next_block[:])
    
    print("blockchain")
    #print(blockchain)

    next_block.clear()


    new_hash = password  ^ new_hash
    next_block.append(new_hash)


    
    block_time_counter = 0
    transaction_counter = 0



# record to .csv

# E Evaluates and record statistics Average number of transaction attempts, average number of successful transactions per time unit. 


#main
#---------------------------

# Generate events
while(limit_on_number_of_events > 0):
    # Randomly, choose the time increment for the next event (a value between 1 and 10) 
    time = random.randint(1, 10)
    event = Transaction_Type_Gen()
    customer = Pick_A_Customer()
    customer2 = customer
    if event == 2:
        while customer == customer2:
            customer2 = Pick_A_Customer()
    
    dollars = (random.randint(1,10000)/100)
    if event == 3:
        dollars = 0

    list_of_events.append([time, customer, event, dollars, customer2])

    limit_on_number_of_events -= 1

# Record the transaction request and its time in a .csv event-file 
rows = list_of_events
Details = ['Time', 'Customer', 'Event', 'Dollars', 'Customer 2'] 
with open('list_of_events.csv', 'w+', newline ='') as f:
    write = csv.writer(f) 
    write.writerow(Details)
    write.writerows(rows) 

#[0] is time, [1] Customer, [2] event, [3] dollar amount, [4] customer2
# Transactions: T0 – Deposit x dollars, T1 – Withdraw y dollars, T2 - Transfer z dollars to another customer, and T3 - null (no) transaction.  
# Infinite loop on events
next_block.append(password)


for x in list_of_events:

    print(x)
    #print(customers_Balance)
    print(block_time_counter)
    
    #did block time pass?
    if is_block_time_full(x[0]) == True:
        #publish block
        print("block time up")
        publish_block()

    transaction_counter += 1

    #if not is next trasacion valid for T1 or T2
    if x[2] == 1 or x[2] == 2:
        if validity(x[1],x[3]) == True:
            update_Balance(x[1],-(x[3]))
            if x[2] == 2:
                update_Balance(x[4],x[3])
        
            next_block.append(x)
        else:
            print("Transaction failed")

    if x[2] == 3:
        next_block.append(x)

    if x[2] == 0:
        update_Balance(x[1],(x[3]))
        next_block.append(x)
    
    if len(next_block) == 4:
        #publish block
        print("block full")
        publish_block()

rows = blockchain
with open('Blockchain.csv', 'w', newline ='') as f:
    write = csv.writer(f) 
    write.writerows(rows) 


#Evaluates and record statistics 


avg_TA = (sum(stat)/len(stat))
avg_STA = 0

for x in blockchain:
    avg_STA += ((len(x))-1)

avg_STA = avg_STA/len(blockchain)
print('')
print('')
print('')
print("Average number of transaction attempts")
print(round(avg_TA,2))
print("Average number of successful transactions per time unit. ")
print(round(avg_STA,2))
print('')

