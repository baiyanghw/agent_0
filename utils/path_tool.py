"""
为整个工程提供统一明确的绝对路径
"""
import os

def get_project_root()->str:
    """
    获取工程所在的根目录
    :return: 字符串目录
    """
    #当前文件绝对路径
    current_file=os.path.abspath(__file__)
    #获取工程根目录
    current_dir=os.path.dirname(current_file)
    project_root=os.path.dirname(current_dir)
    return project_root

def get_abs_path(relative_path:str)->str:
    """
    传递相对路径，获取绝对路径
    :param relative_path:
    :return:
    """
    project_root=get_project_root()
    return os.path.join(project_root,relative_path)

if __name__=="__main__":
    print(__file__)
    print(get_abs_path("config/config.txt"))



