import sys

ITEMS_DICT = {'CH1': ['Chai', 3.11],
              'AP1': ['Apples', 6.00],
              'CF1': ['Coffee', 11.23],
              'MK1': ['Milk', 4.75],
              'OM1': ['Oatmeal', 3.69]}


class basket:
    """Hold your items and do things with them!"""
    current_discounts = {
        'BOGO': 'Buy-One-Get-One-Free Special on Coffee. (Unlimited)',
        'APPL': 'If you buy 3 or more bags of Apples, the price drops to $4.50.',
        'CHMK': 'Purchase a box of Chai and get milk free. (Limit 1)',
        'APOM': 'Purchase a bag of Oatmeal and get 50% off a bag of Apples'}

    def __init__(self):
        """Initializes the basket"""
        pass

    def see_specials(self):
        """Show available specials"""
        print('\n\nSpecials available:\n')
        for discount in self.current_discounts.keys():
            print("{discount} -- {description}".format(discount=discount, description=self.current_discounts[discount]))

    def show_items(self, checkout_basket):
        """Tally items in the basket with specials applied"""
        items_prices = []
        discount_offers = []
        print("\n\nItems in your basket:\n\n")
        try:
            keylist = checkout_basket.keys()
            keylist.sort()
            for item in keylist:
                item_price = ITEMS_DICT[item][1]
                item_num = checkout_basket[item]
                discount_diff = 0.00

                if item_num > 0:
                    # Apples
                    if item == 'AP1':
                        append_list = [item, item_price, discount_diff]
                        if item_num >= 3:
                            discount_diff = 1.50
                            append_list = [item, item_price, discount_diff, 'APPL']
                        else:
                            if checkout_basket['OM1'] == 0:
                                discount_offers.append("APOM -- Buy 1 bag of oatmeal for 50% off 1 bag of Apples.")
                            discount_offers.append("APPL -- Buy {} more Apples for $1.50 off/bag".format(3-item_num))
                            discount_offers.append("\t *Negates APOM")

                        for x in range(0, item_num):
                            items_prices.append(append_list)

                    # Chai
                    elif item == 'CH1':
                        for x in range(0, item_num):
                            items_prices.append([item, item_price, discount_diff])

                    # Coffee
                    elif item == 'CF1':
                        if item_num < 2:
                            discount_offers.append("BOGO -- Buy {} more coffees".format(2-item_num))
                        for x in range(0, item_num):
                            discount_diff = 0.00
                            append_list = [item, item_price, discount_diff]
                            if x % 2 > 0:
                                discount_diff = item_price
                                append_list = [item, item_price, discount_diff, 'BOGO']
                            items_prices.append(append_list)

                    # Milk
                    elif item == 'MK1':
                        if checkout_basket['CH1'] > 0:
                            discount_diff = item_price
                            items_prices.append([item, item_price, discount_diff, 'CHMK'])
                            discount_diff = 0.00
                            for x in range(1, item_num):
                                items_prices.append([item, item_price, discount_diff])
                        else:
                            for x in range(0, item_num):
                                items_prices.append([item, item_price, discount_diff])
                            discount_offers.append("CHMK -- Buy 1 box of Chai to receive 1 Milk free. (Limit 1 Milk)")

                    # Oatmeal
                    elif item == 'OM1':
                        for x in range(0, item_num):
                            items_prices.append([item, item_price, discount_diff])
                        if checkout_basket['OM1'] > 0 and 0 < checkout_basket['AP1'] < 3:
                            for dl in items_prices:
                                if dl[0] == 'AP1':
                                    dl[2] = dl[1] / 2
                                    dl.append('APOM')
                                    break
                        if checkout_basket['OM1'] == 0:
                            discount_offers.append("APOM -- Buy 1 bag of Oatmeal to receive 50% off on apples.")

            total_price = 0.00
            orig_price = 0.00
            # Print the receipt
            for checkout_item in items_prices:
                item_name = ITEMS_DICT[checkout_item[0]][0]
                disc_diff = checkout_item[2]
                item_price = checkout_item[1] - disc_diff
                item_price_str = "{0:.2f}".format(item_price)
                orig_price += checkout_item[1]
                separator = (40 - len(item_name) - len(item_price_str)) * '.'
                print('{item}{sep}{price}'.format(item=item_name,
                                                  sep=separator,
                                                  price=item_price_str))
                print('{item_code}'.format(item_code=checkout_item[0]))
                total_price += item_price
                if checkout_item[2] > 0:
                    print('\tORIG:  {orig}'.format(orig="{0:.2f}".format(checkout_item[1])))
                    print('\t{discount}: -{disc}'.format(disc="{0:.2f}".format(disc_diff), discount=checkout_item[3]))
            print(40 * "=")
            tot_price_fmt = "{0:.2f}".format(total_price)
            print("TOTAL:{sep}{items_total}".format(items_total=tot_price_fmt, sep=' ' * (34-len(tot_price_fmt))))
            print(40 * "=")
            print("Total Without Discounts:\t{orig_total}".format(orig_total="{0:.2f}".format(orig_price)))
            tot_sav = "{0:.2f}".format(orig_price - total_price)
            savings = "   You Saved: {amt_saved}   ".format(amt_saved=tot_sav)
            print("{star}{sav}{star}".format(star=(((40 - len(savings)) / 2) * '*'), sav=savings))
            print("\n\n")
            print("You can save! You're nearly at these Discounts:")
            for offer in discount_offers:
                print("\t\t{offer}".format(offer=offer))
            print("\n\n")
        except Exception as e:
            print("An error has occurred.")


