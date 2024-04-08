# manim_set

使用manim制作的排序可视化视频, 可以根据数组的内容生成视频. 


```shell 
# 克隆官方manim仓库,根据教程从仓库安装manimgl
git clone https://github.com/3b1b/manim.git
cd manim
python3 -m venv your_venv_name 
pip install -e .
manimgl example_scenes.py OpeningManimExample


# 把官方仓库的manimlib复制到本项目   把官方仓库生成的虚拟环境复制到本目录
cp -r 官方仓库/your_venv_name   本仓库
cp -r 官方仓库/manimlib  本仓库

# 进入目录, 运行视频 
cd visual_sort
manimgl visual_quick_sort.py QuickSort 
```
