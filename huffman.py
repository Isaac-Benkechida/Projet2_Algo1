from bytestream import *



class HuffmanTree:
  def __init__(self, freq: int, char: str = None, left = None, right = None):
    self.char = char
    self.freq = freq
    self.left = left
    self.right = right

  def __repr__(self):
    # N'hésitez pas à modifier cette fonction
    return f"({self.char}:{self.freq})"



def build_freqs(text: str) -> dict[str, int]:
  letter_freq = dict()
  for letter in text: 
    existant_key = letter_freq.get(letter)
    if existant_key is not None: #if the key already exists
      letter_freq[letter]+=1 
    else:
      letter_freq[letter] = 1 #initialise a new key
  return letter_freq

def build_node_list(freqs: dict[str, int]):
  nodes = []
  for element in freqs:
    node = HuffmanTree(freqs[element],element)
    nodes.append(node)
  return nodes




def build_huffman_tree(freqs: dict[str, int]) -> HuffmanTree:
  #build a list of nodes

  nodes = build_node_list(freqs)
  if len(nodes) == 0:
    return None
  
  while len(nodes) > 1:
    nodes.sort(key=lambda node: node.freq)
    smallest_node_f1 = nodes.pop(0)
    smallest_node_f2 = nodes.pop(0)

    parent_frequence = smallest_node_f1.freq + smallest_node_f2.freq
    parent = HuffmanTree(parent_frequence,None,smallest_node_f1,smallest_node_f2) #build parent node
    
    nodes.append(parent)

  huffman_tree = nodes[0]
  return huffman_tree




#build the encoding dictionnary by traversing each node of the tree (inorder traversal)
def build_encodings(tree: HuffmanTree) -> dict[str, str]:
  encoding = dict()
  stack = [(tree,"")]

  if tree is None: #edge case
    return encoding
  
  while len(stack) > 0:
      node,node_path = stack.pop() #extract the node and the path that leads to the node
      if node.char is not None: #check if it's a leaf
        encoding[node.char] = node_path
      else:
        if node.right is not None: #going right
          stack.append((node.right,node_path+"1"))
        if node.left is not None: #going left
          stack.append((node.left,node_path+"0"))
  return encoding



def huffman_encode(plain: str, tree: HuffmanTree) -> bytes:
  encodings = build_encodings(tree)
  compressed = ""
  for character in plain:
    compressed = encodings[character]+compressed

  return bin2bytes(compressed)



def huffman_decode(bytestream: bytes, tree: HuffmanTree) -> str:
  compressed = bytes2bin(bytestream)
  plain = ""
  if tree is None:
    return plain
  
  node = tree
  for character in compressed:
    if character == "0": #go left when encountering a 0
      node = node.left
    else:  #go right when encountering a 1
      node = node.right

    if node.char is not None: #found a character in the tree (leaf)
      plain = plain + node.char
      node = tree # go back to the biggining of the tree
  

  return plain


def print_visual_tree(tree: HuffmanTree, level=0, prefix=""):
    if tree is None:
        return
    
    # Print current node
    print("   " * level + prefix + f"({tree.char if tree.char else 'None'}:{tree.freq})")
    
    # Recursively print left and right subtrees
    if tree.left or tree.right:
        print_visual_tree(tree.left, level + 1, "├── ")
        print_visual_tree(tree.right, level + 1, "└── ")


with open("./LICENCE.txt") as f:
    plain = f.read()
    freqs = build_freqs(plain)
    tree = build_huffman_tree(freqs)
    print_visual_tree(tree)
    build_encodings(tree)
