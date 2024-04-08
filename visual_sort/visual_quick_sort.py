
import sys
sys.path.append(".")
sys.path.append("..")


from my_thing import *


from manimlib import *
from typing import List, Tuple, Dict

class QuickSort(Scene):
    # 播放速度
    inner_duration = 0.5
    arr = [1, 7, 4, 9, 6, 8, 3, 5]

    # 提前执行一次快速排序, 目的是知道二叉树的规模. 把根放到何时的位置
    def get_root_position(self) -> int:
        cp_arr = self.arr.copy()
        max_depth = -1
        def qs(arr, l, r, my_depth):
            nonlocal max_depth
            if my_depth > max_depth:
                # print(my_depth, l, r, arr)
                max_depth = my_depth
            if l>=r :
                return
            pivot = arr[r]
            wait = l
            for k in range(l, r):
                if arr[k] < pivot :
                    arr[k], arr[wait] = arr[wait], arr[k]
                    wait += 1
            arr[wait], arr[r] = arr[r], arr[wait]
            qs(arr, l, wait - 1, my_depth + 1)
            qs(arr, wait + 1, r, my_depth + 1)
        qs(cp_arr, 0, len(cp_arr)-1, 0)
        return max_depth




    def construct(self) -> None:

        self.camera.frame.scale(2)

        rect_list = VisualArr(self.arr)
        self.add(rect_list)

        rect_list.arrange(RIGHT, center=True, aligned_edge=DOWN)

        root: TreeNode = TreeNode( (0, len(self.arr) - 1))
        root.shift(RIGHT * 5 + UP * 5)
        max_depth = self.get_root_position()
        # print("root的深度",depth, self.arr)

        self.add(root)


        def quicksort(rect_list: VisualArr, l, r, depth: int, my_root: TreeNode):
            print("\t"*depth , "进入函数", l, r)

            # # 产生 示意递归  的 二叉树  的节点

            rect_list.arrange(RIGHT, center=True, aligned_edge=DOWN, )

            if l >= r:
                print("\t" * depth ,"发生返回", l, r)
                # 这里 用一个返回的小箭头 代表递归到底了.向上返回.
                self.play(FadeIn(my_root), run_time=self.inner_duration)
                return

            pivot_rect: VisualItem = rect_list[r]
            wait_for_small_than_pivot = l
            # 把i创建一个标签

            wait_tag = Text("c", ).next_to(rect_list[l], UP)

            line_unordered = Line(rect_list[l].get_corner(DL), rect_list[r].get_corner(DR), )
            line_unordered.set_color(YELLOW)

            # 创建一个半透明的背景 来表示当前处理数据的范围:
            width_vector = pivot_rect.get_corner(DR) - rect_list[l].get_corner(DL)
            range_doing = Rectangle(fill_opacity=0.5, fill_color=RED, color=RED, stroke_opacity=0.1, width=width_vector[0],
                                    height=rect_list.max + 1)

            range_doing.shift(rect_list[l].get_corner(DL) - range_doing.get_corner(DL))

            # range_doing.next_to(line_unordered)
            self.add(range_doing)

            self.add(wait_tag)
            self.add(line_unordered)

            # 把对比的方块染色
            self.play(pivot_rect.animate.set_color(RED), run_time=self.inner_duration)

            for i in range(l, r):
                i_tag = Text("i" + str(i)).next_to(rect_list[i], UP)
                self.play(FadeIn(i_tag), run_time=self.inner_duration)
                if rect_list[i].num < pivot_rect.num:
                    rect_list.swap_elements(wait_for_small_than_pivot, i)

                    # 展示交换过程
                    # 计算移动距离
                    cooa = rect_list[wait_for_small_than_pivot].get_corner(DL)
                    coob = rect_list[i].get_corner(DL)
                    # cooa - coob >= 0
                    # print(cooa, coob)
                    self.play(
                        rect_list[wait_for_small_than_pivot].animate.shift(LEFT * (cooa - coob)),
                        rect_list[i].animate.shift(RIGHT * (cooa - coob)),
                        run_time=self.inner_duration,
                    )

                    wait_for_small_than_pivot += 1
                    # 移动 等待更小的坐标tag
                    cooa = rect_list[1].get_corner(DL)
                    coob = rect_list[0].get_corner(DL)
                    self.play(wait_tag.animate.shift(RIGHT * (cooa - coob)), run_time=self.inner_duration)

                self.remove(i_tag)

            rect_list.swap_elements(wait_for_small_than_pivot, r)

            cooa = rect_list[wait_for_small_than_pivot].get_corner(DL)
            coob = rect_list[r].get_corner(DL)
            self.play(
                rect_list[wait_for_small_than_pivot].animate.shift(LEFT * (cooa - coob)),
                rect_list[r].animate.shift(RIGHT * (cooa - coob)),
                run_time=self.inner_duration
            )

            # 恢复颜色
            self.play(pivot_rect.animate.set_color(WHITE), run_time=self.inner_duration)

            self.remove(line_unordered)
            self.remove(wait_tag)
            self.remove(range_doing)


            # todo 这里 把两侧的区域 闪烁表示一下.


            left = TreeNode((l, wait_for_small_than_pivot - 1))

            # 默认的方向DL  DR 会造成重叠, 所以要找一个那种比较匾的方向
            # 那种比较匾的方向还是会造成重叠,  构成了一个平行四边形,  所以 节点的连线要 随着深度, 逐渐变小
            # 我是边走边画出二叉树, 无法提前知道最宽处,  只能把最宽处设置成最坏情况.   最坏情况: 退化成链表.二叉树有n层
            # 655. 输出二叉树 - 力扣（LeetCode）
            # https://leetcode.cn/problems/print-binary-tree/description/

            # 2024年04月08日 21:42:48 还是要提前算一遍, 确定二叉树的根的位置在屏幕的中间.   如果边执行边添加节点, 二叉树可能会偏离屏幕.

            de_y = - 1
            de_x =  - pow(2, ( max_depth - depth + 1 ))
            dis  = numpy.array([de_x, de_y, 0])
            left.next_to(my_root, dis)
            # 创建连线
            line = Line(my_root, left, color=YELLOW)

            self.add(left, line)

            quicksort(rect_list, l, wait_for_small_than_pivot - 1, depth + 1, my_root = left)

            # print(l, r, "调用了", l, wait_for_small_than_pivot - 1)



            right = TreeNode((wait_for_small_than_pivot + 1, r))
            right.next_to(my_root, numpy.array([-dis[0], dis[1], dis[2]]))
            line = Line(my_root, right, color=YELLOW)
            self.add(right, line)
            quicksort(rect_list, wait_for_small_than_pivot + 1, r, depth + 1, my_root = right)
            # print(l, r, "调用了", wait_for_small_than_pivot + 1, r)


            # 能走到这一行, 说明函数处理完了, 闪动一下根表示一下
            self.play(FadeIn(my_root), run_time=self.inner_duration)

        rect_list.arrange(RIGHT, center=True, aligned_edge=DOWN)

        quicksort(rect_list, 0, len(rect_list) - 1, 0, my_root = root)
