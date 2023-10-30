import subprocess
import os
# 指定檔案名和其它靜態參數
filename = ["IBMGenerator-master\\DataA.data" , "IBMGenerator-master\\DataB.data", "IBMGenerator-master\\DataC.data"]
script_name = "Apriori_python\\Apriori_python\\apriori_modified_with_dynamic_filename_and_timing_for_log.py"

# 初始化一個支持值（support value）的列表
support_values = [0.05 ,0.01, 0.005, 0.001 ]

# 迴圈執行命令
for f in filename:
    for s in support_values:
        cmd = f"python {script_name} -f {f} -s {s}"
        subprocess.run(cmd, shell=True, cwd='C:\\Users\\User\\OneDrive\\資料探勘_交大\\Data_minning_lab1',check=True)