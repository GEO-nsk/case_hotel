hotel_file_name = 'fund.txt'
booking_file = 'booking_copy.txt'

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
                    if line_list[3] == 'стандарт':
                        self.single_free[line_list[0]].append(2900)
                        self.single_free[line_list[0]].append(3180)
                        self.single_free[line_list[0]].append(3900)
                    if line_list[3] == 'стандарт_улучшенный':
                        self.single_free[line_list[0]].append(3480)
                        self.single_free[line_list[0]].append(3760)
                        self.single_free[line_list[0]].append(4480)
                    if line_list[3] == 'апартамент':
                        self.single_free[line_list[0]].append(4350)
                        self.single_free[line_list[0]].append(4630)
                        self.single_free[line_list[0]].append(5350)

                if line_list[1] == 'двухместный':
                    self.double_free[line_list[0]] = line_list
                    if line_list[3] == 'стандарт':
                        self.double_free[line_list[0]].append(2300)
                        self.double_free[line_list[0]].append(2580)
                        self.double_free[line_list[0]].append(3300)
                    if line_list[3] == 'стандарт_улучшенный':
                        self.double_free[line_list[0]].append(2760)
                        self.double_free[line_list[0]].append(3040)
                        self.double_free[line_list[0]].append(3760)
                    if line_list[3] == 'апартамент':
                        self.double_free[line_list[0]].append(3450)
                        self.double_free[line_list[0]].append(3730)
                        self.double_free[line_list[0]].append(4450)

                if line_list[1] == 'полулюкс':
                    self.half_luxe_free[line_list[0]] = line_list
                    if line_list[3] == 'стандарт':
                        self.half_luxe_free[line_list[0]].append(3200)
                        self.half_luxe_free[line_list[0]].append(3480)
                        self.half_luxe_free[line_list[0]].append(4200)
                    if line_list[3] == 'стандарт_улучшенный':
                        self.half_luxe_free[line_list[0]].append(3840)
                        self.half_luxe_free[line_list[0]].append(4120)
                        self.half_luxe_free[line_list[0]].append(4840)
                    if line_list[3] == 'апартамент':
                        self.half_luxe_free[line_list[0]].append(4800)
                        self.half_luxe_free[line_list[0]].append(5080)
                        self.half_luxe_free[line_list[0]].append(5800)

                if line_list[1] == 'люкс':
                    self.luxe_free[line_list[0]] = line_list
                    if line_list[3] == 'стандарт':
                        self.luxe_free[line_list[0]].append(4100)
                        self.luxe_free[line_list[0]].append(4380)
                        self.luxe_free[line_list[0]].append(5100)
                    if line_list[3] == 'стандарт_улучшенный':
                        self.luxe_free[line_list[0]].append(4920)
                        self.luxe_free[line_list[0]].append(5200)
                        self.luxe_free[line_list[0]].append(5920)
                    if line_list[3] == 'апартамент':
                        self.luxe_free[line_list[0]].append(6150)
                        self.luxe_free[line_list[0]].append(6430)
                        self.luxe_free[line_list[0]].append(7150)

hotel = Hotel()

hotel.read_file(hotel_file_name)


class Clients(Hotel):
    def init(self):
        self.info = {'Количество людей': '',
                     'Дата въезда': '',
                     'Количество дней': '',
                     'Максимальная сумма': ''}

    def read_booking_file(self, booking):
        with open(booking_file, 'r', encoding='utf-8') as file:
            for item in file:
                line_list = []
                for itr in item.split():
                    line_list.append(itr)

                self.info['Количество людей'] = line_list[4]
                self.info['Дата въезда'] = line_list[5]
                self.info['Количество дней'] = line_list[6]
                self.info['Максимальная сумма'] = line_list[7]

                all_possible_costs = []
                '''
                if self.info['Количество людей'] == 1:
                    for k,v in self.single_free:
                        all_possible_costs.append(v[4])
                        all_possible_costs.append(v[5])
                        all_possible_costs.append(v[6])
                
                print(all_possible_costs)
                '''

    def repr(self):
        return f'Info: {self.info}'


client = Clients()
client.read_booking_file(booking_file)
print(client)