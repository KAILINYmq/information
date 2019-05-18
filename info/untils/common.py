# 共用的自 定义工具类
# 过滤器
def do_index_class(index):
    """返回指定索引对应的类名"""
    if index == 1:
        return "first"
    elif index == 2:
        return "second"
    elif index == 3:
        return "third"

    return ""