def get_order(all_products_packs, user_product_qty):
    order = {}
    for product, pack_costs in all_products_packs.iteritems():
        packs = pack_costs.keys()
        user_qty = user_product_qty[product]
        order_qty = get_order_qty(packs, user_qty)
        total_cost = get_order_cost(order_qty, pack_costs)
        order[product] = {
            'qty': order_qty,
            'pack_costs': pack_costs,
            'total_cost': round(total_cost, 2)
        }
    return order


def get_order_qty(packs, user_qty):
    queue = []
    min_order_pack_idx_list = min_packs(packs=packs, user_qty=user_qty)
    start = len(min_order_pack_idx_list) - 1

    if min_order_pack_idx_list[start] == -1:
        # print "No Order possible with available package combinations."
        return {}

    while start != 0:
        pack = packs[min_order_pack_idx_list[start]]
        start = start - pack
        queue.append(pack)

    return {q: queue.count(q) for q in queue}


def min_packs(packs, user_qty):
    idx_range = user_qty + 1
    min_packs = [0 if idx == 0 else float("inf") for idx in range(idx_range)]
    min_order_pack_idx = [-1 for _ in range(idx_range)]

    for j in range(len(packs)):
        for i in range(1, idx_range):
            pack = packs[j]
            if i >= packs[j]:
                if min_packs[i] > 1 + min_packs[i - pack]:
                    min_packs[i] = 1 + min_packs[i - pack]
                    min_order_pack_idx[i] = j

    return min_order_pack_idx


def get_order_cost(order_qty, pack_costs):
    total_cost = 0.00

    for pack, qty in order_qty.iteritems():
        total_cost += qty * pack_costs[pack]

    return total_cost


def main():
    all_products_packs = {
        'VS5': {3: 6.99, 5: 8.99},
        'MB11': {2: 9.95, 5: 16.95, 8: 24.95},
        'CF': {3: 5.95, 5: 9.95, 9: 16.99}
    }

    user_product_qty = {
                'VS5': int(raw_input("How many Vegemite Scrolls you want?:")),
                'MB11': int(raw_input("How many Blueberry muffins you want?")),
                'CF': int(raw_input("How many Croissants you want?"))
                }

    print(get_order(all_products_packs, user_product_qty))


main()



