class Restaurant():
    def __init__(self, name=None, address=None, photo=None, timing=None, priceRange=None, rating=None, link=None):
        self.name = name
        self.address = address
        self.photo = photo  #this is a url
        self.timing = timing
        self.priceRange = priceRange
        self.rating = rating
        self.link = link
    
    def __repr__(self):
        return '<Restauarant {}\n address {}\n photo {}\n timing {}, priceRange {}\n rating {}\n link {}'.format(self.name, self.address, self.photo, self.timing, self.priceRange, self.rating, self.link)
