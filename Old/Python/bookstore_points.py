# CSU Global Bookstore Points
# Option 2: Conditional Logic

books_purchased = int(input("Enter the number of books purchased this month: "))

if books_purchased >= 8:
    points = 60
elif books_purchased >= 6:
    points = 30
elif books_purchased >= 4:
    points = 15
elif books_purchased >= 2:
    points = 5
else:
    points = 0

print(f"You earned {points} points this month.")
