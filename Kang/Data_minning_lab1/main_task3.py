from concurrent.futures import ThreadPoolExecutor
import subprocess
import os
import time
# 獲取當前工作目錄
path = os.getcwd()
# 指定檔案名和其它靜態參數
file_data = {
    "Datasets\\DataA.data": [0.002, 0.005, 0.01],
    "Datasets\\DataB.data": [0.015, 0.002, 0.005],
    "Datasets\\DataC.data": [0.01, 0.02, 0.03]
}
script_name = "task3.py"

# 定義執行命令的函數
def run_cmd(script_name, f, s):
    # 分離原始文件的路徑和文件名
    file_path, file_name = os.path.split(f)
    # 獲取無擴展名的文件名
    base_name = os.path.splitext(file_name)[0]
    # 構造 CSV 文件的完整路徑
    csv_file = os.path.join('output_in_step3', f"{base_name}.csv")
    cmd = f"python {script_name} -f {f} -c {csv_file} -s {s}"
    print(cmd)
    start_time = time.time()
    subprocess.run(cmd, shell=True, cwd=path, check=True)
    end_time = time.time()
    return end_time - start_time


# 使用ThreadPoolExecutor進行多線程執行
with ThreadPoolExecutor() as executor:
    futures = []
    for f, support_values in file_data.items():
        names = f.split("\\")[-1].split(".")[0]
        print(f"檔案名: {names}")
        for s in support_values:
            # 提交任務並獲取執行時間
            future = executor.submit(run_cmd, script_name, f, s)
            futures.append(future)

    # 等待所有的異步任務完成，並獲取執行這些任務所花費的時間
    for future in futures:
        try:
            duration = future.result()
            print(f"Task completed in {duration} seconds.")
        except Exception as e:
            print(f"Task failed: {e}")

