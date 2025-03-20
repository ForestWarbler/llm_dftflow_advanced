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
    idle_count = sum(1 for percent in import time

def read_cpu_times():
    """
    读取 /proc/stat 中各个 CPU 核心的时间信息，返回字典：
    { 'cpu0': [user, nice, system, idle, iowait, irq, softirq, steal, guest, guest_nice], ... }
    """
    cpu_times = {}
    with open("/proc/stat", "r") as f:
        for line in f:
            if line.startswith("cpu") and line[3].isdigit():
                parts = line.split()
                cpu_label = parts[0]
                # 将后续的所有时间信息转为 int
                times = list(map(int, parts[1:]))
                cpu_times[cpu_label] = times
    return cpu_times

def calculate_cpu_usage(prev, curr):
    """
    计算每个核心的使用率百分比
    usage = 100 * (delta_total - delta_idle) / delta_total
    其中 delta_idle = (idle + iowait) 差值
    """
    usage = {}
    for cpu in curr.keys():
        prev_times = prev[cpu]
        curr_times = curr[cpu]
        prev_idle = prev_times[3] + (prev_times[4] if len(prev_times) > 4 else 0)
        curr_idle = curr_times[3] + (curr_times[4] if len(curr_times) > 4 else 0)
        prev_total = sum(prev_times)
        curr_total = sum(curr_times)

        delta_total = curr_total - prev_total
        delta_idle = curr_idle - prev_idle

        if delta_total == 0:
            usage[cpu] = 0.0
        else:
            cpu_usage = (delta_total - delta_idle) / delta_total * 100
            usage[cpu] = cpu_usage
    return usage

def count_idle_cores(threshold=20, interval=1):
    """
    根据采样 interval 秒内计算出的使用率，统计空闲核心数量
    定义空闲为核心使用率低于 threshold%
    """
    prev_stats = read_cpu_times()
    time.sleep(interval)
    curr_stats = read_cpu_times()
    usage = calculate_cpu_usage(prev_stats, curr_stats)

    idle_count = sum(1 for cpu, percent in usage.items() if percent < threshold)
    return idle_count, usage

if __name__ == "__main__":
    threshold = 20  # 使用率低于20%认为空闲
    idle_cores, cpu_usage = count_idle_cores(threshold=threshold, interval=1)
    print("各 CPU 核心使用率:")
    for cpu, usage_percent in cpu_usage.items():
        print(f"  {cpu}: {usage_percent:.2f}%")
    print(f"空闲核心数（使用率低于 {threshold}%）：{idle_cores}")cpu_percentages if percent < threshold)

    return idle_count, cpu_percentages


if __name__ == "__main__":
    # 设定空闲阈值为5%
    threshold = 5
    idle_cores, cpu_usage = count_idle_cores(threshold=threshold, interval=1)

    print("各 CPU 核心使用率:", cpu_usage)
    print(f"空闲核心数（使用率低于 {threshold}%）: {idle_cores}")