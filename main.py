hotel_file_name = 'fund.txt'

class Hotel:
    def __init__(self):
        self.single = {}
        self.double = {}
        self.half_luxe = {}
        self.luxe = {}

    def read_file(self, hotel_file_name):
        with open(hotel_file_name, 'r', encoding='utf-8') as file:
            for item in file:
                line_list = []
                for itr in item.split():
                    line_list.append(itr)
                print(line_list)

hotel = Hotel()

hotel.read_file(hotel_file_name)
