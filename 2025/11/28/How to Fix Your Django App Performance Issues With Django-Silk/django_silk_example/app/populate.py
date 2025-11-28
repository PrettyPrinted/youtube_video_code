from .models import Item, ItemDetail

def populate():
    # Create sample items
    item1 = Item.objects.create(name="Item 1", description="Description for Item 1")
    item2 = Item.objects.create(name="Item 2", description="Description for Item 2")
    item3 = Item.objects.create(name="Item 3", description="Description for Item 3")

    # Create sample item details
    ItemDetail.objects.create(item=item1, detail="Detail 1 for Item 1")
    ItemDetail.objects.create(item=item1, detail="Detail 2 for Item 1")
    ItemDetail.objects.create(item=item2, detail="Detail 1 for Item 2")
    ItemDetail.objects.create(item=item3, detail="Detail 1 for Item 3")
    ItemDetail.objects.create(item=item3, detail="Detail 2 for Item 3")
    ItemDetail.objects.create(item=item3, detail="Detail 3 for Item 3")

    print("Database populated with sample data.")