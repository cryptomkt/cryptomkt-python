from decimal import Decimal
from enum import Enum


class OB_state(Enum):
    UPDATING = 0
    BROKEN = 1
    WAITING = 2

class SideOrder(Enum):
    ASCENDING = 0
    DESCENDING = 1

methodSnapshotOrderbook = "snapshotOrderbook"
methodUpdateOrderbook = "updateOrderbook"

class OrderbookCache:
    def __init__(self):
        self.orderbooks = dict()
        self.ob_states = dict()
    
    def update(self, method: str, key:str, new_data: dict):
        if method == methodSnapshotOrderbook:
            # a new orderbook is always fine, and is updating
            self.ob_states[key] = OB_state.UPDATING
            self.orderbooks[key] = new_data
            return self.orderbooks[key].copy()

        elif method == methodUpdateOrderbook:
            # orderbook must be updating
            if self.ob_states[key] != OB_state.UPDATING: 
                return
            # must be the next update of the orderbook, else is broken
            if new_data['sequence'] - self.orderbooks[key]['sequence'] != 1:
                self.ob_states[key] = OB_state.BROKEN
                return
            # updating orderbook
            old_orderbook = self.orderbooks[key]
            old_orderbook['sequence'] = new_data['sequence']
            old_orderbook['timestamp'] = new_data['timestamp']
            for side, sortOrder in [('ask', SideOrder.ASCENDING), ('bid', SideOrder.DESCENDING)]:
                old_orderbook[side] = update_book_side(old_orderbook[side], new_data[side], sideOrder=SideOrder)

    def get_ob(self, key):
        if key not in self.orderbooks: return None
        return self.orderbooks[key]

    def orderbook_broken(self, key):
        return self.ob_states[key] == OB_state.BROKEN
            
    def wait_orderbook(self, key):
        self.orderbooks_states[key] = OB_state.WAITING
        
    def orderbook_wating(self, key):
        return self.ob_states[key] == OB_state.WAITING


def update_book_side(old_list, update_list, sideOrder):
    new_list = []
    old_idx = 0
    update_idx = 0
    # add entries until one list of entries is empty
    while update_idx < len(update_list) and old_idx < len(old_list):
        update_entry = update_list[update_idx]
        old_entry = old_list[old_idx]
        order = price_order(old_entry, update_entry, sideOrder)
        # if both entries have the same price
        if order == 0:
            # we append the new entry, unless it has a zero size
            if not zero_size(update_entry): new_list.append(update_entry)
            update_idx += 1
            old_idx += 1
        # if the old entry goes first
        elif order == 1:
            new_list.append(old_entry)
            old_idx += 1
        # if the new entry goes first
        else:
            new_list.append(update_entry)
            update_idx += 1
        
    # we add the rest of entries of the not empty list
    if update_idx == len(update_list):
        for idx in range(old_idx, len(old_list)):
            new_list.append(old_list[idx])
    if old_idx == len(old_list):
        for idx in range(update_idx, len(update_list)):
            entry = update_list[idx]
            if not zero_size(entry): new_list.append(entry)
    return new_list

def zero_size(entry): 
    size = Decimal(entry['size'])
    return size.compare(Decimal('0.00')) == 0

def price_order(old_entry, update_entry, sideOrder):
    old_price = Decimal(old_entry['price'])
    update_price = Decimal(update_entry['price'])
    order = old_price.compare(update_price)
    if sideOrder == SideOrder.ASCENDING: return order
    return -order
