from concurrent.futures import ThreadPoolExecutor
import subprocess
import time
import os
path = os.getcwd()
# 指定檔案名和其它靜態參數
file_data = {
    "Datasets\\DataA.data": [0.002, 0.005, 0.01],
    "Datasets\\DataB.data": [0.015, 0.002, 0.005],
    "Datasets\\DataC.data": [0.01, 0.02, 0.03]
}


script_name_1 = "Source_code_in_Step_Ⅱ_and_Ⅲ\\task1.py"
script_name_2 = "Source_code_in_Step_Ⅱ_and_Ⅲ\\task2.py"
# 定義執行命令的函數
def run_cmd(script_name, f, s):
    cmd = f"python {script_name} -f {f} -s {s}"
    start_time = time.time()
    subprocess.run(cmd, shell=True, cwd=path, check=True)
    end_time = time.time()
    return end_time - start_time


# 使用ThreadPoolExecutor進行多線程執行
with ThreadPoolExecutor() as executor:
    for f, support_values in file_data.items():
        names = f.split("\\")[-1].split(".")[0]
        print(f"檔案名: {names}")
        for s in support_values:
            # 獲取Task 1和Task 2的執行時間
            future1 = executor.submit(run_cmd, script_name_1, f, s)
            future2 = executor.submit(run_cmd, script_name_2, f, s)
            # future1.result() 是 concurrent.futures.Future 對象的一個方法，它會阻塞程序執行，直到 future1 對象的結果變得可用。
            # 換句話說，這個方法會等待異步操作（在這個例子中是 executor.submit(run_cmd, script_name_1, f, s)）完成，並返回該操作的結果。
            time1 = future1.result()
            time2 = future2.result()
            # 計算並輸出執行時間比例
            if time1 and time2:
                ratio = (time2 / time1) * 100
                print(f"執行時間比例（{f}, 支持度 {s}）: {ratio}%")
                with open(f"result\\output_in_step2\\Result_file_for_time_ratio.txt", "a") as f1:
                    f1.write(f"{f}C omputation time for Task 1: {time1} seconds \n")
                    f1.write(f"執行時間比例（{f}, 支持度 {s}）: Ratio of computation time compared to that of Task 1: {ratio}% \n")

'''
D
python task1.py -f Datasets\DataA.data -s 0.005
python task2.py -f Datasets\DataA.data -s 0.005
python task1.py -f Datasets\DataA.data -s 0.01
python task2.py -f Datasets\DataA.data -s 0.01
python task1.py -f Datasets\DataB.data -s 0.015
python task2.py -f Datasets\DataB.data -s 0.015
python task1.py -f Datasets\DataB.data -s 0.002
python task2.py -f Datasets\DataB.data -s 0.002
python task1.py -f Datasets\DataB.data -s 0.005
python task2.py -f Datasets\DataB.data -s 0.005
python task1.py -f Datasets\DataC.data -s 0.01
python task2.py -f Datasets\DataC.data -s 0.01
python task1.py -f Datasets\DataC.data -s 0.02
python task2.py -f Datasets\DataC.data -s 0.02
python task1.py -f Datasets\DataC.data -s 0.03
python task2.py -f Datasets\DataC.data -s 0.03

python task1.py -f Datasets\DataA.csv -s 0.002
python task2.py -f Datasets\DataA.csv -s 0.002
python task1.py -f Datasets\DataA.csv -s 0.005
python task2.py -f Datasets\DataA.csv -s 0.005
python task1.py -f Datasets\DataA.csv -s 0.01
python task2.py -f Datasets\DataA.csv -s 0.01
python task1.py -f Datasets\DataB.csv -s 0.015
python task2.py -f Datasets\DataB.csv -s 0.015
python task1.py -f Datasets\DataB.csv -s 0.002
python task2.py -f Datasets\DataB.csv -s 0.002
python task1.py -f Datasets\DataB.csv -s 0.005
python task2.py -f Datasets\DataB.csv -s 0.005
python task1.py -f Datasets\DataC.csv -s 0.01
python task2.py -f Datasets\DataC.csv -s 0.01
python task1.py -f Datasets\DataC.csv -s 0.02
python task2.py -f Datasets\DataC.csv -s 0.02
python task1.py -f Datasets\DataC.csv -s 0.03
python task2.py -f Datasets\DataC.csv -s 0.03

'''