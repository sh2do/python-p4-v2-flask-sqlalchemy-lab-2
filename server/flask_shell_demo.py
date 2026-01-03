#!/usr/bin/env python3
"""
Flask shell demonstration script for the customer review system.
This script demonstrates the complete workflow in an interactive manner
similar to what you would do in a Flask shell.
"""

from app import app
from models import db, Customer, Item, Review


def flask_shell_demo():
    """Demonstrate the complete workflow as if in Flask shell."""
    
    with app.app_context():
        print("=== Flask Shell Demo: Customer Review System ===\n")
        
        # Simulate Flask shell commands
        print(">>> # Starting Flask shell demo")
        print(">>> from models import db, Customer, Item, Review")
        print()
        
        # Create customers
        print(">>> # Create customers")
        print(">>> customer1 = Customer(name='Alice Johnson')")
        customer1 = Customer(name='Alice Johnson')
        
        print(">>> customer2 = Customer(name='Bob Smith')")
        customer2 = Customer(name='Bob Smith')
        
        print(">>> db.session.add_all([customer1, customer2])")
        db.session.add_all([customer1, customer2])
        
        print(">>> db.session.commit()")
        db.session.commit()
        print(f"Created: {customer1}, {customer2}")
        print()
        
        # Create items
        print(">>> # Create items")
        print(">>> item1 = Item(name='Laptop', price=999.99)")
        item1 = Item(name='Laptop', price=999.99)
        
        print(">>> item2 = Item(name='Mouse', price=29.99)")
        item2 = Item(name='Mouse', price=29.99)
        
        print(">>> db.session.add_all([item1, item2])")
        db.session.add_all([item1, item2])
        
        print(">>> db.session.commit()")
        db.session.commit()
        print(f"Created: {item1}, {item2}")
        print()
        
        # Create reviews
        print(">>> # Create reviews")
        print(">>> review1 = Review(comment='Great laptop!', customer=customer1, item=item1)")
        review1 = Review(comment='Great laptop!', customer=customer1, item=item1)
        
        print(">>> review2 = Review(comment='Perfect mouse!', customer=customer2, item=item2)")
        review2 = Review(comment='Perfect mouse!', customer=customer2, item=item2)
        
        print(">>> db.session.add_all([review1, review2])")
        db.session.add_all([review1, review2])
        
        print(">>> db.session.commit()")
        db.session.commit()
        print(f"Created: {review1}, {review2}")
        print()
        
        # Test bidirectional relationships
        print(">>> # Test bidirectional relationships")
        print(">>> customer1.reviews")
        print(f"{customer1.reviews}")
        
        print(">>> item1.reviews")
        print(f"{item1.reviews}")
        
        print(">>> review1.customer")
        print(f"{review1.customer}")
        
        print(">>> review1.item")
        print(f"{review1.item}")
        print()
        
        # Test association proxy
        print(">>> # Test association proxy")
        print(">>> customer1.items")
        print(f"{customer1.items}")
        
        print(">>> [item.name for item in customer1.items]")
        print(f"{[item.name for item in customer1.items]}")
        print()
        
        # Test serialization
        print(">>> # Test serialization")
        print(">>> customer1.to_dict()")
        customer_dict = customer1.to_dict()
        print(f"Customer dict keys: {list(customer_dict.keys())}")
        print(f"Has reviews: {'reviews' in customer_dict}")
        print(f"Number of reviews: {len(customer_dict.get('reviews', []))}")
        
        print(">>> item1.to_dict()")
        item_dict = item1.to_dict()
        print(f"Item dict keys: {list(item_dict.keys())}")
        print(f"Has reviews: {'reviews' in item_dict}")
        
        print(">>> review1.to_dict()")
        review_dict = review1.to_dict()
        print(f"Review dict keys: {list(review_dict.keys())}")
        print(f"Has customer: {'customer' in review_dict}")
        print(f"Has item: {'item' in review_dict}")
        print()
        
        print("=== Flask Shell Demo Complete ===")
        print("✓ All operations completed successfully!")


if __name__ == "__main__":
    flask_shell_demo()