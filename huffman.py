from bytestream import *

class HuffmanTree:
  def __init__(self, freq: int, char: str = None, left = None, right = None):
    self.char = char
    self.freq = freq
    self.left = left
    self.right = right

  def __repr__(self):
    return f"({self.char}:{self.freq})"
  

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Helper Functions~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#builds a list of each which each contain a character
def build_node_list(freqs: dict[str, int]):
  nodes = []
  for element in freqs:
    node = HuffmanTree(freqs[element],element)
    nodes.append(node)
  return nodes

#traverses the tree depending on edge number
def traverse_tree(character,node:HuffmanTree):
  if character == "0": #go left when encountering a 0
      node = node.left
  else:  #go right when encountering a 1
    node = node.right
  return node

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Main Methods~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#builds a dictionary associating a letter to its frequency in a given text
def build_freqs(text: str) -> dict[str, int]:
  letter_frequency = dict()
  for letter in text:
    existant_key = letter_frequency.get(letter)
    if existant_key is not None: #if the key already exists
      letter_frequency[letter] += 1 
    else:
      letter_frequency[letter] = 1 #initialise a new key 

  return letter_frequency


#builds the Huffman tree
def build_huffman_tree(freqs: dict[str, int]) -> HuffmanTree:
  #build a list of nodes

  nodes = build_node_list(freqs)
  if len(nodes) == 0:
    return None
  
  while len(nodes) > 1:
    nodes.sort(key=lambda node: node.freq) # sort the list based on the frequency attribute
    smallest_node_f1 = nodes.pop(0)
    smallest_node_f2 = nodes.pop(0)

    parent_frequence = smallest_node_f1.freq + smallest_node_f2.freq #father frequency = sum of children's frequency
    parent = HuffmanTree(parent_frequence,None,smallest_node_f1,smallest_node_f2) #build parent node
    
    nodes.append(parent)

  huffman_tree = nodes[0]
  return huffman_tree




#build the encoding dictionary by traversing each node of the tree (inorder traversal)
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


#create a binary representation of the text
def huffman_encode(plain: str, tree: HuffmanTree) -> bytes:
  encodings = build_encodings(tree)
  compressed = ""
  for character in plain:
    compressed = compressed + encodings[character]
  return bin2bytes(compressed)


#decodes the stored sentence in the huffman tree
def huffman_decode(bytestream: bytes, tree: HuffmanTree) -> str:
  compressed = bytes2bin(bytestream)
  plain = ""
  if tree is None:
    return plain
  
  node = tree
  for character in compressed:
    node = traverse_tree(character,node)

    if node.char is not None: #found a character in the tree (leaf)
      plain = plain + node.char
      node = tree # go back to the beginning of the tree
  

  return plain

