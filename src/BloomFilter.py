import math
import mmh3
class BloomFilter:
    def __init__(self, size:int, false_positive_rate:float, num_hash_func:int,num_items:int = 18 ):
        self.num_items = num_items
        self.size = size
        self.bit_array = [0] *self.size
        self.false_positive_rate = false_positive_rate
        self.num_hash_func:int = num_hash_func
        
    
    def add(self, item):
        for i in range(self.num_hash_func):
            index = mmh3.hash(item,i) % self.size
            self.bit_array[index] = 1
    
    def contains(self, item):
        for i in range(self.num_hash_func):
            index = mmh3.hash(item,i) % self.size
            if self.bit_array[index] == 0:
                return False
        return True
    
    #Source: https://stackoverflow.com/a/22467497
    @staticmethod
    def _calculateSize(numItems:int, falsePosValue:float) -> float:
      return round(-numItems *  math.log(falsePosValue) / (math.pow(math.log(2),2)))
    
    # Source: https://stackoverflow.com/a/22467497
    @staticmethod
    def _calculateNumHashes(requiredSize:int, numItems:int) -> float:
      return round(requiredSize / numItems * math.log(2))
    
    @staticmethod
    def bloom_filter_from_desired_accuracy(accuracy:float,amount_items:int):
        bloomFilterSize = BloomFilter._calculateSize(amount_items, 1 - accuracy)
        bloomFilterHashes = BloomFilter._calculateNumHashes(
                bloomFilterSize, amount_items)
        false_positive_rate = 1 - accuracy
        return BloomFilter(bloomFilterSize,false_positive_rate ,bloomFilterHashes,amount_items)

    def export(self):
        return {
            "size":self.size,
            "num_hash_func":self.num_hash_func,
            "bit_array":self.bit_array,
            "false_positive_rate":self.false_positive_rate
        }
    
    @staticmethod
    def import_bloom_filter(json:dict):
        bf = BloomFilter(json["size"],json["num_hash_func"],json["false_positive_rate"])
        bf.bit_array = json["bit_array"]
        return bf

    def __str__(self) -> str:
        return f"BloomFilter(size={self.size},num_hash_func={self.num_hash_func},false_positive_rate={self.false_positive_rate},num_items={self.num_items})"
        
                               
