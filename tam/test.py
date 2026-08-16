# ================bmi===================
# weight = float(input("Enter your weight in kilograms:"));
# height = float(input("Etner your height in meter:"));
# bmi= weight / (height*height);
# print("Your bmi is :" + str(bmi));

#  ===============degree=================
# celsius = float(input("Enter temperature in celsius"))
# fahrenheit = (celsius * 9/5)+32
# print("temperature in Fahrenheit is",fahrenheit)

#  ===================if======================
# age=int(input("Enter your age:"))
# if age >= 18 :
#     print("มึงสิแก่")

#  ====================gread====================
# score1=int(input("ใส่คะแนนmathมาค่ะอิแก่ "))
# score2=int(input("ใส่คะแนนartมาค่ะอิแก่" ))
# score3=int(input("ใส่คะแนนcomproมาค่ะอิแก่ "))
# sum=(score1+score2+score3/3)
# print(sum)
# if sum > 95 :
#     print ("congratulations!")

#  =================if else======================
# A=int(input("Enter the score for test 1:"))
# B=int(input("Enter the score for test 2:"))
# C=int(input("Enter the score for test 3:"))
# average = (A+B+C/3)
# if average > 95 :
#     print("congratulations!")
# else :
#     print ("(The average is ",(average),)

#  ================= if elif else =================
# num = float(input("Enter a number:"))
# if num > 0:
#     print("Positive number")
# elif num == 0:
#     print("Zero")
# else:
#     print("Negative number")

#  ===============Flowchart==============
# score = int(input("your score : "))
# if score >= 50 :
#     print("pass")
# else :
#     print("fail")
    
#  ===================Flowchart2============
# age = 25
# income = 2500
# if age >= 18 and age <= 65 and income > 30000 :
#     print("your are eligible for the loan")
# else :
#     print("you are not eligible for the loan")

#  ======================Ex4==================
# print("Please select operation -")
# print("1. Add")
# print("2. Subtract")
# print("3. Multiply")
# print("4. Divide")

# choice = int(input("Select operations form 1, 2, 3, 4 : "))
# num1 = float(input("Enter first number : "))
# num2 = float(input("Enter second number : "))

# if choice == 1:
#     result = num1 + num2
#     print(f"{num1} + {num2} = {result}")
# elif choice == 2:
#     result = num1 - num2
#     print(f"{num1} - {num2} = {result}")
# elif choice == 3:
#     result = num1 * num2
#     print(f"{num1} * {num2} = {result}")
# elif choice == 4:
#     if num2 != 0:
#         result = num1 / num2
#         print(f"{num1} / {num2} = {result}")
#     else:
#         print("Error: Division by zero")
# else:
#     print("Invalid choice")

# ===================for loop==================
# for i in "Hello" :
#      print(i) output# H
#                     # e
#                     # l
#                     # l
#                     # o

# i = ["apple" , "banana" , "grape"]
# for t in i :
#     print(t)

# ==================สระ=================
# your_string = input("Enter a string : ")
# modified_string = ""
# vowels = "aeiouAEIOU"
# for char in your_string:
#     upper_char = char.upper()
#     if upper_char in vowels :
#         modified_string += "*"
#     else:
#         modified_string += upper_char
# print("Modified string:",modified_string)
# output = Enter a string : tam
# Modified string: T*M

# =====================for range=================
# for i in range(5,30,5) : # (start,stop,step)
#     print(i)

# print('Number\tSquare')
# print('--------------')
# for number in range(1,11) :
#     square = number**2
#     print(number , '\t' , square)
# output
# Number  Square
# --------------
# 1        1
# 2        4
# 3        9
# 4        16
# 5        25
# 6        36
# 7        49
# 8        64
# 9        81
# 10       100

# print('KPH\tMPH')
# print('--------------')
# for KPH in range(60,140,10) :
#     MPH=KPH*0.6214 
#     print(KPH , '\t' , MPH,)
# output
# KPH     MPH
# --------------
# 60       37.284
# 70       43.498
# 80       49.711999999999996
# 90       55.925999999999995
# 100      62.13999999999999
# 110      68.354
# 120      74.568
# 130      80.782
