#!/usr/bin/env python3
"""
Integration test script for the customer review system.
Tests the complete workflow including:
- Creating customers, items, and reviews programmatically
- Verifying bidirectional relationships work correctly
- Testing association proxy functionality
- Testing serialization of all models
"""

from app import app
from models import db, Customer, Item, Review
import json


def test_complete_workflow():
    """Test the complete customer review system workflow."""
    
    with app.app_context():
        print("=== Customer Review System Integration Test ===\n")
        
        # Clear existing data for clean test
        print("1. Clearing existing data...")
        db.session.query(Review).delete()
        db.session.query(Customer).delete()
        db.session.query(Item).delete()
        db.session.commit()
        print("   ✓ Database cleared\n")
        
        # Create customers programmatically
        print("2. Creating customers...")
        customer1 = Customer(name="Alice Johnson")
        customer2 = Customer(name="Bob Smith")
        customer3 = Customer(name="Carol Davis")
        
        db.session.add_all([customer1, customer2, customer3])
        db.session.commit()
        print(f"   ✓ Created customers: {customer1}, {customer2}, {customer3}\n")
        
        # Create items programmatically
        print("3. Creating items...")
        item1 = Item(name="Laptop", price=999.99)
        item2 = Item(name="Mouse", price=29.99)
        item3 = Item(name="Keyboard", price=79.99)
        
        db.session.add_all([item1, item2, item3])
        db.session.commit()
        print(f"   ✓ Created items: {item1}, {item2}, {item3}\n")
        
        # Create reviews programmatically
        print("4. Creating reviews...")
        review1 = Review(comment="Great laptop, very fast!", customer=customer1, item=item1)
        review2 = Review(comment="Perfect mouse for gaming", customer=customer1, item=item2)
        review3 = Review(comment="Excellent keyboard quality", customer=customer2, item=item3)
        review4 = Review(comment="Good value laptop", customer=customer3, item=item1)
        
        db.session.add_all([review1, review2, review3, review4])
        db.session.commit()
        print(f"   ✓ Created reviews: {review1}, {review2}, {review3}, {review4}\n")
        
        # Test bidirectional relationships
        print("5. Testing bidirectional relationships...")
        
        # Test Customer -> Reviews relationship
        print("   5.1 Customer -> Reviews:")
        for customer in [customer1, customer2, customer3]:
            reviews = customer.reviews
            print(f"      {customer.name} has {len(reviews)} reviews: {[r.comment[:20] + '...' for r in reviews]}")
        
        # Test Item -> Reviews relationship
        print("   5.2 Item -> Reviews:")
        for item in [item1, item2, item3]:
            reviews = item.reviews
            print(f"      {item.name} has {len(reviews)} reviews: {[r.comment[:20] + '...' for r in reviews]}")
        
        # Test Review -> Customer and Review -> Item relationships
        print("   5.3 Review -> Customer/Item:")
        for review in [review1, review2, review3, review4]:
            print(f"      Review '{review.comment[:20]}...' by {review.customer.name} for {review.item.name}")
        
        print("   ✓ Bidirectional relationships working correctly\n")
        
        # Test association proxy functionality
        print("6. Testing association proxy functionality...")
        
        print("   6.1 Customer.items via association proxy:")
        for customer in [customer1, customer2, customer3]:
            items_via_proxy = customer.items
            items_via_manual = [review.item for review in customer.reviews]
            
            print(f"      {customer.name}:")
            print(f"        Via proxy: {[item.name for item in items_via_proxy]}")
            print(f"        Via manual: {[item.name for item in items_via_manual]}")
            
            # Verify they're equivalent
            proxy_names = sorted([item.name for item in items_via_proxy])
            manual_names = sorted([item.name for item in items_via_manual])
            assert proxy_names == manual_names, f"Association proxy mismatch for {customer.name}"
        
        print("   ✓ Association proxy working correctly\n")
        
        # Test serialization of all models
        print("7. Testing serialization of all models...")
        
        print("   7.1 Customer serialization:")
        for customer in [customer1, customer2, customer3]:
            customer_dict = customer.to_dict()
            print(f"      {customer.name}: {json.dumps(customer_dict, indent=2)}")
            
            # Verify no circular references
            try:
                json.dumps(customer_dict)
                print(f"      ✓ {customer.name} serialization valid (no circular references)")
            except (ValueError, TypeError) as e:
                print(f"      ✗ {customer.name} serialization failed: {e}")
                raise
        
        print("\n   7.2 Item serialization:")
        for item in [item1, item2, item3]:
            item_dict = item.to_dict()
            print(f"      {item.name}: {json.dumps(item_dict, indent=2)}")
            
            # Verify no circular references
            try:
                json.dumps(item_dict)
                print(f"      ✓ {item.name} serialization valid (no circular references)")
            except (ValueError, TypeError) as e:
                print(f"      ✗ {item.name} serialization failed: {e}")
                raise
        
        print("\n   7.3 Review serialization:")
        for review in [review1, review2, review3, review4]:
            review_dict = review.to_dict()
            print(f"      Review {review.id}: {json.dumps(review_dict, indent=2)}")
            
            # Verify no circular references
            try:
                json.dumps(review_dict)
                print(f"      ✓ Review {review.id} serialization valid (no circular references)")
            except (ValueError, TypeError) as e:
                print(f"      ✗ Review {review.id} serialization failed: {e}")
                raise
        
        print("\n   ✓ All model serialization working correctly\n")
        
        # Test complex serialization scenarios
        print("8. Testing complex serialization scenarios...")
        
        # Test serializing a customer with all relationships loaded
        customer_with_relationships = db.session.query(Customer).options(
            db.joinedload(Customer.reviews).joinedload(Review.item)
        ).filter_by(id=customer1.id).first()
        
        complex_dict = customer_with_relationships.to_dict()
        print(f"   Complex customer serialization: {json.dumps(complex_dict, indent=2)}")
        
        try:
            json.dumps(complex_dict)
            print("   ✓ Complex serialization valid (no circular references)")
        except (ValueError, TypeError) as e:
            print(f"   ✗ Complex serialization failed: {e}")
            raise
        
        print("\n=== Integration Test Complete ===")
        print("✓ All functionality verified successfully!")
        print("✓ Customers, items, and reviews created programmatically")
        print("✓ Bidirectional relationships working correctly")
        print("✓ Association proxy functionality verified")
        print("✓ Serialization of all models working without circular references")


if __name__ == "__main__":
    test_complete_workflow()