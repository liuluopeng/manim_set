import random
import sys

import numpy

sys.path.append(".")
sys.path.append("..")

from my_thing import *
from manimlib import *


# 使用最小堆进行排序.

class HeapSort(Scene):
    arr = [1, 7, 4, 9, 6, 8, 3, 5]

    arr = []
    for i in range(10):
        arr.append(random.randint(1,10))

    # arr = [1, 7,]

    min_heap = MinHeap()



    inner_duration = 0.2

    def construct(self) -> None:
        self.add(self.min_heap)

        # self.play_insert_tree(99)
        # self.play_insert_tree(88)
        # self.play_insert_tree(10)
        # return

        for num in self.arr:
            self.play_insert_sq_arr(num)
            self.play_insert_tree(num)

        print("现在的最小堆", self.min_heap.sq_arr.get_num_list())

        res = MinHeapArr()
        self.add(res)


        # print("7的左右", self.min_heap.tree.root.left.val, "  ", self.min_heap.tree.root.val, " ",self.min_heap.tree.root.left.right.val)

        while not self.min_heap.is_empty():
            res.add(self.min_heap.sq_arr.pop().copy())

            self.play_queeee(res)
            self.play(res.animate.shift(DOWN), run_time=self.inner_duration)

            self.min_heap.tree.pop()

        print("用最小堆的排序结果", res)

    def play_insert_sq_arr(self, num):
        # 加入前:

        for i in range(0, len(self.min_heap.sq_arr.submobjects) - 1):
            # 寻找-1位置的DL, 然后拼接上.
            i_position = self.min_heap.sq_arr.submobjects[i].get_corner(DR)
            i1_position = self.min_heap.sq_arr.submobjects[i + 1].get_corner(DL)

            # print(last_elem_DR_position)

            move_vector = i_position - i1_position

            # self.min_heap.sq_arr.submobjects[i + 1].shift(move_vector)

            self.min_heap.sq_arr[i + 1].next_to(self.min_heap.sq_arr[i], RIGHT)

        # 加入:
        # res_tup = self.min_heap.insert(num)
        res_tup = self.min_heap.sq_arr.insert(num)

        # 动画 是 一个元素贴到后面.

        new_sq = res_tup[0]
        new_sq.next_to(self.min_heap.sq_arr[-1], RIGHT)
        self.play(new_sq.animate.shift(UP), run_time=self.inner_duration)
        self.play(new_sq.animate.shift(DOWN), run_time=self.inner_duration)

        # 加入后:
        for i in range(0, len(self.min_heap.sq_arr.submobjects) - 1):
            # 寻找-1位置的DL, 然后拼接上.
            i_position = self.min_heap.sq_arr.submobjects[i].get_corner(DR)
            i1_position = self.min_heap.sq_arr.submobjects[i + 1].get_corner(DL)

            # print(last_elem_DR_position)

            move_vector = i_position - i1_position

            # self.min_heap.sq_arr.submobjects[i + 1].shift(move_vector)

            self.min_heap.sq_arr[i + 1].next_to(self.min_heap.sq_arr[i], RIGHT)

        # new_sq.move_to(numpy.array([0,0,0]))

        # 闪动一下新加入的元素
        # self.play(new_sq.animate.shift(UP*5), run_time= self.inner_duration)

        # 闪动一下最后一个元素
        # self.play(FadeIn(self.min_heap.sq_arr[-1] ), run_time=self.inner_duration)

        # 闪动一下 新元素的最后的位置
        # self.play(self.min_heap.sq_arr[ res_tup[2] ].animate.shift(UP) , run_time=self.inner_duration)

        self.play(self.min_heap.sq_arr[res_tup[2]].animate.shift(UP), run_time=self.inner_duration)
        self.play(self.min_heap.sq_arr[res_tup[2]].animate.shift(DOWN), run_time=self.inner_duration)

        print("闪动的是", self.min_heap.sq_arr[res_tup[2]].num)

        # 实际动作中记录了 每次 交换的两个索引
        swap_msg = res_tup[1]
        print("交换:", swap_msg)

    def play_insert_tree(self, num):

        print(self.min_heap.tree)

        # 实际:
        self.min_heap.tree.insert(num)

        # 展示一下:
        self.min_heap.tree.zl_tree()


    def play_queeee(self, sq_arr):
        for i in range(0, len(sq_arr) - 1):
            sq_arr[i + 1].next_to(sq_arr[i], RIGHT)
