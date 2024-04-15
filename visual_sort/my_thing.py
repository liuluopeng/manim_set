import random

import numpy

from manimlib import *
from typing import List, Tuple, Dict


# 一个visual item包含:  数字  长方形长条   数字的text
class VisualItem(VGroup):
    num: int
    rec: Rectangle
    tag: Text
    rec_width = 0

    def __init__(self, num: int, width: float):
        self.num = num
        new_rec = Rectangle(width=width, height=num, fill_color=GREEN)
        new_tag = Text(str(num)).next_to(new_rec, DOWN)
        self.rec = new_rec
        self.tag = new_tag
        super().__init__(new_rec, new_tag)


# 继承VGroup的目的是:  原来的vgroup不支持交换元素.
class VisualArr(VGroup):
    min = 0
    max = 0
    size: int
    arr: List[int]
    width: float

    def __init__(self, arr: List[int]):
        self.size = len(arr)
        if len(arr) > 0:
            self.min = min(arr)
            self.max = max(arr)
        self.arr = arr

        self.width = (self.max - self.min) / 2 / 10

        visual_arr: List[VisualItem] = []

        for num in arr:
            new_visual_item = VisualItem(num, width=self.width)
            visual_arr.append(new_visual_item)

        super().__init__(visual_arr)

    def swap_elements(self, index1, index2):
        if 0 <= index1 < len(self) and 0 <= index2 < len(self):
            # print("发生元素交换", index1, index2)
            self.submobjects[index1], self.submobjects[index2] = self.submobjects[index2], self.submobjects[index1]

    def append(self, new_item):
        self.add(new_item)

    def __getitem__(self, index):
        return self.submobjects[index]

    def __setitem__(self, index, value):
        self.submobjects[index] = value


# 一个圆圈 圆圈里面是节点的内容
class TreeNode(VGroup):
    left = None
    right = None
    cir: Circle
    tag: Text

    def __init__(self, val, left=None, right=None, *vmobjects: SubVmobjectType | Iterable[SubVmobjectType], **kwargs):
        self.val = val
        self.left = left
        self.right = right
        self.cir = Circle(radius=0.3, color=GREEN)
        self.tag = Text(str(self.val)).next_to(self.cir, DOWN)
        super().__init__(self.cir, self.tag)


class HowFarAwayFromFather:
    def __init__(self, de_x, de_y):
        self.de_x = de_x
        self.de_y = de_y


# 表示下标的移动  相当于arr[i]
class Subscript(Text):
    index = 0

    def __init__(self, index, msg):
        self.index = index
        super().__init__(msg + ":" + str(index))

    def get_index(self):
        return self.index

    def __iadd__(self, other):
        self.index += other

        return self



# 一个半透明的背景, 用来表示正在处理的范围
class Drape(Rectangle):

    def __init__(self, l, r, rects: VisualArr):  # 左索引  右索引  最高的高度

        width =  rects[r].get_corner(DR)[0] - rects[l].get_corner(DL)[0]
        # print(width)

        height = rects.max

        super().__init__(width=width, height=height,fill_opacity=0.5, fill_color=RED, color=RED, stroke_opacity=0.1,)

        #  重合DL
        cooa = rects[l].get_corner(DL)
        coob = self.get_corner(DL)
        self.shift(RIGHT * (cooa - coob) )
