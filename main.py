hotel_file_name = 'fund.txt'

class Hotel:
    def __init__(self):
        self.single_free = {}
        self.double_free = {}
        self.half_luxe_free = {}
        self.luxe_free = {}
        self.single_full = {}
        self.double_full = {}
        self.half_luxe_full = {}
        self.luxe_full = {}

    def read_file(self, hotel_file_name):
        with open(hotel_file_name, 'r', encoding='utf-8') as file:
            for item in file:
                line_list = []
                for itr in item.split():
                    line_list.append(itr)
                if line_list[1] == 'одноместный':
                    self.single_free[line_list[0]] = line_list
                    self.single_free[line_list[0]].append(2900)
                if line_list[1] == 'двухместный':
                    self.double_free[line_list[0]] = line_list
                    self.double_free[line_list[0]].append(2300)
                if line_list[1] == 'полулюкс':
                    self.half_luxe_free[line_list[0]] = line_list
                    self.half_luxe_free[line_list[0]].append(3200)
                if line_list[1] == 'люкс':
                    self.luxe_free[line_list[0]] = line_list
                    self.luxe_free[line_list[0]].append(4100)

hotel = Hotel()

hotel.read_file(hotel_file_name)

print(hotel.single_free)
