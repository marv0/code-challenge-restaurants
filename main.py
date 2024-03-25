import sqlite3
from models import Restaurant, Customer, Review

restaurant1 = Restaurant("Restaurant A", 3)
restaurant2 = Restaurant("Restaurant B", 4)

customer1 = Customer("John", "Doe")
customer2 = Customer("Jane", "Smith")


conn = sqlite3.connect('restaurant_reviews.db')
c = conn.cursor()


review1 = Review(restaurant1.id, customer1.id, 5)
review2 = Review(restaurant2.id, customer2.id, 4)


print(review1.customer())  # should return Customer instance
print(review1.restaurant())  # should return Restaurant instance

print(restaurant1.reviews())  # should return reviews for Restaurant 1
print(restaurant1.customers())  # should return customers who reviewed Restaurant 1

print(customer1.reviews())  # should return reviews by Customer 1
print(customer1.restaurants())  # should return restaurants reviewed by Customer 1


