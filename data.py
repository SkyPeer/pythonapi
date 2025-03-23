class Data:
    def __init__(self):
        self.items = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']

    def get_items_with_offset(self, offset):
        items_length = len(self.items)
        offset = slice(offset, items_length)
        # print(self.items)
        return self.items[offset]

    def get_fruits(self):
        self.items = ["item1", "item2", "item3"]
        # for item in self.items:
        #     print('item',item)
        return self.items