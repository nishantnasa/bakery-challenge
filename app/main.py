class Order:

    def __init__(self, all_products_packs={}, user_product_qty={}):
        """
        self.all_products_packs contains the mapping of each product with its package-denomination to package-cost
            Format @Dict {<product-id>@string: @Dict {<package-denomination>@int: <this-package-cost>@float}, ... }
            Example {
                        'VS5': {3: 6.99, 5: 8.99},
                        'MB11': {2: 9.95, 5: 16.95, 8: 24.95},
                        'CF': {3: 5.95, 5: 9.95, 9: 16.99}
                    }
        self.user_product_qty contains the mapping of each product with its user requested quantity
            Format @Dict {<product-id>@string: <product-quantity>@int, ... }
            Example {
                        'VS5': 10,
                        'MB11': 14,
                        'CF': 0
                    }
        self.order contains the mapping of each product with total order cost & order_quantity of each package-denomination
            Format @Dict {<product-id>@string: @Dict {<total_cost>@int , <order-quantity>@Dict {<package-denomination>@int: <this-package-order-quantity>@int}}, ... }
            Example {
                        'MB11': {'total_cost': 54.8, 'qty': {8: 1, 2: 3}}, 
                        'VS5': {'total_cost': 17.98, 'qty': {5: 2}}, 
                        'CF': {'total_cost': 25.85, 'qty': {3: 1, 5: 2}}
                    }
        """
        self.all_products_packs = all_products_packs
        self.user_product_qty = user_product_qty
        self.order = {}
        self.get_order(printing=False)

    def get_order(self, printing=True):
        """
        For each product:
            Uses an algorithm to minimize the number of packages required to fulfil user's quantity request
            Calculates the total_cost for (this product's) order
            Inserts the minimized package quantity & total_cost data (for this product) into final_order
        Prints the final_order (self.order) details for all products in required format.
        
        >>> o = Order({\
            'VS5': {3: 6.99, 5: 8.99},\
            'MB11': {2: 9.95, 5: 16.95, 8: 24.95},\
            'CF': {3: 5.95, 5: 9.95, 9: 16.99}\
            }, \
            {\
                'VS5': 10,\
                'MB11': 14,\
                'CF': 13\
            })
        >>> o.get_order(printing=False)
        >>> o.order
        {'MB11': {'total_cost': 54.8, 'qty': {8: 1, 2: 3}}, 'VS5': {'total_cost': 17.98, 'qty': {5: 2}}, 'CF': {'total_cost': 25.85, 'qty': {3: 1, 5: 2}}}
        """
        for product, pack_costs in self.all_products_packs.iteritems():
            packs = pack_costs.keys()
            user_qty = self.user_product_qty[product]
            order_qty = self.__get_order_qty(packs, user_qty)
            total_cost = self.__get_order_cost(order_qty, pack_costs)
            self.order[product] = {
                'qty': order_qty,
                'total_cost': round(total_cost, 2)
            }
        if printing is True:
            self.__print_order()

    def __get_order_qty(self, packs, user_qty):
        """
        Given: 
            packs - list (array) of available packet denominations
                Format @list[<packet-denomination>@int, ... ]
                Example [5, 2, 8]
            user_qty - total value of items quantity required
                Format @int
        Returns a dictionary mapping of packet-denomination to its minmized quantity
            Format @dict{<packet-denomincation>@int: <minimized-quantity>@int} 
        """
        queue = []
        min_order_pack_idx = self.__min_packs(packs=packs, user_qty=user_qty)
        start = len(min_order_pack_idx) - 1

        if min_order_pack_idx[start] == -1:
            # print "No Order possible with available package combinations."
            return {}

        while start != 0:
            pack = packs[min_order_pack_idx[start]]
            start = start - pack
            queue.append(pack)

        return {q: queue.count(q) for q in queue}

    def __min_packs(self, packs, user_qty):
        """
        This is an algorithm to minimize the packet denominations for a particular total quantity of items
        Given: 
            packs - list (array) of available packet denominations
                Format @list[<packet-denomination>@int, ... ]
                Example [5, 2, 8]
            user_qty - total value of items quantity required
                Format @int
        
        Algorithm uses two 1-D arrays (lists) to store intermeditate results
            min_packs[i] contains the minimum packages required for a total quantity of i
                Initially populated with value of floating point infinity at all indexes
            min_order_pack_idx[i] contains the index-value from list of package-denominations (packs) where min_packs[i] was updated
                Initially populated with value of -1 at all indexes
            For each package-denomination, if j refers to index from list of package-denominations 
                For each quantity till user_quantity value, if i refers to quantity 
                    if quantity >= packet-denomination (example a packet of 2 can't make quantity of 1)
                        min_packs[i] = min(min_packs[i], 1 + min_packs[i - packs[j]<packet-denomination>])
                        min_order_pack_idx[i] = j, j is the index of current <package-denomination> 
            After the preceding loop
                min_packs will contain the minimum number of packets required for a quantity of i
                min_order_pack_idx[i] will contain the indexes of packet-denominations which resulted in current value of min_packs[i]
            The packet-denominations to minimize number of packets for user-quantity can be calculated from min_order_pack_idx 
        """
        qty_range = user_qty + 1
        min_packs = [0 if idx == 0 else float("inf") for idx in range(qty_range)]
        min_order_pack_idx = [-1 for _ in range(qty_range)]

        for j in range(len(packs)):
            for i in range(1, qty_range):
                pack = packs[j]
                if i >= packs[j]:
                    if min_packs[i] > 1 + min_packs[i - pack]:
                        min_packs[i] = 1 + min_packs[i - pack]
                        min_order_pack_idx[i] = j

        return min_order_pack_idx

    def __get_order_cost(self, order_qty, pack_costs):
        """
        Returns the total_cost of order
        """
        total_cost = 0.00

        for pack, qty in order_qty.iteritems():
            total_cost += qty * pack_costs[pack]

        return total_cost

    def __print_order(self):
        """
        Prints the order details in required format
        Returns None
        """
        for product, user_qty in self.user_product_qty.iteritems():
            if user_qty > 0:
                print "%(uq)s %(p)s $%(tc)s" % {'uq': user_qty, 'p': product, 'tc': self.order[product]['total_cost']}
                for pack, pack_qty in self.order[product]['qty'].iteritems():
                    pack_unit_cost = self.all_products_packs[product][pack]
                    print "\t %(pkq)s x %(pk)s $%(pkuc)s" % {'pkq': pack_qty, 'pk': pack, 'pkuc': pack_unit_cost}


# This function supports running the application
def get_user_qty(message):
    """
    Error handling for invalid user inputs for quantity 
    """
    user_qty_input = 0
    while True:
        try:
            user_qty_input = int(raw_input(message))
        except ValueError:
            print("Invalid input! Please try again.")
            continue
        else:
            break
    return user_qty_input


if __name__ == '__main__':
    all_products_packs = {
        'VS5': {3: 6.99, 5: 8.99},
        'MB11': {2: 9.95, 5: 16.95, 8: 24.95},
        'CF': {3: 5.95, 5: 9.95, 9: 16.99}
    }
    user_product_qty = {
        'VS5': get_user_qty("How many Vegemite Scrolls you want? "),
        'MB11': get_user_qty("How many Blueberry muffins you want? "),
        'CF': get_user_qty("How many Croissants you want? ")
    }

    order = Order()
    order.all_products_packs = all_products_packs
    order.user_product_qty = user_product_qty
    order.get_order()
