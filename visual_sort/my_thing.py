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

        width = rects[r].get_corner(DR)[0] - rects[l].get_corner(DL)[0]
        # print(width)

        height = rects.max

        super().__init__(width=width, height=height, fill_opacity=0.5, fill_color=RED, color=RED, stroke_opacity=0.1, )

        #  重合DL
        cooa = rects[l].get_corner(DL)
        coob = self.get_corner(DL)
        self.shift(RIGHT * (cooa - coob))


class SqWithNum(VGroup):
    sq: Square
    tag: Text
    num: int

    def __init__(self, num, side_length, *vmobjects: SubVmobjectType | Iterable[SubVmobjectType], **kwargs):
        self.num = num
        self.sq = Square(side_length=side_length)
        self.tag = Text(str(num))

        super().__init__(self.sq, self.tag)


class MinHeapArr(VGroup):
    # 由很多小正方形组成的数组
    side_length = 1

    def __init__(self):
        super().__init__()

    def insert(self, new_num):

        new_sq = SqWithNum(new_num, self.side_length)

        self.add(new_sq)
        # 以0为首    父亲的下标是 (i-1)//2

        index = len(self.submobjects) - 1
        swap_msg = []
        while self.submobjects[(index - 1) // 2].num > self.submobjects[index].num:
            self.swap_elements((index - 1) // 2, index)
            swap_msg.append([(index - 1) // 2, index])
            index = (index - 1) // 2

        return (new_sq, swap_msg, index)

    def pop(self):
        # 先保存第一个元素
        ret = self.submobjects[0]
        # 用最后一个元素 覆盖 第一个元素, 然后逐渐使得最小堆成立.
        self.submobjects[0] = self.submobjects[-1]
        # self.remove(self.submobjects[-1])  # 这个remove不行
        self.submobjects.pop()

        index = 0

        print("开始调整之前", ret, self.get_num_list())
        while index * 2 + 1 < len(self.submobjects):
            # 找到左孩子  右孩子 中比较小的那一个
            less_index = 2 * index + 1
            if 2 * index + 2 < len(self.submobjects):
                if self.submobjects[2 * index + 1].num > self.submobjects[
                    2 * index + 2].num:
                    less_index = 2 * index + 2

            if self.submobjects[index].num < self.submobjects[less_index].num:
                break

            self.swap_elements(index, less_index)
            index = less_index

        print("开始调整之后", ret, self.get_num_list())
        print()

        return ret

    def get_num_list(self) -> List:
        arr = []
        for i in self.submobjects:
            arr.append(i.num)
        return arr

    def swap_elements(self, index1, index2):
        if 0 <= index1 < len(self) and 0 <= index2 < len(self):
            # print("发生元素交换", index1, index2)
            self.submobjects[index1], self.submobjects[index2] = self.submobjects[index2], self.submobjects[index1]


# 最小堆不用竖条. 因为在二叉树中节点用长条不好看.


class MinHeapBTNode(VGroup):

    def __init__(self, val, left, right, father, side,
                 *vmobjects: SubVmobjectType | Iterable[SubVmobjectType], **kwargs):
        self.val = val
        self.left = left
        self.right = right
        self.father = father
        self.side = side
        self.cir = Circle(radius=0.3, color=GREEN)
        self.tag = Text(str(self.val))
        self.tag.move_to(self.cir.get_center())
        self.left_leg = Line()
        self.right_leg = Line()
        self.father_leg = Line()

        super().__init__(self.cir, self.tag)


# # 最小堆的   二叉树
class MinHeapBT(VGroup):
    root = None

    def __init__(self, ):
        super().__init__()

    # 完全二叉树高度公式是
    def get_tree_height(self, nodes_count):
        return 5
        return math.ceil(math.log2(nodes_count + 1)) - 1

    # 用细条连接各个结点  把在内存中没有相对位置的结点  通过next_to在画布中展示位置.
    def zl_tree(self):
        height = self.get_tree_height(99)
        # 展示出所有的结点:     用一个queue
        root = self.root
        queue = []
        if root:
            queue = [root]

        height_now = 0

        # 保存每个遍历过的queue
        tv  = [ ]
        while queue:
            tmp_queue = []
            for curr_node in queue:
                print("现在在画的结点:", curr_node.val)

                if curr_node.side == "left":  # curr_node是从左侧连接到树的.
                    # 改变结点的位置:
                    de_x = - pow(2, (height - height_now - 1))
                    de_y = - 4
                    dis = numpy.array([de_x, de_y, 0])
                    curr_node.next_to(curr_node.father, dis)
                    # 把leg连接到左孩子

                elif curr_node.side == "right":
                    # 改变结点的位置:
                    de_x = pow(2, (height - height_now - 1))
                    de_y = - 2
                    dis = numpy.array([de_x, de_y, 0])
                    curr_node.next_to(curr_node.father, dis)

                if height_now != 0:
                    print("现在的高度:", height_now, tv)
                    line = Line(curr_node, curr_node.father, color=RED)
                    self.add(line)
                    pass

                if curr_node.left:
                    print("左边有 添加", curr_node.left.val)
                    tmp_queue.append(curr_node.left)
                if curr_node.right:
                    print("右边有 添加", curr_node.right.val)

                    tmp_queue.append(curr_node.right)

            print()
            tv.append(queue)
            queue = tmp_queue
            height_now += 1

    #
    def insert(self, num):

        new_node = MinHeapBTNode(val=num, left=None, right=None, father=None, side="")
        self.add(new_node)

        if self.root is None:
            self.root: MinHeapBTNode = new_node
        else:  # 先挂到层序遍历的最后一个节点的后面.
            queue = [self.root]

            while queue:
                node = queue.pop(0)

                if node.left is not None:
                    queue.append(node.left)
                else:
                    # 左孩子 空缺
                    new_node.side = "left"
                    node.left = new_node
                    new_node.father = node
                    break
                if node.right is not None:
                    queue.append(node.right)
                else:
                    # 右孩子 空缺
                    new_node.side = "right"
                    node.right = new_node
                    new_node.father = node
                    break

        # 进行shift up操作
        child_node = new_node
        while child_node.father:
            print("孩子 ", child_node.val, "父亲 ", child_node.father.val)
            if child_node.father.val > child_node.val:
                # father_copy = child_node.father
                self.swap_bt_node(child_node)
                # child_node = father_copy
            else:
                break

    # 在一个二叉树中, 交换父子关系的 两个结点的位置
    def swap_bt_node(self, child_node):
        if child_node is None:
            return

        father_node = child_node.father

        # 如果child_node已经是root: 什么也不做
        if father_node is None:
            return  # 这一行往下 存在父子结点

        print("开始交换二叉树结点", child_node.val, father_node.val)

        bro_node = None
        # 寻找 child_node的兄弟
        if child_node.side == "left":
            bro_node = father_node.right
        elif child_node.side == "right":
            bro_node = father_node.left

        # 寻找 child node 的孩子
        kid_left = child_node.left
        kid_right = child_node.right

        # 更改新的self.root
        if father_node.father is None:
            self.root = child_node

        # 先 改那些影响不大的辅助成员变量: side father     最后再实际改变关系
        grandfather_node = father_node.father

        # child 的左右孩子的父亲  从 child  变成  father
        if kid_left:
            kid_left.father = father_node
        if kid_right:
            kid_right.father = father_node

        # child 的父亲  从 father 变成 祖父
        child_node.father = grandfather_node
        # father 的父亲  变成 child
        father_node.father = child_node
        if bro_node:
            bro_node.father = child_node

        direc_between_child_and_father = child_node.side
        direc_between_father_and_grand = father_node.side

        if direc_between_child_and_father == "left":
            child_node.left = father_node
            child_node.right = bro_node
        elif direc_between_child_and_father == "right":
            child_node.right = father_node
            child_node.left = bro_node
        father_node.left = kid_left
        father_node.right = kid_right

        if direc_between_father_and_grand == "left":
            grandfather_node.left = child_node
        elif direc_between_father_and_grand == "right":
            grandfather_node.right = child_node

        # 让child的来向  变成  father的来向
        child_node.side, father_node.side = father_node.side, child_node.side

        # 输入(孩子, 父亲)
        # 返回(新的孩子, 新的父亲)
        return father_node, child_node
    def pop(self):
        ret = self.root
        # self.remove(ret)

        print("现在二叉树的root 最小值 ", ret.val)

        left_sub = self.root.left
        right_sub = self.root.right

        last_node = self.get_last_node()
        print("last node:  ", last_node.val)


        # 断开 last node 与它父亲的联系
        if last_node.side == "left":
            last_node.father.left = None
        elif last_node.side == "right":
            last_node.father.right = None
        last_node.left = None
        last_node.right = None

        # 左右子树的父亲现在是last node
        if left_sub:
            left_sub.father = last_node
        if right_sub:
            right_sub.father = last_node

        if last_node is not left_sub:
            last_node.left = left_sub
        else:
            last_node.left = None

        if last_node is not right_sub:
            last_node.right = right_sub
        else:
            last_node.right = None

        # last node 要做root了, 它没有父亲:
        last_node.father = None
        last_node.side = ""

        self.root = last_node
        print("新的root ",  last_node.val)

        # 然后开始shift down
        child_node = self.get_smaller_one(left_sub, right_sub)
        father_node = last_node


        while child_node:
            print("看看 是否交换 ", child_node.val, father_node.val)
            if father_node.val > child_node.val:

                print("开始交换 ", child_node.val, father_node.val)

                # new_father: 交换位置后的新父亲
                new_child, new_father = self.swap_bt_node(child_node)

                # 更新:
                father_node = new_child
                child_node = self.get_smaller_one(new_child.left, new_child.right)

            else:  # 这种情况 说明到位了
                break

        # 重新排位置
        self.zl_tree()

    def get_smaller_one(self, node1, node2) -> MinHeapBTNode:
        if node1 is None and node2:
            return node2
        if node2 is None and node1:
            return node1
        if node1 is None and node2 is None:
            return None

        if node1.val < node2.val:
            return node1
        else:
            return node2

    def get_last_node(self) -> MinHeapBTNode:
        if self.root is None:
            return None
        # tree是一个完全二叉树, 用一个queue得到最后一个结点
        queue = [self.root]

        res = []
        while queue:
            tmp_queue = []
            for current_node in queue:
                if current_node.left:
                    tmp_queue.append(current_node.left)
                if current_node.right:
                    tmp_queue.append(current_node.right)
            res.append(queue)
            queue = tmp_queue

        return res[-1][-1]




class MinHeap(VGroup):

    def __init__(self, *vmobjects: SubVmobjectType | Iterable[SubVmobjectType], **kwargs):
        self.sq_arr = MinHeapArr()

        # self.root: MinHeapBTNode = None

        self.tree = MinHeapBT()

        super().__init__(self.sq_arr, self.tree)

    def insert(self, num):
        res1 = self.sq_arr.insert(num)
        res2 = self.tree.insert(num)

        return res1

    def pop(self):
        ret = self.sq_arr.pop()

        ret2 = self.tree.pop()
        return ret

    def is_empty(self) -> bool:
        return len(self.sq_arr.submobjects) == 0

    def print_num(self):
        arr = []
        for i in self.sq_arr.submobjects:
            arr.append(i.num)
        print(arr)
