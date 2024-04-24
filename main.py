'''
Gagol Egor 80
Tarlo Evgeny 80
'''

import ru_local as ru


class Date:
    '''
    Class of date.

    Parameters:
    -----------
    entry_date : str
                 Check-in date.
    duration : str
               Length of stay of customers in the hotel.
    '''


    def __init__(self, entry_date, duration):
        self.entry_date = entry_date
        self.dd = int(entry_date[:2])
        self.mm = int(entry_date[3:5])
        self.yyyy = int(entry_date[6:10])
        self.duration = int(duration)
        self.departure_date = None

    def get_departure_date(self):
        '''
        Calculates customers departure date.

        Returns:
        --------
        str
           Customers departure date.
        '''


        self.dd += self.duration
        if self.dd > 31:
            self.mm += 1
            self.dd -= 31
        if self.mm > 12:
            self.yyyy += 1
            self.mm -= 12
        self.departure_date = f'{self.dd:02d}.{self.mm:02d}.{self.yyyy}'
        return self.departure_date


class Hotel(Date):
    '''
    Class of hotel.
    '''


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
        '''
        Gets information about rooms from file and add its available costs.

        Parameters:
        -----------
        hotel_file_name : str
                          Name of file contained information about hotel rooms.

        Modifies:
        ---------
        self.single_free : dict
        self.double_free : dict
        self.half_luxe_free : dict
        self.luxe_free : dict
                         Add all possible rooms costs.
        '''


        with open(hotel_file_name, 'r', encoding='utf-8') as file:
            for item in file:
                line_list = []
                for itr in item.split():
                    line_list.append(itr)

                if line_list[1] == ru.single:
                    self.single_free[line_list[0]] = line_list
                    if line_list[3] == ru.standard:
                        self.single_free[line_list[0]].append(2900)
                        self.single_free[line_list[0]].append(3180)
                        self.single_free[line_list[0]].append(3900)
                    if line_list[3] == ru.upgraded_standard:
                        self.single_free[line_list[0]].append(3480)
                        self.single_free[line_list[0]].append(3760)
                        self.single_free[line_list[0]].append(4480)
                    if line_list[3] == ru.apartament:
                        self.single_free[line_list[0]].append(4350)
                        self.single_free[line_list[0]].append(4630)
                        self.single_free[line_list[0]].append(5350)

                if line_list[1] == ru.double:
                    self.double_free[line_list[0]] = line_list
                    if line_list[3] == ru.standard:
                        self.double_free[line_list[0]].append(2300)
                        self.double_free[line_list[0]].append(2580)
                        self.double_free[line_list[0]].append(3300)
                    if line_list[3] == ru.upgraded_standard:
                        self.double_free[line_list[0]].append(2760)
                        self.double_free[line_list[0]].append(3040)
                        self.double_free[line_list[0]].append(3760)
                    if line_list[3] == ru.apartament:
                        self.double_free[line_list[0]].append(3450)
                        self.double_free[line_list[0]].append(3730)
                        self.double_free[line_list[0]].append(4450)

                if line_list[1] == ru.half_luxe:
                    self.half_luxe_free[line_list[0]] = line_list
                    if line_list[3] == ru.standard:
                        self.half_luxe_free[line_list[0]].append(3200)
                        self.half_luxe_free[line_list[0]].append(3480)
                        self.half_luxe_free[line_list[0]].append(4200)
                    if line_list[3] == ru.upgraded_standard:
                        self.half_luxe_free[line_list[0]].append(3840)
                        self.half_luxe_free[line_list[0]].append(4120)
                        self.half_luxe_free[line_list[0]].append(4840)
                    if line_list[3] == ru.apartament:
                        self.half_luxe_free[line_list[0]].append(4800)
                        self.half_luxe_free[line_list[0]].append(5080)
                        self.half_luxe_free[line_list[0]].append(5800)

                if line_list[1] == ru.luxe:
                    self.luxe_free[line_list[0]] = line_list
                    if line_list[3] == ru.standard:
                        self.luxe_free[line_list[0]].append(4100)
                        self.luxe_free[line_list[0]].append(4380)
                        self.luxe_free[line_list[0]].append(5100)
                    if line_list[3] == ru.upgraded_standard:
                        self.luxe_free[line_list[0]].append(4920)
                        self.luxe_free[line_list[0]].append(5200)
                        self.luxe_free[line_list[0]].append(5920)
                    if line_list[3] == ru.apartament:
                        self.luxe_free[line_list[0]].append(6150)
                        self.luxe_free[line_list[0]].append(6430)
                        self.luxe_free[line_list[0]].append(7150)


