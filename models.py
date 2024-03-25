import sqlite3

def fetch_customer_by_id(customer_id):
    conn = sqlite3.connect('restaurant_reviews.db')
    c = conn.cursor()
    
    c.execute("SELECT * FROM customers WHERE id=?", (customer_id,))
    customer_data = c.fetchone()
    
    conn.close()
    
    if customer_data:
        customer_instance = Customer(customer_data[1], customer_data[2])  
        customer_instance.id = customer_data[0]  
        return customer_instance
    else:
        return None
    
def fetch_restaurant_by_id(restaurant_id):
    conn = sqlite3.connect('restaurant_reviews.db')
    c = conn.cursor()
    
    c.execute("SELECT * FROM restaurants WHERE id=?", (restaurant_id,))
    restaurant_data = c.fetchone()
    
    conn.close()
    
    if restaurant_data:
        restaurant_instance = Restaurant(restaurant_data[1], restaurant_data[2])  
        restaurant_instance.id = restaurant_data[0] 
        return restaurant_instance
    else:
        return None

class Restaurant:
    def __init__(self, name, price):
        self.id = None  
        self.name = name
        self.price = price

    def reviews(self):
        conn = sqlite3.connect('restaurant_reviews.db')
        c = conn.cursor()
        
        c.execute("SELECT * FROM reviews WHERE restaurant_id=?", (self.id,))
        reviews_data = c.fetchall()
        
        conn.close()
        
        reviews = []
        for review_data in reviews_data:
            review_instance = Review(review_data[0], review_data[1], review_data[2], review_data[3])  # Add the review ID to the Review instance
        reviews.append(review_instance)
        
        return reviews
    
    def customers(self):
        conn = sqlite3.connect('restaurant_reviews.db')
        c = conn.cursor()
        
        c.execute("SELECT DISTINCT c.* FROM customers c INNER JOIN reviews r ON c.id = r.customer_id WHERE r.restaurant_id=?", (self.id,))
        customers_data = c.fetchall()
        
        conn.close()
        
        customers = []
        for customer_data in customers_data:
            customer_instance = Customer(customer_data[1], customer_data[2])
            customer_instance.id = customer_data[0]  
            customers.append(customer_instance)
        
        return customers
    
    @classmethod
    def fanciest(cls):
        conn = sqlite3.connect('restaurant_reviews.db')
        c = conn.cursor()
        
        c.execute("SELECT * FROM restaurants ORDER BY price DESC LIMIT 1")
        restaurant_data = c.fetchone()
        
        conn.close()
        
        if restaurant_data:
            fanciest_restaurant = Restaurant(restaurant_data[1], restaurant_data[2])
            fanciest_restaurant.id = restaurant_data[0]
            return fanciest_restaurant
        else:
            return None

    def all_reviews(self):
        reviews = self.reviews()
        formatted_reviews = []
        for review in reviews:
            customer = review.customer().full_name()
            formatted_reviews.append(f"Review for {self.name} by {customer}: {review.star_rating} stars.")
        return formatted_reviews

class Customer:
    
    def __init__(self, first_name, last_name):
        self.id = None 
        self.first_name = first_name
        self.last_name = last_name

    def reviews(self):
        conn = sqlite3.connect('restaurant_reviews.db')
        c = conn.cursor()
        
        c.execute("SELECT * FROM reviews WHERE customer_id=?", (self.id,))
        reviews_data = c.fetchall()
        
        conn.close()
        
        reviews = []
        for review_data in reviews_data:
            review_instance = reviews(review_data[1], review_data[2], review_data[3])
            review_instance.id = review_data[0]  
            reviews.append(review_instance)
        
        return reviews   

    def restaurants(self):
        conn = sqlite3.connect('restaurant_reviews.db')
        c = conn.cursor()
        
        c.execute("SELECT DISTINCT r.* FROM restaurants r INNER JOIN reviews rev ON r.id = rev.restaurant_id WHERE rev.customer_id=?", (self.id,))
        restaurants_data = c.fetchall()
        
        conn.close()
        
        restaurants = []
        for restaurant_data in restaurants_data:
            restaurant_instance = Restaurant(restaurant_data[1], restaurant_data[2])
            restaurant_instance.id = restaurant_data[0]  
            restaurants.append(restaurant_instance)
        
        return restaurants 

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def favorite_restaurant(self):
        conn = sqlite3.connect('restaurant_reviews.db')
        c = conn.cursor()
        
        c.execute("SELECT r.* FROM restaurants r INNER JOIN reviews rev ON r.id = rev.restaurant_id WHERE rev.customer_id=? ORDER BY rev.star_rating DESC LIMIT 1", (self.id,))
        restaurant_data = c.fetchone()
        
        conn.close()
        
        if restaurant_data:
            favorite_restaurant = Restaurant(restaurant_data[1], restaurant_data[2])
            favorite_restaurant.id = restaurant_data[0]
            return favorite_restaurant
        else:
            return None

    def add_review(self, restaurant, rating):
        conn = sqlite3.connect('restaurant_reviews.db')
        c = conn.cursor()
        
        c.execute("INSERT INTO reviews (restaurant_id, customer_id, star_rating) VALUES (?, ?, ?)", (restaurant.id, self.id, rating))
        conn.commit()
        
        conn.close()

    def delete_reviews(self, restaurant):
        conn = sqlite3.connect('restaurant_reviews.db')
        c = conn.cursor()
    
        c.execute("DELETE FROM reviews WHERE restaurant_id=? AND customer_id=?", (restaurant.id, self.id))
        conn.commit()
    
        conn.close()
       
class Review:
    def __init__(self, id, restaurant_id, customer_id, star_rating):
        self.id = None
        self.restaurant_id = restaurant_id
        self.customer_id = customer_id
        self.star_rating = star_rating

    def restaurant(self):
        restaurant_instance = fetch_restaurant_by_id(self.restaurant_id)
        return restaurant_instance

    def customer(self):
        customer_instance = fetch_customer_by_id(self.customer_id)
        return customer_instance

    def full_review(self):
        restaurant = self.restaurant().name
        customer = self.customer().full_name()
        return f"Review for {restaurant} by {customer}: {self.star_rating} stars."