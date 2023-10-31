from concurrent.futures import ThreadPoolExecutor
import subprocess
import time

# 指定檔案名和其它靜態參數
filenames = ["my_dataset\\DataA.data"]
# filenames = ["my_dataset\\DataA.data", 
#              "my_dataset\\DataB.data", 
#              "my_dataset\\DataC.data"]
# filenames = ["my_dataset\DataA.csv",
#              "my_dataset\DataB.csv",
#              "my_dataset\DataC.csv"]

script_name_1 = "Apriori_python\Apriori_python\\task1.py"
script_name_2 = "Apriori_python\Apriori_python\\task2.py"

# 初始化一個支持值（support value）的列表
support_values = [0.05]
time_dict = {}
# 定義執行命令的函數
def run_cmd(script_name, f, s):
    cmd = f"python {script_name} -f {f} -s {s}"
    start_time = time.time()
    subprocess.run(cmd, shell=True, cwd='C:\\Users\\User\\Desktop\\Data_minning_together\\Kang\\Data_minning_lab1', check=True)
    end_time = time.time()
    elapsed_time = end_time - start_time
    # 輸出執行時間
    time_dict[(script_name, f, s)] = elapsed_time
    

# 使用ProcessPoolExecutor進行多線程執行
with ProcessPoolExecutor() as executor:
    for f in filenames:
        names = f.split("\\\\")[-1].split(".")[0]
        print(f"檔案名: {names}")
        for s in support_values:
            # 獲取Task 1和Task 2的執行時間
            future1 = executor.submit(run_cmd, script_name_1, f, s)
            future2 = executor.submit(run_cmd, script_name_2, f, s)
         
            
# 計算並輸出執行時間比例
for i in time_dict.keys():
    script, f, s = i  # 拆解字典鍵
    if script == script_name_1:
        time1 = time_dict[(script_name_1, f, s)]
        time2 = time_dict.get((script_name_2, f, s), None)  # 使用 get 方法防止 KeyError
        if time1 and time2:
            ratio = (time2 / time1) * 100
            with open(f"result\\Time_Ratios.txt", "a") as f1:
                f1.write(f"Time ratio for {f}, support {s}: {ratio}%\n")