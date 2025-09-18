class Color:
    """ANSI 颜色代码"""
    # 前景色
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    # 亮色前景色
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'
    
    # 背景色
    BG_BLACK = '\033[40m'
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'
    
    # 亮色背景色
    BG_BRIGHT_BLACK = '\033[100m'
    BG_BRIGHT_RED = '\033[101m'
    BG_BRIGHT_GREEN = '\033[102m'
    BG_BRIGHT_YELLOW = '\033[103m'
    BG_BRIGHT_BLUE = '\033[104m'
    BG_BRIGHT_MAGENTA = '\033[105m'
    BG_BRIGHT_CYAN = '\033[106m'
    BG_BRIGHT_WHITE = '\033[107m'
    
    # 样式
    RESET = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    REVERSE = '\033[7m'

def color_print(text, color="", bg_color="", style="", end="\n"):
    """
    打印带颜色的文本
    
    参数:
        text: 要打印的文本
        color: 前景色 (使用Color类中的常量)
        bg_color: 背景色 (使用Color类中的常量)
        style: 文本样式 (使用Color类中的常量)
        end: 行结束符
    """
    print(f"{style}{bg_color}{color}{text}{Color.RESET}", end=end)

def print_success(text):
    """打印成功信息 (绿色对勾)"""
    color_print(f"✓ {text}", color=Color.BRIGHT_GREEN, style=Color.BOLD)

def print_error(text):
    """打印错误信息 (红色叉号)"""
    color_print(f"✗ {text}", color=Color.BRIGHT_RED, style=Color.BOLD)

def print_warning(text):
    """打印警告信息 (黄色感叹号)"""
    color_print(f"! {text}", color=Color.BRIGHT_YELLOW, style=Color.BOLD)

def print_info(text):
    """打印信息 (蓝色i)"""
    color_print(f"i {text}", color=Color.BRIGHT_CYAN, style=Color.BOLD)

def print_highlight(text):
    """高亮显示文本 (黄色粗体)"""
    color_print(text, color=Color.BRIGHT_YELLOW, style=Color.BOLD)

def print_debug(text):
    """打印调试信息 (灰色)"""
    color_print(f"[DEBUG] {text}", color=Color.BRIGHT_BLACK)

# 测试函数
if __name__ == "__main__":
    print_success("操作成功完成")
    print_error("发生了一个错误")
    print_warning("这是一个警告")
    print_info("这是一条信息")
    print_highlight("这是高亮文本")
    print_debug("调试信息")
