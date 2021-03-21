from tqdm import tqdm

class Apriori:
    def __init__(self, root):
        self.root = root
        #self.result = dict()
    
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
    
    
    def join(self, l):
        c = dict()
        for left in l.keys():
            for right in l.keys():
                if left[-1] < right[-1] and left[:-1]==right[:-1]:
                    c[left+right[-1]] = 0
        return c

    def add_l_in_tree(self, node, l, pos = 0):
        if len(l)==pos:
            node.count += 1
            self.hash_pointer[l] = node
            return
        for child in node.children:
            if child.data == l[pos]:
                self.add_l_in_tree(child, l, pos+1)
                return
        new_node = Node(l[pos])
        node.add_child(new_node)
        self.add_l_in_tree(new_node, l, pos+1)
        return
    
    def process_line(self, node, line, depth, count = 1e8):
        for child in node.children:
            if child.data in line:
                count = min(count,line.count(child.data))
                if depth == 1:
                    child.count += count
                else:
                    self.process_line(child, line, depth - 1, count)



    def run(self, min_sup = 3000):
        self.min_sup = min_sup
        
        c1 = self.make_c1()
        l1 = self.make_l1(c1)
        print(c1)
        print(l1)
        self.hash_pointer = dict()
        for key in l1.keys():
            self.add_l_in_tree(self.root, key, pos=0)
        for line in tqdm(self.dat):
            self.process_line(self.root,line,depth=1)
#        self.hash_pointer = dict()
        l =l1
        for depth in range(1,100000000):
            print("###########")
            c = self.join(l)
            #print("#", c.keys())
            if len(c.keys())==0:
                break
            for key in c.keys():
                self.add_l_in_tree(self.root, key, pos = 0)
            #print('# : ', self.hash_pointer)
            for line in tqdm(self.dat):
                self.process_line(self.root, line, depth)
            l = dict()
            for key, value in reversed(self.hash_pointer.items()):
                if len(key)<depth:
                    break
                if len(key) == depth and value.count >= self.min_sup:
                    l[key] = value.count
            for i in l.keys():
                print(depth, i, len(i))
            print(f"Candidate {len(c.keys())} Pruned {len(l.keys())}")
class Node:
    def __init__(self, data):
        self.data = data
        self.children = []
        self.count = 0
    def get_children(self):
        return self.children
    def add_child(self, child):
        self.children.append(child)
    def add_count(self, cnt):
        self.count = cnt

def traverse(node):
    print(node.data, node.count, node.children)
    if len(node.children)==0:
        return
    for child in node.children:
        traverse(child)

root = Node("")
apriori = Apriori(root)
apriori.read_data()
apriori.run()
#traverse(apriori.root)
print(apriori.hash_pointer)
