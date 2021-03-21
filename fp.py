import os
import psutil
import time
import argparse
from itertools import combinations
from tqdm import tqdm

class FP:
    def __init__(self, root):
        self.root = root
        #self.result = dict()
        self.max_mem = -1    
    def make_c1(self):
        c1 = dict()
        for line in self.dat:
            for item in line:
                #print(c1)
                if item in c1:
                    c1[item]+=1
                else:
                    c1[item]=0
        return c1
    
    def make_l1(self, c1):
        entry_to_be_deleted = []
        for key in c1.keys():
            if c1[key]<self.min_sup:
                entry_to_be_deleted.append(key)
        for entry in entry_to_be_deleted:
            del c1[entry]
        #print(c1)
        return c1

    def read_data(self, data_path="chess.dat"):
        f = open(data_path,'r')
        #self.dat = [[chr(int(word))] for line in f for word in line.strip().split()]
        self.dat = []
        for line in f:
            a = []
            for word in line.strip().split():
                a.append(chr(int(word)))
            self.dat.append(a)
        #print(self.dat)
    def process_line(self, line, p1, ht):
        to_add_in_tree = []
        for key in p1.keys():
            if key in line:
                to_add_in_tree.append((key, line.count(key)))
        #print(to_add_in_tree)
        self.add_in_tree(self.root, to_add_in_tree, pos=0, ht=ht)

    def add_in_tree(self, node, to_add_in_tree, pos, ht):
        if pos>=len(to_add_in_tree):
            return
        for child in node.children:
            if child.data == to_add_in_tree[pos][0]:
                child.add_count(to_add_in_tree[pos][1])
                self.add_in_tree(child, to_add_in_tree, pos+1, ht)
                return
        new_node = Node(to_add_in_tree[pos][0])
        new_node.add_count(to_add_in_tree[pos][1])
        node.add_child(new_node)
        if to_add_in_tree[pos][0] in ht:
            ht[to_add_in_tree[pos][0]].append(new_node)
        else:
            ht[to_add_in_tree[pos][0]] = []
            ht[to_add_in_tree[pos][0]].append(new_node)
        self.add_in_tree(new_node, to_add_in_tree, pos+1, ht)
        return
    def down_to_up(self, node, pattern):
        if node == None:
            return pattern
        #print(pattern)
        return self.down_to_up(node.parent, node.data+pattern)

    def recursive_count_(self, pattern, value, cnt,  tmp):
        if value == None:
            return
        if len(pattern) ==0:
            return
        if value.data in pattern:
            if value.data in tmp:
                    tmp[value.data] += cnt
            else:
                tmp[value.data] = cnt
        self.recursive_count_(pattern, value.parent, cnt, tmp)

    def recursive_count(self, pattern, values, cnt, tmp):
        #print(values)
        for value in values:
            cnt = value.count
            self.recursive_count_(pattern, value.parent, cnt, tmp)
    def extract(self, last, values):
        all_found = {}
        all_patterns = []
        for value in values:
            cnt = value.count
            found = self.down_to_up(value.parent, "")
            all_patterns.append(found)
            for i in found:
                if i in all_found:
                    all_found[i] += cnt
                else:
                    all_found[i] = cnt
        #print(all_found)
        entry_to_be_deleted = []
        key_to_be_deleted = []
        for key in all_found.keys():
            if all_found[key]<self.min_sup:
                key_to_be_deleted.append(key)
                entry_to_be_deleted.append(key)
        for entry in entry_to_be_deleted:
            del all_found[entry]
        for pattern in all_patterns:
            tmp = {}
            for key in key_to_be_deleted:
                pattern.replace(key,'')
            first = True
            for i in range(len(pattern), 0, -1):
                for l in combinations(pattern, i):
                    #print(''.join(l))
                    #print([ord(x) for x in ''.join(l)])
                    if first:
                        #print(key, values)
                        self.recursive_count(''.join(l), values, cnt, tmp)
                        #print(tmp)
                        first = False
                    cur_count = self.min_sup
                    for alpha in ''.join(l):
                        cur_count = min(cur_count, tmp[alpha])
                        if cur_count < self.min_sup:
                            break
                    if cur_count >= self.min_sup:
                        print([ord(x) for x in ''.join(l)+last])
        process = psutil.Process(os.getpid())                           
        mem = process.memory_info().rss /1024
        self.max_mem = max(self.max_mem, mem)
        #print(all_found)
        #merged_str = ""
        #for key in all_found.keys():
        #    merged_str+=key
        
        #print(merged_str)



    def run(self, min_sup=70):
        self.min_sup = min_sup*len(self.dat)/100
        print(self.min_sup)
        c1 = self.make_c1()
        l1 = self.make_l1(c1)
        #print(l1)
        p1 = dict(sorted(l1.items(), key=lambda kv: kv[1], reverse=True))
        #print(p1)
        ht = {}
        for line in self.dat:
            self.process_line(line, p1, ht)
        #print(ht)

        for key, values in reversed(ht.items()):
            self.all_counts = {}
            print("################")
            self.extract(key, values)
            print(key, values)
class Node:
    def __init__(self, data):
        self.data = data
        self.children = []
        self.count = 0
        self.parent = None
    def get_children(self):
        return self.children
    def add_child(self, child):
        child.parent = self
        self.children.append(child)
    def add_count(self, cnt):
        self.count += cnt
    #def __repr__(self):
    #    return f"{self.data} {self.children} {self.count}"

def traverse(node):
    print(str(node.data), node.children, node.count, node.parent)
    if len(node.children)==0:
        return
    for child in node.children:
        traverse(child)


if __name__ == "__main__":
    start_time = time.time()
    my_parser = argparse.ArgumentParser(description='')
    my_parser.add_argument('-p', help='the path to list')
    #my_parser.add_argument("-e",action="store_true",help="just a flag argument")
    my_parser.add_argument('-m', help='min support in %')
    args = my_parser.parse_args()


    root = Node("")
    fp = FP(root)

    fp.read_data(vars(args)['p'])
    fp.run(int(vars(args)['m']))
    print(time.time()-start_time)
    print(fp.max_mem)

#traverse(fp.root)
#a = Node("a"); root.add_child(a);
#b = Node("b"); root.add_child(b)
#c = Node("c");b.add_child(c)
#traverse(root)