class menu:
    """What does the user want to do?"""
    # code: number of items
    checkout_basket = {'CH1': 0,
                       'AP1': 0,
                       'CF1': 0,
                       'MK1': 0,
                       'OM1': 0}
    order_basket = basket()

    def __init__(self):
        """initialize menu and program"""
        self.show_main_menu()

    def quit_program(self):
        """exit program"""
        print("Quitting program.")
        sys.exit()

    def reset_basket(self):
        for item in self.checkout_basket.keys():
            self.checkout_basket[item] = 0
        self.order_basket = basket()
        print("Ready for new order.")

    def add_items(self):
        add_item_code_msg = '''
        For each item, enter how many items you have of each.
        Enter:
         "s" or "skip" to skip item,
         "q" or "quit" to exit add items
         "b" or "basket" to view current items
        '''
        print(add_item_code_msg)
        for item in self.checkout_basket.keys():
            item_name = ITEMS_DICT[item][0]
            get_number_msg = '\n\t{item}:\t'.format(item=item_name)
            num_items = ''
            while num_items == '' and num_items.lower() not in ['q', 'quit', 's', 'skip']:
                try:
                    num_items = raw_input(get_number_msg).strip()
                    self.checkout_basket[item] += int(num_items)
                    if self.checkout_basket[item] < 0:
                        self.checkout_basket[item] = 0
                except Exception as e:
                    if num_items in ['s', 'skip']:
                        continue
                    if num_items in ['q', 'quit']:
                        print("Leaving Add Items menu.")
                        break
                    if num_items in ['b', 'basket']:
                        self.order_basket.show_items(self.checkout_basket)
                    num_items = ''
                    print('Please enter a number. Enter "s" or "skip" to skip item, or "q" or "quit" to exit add item.')
            # kick back to main menu
            if num_items == 'q':
                break

        self.order_basket.show_items(self.checkout_basket)

    def checkout(self):
        self.order_basket.show_items(self.checkout_basket)
        print("***** Order Complete. Begin New Order. *****")
        print("\n\n")
        self.reset_basket()

    def main_menu(self):
        main_menu_script = """
        The Farmer's Market

        Please choose the corresponding number for the following options:
        1. Add items to your basket - add '-' to your number to take away your specified amount
        2. Show Items in your basket - Print your itemsto screen
        3. Checkout - Complete Order
        4. See Specials - Print available specials to screen
        5. Cancel/Create New Order - Delete your basket and start over

        or

        Enter:
            "b" or "basket" to see items in your basket
            "q" or "quit" to exit program
            "m" or "menu" for menu \n\n"""
        print (main_menu_script)

    def format_input(self, u_input):
        if u_input == 'quit':
            u_input = 'q'
        if u_input == 'basket':
            u_input = 'b'
        if u_input == 'menu':
            u_input = 'm'
        return u_input

    def show_main_menu(self):
        """Menu Setup"""
        run_program = True
        get_choice = "\nYour Selection:\t\t"
        menu_choice = {'1' or 1: self.add_items,
                       '2' or 2: self.order_basket.show_items,
                       '3' or 3: self.checkout,
                       '4' or 4: self.order_basket.see_specials,
                       '5' or 5: self.reset_basket,
                       'b' or 'basket': self.order_basket.show_items,
                       'q' or 'quit': self.quit_program,
                       'm' or 'menu': self.main_menu}

        try_counter = 0
        self.main_menu()
        while run_program:
            try:
                option = self.format_input(raw_input(get_choice).strip())

                if option.lower() in menu_choice.keys():
                    if option in ['2', 2]:
                        menu_choice[option](checkout_basket=self.checkout_basket)
                    else:
                        menu_choice[option]()
                    self.main_menu()
                else:
                    if try_counter > 4:
                        print("Too many invalid selections. Quitting program.")
                        menu_choice['q']()
                    else:
                        print("Invalid selection. Please try again.")
                        try_counter += 1

            except Exception as e:
                print (e)
                self.quit_program()

"""Run the program"""
menu()
