import sys
sys.path.append(".")
sys.path.append("..")


from visual_sort.my_thing import *


class SelectionSort(Scene):
    # 播放速度 秒
    inner_duration = 0.0000000001

    # with open("d2.txt", "r") as f:
    #     arr = [int(float(line) * 1000) for line in f]

    with open("d2.txt", "r") as f:
        arr = [int(line) for line in f]


    print(arr)

    def construct(self) -> None:


        rect_list = VisualArr(self.arr)

        self.add(rect_list)

        rect_list.arrange(RIGHT, center=True, aligned_edge=DOWN)

        # 选择排序 每次寻找一个最小的
        for i in range(0, len(rect_list)):
            min_index = i
            min_rect = rect_list[i]
            # arr[min_index] 红色   与之比较的:蓝色

            # 把i创建一个标签
            i_tag = Text("i").next_to(rect_list[i], UP)
            self.add(i_tag)

            if i != len(rect_list) - 1:
                line_unordered = Line(rect_list[i].get_corner(DL), rect_list[-1].get_corner(DR))
                line_unordered.set_color(BLUE_A)
                self.add(line_unordered)

            self.play(rect_list[i].animate.set_color(RED), run_time=self.inner_duration)
            for j in range(i + 1, len(rect_list)):

                # 比较 arr[min_index] arr[j]
                to_comp_rect = rect_list[j]
                j_tag = Text("j").next_to(to_comp_rect, UP)
                self.add(j_tag)

                self.play(to_comp_rect.animate.set_color(BLUE), run_time=self.inner_duration)
                if to_comp_rect.num < min_rect.num:
                    # 变更min前把原来的min恢复颜色
                    self.play(min_rect.animate.set_color(WHITE), run_time=self.inner_duration)
                    min_index = j
                    min_rect = to_comp_rect
                    self.play(min_rect.animate.set_color(RED), run_time=self.inner_duration)
                if min_index != j:
                    self.play(to_comp_rect.animate.set_color(WHITE), run_time=self.inner_duration)
                self.remove(j_tag)
            # 此时 找到了当前最小高度
            rect_list.swap_elements(min_index, i)

            # 计算移动距离
            cooa = rect_list[min_index].get_corner(DL)
            coob = rect_list[i].get_corner(DL)
            # cooa - coob >= 0
            self.play(

                rect_list[min_index].animate.shift(LEFT * (cooa - coob)),
                rect_list[i].animate.shift(RIGHT * (cooa - coob)),
                run_time=self.inner_duration
            )

            # 位置i已经不用管了, 把它恢复颜色
            self.play(rect_list[i].animate.set_color(WHITE), run_time=self.inner_duration)
            self.remove(i_tag)

            # 此时i以及i以前的位置都是有序的:
            # 划分当前已经处理的的范围[0..i]
            line_ordered = Line(rect_list[0].get_corner(DL), rect_list[i].get_corner(DR))
            line_ordered.set_color(GREY)
            self.add(line_ordered)

        rect_list.arrange(RIGHT, center=True, aligned_edge=DOWN)


