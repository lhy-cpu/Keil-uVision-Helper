# Add File

**简介：** 这是一份用于快速给Keil项目添加 .c 和 .h 文件的Python脚本

**用法：**

1. 将该文件放置在与Keil uVision的项目文件同级目录内（目录里有*.uvprojx或*.uvproj文件）
2. 使用文本编辑器根据需要修改脚本内的变量

| 变量名 | 描述 | 默认值 |
| :--: | :--: | :--: |
|`source_file_path`| 源文件存放位置（\*.c） | `"./"` |
| `header_file_path` | 头文件存放位置（\*.h） | `"./Header"` |
| `source_group_name` | 源文件存放的组名 | `"Source"` |
| `header_group_name` | 头文件存放的组名 | `"Header"` |
| `auto_include_in_source` | 新建源文件时在头部加入的字符串 | `'#include "Header/AI8H.H"'` |
| `change_to_create_hex_file` | 修改项目文件在编译时创建HEX文件 | `True` |

3. 运行该脚本
4. 输入要创建的文件名（包括 ".c" 或 ".h" 后缀）
   <br>
   <font color="Grey">  *此处如果输入 ".c" 为后缀，则接下来会询问是否同时创建相应的头文件，".h"则直接开始创建*</font>
6. 创建成功，直接使用（如果使用的是 **VScode** 的 **Keil uVision Assistant** 会自动重新加载，写好代码直接点击编译即可）

---

## 使用前须知：

该代码未经充分验证，虽含有保护源代码不被覆写的功能，请在正式使用前先进行**测试**是否可用，并**备份**相关项目文件，以免出现意外，使用风险自负。

**USE AT YOUR OWN RISK**
