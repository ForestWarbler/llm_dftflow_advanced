import psutil
import time


def count_idle_cores(threshold=20, interval=1):
    """
    采样 interval 秒内的 CPU 使用率，返回空闲核心的数量
    (空闲定义为该核心使用率低于 threshold%)
    """
    # 采样每个核心的使用率，interval 表示采样时长（单位秒）
    cpu_percentages = psutil.cpu_percent(interval=interval, percpu=True)
    # 统计使用率低于阈值的核心数量
    idle_count = sum(1 for percent in cpu_percentages if percent < threshold)

    return idle_count, cpu_percentages


if __name__ == "__main__":
    # 设定空闲阈值为5%
    threshold = 5
    idle_cores, cpu_usage = count_idle_cores(threshold=threshold, interval=1)

    print("各 CPU 核心使用率:", cpu_usage)
    print(f"空闲核心数（使用率低于 {threshold}%）: {idle_cores}")