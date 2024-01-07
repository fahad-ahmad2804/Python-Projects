import math

print("Investment - calculate the amount of interest you'll earn on your investment\n")
print("Bond - calculate the amount you'll have to pay on a home loan\n")

selection = input("""Please enter either 'Investment' or 'Bond' to select which calculation you wish to perform:\n""").lower()

if selection == "investment":
    print("")
    print("You have selected 'Investment'\n")

    principal = float(input("Please enter the amount of money you wish to deposit: "))
    rate = float(input("Please enter the interest rate: "))
    time = float(input("Please enter the time in years: "))
    
    print("")

    interest = input('''Please enter either 'Simple' or 'Compound' to calculate the 
correct type of interest:\n''').lower()
    
    if interest == "simple":
      simple_interest = principal * (1 + rate / 100 * time)
      print(f"Your return will be {simple_interest} ")

    elif interest == "compound":
        compound_interest = principal * math.pow((1 + rate / 100), time)
        c_round = round(compound_interest, 2)  
        print(f"Your return will be {c_round}")

    else:
        print("Invalid Input")

elif selection == "bond":
    print("You have selected 'Bond'")
    value = float(input("Please enter the present value of the property: "))
    b_rate = float(input("Please enter the interest rate: "))
    
    bm_rate = (b_rate / 100) / 12
    b_time = int(input("Please enter the time in months you plan to repay: "))
    repayment = (bm_rate * value) / (1 - (1 + bm_rate)**(-b_time))
    r_round = round(repayment, 2)
    print(f"The amount you'll have to repay each month is: {r_round}")
else:
  print("Invalid Input")