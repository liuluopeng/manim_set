import random
import sys

sys.path.append(".")
sys.path.append("..")

from my_thing import *
from manimlib import *


class InsertionSort(Scene):
    inner_duration = 0.5

    arr = []
    arr = [1, 7, 4, 9, 6, 8, 3, 5]
    rects: [VisualItem]


    def construct(self) -> None:
        self.rects = VisualArr(self.arr)
        self.add(self.rects)

        self.rects.arrange(RIGHT, center=True, aligned_edge=DOWN)

        # 第一个元素是有顺序的, 从第二个元素开始
        for i in range(1, len(self.rects)):
            # arr[i] 可能的落位是[i,len(arr)-1]
            for j in range(len(self.rects) - 1, i, -1):
                if self.rects[j - 1].num > self.rects[j].num:
                    # self.rects.swap_elements(j, j - 1)
                    self.play_swap(j-1, j )
        self.rects.arrange(RIGHT, center=True, aligned_edge=DOWN)

        pass

    # 展示两个长条的交换过程
    def play_swap(self, l, r):

        cooa = self.rects[l].get_corner(DL)
        coob = self.rects[r].get_corner(DL)
        self.rects.swap_elements(l, r - 1)
        self.play(
            self.rects[l].animate.shift(LEFT * (cooa - coob)),
            self.rects[r].animate.shift(RIGHT * (cooa - coob)),
            run_time=self.inner_duration
        )

        pass
