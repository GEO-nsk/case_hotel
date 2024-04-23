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
        self.profit = []

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
    day_profit = 0
    day_lost = 0

    def __init__(self):
        self.info = {}
        self.profit = 0
        self.single_free_que = {'стандарт': [], 'стандарт_улучшенный': [], 'апартамент': []}
        self.double_free_que = {'стандарт': [], 'стандарт_улучшенный': [], 'апартамент': []}
        self.half_luxe_free_que = {'стандарт': [], 'стандарт_улучшенный': [], 'апартамент': []}
        self.luxe_free_que = {'стандарт': [], 'стандарт_улучшенный': [], 'апартамент': []}

    def read_booking_file(self, booking_file):
        count = 0
        with open(booking_file, 'r', encoding='utf-8') as file:
            for item in file:
                count += 1
                line_list = []
                for itr in item.split():
                    line_list.append(itr)
                self.info[count] = line_list

    def time_check_single(self, entry_date, duration, room_type, room_num):
        date = Date(entry_date, duration)
        if len(self.single_free_que) == 0:
            self.single_free_que[room_type].append((entry_date, date.get_departure_date(), room_num))
            return True
        else:
            if all((int(entry_date[:2]) < int(period[0][:2]) and int(date.get_departure_date()[:2]) < int(period[0][:2]))
                   or (int(entry_date[:2]) > int(period[1][:2]) and int(date.get_departure_date()[:2]) > int(period[1][:2]))
                   for period in self.single_free_que[room_type]):
                self.single_free_que[room_type].append((entry_date, date.get_departure_date(), room_num))
                return True
            else:
                return False

    def time_check_double(self, entry_date, duration, room_type, room_num):
        date = Date(entry_date, duration)
        if len(self.double_free_que) == 0:
            self.double_free_que[room_type].append((entry_date, date.get_departure_date(), room_num))
            return True
        else:
            if all((int(entry_date[:2]) < int(period[0][:2]) and int(date.get_departure_date()[:2]) < int(period[0][:2]))
                   or (int(entry_date[:2]) > int(period[1][:2]) and int(date.get_departure_date()[:2]) > int(period[1][:2]))
                   for period in self.double_free_que[room_type]):
                self.double_free_que[room_type].append((entry_date, date.get_departure_date(), room_num))
                return True
            else:
                return False

    def time_check_half_luxe(self, entry_date, duration, room_type, room_num):
        date = Date(entry_date, duration)
        if len(self.half_luxe_free_que) == 0:
            self.half_luxe_free_que[room_type].append((entry_date, date.get_departure_date(), room_num))
            return True
        else:
            if all((int(entry_date[:2]) < int(period[0][:2]) and int(date.get_departure_date()[:2]) < int(period[0][:2]))
                   or (int(entry_date[:2]) > int(period[1][:2]) and int(date.get_departure_date()[:2]) > int(period[1][:2]))
                   for period in self.half_luxe_free_que[room_type]):
                self.half_luxe_free_que[room_type].append((entry_date, date.get_departure_date(), room_num))
                return True
            else:
                return False

    def time_check_luxe(self, entry_date, duration, room_type, room_num):
        date = Date(entry_date, duration)
        if len(self.luxe_free_que) == 0:
            self.luxe_free_que[room_type].append((entry_date, date.get_departure_date(), room_num))
            return True
        else:
            if all((int(entry_date[:2]) < int(period[0][:2]) and int(date.get_departure_date()[:2]) < int(period[0][:2]))
                   or (int(entry_date[:2]) > int(period[1][:2]) and int(date.get_departure_date()[:2]) > int(period[1][:2]))
                   for period in self.luxe_free_que[room_type]):
                self.luxe_free_que[room_type].append((entry_date, date.get_departure_date(), room_num))
                return True
            else:
                return False

    def find_single(self, enter_date):
        all_possible_costs = []
        for i in hotel.single_free:
            if hotel.single_free[i][4] <= int(enter_date[7]):
                all_possible_costs.append(hotel.single_free[i][4])
            if hotel.single_free[i][5] <= int(enter_date[7]):
                all_possible_costs.append(hotel.single_free[i][5])
            if hotel.single_free[i][6] <= int(enter_date[7]):
                all_possible_costs.append(hotel.single_free[i][6])
        for i in hotel.half_luxe_free:
            if hotel.half_luxe_free[i][2] == '1':
                if hotel.half_luxe_free[i][4] <= int(enter_date[7]):
                    all_possible_costs.append(hotel.half_luxe_free[i][4])
                if hotel.half_luxe_free[i][5] <= int(enter_date[7]):
                    all_possible_costs.append(hotel.half_luxe_free[i][5])
                if hotel.half_luxe_free[i][6] <= int(enter_date[7]):
                    all_possible_costs.append(hotel.half_luxe_free[i][6])
        if len(all_possible_costs):
            maxi_cost = max(all_possible_costs)

            cnt = 0
            for k, v in hotel.single_free.items():
                if v[4] == maxi_cost or v[5] == maxi_cost or v[6] == maxi_cost:
                    if self.time_check_single(enter_date[5], enter_date[6], hotel.single_free[k][3], k):
                        hotel.single_full[k] = v
                        new_date = Date(enter_date[5], enter_date[6])
                        hotel.single_full[k].append(new_date.get_departure_date())
                        cnt = k
                        break
            for k, v in hotel.half_luxe_free.items():
                if v[2] == '1':
                    if v[4] == maxi_cost or v[5] == maxi_cost or v[6] == maxi_cost:
                        if self.time_check_half_luxe(enter_date[5], enter_date[6], hotel.half_luxe_free[k][3], k):
                            hotel.half_luxe_full[k] = v
                            new_date = Date(enter_date[5], enter_date[6])
                            hotel.half_luxe_full[k].append(new_date.get_departure_date())
                            cnt = k
                            break

            if cnt in hotel.single_free.keys():
                del hotel.single_free[str(cnt)]
            if cnt in hotel.half_luxe_free.keys():
                del hotel.half_luxe_free[str(cnt)]

            Clients.day_profit += maxi_cost

            return maxi_cost
        else:
            for i in hotel.double_free:
                if hotel.double_free[i][4] <= int(enter_date[7]):
                    all_possible_costs.append(hotel.double_free[i][4])
                if hotel.double_free[i][5] <= int(enter_date[7]):
                    all_possible_costs.append(hotel.double_free[i][5])
                if hotel.double_free[i][6] <= int(enter_date[7]):
                    all_possible_costs.append(hotel.double_free[i][6])
            for i in hotel.half_luxe_free:
                if hotel.half_luxe_free[i][2] == '1':
                    if hotel.half_luxe_free[i][4] <= int(enter_date[7]):
                        all_possible_costs.append(hotel.half_luxe_free[i][4])
                    if hotel.half_luxe_free[i][5] <= int(enter_date[7]):
                        all_possible_costs.append(hotel.half_luxe_free[i][5])
                    if hotel.half_luxe_free[i][6] <= int(enter_date[7]):
                        all_possible_costs.append(hotel.half_luxe_free[i][6])
            if len(all_possible_costs):
                maxi_cost = max(all_possible_costs)

                cnt = 0
                for k, v in hotel.double_free.items():
                    if v[4] == maxi_cost or v[5] == maxi_cost or v[6] == maxi_cost:
                        if self.time_check_double(enter_date[5], enter_date[6], hotel.double_free[k][3], k):
                            hotel.double_full[k] = v
                            new_date = Date(enter_date[5], enter_date[6])
                            hotel.double_full[k].append(new_date.get_departure_date())
                            cnt = k
                            break
                for k, v in hotel.half_luxe_free.items():
                    if v[2] == '1':
                        if v[4] == maxi_cost or v[5] == maxi_cost or v[6] == maxi_cost:
                            if self.time_check_half_luxe(enter_date[5], enter_date[6], hotel.half_luxe_free[k][3], k):
                                hotel.half_luxe_full[k] = v
                                new_date = Date(enter_date[5], enter_date[6])
                                hotel.half_luxe_full[k].append(new_date.get_departure_date())
                                cnt = k
                                break

                if cnt in hotel.double_free.keys():
                    del hotel.double_free[str(cnt)]
                if cnt in hotel.half_luxe_free.keys():
                    del hotel.half_luxe_free[str(cnt)]

                Clients.day_profit += maxi_cost

                return maxi_cost
            else:
                client.day_lost += int(enter_date[7])
                return 0

    def find_double(self, enter_date):
        all_possible_costs = []
        for i in hotel.double_free:
            if hotel.double_free[i][4] <= int(enter_date[7]):
                all_possible_costs.append(hotel.double_free[i][4])
            if hotel.double_free[i][5] <= int(enter_date[7]):
                all_possible_costs.append(hotel.double_free[i][5])
            if hotel.double_free[i][6] <= int(enter_date[7]):
                all_possible_costs.append(hotel.double_free[i][6])
        for i in hotel.half_luxe_free:
            if hotel.half_luxe_free[i][2] == '2':
                if hotel.half_luxe_free[i][4] <= int(enter_date[7]):
                    all_possible_costs.append(hotel.half_luxe_free[i][4])
                if hotel.half_luxe_free[i][5] <= int(enter_date[7]):
                    all_possible_costs.append(hotel.half_luxe_free[i][5])
                if hotel.half_luxe_free[i][6] <= int(enter_date[7]):
                    all_possible_costs.append(hotel.half_luxe_free[i][6])
        if len(all_possible_costs):
            maxi_cost = max(all_possible_costs)

            cnt = 0
            for k, v in hotel.double_free.items():
                if v[4] == maxi_cost or v[5] == maxi_cost or v[6] == maxi_cost:
                    if self.time_check_double(enter_date[5], enter_date[6], hotel.double_free[k][3], k):
                        hotel.double_full[k] = v
                        new_date = Date(enter_date[5], enter_date[6])
                        hotel.double_full[k].append(new_date.get_departure_date())
                        cnt = k
                        break
            for k, v in hotel.half_luxe_free.items():
                if v[2] == '2':
                    if v[4] == maxi_cost or v[5] == maxi_cost or v[6] == maxi_cost:
                        if self.time_check_half_luxe(enter_date[5], enter_date[6], hotel.half_luxe_free[k][3], k):
                            hotel.half_luxe_full[k] = v
                            new_date = Date(enter_date[5], enter_date[6])
                            hotel.half_luxe_full[k].append(new_date.get_departure_date())
                            cnt = k
                            break

            if cnt in hotel.double_free.keys():
                del hotel.double_free[str(cnt)]
            if cnt in hotel.half_luxe_free.keys():
                del hotel.half_luxe_free[str(cnt)]

            Clients.day_profit += maxi_cost

            return maxi_cost
        else:
            for i in hotel.half_luxe_free:
                if hotel.half_luxe_free[i][2] == '2':
                    if hotel.half_luxe_free[i][4] <= int(enter_date[7]):
                        all_possible_costs.append(hotel.half_luxe_free[i][4])
                    if hotel.half_luxe_free[i][5] <= int(enter_date[7]):
                        all_possible_costs.append(hotel.half_luxe_free[i][5])
                    if hotel.half_luxe_free[i][6] <= int(enter_date[7]):
                        all_possible_costs.append(hotel.half_luxe_free[i][6])
            for i in hotel.luxe_free:
                if hotel.luxe_free[i][2] == '2':
                    if hotel.luxe_free[i][4] <= int(enter_date[7]):
                        all_possible_costs.append(hotel.luxe_free[i][4])
                    if hotel.luxe_free[i][5] <= int(enter_date[7]):
                        all_possible_costs.append(hotel.luxe_free[i][5])
                    if hotel.luxe_free[i][6] <= int(enter_date[7]):
                        all_possible_costs.append(hotel.luxe_free[i][6])
            if len(all_possible_costs):
                maxi_cost = max(all_possible_costs)

                cnt = 0
                for k, v in hotel.half_luxe_free.items():
                    if v[2] == '2':
                        if v[4] == maxi_cost or v[5] == maxi_cost or v[6] == maxi_cost:
                            if self.time_check_half_luxe(enter_date[5], enter_date[6], hotel.half_luxe_free[k][3], k):
                                hotel.half_luxe_full[k] = v
                                new_date = Date(enter_date[5], enter_date[6])
                                hotel.half_luxe_full[k].append(new_date.get_departure_date())
                                cnt = k
                                break
                for k, v in hotel.luxe_free.items():
                    if v[2] == '2':
                        if v[4] == maxi_cost or v[5] == maxi_cost or v[6] == maxi_cost:
                            if self.time_check_luxe(enter_date[5], enter_date[6], hotel.luxe_free[k][3], k):
                                hotel.luxe_full[k] = v
                                new_date = Date(enter_date[5], enter_date[6])
                                hotel.luxe_full[k].append(new_date.get_departure_date())
                                cnt = k
                                break

                if cnt in hotel.half_luxe_free.keys():
                    del hotel.half_luxe_free[str(cnt)]
                if cnt in hotel.luxe_free.keys():
                    del hotel.luxe_free[str(cnt)]

                Clients.day_profit += maxi_cost

                return maxi_cost
            else:
                client.day_lost += int(enter_date[7])
                return 0

    def find_half_luxe(self, enter_date):
        all_possible_costs = []
        for i in hotel.half_luxe_free:
            if hotel.half_luxe_free[i][2] == '3':
                if hotel.half_luxe_free[i][4] <= int(enter_date[7]):
                    all_possible_costs.append(hotel.half_luxe_free[i][4])
                if hotel.half_luxe_free[i][5] <= int(enter_date[7]):
                    all_possible_costs.append(hotel.half_luxe_free[i][5])
                if hotel.half_luxe_free[i][6] <= int(enter_date[7]):
                    all_possible_costs.append(hotel.half_luxe_free[i][6])
        for i in hotel.luxe_free:
            if hotel.luxe_free[i][2] == '3':
                if hotel.luxe_free[i][4] <= int(enter_date[7]):
                    all_possible_costs.append(hotel.luxe_free[i][4])
                if hotel.luxe_free[i][5] <= int(enter_date[7]):
                    all_possible_costs.append(hotel.luxe_free[i][5])
                if hotel.luxe_free[i][6] <= int(enter_date[7]):
                    all_possible_costs.append(hotel.luxe_free[i][6])
        if len(all_possible_costs):
            maxi_cost = max(all_possible_costs)

            cnt = 0
            for k, v in hotel.half_luxe_free.items():
                if v[2] == '3':
                    if v[4] == maxi_cost or v[5] == maxi_cost or v[6] == maxi_cost:
                        if self.time_check_half_luxe(enter_date[5], enter_date[6], hotel.half_luxe_free[k][3], k):
                            hotel.half_luxe_full[k] = v
                            new_date = Date(enter_date[5], enter_date[6])
                            hotel.half_luxe_full[k].append(new_date.get_departure_date())
                            cnt = k
                            break
            for k, v in hotel.luxe_free.items():
                if v[2] == '3':
                    if v[4] == maxi_cost or v[5] == maxi_cost or v[6] == maxi_cost:
                        if self.time_check_luxe(enter_date[5], enter_date[6], hotel.luxe_free[k][3], k):
                            hotel.luxe_full[k] = v
                            new_date = Date(enter_date[5], enter_date[6])
                            hotel.luxe_full[k].append(new_date.get_departure_date())
                            cnt = k
                            break

            if cnt in hotel.half_luxe_free.keys():
                del hotel.half_luxe_free[str(cnt)]
            if cnt in hotel.luxe_free.keys():
                del hotel.luxe_free[str(cnt)]

            Clients.day_profit += maxi_cost

            return maxi_cost
        else:
            for i in hotel.luxe_free:
                if hotel.luxe_free[i][2] == '3':
                    if hotel.luxe_free[i][4] <= int(enter_date[7]):
                        all_possible_costs.append(hotel.luxe_free[i][4])
                    if hotel.luxe_free[i][5] <= int(enter_date[7]):
                        all_possible_costs.append(hotel.luxe_free[i][5])
                    if hotel.luxe_free[i][6] <= int(enter_date[7]):
                        all_possible_costs.append(hotel.luxe_free[i][6])
            if len(all_possible_costs):
                maxi_cost = max(all_possible_costs)

                cnt = 0
                for k, v in hotel.luxe_free.items():
                    if v[2] == '3':
                        if v[4] == maxi_cost or v[5] == maxi_cost or v[6] == maxi_cost:
                            if self.time_check_luxe(enter_date[5], enter_date[6], hotel.luxe_free[k][3], k):
                                hotel.luxe_full[k] = v
                                new_date = Date(enter_date[5], enter_date[6])
                                hotel.luxe_full[k].append(new_date.get_departure_date())
                                cnt = k
                                break

                if cnt in hotel.half_luxe_free.keys():
                    del hotel.half_luxe_free[str(cnt)]
                if cnt in hotel.luxe_free.keys():
                    del hotel.luxe_free[str(cnt)]

                Clients.day_profit += maxi_cost

                return maxi_cost
            else:
                client.day_lost += int(enter_date[7])
                return 0

    def find_luxe(self, enter_date):
        all_possible_costs = []
        for i in hotel.luxe_free:
            if hotel.luxe_free[i][2] == '4' or hotel.luxe_free[i][2] == '5' or \
                    hotel.luxe_free[i][2] == '6':
                if hotel.luxe_free[i][4] <= int(enter_date[7]):
                    all_possible_costs.append(hotel.luxe_free[i][4])
                if hotel.luxe_free[i][5] <= int(enter_date[7]):
                    all_possible_costs.append(hotel.luxe_free[i][5])
                if hotel.luxe_free[i][6] <= int(enter_date[7]):
                    all_possible_costs.append(hotel.luxe_free[i][6])
        if len(all_possible_costs):
            maxi_cost = max(all_possible_costs)

            cnt = 0
            for k, v in hotel.luxe_free.items():
                if v[2] == '4' or v[2] == '5' or v[2] == '6':
                    if v[4] == maxi_cost or v[5] == maxi_cost or v[6] == maxi_cost:
                        if self.time_check_luxe(enter_date[5], enter_date[6], hotel.luxe_free[k][3], k):
                            hotel.luxe_full[k] = v
                            new_date = Date(enter_date[5], enter_date[6])
                            hotel.luxe_full[k].append(new_date.get_departure_date())
                            cnt = k
                            break

            if cnt in hotel.luxe_free.keys():
                del hotel.luxe_free[str(cnt)]

            Clients.day_profit += maxi_cost

            return maxi_cost
        else:
            client.day_lost += int(enter_date[7])
            return 0

    def out_single(self, day):
        out_list_single = []
        for k, v in hotel.single_full.items():
            if int(v[-1][0:2]) == day:
                hotel.single_free[k] = v
                out_list_single.append(k)
        for i in out_list_single:
            del hotel.single_full[i]

            cnt = i
            for room in self.single_free_que:
                if len(self.single_free_que[room]) > 0:
                    for j in range(len(self.single_free_que[room])):
                        if self.single_free_que[room][j-1][2] == cnt:
                            del self.single_free_que[room][j-1]

    def out_double(self, day):
        out_list_double = []
        for k, v in hotel.double_full.items():
            if int(v[-1][0:2]) == day:
                hotel.double_free[k] = v
                out_list_double.append(k)
        for i in out_list_double:
            del hotel.double_full[i]

            cnt = i
            for room in self.double_free_que:
                if len(self.double_free_que[room]) > 0:
                    for j in range(len(self.double_free_que[room])):
                        if self.double_free_que[room][j-1][2] == cnt:
                            del self.double_free_que[room][j-1]

    def out_half_luxe(self, day):
        out_list_half_luxe = []
        for k, v in hotel.half_luxe_full.items():
            if int(v[-1][0:2]) == day:
                hotel.half_luxe_free[k] = v
                out_list_half_luxe.append(k)
        for i in out_list_half_luxe:
            del hotel.half_luxe_full[i]

            cnt = i
            for room in self.half_luxe_free_que:
                if len(self.half_luxe_free_que[room]) > 0:
                    for j in range(len(self.half_luxe_free_que[room])):
                        if self.half_luxe_free_que[room][j-1][2] == cnt:
                            del self.half_luxe_free_que[room][j-1]


    def out_luxe(self, day):
        out_list_luxe = []
        for k, v in hotel.luxe_full.items():
            if int(v[-1][0:2]) == day:
                hotel.luxe_free[k] = v
                out_list_luxe.append(k)
        for i in out_list_luxe:
            del hotel.luxe_full[i]

            cnt = i
            for room in self.luxe_free_que:
                if len(self.luxe_free_que[room]) > 0:
                    for j in range(len(self.luxe_free_que[room])):
                        if self.luxe_free_que[room][j-1][2] == cnt:
                            del self.luxe_free_que[room][j-1]

    def show_info(self, day):
        booked = 0
        for i in self.single_free_que:
            if int(i[0][:2]) == day:
                booked += 1
        return booked, Hotel.day_profit, Hotel.day_lost

    def __repr__(self):
        return f'Info: {self.info}'


