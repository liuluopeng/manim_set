import random

import numpy

from manimlib import *
from typing import List, Tuple, Dict


# 一个visual item包含:  数字  长方形长条   数字的text
class VisualItem(VGroup):
    num: int
    rec: Rectangle
    tag: Text

    def __init__(self, num: int):
        self.num = num
        new_rec = Rectangle(width=0.5, height=num, fill_color=GREEN)
        new_tag = Text(str(num)).next_to(new_rec, DOWN)
        self.rec = new_rec
        self.tag = new_tag
        super().__init__(new_rec, new_tag)


# 继承VGroup的目的是:  原来的vgroup不支持交换元素.
class VisualArr(VGroup):
    min = 0
    max = 0
    arr: List[int]

    def __init__(self, arr: List[int]):
        visual_arr: List[VisualItem] = []
        for num in arr:
            new_visual_item = VisualItem(num)
            visual_arr.append(new_visual_item)
        self.min = min(arr)
        self.max = max(arr)
        self.arr = arr
        super().__init__(visual_arr)

    def swap_elements(self, index1, index2):
        if 0 <= index1 < len(self) and 0 <= index2 < len(self):
            # print("发生元素交换", index1, index2)
            self.submobjects[index1], self.submobjects[index2] = self.submobjects[index2], self.submobjects[index1]

    def __getitem__(self, index):
        return self.submobjects[index]

    def __setitem__(self, index, value):
        self.submobjects[index] = value





# 一个圆圈 圆圈里面是节点的内容
class TreeNode(VGroup):

    left = None
    right = None
    cir : Circle
    tag : Text
    def __init__(self, val, left=None, right=None, *vmobjects: SubVmobjectType | Iterable[SubVmobjectType], **kwargs):
        self.val = val
        self.left = left
        self.right = right
        self.cir = Circle(radius=0.3, color=GREEN)
        self.tag = Text(str(self.val)).next_to(self.cir, DOWN)
        super().__init__(self.cir, self.tag)

def prettyPrintTree(node, prefix="", isLeft=True):
    if not node:
        print("Empty Tree")
        return

    if node.right:
        prettyPrintTree(node.right, prefix + ("│   " if isLeft else "    "), False)

    print(prefix + ("└── " if isLeft else "┌── ") + str(node.val))

    if node.left:
        prettyPrintTree(node.left, prefix + ("    " if isLeft else "│   "), True)


# # 一个二叉树 继承自vgroup
# class VisualBinaryTree(VGroup):
#
#
#     # 添加元素
#     def add(self, item, side)   :
#         pass

