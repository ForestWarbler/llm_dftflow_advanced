import os
import time

def find_log_files(root_dir):
    """
    根据结构根目录，构造一个日志文件字典：
      - key: 日志标识（如 'slurm', 'Relax', ...）
      - value: 对应的日志文件的绝对路径
    """
    logs = {}
    # 假设根目录下的 slurm 日志文件名为 slurm.log
    logs["slurm"] = os.path.join(root_dir, "slurm.log")
    # 子目录列表（根据实际情况可以扩展或修改）
    subdirs = ["Test_spin", "Relax", "Coarse_relax", "Scf", "Band", "Dos"]
    for sub in subdirs:
        logs[sub] = os.path.join(root_dir, sub, "yh.log")
    return logs

def monitor_logs(log_files, check_interval=10, stable_time=60):
    """
    监测日志文件是否停止更新：
      - check_interval: 每隔多少秒检查一次（默认10秒）
      - stable_time: 连续多久（秒）文件大小和修改时间都不变，则认为“稳定”
    """
    # 记录每个文件上次状态对应的时间戳
    stable_since = {path: None for path in log_files.values()}
    # 记录上一次检查时文件的大小和修改时间
    last_info = {}

    while True:
        all_stable = True  # 假设所有日志都稳定
        for key, path in log_files.items():
            # 对于 yh.log，如果文件不存在，则认为该阶段没有产生日志，直接视为完成
            if not os.path.exists(path):
                print(f"{key} 日志 ({path}) 不存在，视为完成。")
                continue

            try:
                current_stat = os.stat(path)
            except Exception as e:
                print(f"获取 {path} 状态失败：{e}")
                all_stable = False
                continue

            size = current_stat.st_size
            mtime = current_stat.st_mtime

            # 判断是否有之前的记录
            if path in last_info:
                prev_size, prev_mtime = last_info[path]
                if size == prev_size and mtime == prev_mtime:
                    # 如果没有记录稳定开始时间，则记录当前时间
                    if stable_since[path] is None:
                        stable_since[path] = time.time()
                    else:
                        # 如果距离开始稳定的时间还不足 stable_time，则仍认为不稳定
                        if time.time() - stable_since[path] < stable_time:
                            all_stable = False
                        else:
                            print(f"{key} 日志已稳定 {stable_time} 秒。")
                else:
                    # 文件发生变化，重置计时器
                    stable_since[path] = time.time()
                    all_stable = False
                    print(f"{key} 日志正在更新...")
            else:
                # 首次记录文件状态，开始计时
                stable_since[path] = time.time()
                all_stable = False
                print(f"{key} 日志开始监测...")

            # 更新记录信息
            last_info[path] = (size, mtime)

        if all_stable:
            print("所有日志均已停止更新，监测完成。")
            break

        time.sleep(check_interval)

if __name__ == '__main__':
    # 替换为你实际结构的根目录
    root_directory = "/HOME/nscc-gz_material_1/matgen_dft/err_struct/raise_incar_error/struct/icsd_107448-Cs6Pb8Au2"
    logs = find_log_files(root_directory)
    print("开始监测以下日志文件：")
    for key, path in logs.items():
        print(f"{key}: {path}")

    monitor_logs(logs)