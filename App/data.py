from datetime import datetime
import requests
import random
from App.models import Book

def saveData():
    for j in range(1, 35):  # Loop through pages
        url = f'https://frappe.io/api/method/frappe-library?page={j}&title=and'
        response = requests.get(url)

        # Ensure response is valid
        if response.status_code != 200:
            print(f"Failed to fetch data from page {j}: {response.status_code}")
            continue

        data = response.json()
        if 'message' not in data:
            print(f"No 'message' field in API response for page {j}")
            continue

        data = data['message']

        for i in data:
            # Handle publication_date
            original_date = i.get('publication_date')
            try:
                if original_date and original_date != '0':
                    formatted_date = datetime.strptime(original_date, "%m/%d/%Y").strftime("%Y-%m-%d")
                else:
                    formatted_date = None
            except ValueError:
                print(f"Invalid publication_date for book {i['title']}: {original_date}")
                formatted_date = None

            # Handle average_rating
            try:
                average_rating = float(i.get('average_rating', 0))
            except (ValueError, TypeError):
                print(f"Invalid average_rating for book {i['title']}: {i.get('average_rating')}")
                average_rating = None  # Assign None or a default value

            # Handle price (optional randomization)
            price = random.randint(100, 1000)
            stock = random.randint(10,150)

            # Create and save the book object
            try:
                Book.objects.create(
                    book_id=i['bookID'],
                    title=i['title'],
                    author=i['authors'],
                    average_rating=average_rating,
                    language_code=i['language_code'],
                    publication_date=formatted_date,
                    publisher=i['publisher'],
                    price=price,
                    stock=stock
                )
            except Exception as e:
                print(f"Error saving book {i['title']}: {e}")
                continue

    return "Data saved successfully!"