class Clients(Hotel):
    '''
    Class of clients.

    Attributes:
    -----------
    day_profit : int
                 Calculates profit per day.
    day_lost : int
               Calculates lost profit per day.
    '''


    day_profit = 0
    day_lost = 0

    def __init__(self):
        self.info = {}
        self.single_free_que = {ru.standard: [], ru.upgraded_standard: [], ru.apartament: []}
        self.double_free_que = {ru.standard: [], ru.upgraded_standard: [], ru.apartament: []}
        self.half_luxe_free_que = {ru.standard: [], ru.upgraded_standard: [], ru.apartament: []}
        self.luxe_free_que = {ru.standard: [], ru.upgraded_standard: [], ru.apartament: []}

    def read_booking_file(self, booking_file):
        '''
        Reads information about booking clients from file and adds it to "self.info".

        Parameters:
        -----------
        booking_file : str
                       File with information about booking clients.
        '''
        count = 0
        with open(booking_file, 'r', encoding='utf-8') as file:
            for item in file:
                count += 1
                line_list = []
                for itr in item.split():
                    line_list.append(itr)
                self.info[count] = line_list

    def time_check_single(self, entry_date, duration, room_type, room_num):
        '''
        Checks for available time period to book a single room.

        Parameters:
        -----------
        entry_date : str
                     Customers check-in date.
        duration : str
                   Length of stay of customers in the hotel.
        room_type : str
                    Type of room.
        room_num : str
                   Number of room.

        Returns:
        --------
        "True" if certain period is available, "False" if it is not available.
        '''


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
        '''
        Checks for available time period to book a double room.

        Parameters:
        -----------
        entry_date : str
                     Customers check-in date.
        duration : str
                   Length of stay of customers in the hotel.
        room_type : str
                    Type of room.
        room_num : str
                   Number of room.

        Returns:
        --------
        "True" if certain period is available, "False" if it is not available.
        '''


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
        '''
        Checks for available time period to book a half luxe room.

        Parameters:
        -----------
        entry_date : str
                     Customers check-in date.
        duration : str
                   Length of stay of customers in the hotel.
        room_type : str
                    Type of room.
        room_num : str
                   Number of room.

        Returns:
        --------
        "True" if certain period is available, "False" if it is not available.
        '''


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
        '''
        Checks for available time period to book a luxe room.

        Parameters:
        -----------
        entry_date : str
                     Customers check-in date.
        duration : str
                   Length of stay of customers in the hotel.
        room_type : str
                    Type of room.
        room_num : str
                   Number of room.

        Returns:
        --------
        "True" if certain period is available, "False" if it is not available.
        '''


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
        '''
        Finds the right single room and calculates the final cost.

        Parameters:
        -----------
        enter_date : str
                     Customers check-in date.
        
        Returns:
        --------
        maxi_cost : int
                    Cost of accommodation.
        '''


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
        '''
        Finds the right double room and calculates the final cost.

        Parameters:
        -----------
        enter_date : str
                     Customers check-in date.
        
        Returns:
        --------
        maxi_cost : int
                    Cost of accommodation.
        '''


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
        '''
        Finds the right half luxe room and calculates the final cost.

        Parameters:
        -----------
        enter_date : str
                     Customers check-in date.
        
        Returns:
        --------
        maxi_cost : int
                    Cost of accommodation.
        '''


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
        '''
        Finds the right luxe room and calculates the final cost.

        Parameters:
        -----------
        enter_date : str
                     Customers check-in date.
        
        Returns:
        --------
        maxi_cost : int
                    Cost of accommodation.
        '''


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
        '''
        Checks guests out of single room when their check-out date arrives.

        Parameters:
        -----------
        day : int
              Today's date (day).
        '''


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
        '''
        Checks guests out of double room when their check-out date arrives.

        Parameters:
        -----------
        day : int
              Today's date (day).
        '''


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
        '''
        Checks guests out of half luxe room when their check-out date arrives.

        Parameters:
        -----------
        day : int
              Today's date (day).
        '''


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
        '''
        Checks guests out of luxe room when their check-out date arrives.

        Parameters:
        -----------
        day : int
              Today's date (day).
        '''


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


hotel_file_name = 'fund.txt'
booking_file = 'booking.txt'

hotel = Hotel()
hotel.read_file(hotel_file_name)

client = Clients()
client.read_booking_file(booking_file)


for day in range(1, 31):
    print(f'{ru.day}: {day}')
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
    print(f'{ru.room_occupancy}:', full_rooms)
    free_rooms = len(hotel.single_free) + len(hotel.double_free) + len(hotel.half_luxe_free)\
                 + len(hotel.luxe_free)
    print(f'{ru.room_availability}:', free_rooms)
    full_single_rooms = len(hotel.single_full)
    free_single_rooms = len(hotel.single_free)
    full_double_rooms = len(hotel.double_full)
    free_double_rooms = len(hotel.double_free)
    full_half_luxe_rooms = len(hotel.half_luxe_full)
    free_half_luxe_rooms = len(hotel.half_luxe_free)
    full_luxe_rooms = len(hotel.luxe_full)
    free_luxe_rooms = len(hotel.luxe_free)
    print(f'{ru.single_room_occupancy_rate}:',\
          full_single_rooms/(full_single_rooms + free_single_rooms) * 100,'%')
    print(f'{ru.double_room_occupancy_rate}:', \
          full_double_rooms / (full_double_rooms + free_double_rooms) * 100, '%')
    print(f'{ru.half_luxe_room_occupancy_rate}:', \
          full_half_luxe_rooms / (full_half_luxe_rooms + free_half_luxe_rooms) * 100, '%')
    print(f'{ru.luxe_room_occupancy_rate}:', \
          full_luxe_rooms / (full_luxe_rooms + free_luxe_rooms) * 100, '%')
    print(f'{ru.hotel_occupancy_rate}:', full_rooms / (full_rooms + free_rooms) * 100, '%')
    print(f'{ru.profit_per_day}:', client.day_profit)
    print(f'{ru.lost_per_day}:', client.day_lost)
    print('-' * 10)
