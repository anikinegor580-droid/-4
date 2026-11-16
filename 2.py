class Book:
    def __init__(self, title, author, isbn, year, pages):
        if pages <= 0:
            raise ValueError("Количество страниц должно быть положительным")
        self.title = title
        self.author = author
        self.isbn = isbn
        self.year = year
        self.pages = pages
        self._is_available = True
        self._last_read_pages = 0

    @property
    def is_available(self):
        return self._is_available

    @property
    def last_read_pages(self):
        return self._last_read_pages

    def borrow(self):
        if not self._is_available:
            raise ValueError("Книга уже выдана")
        self._is_available = False

    def give_back(self, pages_read):
        if self._is_available:
            raise ValueError("Книга и так находится на полке")
        if not (0 <= pages_read <= self.pages):
            raise ValueError(f"В книге всего {self.pages} страниц")
        self._is_available = True
        self._last_read_pages = pages_read

    def __eq__(self, other):
        if not isinstance(other, Book):
            return NotImplemented
        return self.isbn == other.isbn

    def __lt__(self, other):
        if not isinstance(other, Book):
            return NotImplemented
        return self.year < other.year

    def __repr__(self):
        return (
            f"Book({self.title!r}, {self.author!r}, "
            f"{self.isbn!r}, {self.year}, {self.pages})"
        )


if __name__ == "__main__":
    b = Book("1984", "Оруэлл", "123", 1949, 328)
    print(b.is_available)     
    print(b.last_read_pages)  

    b.borrow()
    print(b.is_available)     

    try:
        b.borrow()
    except ValueError as e:
        print(f"ValueError: {e}")

    try:
        b.is_available = True
    except AttributeError:
        print("AttributeError: нельзя изменить свойство напрямую")

    try:
        b.give_back(400)
    except ValueError as e:
        print(f"ValueError: {e}")

    print(b.is_available)     
    b.give_back(120)
    print(b.last_read_pages)  
    print(b == Book("1984", "Оруэлл", "123", 1949, 328))  

    old = Book("Мы", "Замятин", "456", 1924, 224)
    print(sorted([b, old]))   
