import os
import argparse
class DS:
    def __init__(self):
        pass
        #self.result = dict()
    
    def read_data(self, data_path="kosarak.dat"):
        self.data_path = data_path
        f = open(data_path,'r')
        #self.dat = [[chr(int(word))] for line in f for word in line.strip().split()]
        self.dat = []
        for line in f:
            a = []
            for word in line.strip().split():
                a.append(chr(int(word)))
            self.dat.append(a)
    def make_stat(self):
        #print(self.dat)
        self.size = os.path.getsize(self.data_path)/(1024*1024)
        self.trans = len(self.dat)
        all_items = [itm for line in self.dat for itm in line]
        all_items = set(all_items)
        self.items = len(all_items)
        

        # max TL
        cur_max = -100000000
        sum_t = 0
        for line in self.dat:
            cur_max = max(cur_max, len(line))
            sum_t += len(line)
        self.max_tl = cur_max

        #avg TL
        self.avg_tl = sum_t / self.trans

        # avg_tl / #item
        self.avg_tl_per_item = self.avg_tl/self.items*100.0
        print(f"| {self.data_path} | {self.size:.2f} | {self.trans} | {self.items} | {self.max_tl} | {self.avg_tl:.2f} | {self.avg_tl_per_item:.2f} |")
        #print("___")


        

#import os
#import psutil
#process = psutil.Process(os.getpid())
#print(process.memory_info().rss /1024)


if __name__ == "__main__":
    my_parser = argparse.ArgumentParser(description='')
    my_parser.add_argument('-p', help='the path to list')
    #my_parser.add_argument("-e",action="store_true",help="just a flag argument")
    args = my_parser.parse_args()

    ds = DS()

    ds.read_data(vars(args)['p'])
    ds.make_stat()
