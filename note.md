

# GPT

```python
class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None
        self.parent = None

class MinHeap:
    def __init__(self):
        self.root = None

    def insert(self, value):
        node = TreeNode(value)
        if not self.root:
            self.root = node
        else:
            queue = [self.root]
            while queue:
                current = queue.pop(0)
                if not current.left:
                    current.left = node
                    node.parent = current
                    self._sift_up(node)
                    break
                else:
                    queue.append(current.left)
                if not current.right:
                    current.right = node
                    node.parent = current
                    self._sift_up(node)
                    break
                else:
                    queue.append(current.right)

    def _sift_up(self, node):
        while node.parent and node.parent.value > node.value:
            self._swap_nodes(node.parent, node)

    def _swap_nodes(self, parent, child):
        if parent.parent:
            if parent.parent.left == parent:
                parent.parent.left = child
            else:
                parent.parent.right = child
        else:
            self.root = child

        if parent.left == child:
            parent.left, child.right = child.right, parent
            parent.right, child.left = child.left, parent
        else:
            parent.right, child.left = child.left, parent
            parent.left, child.right = child.right, parent

        parent.parent, child.parent = child, parent.parent
        
        if child.left:
            child.left.parent = child
        if child.right:
            child.right.parent = child
        if parent.left:
            parent.left.parent = parent
        if parent.right:
            parent.right.parent = parent

    def pop(self):
        if not self.root:
            return None
        min_value = self.root.value
        node = self.root
        queue = [node]
        while queue:
            current = queue.pop(0)
            node = current
            if current.left: queue.append(current.left)
            if current.right: queue.append(current.right)
        
        if node != self.root:
            self._swap_nodes(node, self.root)
            if node.parent.left == node:
                node.parent.left = None
            else:
                node.parent.right = None
        else:
            self.root = None
        
        self._sift_down(self.root)
        return min_value

    def _sift_down(self, node):
        while node and (node.left or node.right):
            smaller_child = None
            if node.left and node.right:
                smaller_child = node.left if node.left.value < node.right.value else node.right
            elif node.left:
                smaller_child = node.left
            elif node.right:
                smaller_child = node.right
            
            if smaller_child and node.value > smaller_child.value:
                self._swap_nodes(node, smaller_child)
            else:
                break

# 示例
heap = MinHeap()
heap.insert(5)
heap.insert(3)
heap.insert(8)
heap.insert(2)
heap.insert(1)
heap.insert(7)

print(heap.pop())  # 输出: 1
print(heap.pop())  # 输出: 2
```


# 同时移动
在manim库里，要同时移动两个对象，一个向右（RIGHT）另一个向下（2*DOWN），你可以使用AnimationGroup或者VGroup来组织这两个动作。以下是一个示例代码，展示如何使用AnimationGroup同时移动两个形状：
python
from manim import *

class SimultaneousMovement(Scene):
    def construct(self):
        # 创建两个形状
        square = Square(color=BLUE, fill_opacity=1)
        circle = Circle(color=RED, fill_opacity=1)
        # 将圆形向左移动以便初始位置不同
        circle.shift(LEFT)

        # 使用AnimationGroup来同时移动这两个形状
        self.play(AnimationGroup(
            square.animate.shift(RIGHT),
            circle.animate.shift(2 * DOWN),
            lag_ratio=0.5  # 这里的lag_ratio用于控制动画之间的延迟，可以根据需要调整
        ))

        self.wait()
在这段代码中，AnimationGroup被用来将两个移动动作组合在一起。square.animate.shift(RIGHT)使方形向右移动，而circle.animate.shift(2*DOWN)则使圆形向下移动。通过AnimationGroup，这两个动作会被视为一个整体同时执行，从而实现你的需求。
确保你已经安装了最新版的manim库。如果你还没有安装，可以通过pip命令来安装：
plaintext
pip install manim
运行以上代码时，你将看到一个方形向右移动，同时一个圆形向下移动。这段示例代码能够为你提供一个基础，了解如何在manim中同时控制多个动画。