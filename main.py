hotel_file_name = 'fund.txt'
booking_file = 'booking_copy.txt'

class Date:
    def __init__(self, entry_date, duration):
        self.entry_date = entry_date
        self.dd = int(entry_date[:2])
        self.mm = int(entry_date[3:5])
        self.yyyy = int(entry_date[6:10])
        self.duration = int(duration)
        self.departure_date = None

    def get_departure_date(self):
        self.dd += self.duration
        if self.dd > 31:
            self.mm += 1
            self.dd -= 31
        if self.mm > 12:
            self.yyyy += 1
            self.mm -= 12
        self.departure_date = f'{self.dd:02d}.{self.mm:02d}.{self.yyyy}'
        return self.departure_date

    def __repr__(self):
        return f'Дата въезда: {self.entry_date}\nДата выезда: {self.departure_date}'


class Hotel(Date):
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
    def __init__(self):
        self.info = {'Количество людей': '',
                     'Дата въезда': '',
                     'Количество дней': '',
                     'Максимальная сумма': ''}

    def read_booking_file(self, booking_file):
        with open(booking_file, 'r', encoding='utf-8') as file:
            for item in file:
                line_list = []
                for itr in item.split():
                    line_list.append(itr)

                self.info['дата'] = line_list[0]
                self.info['Количество людей'] = line_list[4]
                self.info['Дата въезда'] = line_list[5]
                self.info['Количество дней'] = line_list[6]
                self.info['Максимальная сумма'] = line_list[7]

                all_possible_costs = []

                out_list_single = []
                for k,v in hotel.single_full.items():
                    if v[7] == self.info['дата']:
                        hotel.single_free[k] = v
                        out_list_single.append(k)
                for i in out_list_single:
                    del hotel.single_full[i]

                out_list_double = []
                for k, v in hotel.double_full.items():
                    if v[7] == self.info['дата']:
                        hotel.double_free[k] = v
                        out_list_double.append(k)
                for i in out_list_double:
                    del hotel.double_full[i]

                out_list_half_luxe = []
                for k, v in hotel.half_luxe_full.items():
                    if v[7] == self.info['дата']:
                        hotel.half_luxe_free[k] = v
                        out_list_half_luxe.append(k)
                for i in out_list_half_luxe:
                    del hotel.half_luxe_full[i]

                out_list_luxe = []
                for k, v in hotel.luxe_full.items():
                    if v[7] == self.info['дата']:
                        hotel.luxe_free[k] = v
                        out_list_luxe.append(k)
                for i in out_list_luxe:
                    del hotel.luxe_full[i]


                if self.info['Количество людей'] == '1':
                    for i in hotel.single_free:
                        if hotel.single_free[i][4] <= int(self.info['Максимальная сумма']):
                            all_possible_costs.append(hotel.single_free[i][4])
                        if hotel.single_free[i][5] <= int(self.info['Максимальная сумма']):
                            all_possible_costs.append(hotel.single_free[i][5])
                        if hotel.single_free[i][6] <= int(self.info['Максимальная сумма']):
                            all_possible_costs.append(hotel.single_free[i][6])
                    for i in hotel.half_luxe_free:
                        if hotel.half_luxe_free[i][2] =='1':
                            if hotel.half_luxe_free[i][4] <= int(self.info['Максимальная сумма']):
                                all_possible_costs.append(hotel.half_luxe_free[i][4])
                            if hotel.half_luxe_free[i][5] <= int(self.info['Максимальная сумма']):
                                all_possible_costs.append(hotel.half_luxe_free[i][5])
                            if hotel.half_luxe_free[i][6] <= int(self.info['Максимальная сумма']):
                                all_possible_costs.append(hotel.half_luxe_free[i][6])
                    print(all_possible_costs)
                    if len(all_possible_costs):
                        maxi_cost = max(all_possible_costs)
                        print(maxi_cost)

                        cnt = 0
                        for k,v in hotel.single_free.items():
                            if v[4] == maxi_cost or v[5] == maxi_cost or v[6] == maxi_cost:
                                hotel.single_full[k] = v
                                new_date = Date(self.info['Дата въезда'], self.info['Количество дней'])
                                hotel.single_full[k].append(new_date.get_departure_date())
                                cnt = k
                                break
                        for k,v in hotel.half_luxe_free.items():
                            if v[2] == '1':
                                if v[4] == maxi_cost or v[5] == maxi_cost or v[6] == maxi_cost:
                                    hotel.half_luxe_full[k] = v
                                    new_date = Date(self.info['Дата въезда'], self.info['Количество дней'])
                                    hotel.half_luxe_full[k].append(new_date.get_departure_date())
                                    cnt = k
                                    break

                        if cnt in hotel.single_free.keys():
                            del hotel.single_free[str(cnt)]
                        if cnt in hotel.half_luxe_free.keys():
                            del hotel.half_luxe_free[str(cnt)]
                        #print(hotel.single_full)
                        #print(hotel.single_free)
                    else:
                        if self.info['Количество людей'] == '1':
                            for i in hotel.double_free:
                                if hotel.double_free[i][4] <= int(self.info['Максимальная сумма']):
                                    all_possible_costs.append(hotel.double_free[i][4])
                                if hotel.double_free[i][5] <= int(self.info['Максимальная сумма']):
                                    all_possible_costs.append(hotel.double_free[i][5])
                                if hotel.double_free[i][6] <= int(self.info['Максимальная сумма']):
                                    all_possible_costs.append(hotel.double_free[i][6])
                            for i in hotel.half_luxe_free:
                                if hotel.half_luxe_free[i][2] == '1':
                                    if hotel.half_luxe_free[i][4] <= int(self.info['Максимальная сумма']):
                                        all_possible_costs.append(hotel.half_luxe_free[i][4])
                                    if hotel.half_luxe_free[i][5] <= int(self.info['Максимальная сумма']):
                                        all_possible_costs.append(hotel.half_luxe_free[i][5])
                                    if hotel.half_luxe_free[i][6] <= int(self.info['Максимальная сумма']):
                                        all_possible_costs.append(hotel.half_luxe_free[i][6])
                            print(all_possible_costs)
                            if len(all_possible_costs):
                                maxi_cost = max(all_possible_costs)
                                print(maxi_cost)

                                cnt = 0
                                for k, v in hotel.double_free.items():
                                    if v[4] == maxi_cost or v[5] == maxi_cost or v[6] == maxi_cost:
                                        hotel.double_full[k] = v
                                        new_date = Date(self.info['Дата въезда'], self.info['Количество дней'])
                                        hotel.double_full[k].append(new_date.get_departure_date())
                                        cnt = k
                                        break
                                for k, v in hotel.half_luxe_free.items():
                                    if v[2] == '1':
                                        if v[4] == maxi_cost or v[5] == maxi_cost or v[6] == maxi_cost:
                                            hotel.half_luxe_full[k] = v
                                            new_date = Date(self.info['Дата въезда'], self.info['Количество дней'])
                                            hotel.half_luxe_full[k].append(new_date.get_departure_date())
                                            cnt = k
                                            break

                                if cnt in hotel.double_free.keys():
                                    del hotel.double_free[str(cnt)]
                                if cnt in hotel.half_luxe_free.keys():
                                    del hotel.half_luxe_free[str(cnt)]
                                # print(hotel.single_full)
                                # print(hotel.single_free)
                            else:
                                print('вы бомж')

                if self.info['Количество людей'] == '2':
                    for i in hotel.double_free:
                        if hotel.double_free[i][4] <= int(self.info['Максимальная сумма']):
                            all_possible_costs.append(hotel.double_free[i][4])
                        if hotel.double_free[i][5] <= int(self.info['Максимальная сумма']):
                            all_possible_costs.append(hotel.double_free[i][5])
                        if hotel.double_free[i][6] <= int(self.info['Максимальная сумма']):
                            all_possible_costs.append(hotel.double_free[i][6])
                    for i in hotel.half_luxe_free:
                        if hotel.half_luxe_free[i][2] == '2':
                            if hotel.half_luxe_free[i][4] <= int(self.info['Максимальная сумма']):
                                all_possible_costs.append(hotel.half_luxe_free[i][4])
                            if hotel.half_luxe_free[i][5] <= int(self.info['Максимальная сумма']):
                                all_possible_costs.append(hotel.half_luxe_free[i][5])
                            if hotel.half_luxe_free[i][6] <= int(self.info['Максимальная сумма']):
                                all_possible_costs.append(hotel.half_luxe_free[i][6])
                    print(all_possible_costs)
                    if len(all_possible_costs):
                        maxi_cost = max(all_possible_costs)
                        print(maxi_cost)

                        cnt = 0
                        for k,v in hotel.double_free.items():
                            if v[4] == maxi_cost or v[5] == maxi_cost or v[6] == maxi_cost:
                                hotel.double_full[k] = v
                                new_date = Date(self.info['Дата въезда'], self.info['Количество дней'])
                                hotel.double_full[k].append(new_date.get_departure_date())
                                cnt = k
                                break
                        for k,v in hotel.half_luxe_free.items():
                            if v[2] == '2':
                                if v[4] == maxi_cost or v[5] == maxi_cost or v[6] == maxi_cost:
                                    hotel.half_luxe_full[k] = v
                                    new_date = Date(self.info['Дата въезда'], self.info['Количество дней'])
                                    hotel.half_luxe_full[k].append(new_date.get_departure_date())
                                    cnt = k
                                    break

                        if cnt in hotel.double_free.keys():
                            del hotel.double_free[str(cnt)]
                        if cnt in hotel.half_luxe_free.keys():
                            del hotel.half_luxe_free[str(cnt)]
                        #print(hotel.single_full)
                        #print(hotel.single_free)
                    else:
                        if self.info['Количество людей'] == '2':
                            for i in hotel.half_luxe_free:
                                if hotel.half_luxe_free[i][2] == '2':
                                    if hotel.half_luxe_free[i][4] <= int(self.info['Максимальная сумма']):
                                        all_possible_costs.append(hotel.half_luxe_free[i][4])
                                    if hotel.half_luxe_free[i][5] <= int(self.info['Максимальная сумма']):
                                        all_possible_costs.append(hotel.half_luxe_free[i][5])
                                    if hotel.half_luxe_free[i][6] <= int(self.info['Максимальная сумма']):
                                        all_possible_costs.append(hotel.half_luxe_free[i][6])
                            for i in hotel.luxe_free:
                                if hotel.luxe_free[i][2] == '2':
                                    if hotel.luxe_free[i][4] <= int(self.info['Максимальная сумма']):
                                        all_possible_costs.append(hotel.luxe_free[i][4])
                                    if hotel.luxe_free[i][5] <= int(self.info['Максимальная сумма']):
                                        all_possible_costs.append(hotel.luxe_free[i][5])
                                    if hotel.luxe_free[i][6] <= int(self.info['Максимальная сумма']):
                                        all_possible_costs.append(hotel.luxe_free[i][6])
                            print(all_possible_costs)
                            if len(all_possible_costs):
                                maxi_cost = max(all_possible_costs)
                                print(maxi_cost)

                                cnt = 0
                                for k, v in hotel.half_luxe_free.items():
                                    if v[2] == '2':
                                        if v[4] == maxi_cost or v[5] == maxi_cost or v[6] == maxi_cost:
                                            hotel.half_luxe_full[k] = v
                                            new_date = Date(self.info['Дата въезда'], self.info['Количество дней'])
                                            hotel.half_luxe_full[k].append(new_date.get_departure_date())
                                            cnt = k
                                            break
                                for k, v in hotel.luxe_free.items():
                                    if v[2] == '2':
                                        if v[4] == maxi_cost or v[5] == maxi_cost or v[6] == maxi_cost:
                                            hotel.luxe_full[k] = v
                                            new_date = Date(self.info['Дата въезда'], self.info['Количество дней'])
                                            hotel.luxe_full[k].append(new_date.get_departure_date())
                                            cnt = k
                                            break

                                if cnt in hotel.half_luxe_free.keys():
                                    del hotel.half_luxe_free[str(cnt)]
                                if cnt in hotel.luxe_free.keys():
                                    del hotel.luxe_free[str(cnt)]
                                # print(hotel.single_full)
                                # print(hotel.single_free)
                            else:
                                print('вы бомж')

                if self.info['Количество людей'] == '3':
                    for i in hotel.half_luxe_free:
                        if hotel.half_luxe_free[i][2] == '3':
                            if hotel.half_luxe_free[i][4] <= int(self.info['Максимальная сумма']):
                                all_possible_costs.append(hotel.half_luxe_free[i][4])
                            if hotel.half_luxe_free[i][5] <= int(self.info['Максимальная сумма']):
                                all_possible_costs.append(hotel.half_luxe_free[i][5])
                            if hotel.half_luxe_free[i][6] <= int(self.info['Максимальная сумма']):
                                all_possible_costs.append(hotel.half_luxe_free[i][6])
                    for i in hotel.luxe_free:
                        if hotel.luxe_free[i][2] == '3':
                            if hotel.luxe_free[i][4] <= int(self.info['Максимальная сумма']):
                                all_possible_costs.append(hotel.luxe_free[i][4])
                            if hotel.luxe_free[i][5] <= int(self.info['Максимальная сумма']):
                                all_possible_costs.append(hotel.luxe_free[i][5])
                            if hotel.luxe_free[i][6] <= int(self.info['Максимальная сумма']):
                                all_possible_costs.append(hotel.luxe_free[i][6])
                    print(all_possible_costs)
                    if len(all_possible_costs):
                        maxi_cost = max(all_possible_costs)
                        print(maxi_cost)

                        cnt = 0
                        for k,v in hotel.half_luxe_free.items():
                            if v[2] == '3':
                                if v[4] == maxi_cost or v[5] == maxi_cost or v[6] == maxi_cost:
                                    hotel.half_luxe_full[k] = v
                                    new_date = Date(self.info['Дата въезда'], self.info['Количество дней'])
                                    hotel.half_luxe_full[k].append(new_date.get_departure_date())
                                    cnt = k
                                    break
                        for k,v in hotel.luxe_free.items():
                            if v[2] == '3':
                                if v[4] == maxi_cost or v[5] == maxi_cost or v[6] == maxi_cost:
                                    hotel.luxe_full[k] = v
                                    new_date = Date(self.info['Дата въезда'], self.info['Количество дней'])
                                    hotel.luxe_full[k].append(new_date.get_departure_date())
                                    cnt = k
                                    break

                        if cnt in hotel.half_luxe_free.keys():
                            del hotel.half_luxe_free[str(cnt)]
                        if cnt in hotel.luxe_free.keys():
                            del hotel.luxe_free[str(cnt)]
                        #print(hotel.single_full)
                        #print(hotel.single_free)
                    else:
                        if self.info['Количество людей'] == '3':
                            for i in hotel.luxe_free:
                                if hotel.luxe_free[i][2] == '3':
                                    if hotel.luxe_free[i][4] <= int(self.info['Максимальная сумма']):
                                        all_possible_costs.append(hotel.luxe_free[i][4])
                                    if hotel.luxe_free[i][5] <= int(self.info['Максимальная сумма']):
                                        all_possible_costs.append(hotel.luxe_free[i][5])
                                    if hotel.luxe_free[i][6] <= int(self.info['Максимальная сумма']):
                                        all_possible_costs.append(hotel.luxe_free[i][6])
                            print(all_possible_costs)
                            if len(all_possible_costs):
                                maxi_cost = max(all_possible_costs)
                                print(maxi_cost)

                                cnt = 0
                                for k, v in hotel.luxe_free.items():
                                    if v[2] == '3':
                                        if v[4] == maxi_cost or v[5] == maxi_cost or v[6] == maxi_cost:
                                            hotel.luxe_full[k] = v
                                            new_date = Date(self.info['Дата въезда'], self.info['Количество дней'])
                                            hotel.luxe_full[k].append(new_date.get_departure_date())
                                            cnt = k
                                            break

                                if cnt in hotel.half_luxe_free.keys():
                                    del hotel.half_luxe_free[str(cnt)]
                                if cnt in hotel.luxe_free.keys():
                                    del hotel.luxe_free[str(cnt)]
                                # print(hotel.single_full)
                                # print(hotel.single_free)
                            else:
                                print('вы бомж')

                if self.info['Количество людей'] == '4' or self.info['Количество людей'] == '5' or \
                        self.info['Количество людей'] == '6':
                    for i in hotel.luxe_free:
                        if hotel.luxe_free[i][2] == '4' or hotel.luxe_free[i][2] == '5' or \
                                hotel.luxe_free[i][2] == '6':
                            if hotel.luxe_free[i][4] <= int(self.info['Максимальная сумма']):
                                all_possible_costs.append(hotel.luxe_free[i][4])
                            if hotel.luxe_free[i][5] <= int(self.info['Максимальная сумма']):
                                all_possible_costs.append(hotel.luxe_free[i][5])
                            if hotel.luxe_free[i][6] <= int(self.info['Максимальная сумма']):
                                all_possible_costs.append(hotel.luxe_free[i][6])
                    print(all_possible_costs)
                    if len(all_possible_costs):
                        maxi_cost = max(all_possible_costs)
                        print(maxi_cost)

                        cnt = 0
                        for k,v in hotel.luxe_free.items():
                            if v[2] == '4' or v[2] == '5' or v[2] == '6':
                                if v[4] == maxi_cost or v[5] == maxi_cost or v[6] == maxi_cost:
                                    hotel.luxe_full[k] = v
                                    new_date = Date(self.info['Дата въезда'], self.info['Количество дней'])
                                    hotel.luxe_full[k].append(new_date.get_departure_date())
                                    cnt = k
                                    break

                        if cnt in hotel.half_luxe_free.keys():
                            del hotel.half_luxe_free[str(cnt)]
                        if cnt in hotel.luxe_free.keys():
                            del hotel.luxe_free[str(cnt)]
                        #print(hotel.single_full)
                        #print(hotel.single_free)
                    else:
                        print('вы бомж')
                print('new_client')
                print(hotel.single_free)
                print(hotel.single_full)
                print(hotel.double_free)
                print(hotel.double_full)
                print(hotel.half_luxe_free)
                print(hotel.half_luxe_full)
                print(hotel.luxe_free)
                print(hotel.luxe_full)


    def __repr__(self):
        return f'Info: {self.info}'


client = Clients()
client.read_booking_file(booking_file)
#print(client)