from Source.Book import Book
titles = [
    'The Hunger Games',
    'Harry Potter and the Philosopher\'s Stone',
    'Harry Potter and the Chamber of Secrets',
    'Harry Potter and the Prisoner of Azkaban',
    'Harry Potter and the Goblet of Fire'
]
authors = ['Suzanne Collins'] + ['J.K. Rowling'] * 4
releaseYears = [
    '2008',
    '1997',
    '1998',
    '1999',
    '2000'
]

imagePaths = [
    '/static/The Hunger Games.jpg',
    '/static/Harry Potter and the Philosopher\'s Stone.jpg',
    '/static/Harry Potter and the Chamber of Secrets.jpg',
    '/static/Harry Potter and the Prisoner of Azkaban.jpg',
    '/static/Harry Potter and the Goblet of Fire.jpg'
]

descriptions = [
    r"""In Suzanne Collins' dystopian masterpiece, "The Hunger Games", 16-year-old Katniss Everdeen volunteers to """
    'replace her sister in a televised survival competition, where 24 participants from 12 districts fight to the '
    'death. '] + ['Lorem ipsum dolor sit amet, consectetur adipiscing elit.'] * 4

prices = [
    "5.50",
    "5.60",
    "5.70",
    "5.80",
    "5.90"
]
booksForTest = []
for i in range(5):
    booksForTest.append(Book(titles[i], authors[i], releaseYears[i], imagePaths[i], descriptions[i], prices[i]))