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
  pass  # TODO



def build_huffman_tree(freqs: dict[str, int]) -> HuffmanTree:
  pass  # TODO



def build_encodings(tree: HuffmanTree) -> dict[str, str]:
  pass  # TODO



def huffman_encode(plain: str, tree: HuffmanTree) -> bytes:
  encodings = build_encodings(tree)

  compressed = ""  # TODO

  return bin2bytes(compressed)



def huffman_decode(bytestream: bytes, tree: HuffmanTree) -> str:
  compressed = bytes2bin(bytestream)

  plain = ""  # TODO

  return plain
