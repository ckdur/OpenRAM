
class drc_lut():
    """ 
    Implement a lookup table of rules. 
    Each element is a tuple with the last value being the rule.
    It searches through backwards until all of the key values are
    met and returns the rule value.
    For exampe, the key values can be width and length,
    and it would return the rule for a wire of a given width and length.
    A key can be not compared by passing a None.
    """
    def __init__(self, table):
        self.table = table

    def __call__(self, *args):
        """
        Lookup a given tuple in the table.
        """
        
        key_tuple = args
        if not key_tuple:
            key_size = len(list(self.table.keys())[0])
            key_tuple = tuple(0 for i in range(key_size))
        for key in sorted(self.table.keys(), reverse=True):
            if self.match(key_tuple, key):
                return self.table[key]

    def match(self, t1, t2):
        """
        Determine if t1>t2 for each tuple pair.
        """
        # If any one pair is less than, return False
        for i in range(len(t1)):
            if t1[i] < t2[i]:
                return False
        return True
                
            
        

