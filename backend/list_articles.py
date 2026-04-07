from app import app
from models import KnowledgeArticle

with app.app_context():
    articles = KnowledgeArticle.query.all()
    
    if articles:
        print(f"Found {len(articles)} knowledge base articles:")
        for article in articles:
            print(f"ID: {article.id}")
            print(f"Title: {article.title}")
            print(f"Category: {article.category}")
            print(f"Author: {article.author}")
            print(f"Created: {article.created_at}")
            print(f"Content: {article.content[:100]}...")  # Show first 100 chars
            print("-" * 50)
    else:
        print("No knowledge base articles found in the database.")
        print("\nPopular articles shown in the sidebar:")
        print("- Sustainable Farming Practices")
        print("- Water Conservation Techniques")
        print("- Natural Pest Control Methods")
        print("- Soil Health Management")
        print("- Crop Rotation Benefits")
        
        print("\nSeasonal Guides shown in the sidebar:")
        print("- Summer Crops")
        print("- Monsoon Farming")
        print("- Winter Crops")
        print("- Spring Planting")