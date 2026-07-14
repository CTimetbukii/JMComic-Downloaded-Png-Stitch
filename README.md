# JMComic-Download-Png-Stitch

该脚本特用于将从[JMComic-qt](https://github.com/tonquer/JMComic-qt)上下载的本拼接为一张长图。

# 使用方法

下载仓库中的 [stitch.py](stitch.py) 脚本，将其放在JMComic-qt的漫画下载目录中。例如

<img width="1460" height="953" alt="image" src="https://github.com/user-attachments/assets/b576b4f6-4f72-4ea0-9539-1aaeeed9c704" />

然后运行它

`python stitch.py`

由于在JMComic-qt上下载的本都遵循一定的文件夹格式，其内容总是放在 本/original/第1话 中。因此，该脚本从这个目录中读取图片，并按照JMComic-qt为图片的编号，纵向生成一张长图。

以25张为一个单位生成一张长图。默认与original目录放在一起。