client = Clients()

client.read_booking_file(booking_file)

for day in range(1, 31):

    client.day_profit = 0
    client.day_lost = 0

    client.out_single(day)
    client.out_double(day)
    client.out_half_luxe(day)
    client.out_luxe(day)

    for client_number, enter_date in client.info.items():
        if day == int(enter_date[0][1:2]):
            if enter_date[4] == '1':
                client.day_profit += int(client.find_single(enter_date))
            if enter_date[4] == '2':
                client.day_profit += int(client.find_double(enter_date))
            if enter_date[4] == '3':
                client.day_profit += int(client.find_half_luxe(enter_date))
            if enter_date[4] == '4' or enter_date[4] == '5' or enter_date[4] == '6':
                client.day_profit += int(client.find_luxe(enter_date))
    full_rooms = len(hotel.single_full) + len(hotel.double_full) + len(hotel.half_luxe_full)\
                 + len(hotel.luxe_full)
    print('количество занятых номеров:', full_rooms)
    free_rooms = len(hotel.single_free) + len(hotel.double_free) + len(hotel.half_luxe_free)\
                 + len(hotel.luxe_free)
    print('количество свободных номеров:', free_rooms)
    full_single_rooms = len(hotel.single_full)
    free_single_rooms = len(hotel.single_free)
    full_double_rooms = len(hotel.double_full)
    free_double_rooms = len(hotel.double_free)
    full_half_luxe_rooms = len(hotel.half_luxe_full)
    free_half_luxe_rooms = len(hotel.half_luxe_free)
    full_luxe_rooms = len(hotel.luxe_full)
    free_luxe_rooms = len(hotel.luxe_free)
    print('процент загруженности одноместных номеров:',\
          full_single_rooms/(full_single_rooms + free_single_rooms) * 100,'%')
    print('процент загруженности двуместных номеров:', \
          full_double_rooms / (full_double_rooms + free_double_rooms) * 100, '%')
    print('процент загруженности полу-люкс номеров:', \
          full_half_luxe_rooms / (full_half_luxe_rooms + free_half_luxe_rooms) * 100, '%')
    print('процент загруженности люкс номеров:', \
          full_luxe_rooms / (full_luxe_rooms + free_luxe_rooms) * 100, '%')
    print('процент загруженности отеля:', full_rooms / (full_rooms + free_rooms) * 100, '%')
    print('полученный доход за день:', client.day_profit)
    print('упущенный доход за день:', client.day_lost)
'''
print('final')
print(hotel.single_free)
print(hotel.single_full)
print(hotel.double_free)
print(hotel.double_full)
print(hotel.half_luxe_free)
print(hotel.half_luxe_full)
print(hotel.luxe_free)
print(hotel.luxe_full)
print(client.profit)
print('\n' * 3)
print(client.single_free_que)
print(client.double_free_que)
print(client.half_luxe_free_que)
print(client.luxe_free_que)
'''
