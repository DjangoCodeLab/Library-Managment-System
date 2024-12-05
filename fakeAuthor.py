import os
import django
from django.db.models import *
from datetime import date
from LMS.settings import LANGUAGE_CODE
from django.db.models import *
# Set up Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LMS.settings')  # Replace 'LMS.settings' with your project's settings module.
django.setup()

from App.models import Book  # Import models after setting up Django

def handle():
    book = Book.objects.all()
    data = {
        'book_id':1,
        'title':'Rich Dad Poor Dad',
        'author':'siddhu',
        'average_rating':3.3,
        'language_code':'en',
        'publication_date':'2002-02-20',
        'publisher':'hennel',
        'price':400,
    }
    #Save the data like this.
    # book.create(
    #     **data 
    # )
    # print(book)
    filterByTitle = book.get(title = "Quicksand")
    filterByLangCode = book.filter(language_code = "en")
    orderByPrice = book.order_by('-price')
    print(orderByPrice)
    print("The filtered language code is:",filterByLangCode)
    print(filterByTitle)
    excludeDate = book.filter(publication_date__gte = date(2000, 1,1))

    averageRate = book.filter(average_rating__gte = 4.0).values_list('title', 'price').count()
    print(averageRate)
    publisherCount = book.filter(publisher__icontains = "Penguin").count()
    print("The count of Penguin  is:",publisherCount)
    priceRange = book.filter(price__gte = 100, price__lte = 500).values('price')
    print(priceRange)
    book.update(price = F('price')*1.10)
    data = book.all().values_list('title','price')
    print(data)
    data = book.aggregate(price = Avg('price'))
    print(data)
    data = book.annotate(
        avg_price = Avg('price'),
        total_books = Count('id')
    )
    for i in data:
        print(f"The Author is {i.author}.Total Count is:{i.total_books}.The average price is:{i.avg_price}")
    


   


    # for i in averageRate:
    #     print(i[0],i[1])
    # for i in averageRate:
    #     print(f'the {i.publisher} and Rating is {i.average_rating}')

    # for i in excludeDate:
    #     print(f'The book is :{(i.title)[:10]} And date is :{i.publication_date}')


    

handle()
