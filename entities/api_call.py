class APICall:
    
    def __init__(self, call_timestamp, status, cities_fetched):
        self.call_timestamp = call_timestamp
        self.status = status
        self.cities_fetched = cities_fetched
