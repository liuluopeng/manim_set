import random
import sys

import numpy

sys.path.append(".")
sys.path.append("..")

from my_thing import *
from manimlib import *


class MergeSort(Scene):
    inner_duration = 0.5

    arr = []
    arr = [1, 7, 4, 9, 6, 8, 3, 5]
    rects: [VisualItem]

    def construct(self) -> None:
        self.rects = VisualArr(self.arr)

        def _merge_sort(rects, l, r):
            if l >= r:
                return

            mid = (l + r) // 2
            _merge_sort(rects, l, mid)
            _merge_sort(rects, mid + 1, r)

            # 能到这一步, 已经能保证[l1,mid] [mid + 1, r2]这两个数组都是有序的, 用这个两个有序数组构造出一个有序数组
            i = Subscript(l, "i")
            j = Subscript(mid + 1, "j")
            i.next_to(self.rects[l], UP)
            j.next_to(self.rects[mid + 1], UP)



            temp_rects: VisualArr = VisualArr([])
            self.add(i, j)
            self.add(temp_rects)

            drape = Drape(l, r, self.rects)
            print("范围", l,  mid , "     ", mid+1, r)
            self.add(drape)

            # 只要有一个的数组还没有遍历完:
            k = l
            while i.index != mid + 1 or j.index != r + 1:

                # 标注

                if i.index == mid + 1:  # 这种情况第一个数组走完了, 把第二个数组填补到新数组即可

                    self.play_temp_arr_append(temp_rects, self.rects[j.index], k)
                    self.play_sub_move_iadd(j)
                    k += 1
                elif j.index == r + 1:

                    self.play_temp_arr_append(temp_rects, self.rects[i.index], k)
                    self.play_sub_move_iadd(i)
                    k += 1
                elif self.rects[i.index].num < self.rects[j.index].num:

                    self.play_temp_arr_append(temp_rects, self.rects[i.index], k)
                    self.play_sub_move_iadd(i)
                    k += 1
                else:

                    self.play_temp_arr_append(temp_rects, self.rects[j.index], k)
                    self.play_sub_move_iadd(j)
                    k += 1

            # print(self.rects)

            nonlocal  coo_msg
            for k in range(l, r + 1):
                self.play_move_temp_to_arr(temp_rects, l, k, coo_msg)


            print("\t结果", self.rects[l].num, self.rects[r].num, )

            # self.remove(temp_rects)
            # pos_list = []

            self.remove(i, j)
            self.remove(drape)

        self.add(self.rects)
        self.rects.arrange(RIGHT, center=True, aligned_edge=DOWN)

        # 在这里, 记录下初始 的 位置 , 方便归并后 把 temp arr 移动到原来的位置
        coo_msg = []
        for i in range(0, len(self.rects)):
            coo_msg.append(self.rects[i].get_corner(DL))

        print("初始的位置", coo_msg)

        _merge_sort(self.rects, 0, len(self.rects) - 1)

        self.rects.arrange(RIGHT, center=True, aligned_edge=DOWN)

    # 移动一个单位的动画
    def play_sub_move_iadd(self, subs: Subscript):

        # 先实际移动
        subs += 1

        # 然后再动画演示
        if subs.index < len(self.rects):
            self.play(subs.animate.next_to(self.rects[subs.index], UP), run_time=self.inner_duration)
        else:
            pass

    # 临时数组的新元素加入 的 动画
    def play_temp_arr_append(self, temp_rects, new_elem, k ):
        # new_elem_c = new_elem.copy()

        new_elem_c = new_elem
        # 实际
        temp_rects.append(new_elem_c)

        # 动画
        # 虚线移动new ele

        # self.play(new_elem.animate.shift(UP), run_time=self.inner_duration)

        # self.play(new_elem_c.animate.shift(DOWN * 3), run_time=self.inner_duration)

        self.play(self.rects[k].animate.shift(DOWN * 10), run_time=self.inner_duration)
    # 放回去的动画
    def play_move_temp_to_arr(self, temp_rects, offset, now_index, pos_list):
        # 实际
        # ori = self.rects[now_index]
        # self.rects.remove(ori)

        self.rects[now_index] = temp_rects[now_index - offset]

        # 动画
        #  重合DL
        coo_now = temp_rects[now_index - offset].get_corner(DL)
        coo_dest = pos_list[now_index]

        move_vector = coo_dest - coo_now
        print(move_vector, "移动的向量", coo_now, "去 ", coo_dest, self.rects[now_index])
        self.play(temp_rects[now_index-offset].animate.shift(move_vector), run_time=self.inner_duration)
