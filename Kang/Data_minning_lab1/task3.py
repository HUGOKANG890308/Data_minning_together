import time
from optparse import OptionParser
import sys
from mlxtend.frequent_patterns import fpgrowth
from mlxtend.preprocessing import TransactionEncoder
import pandas as pd

# 從數據中獲取交易列表
def getTransactionList(data_iterator):
    transactionList = []
    for record in data_iterator:
        transaction = list(record)
        transactionList.append(transaction)
    return transactionList

# 運行 FP-Growth 算法
def runFPGrowth(transactionList, minSupport_task3):
    te = TransactionEncoder()
    te_ary = te.fit(transactionList).transform(transactionList)
    df = pd.DataFrame(te_ary, columns=te.columns_)
    # 使用 FP-Growth 算法找出頻繁項目集
    frequent_itemsets_task3 = fpgrowth(df, min_support=minSupport_task3, use_colnames=True)
    return frequent_itemsets_task3

def convertToCSV(input_file_path, output_csv_path):
    """
    轉換原始數據文件到 CSV 格式。
    :param input_file_path: 原始數據文件的路徑。
    :param output_csv_path: 要生成的 CSV 文件的路徑。
    
    使用範例：
    convertToCSV('path_to_your_input_file.txt', 'output_data.csv')
    """
    # with open(input_file_path, 'r') as f:
    #     transactions = [line.strip().split() for line in f]
    #     df = pd.DataFrame(transactions)
    #     basename = os.path.basename(input_file_path)  # 獲取路徑的基本名稱（最後一部分）
    #     name, ext = os.path.splitext(basename)  # 分離基本名稱和擴展名
    #     output_csv_path = os.path.join(output_csv_path, f"{name}.csv")
    #     df.to_csv(f"result\\output_in_step3\\{name}.csv", index=False, header=False)
    with open(input_file_path, 'r') as infile, open(output_csv_path, 'w') as outfile:
        for line in infile:
            # 假設每個項目由空格分隔，可以根據需要修改分隔符
            line_items = line.strip().split()
            # 將項目連接成以逗號分隔的字符串
            csv_line = ','.join(line_items)
            # 寫入到 CSV 文件
            outfile.write(csv_line + '\n')
            
input_file_path = 'my_dataset\\DataA.data'

# 從文件中讀取數據
def dataFromFile(fname):
    file_iter = open(fname, 'r')
    for line in file_iter:
        line = line.strip().rstrip(",")
        record = line.split(',')[3:]  # 從第三個元素到列表末尾
        yield record

# 打印結果
def printResults(frequent_itemsets_task3, filename, minSupport_task3):
    # 結果輸出路徑可能需要根據您的文件結構進行調整
    output_path = f"result\\output_in_step3\\task1\\result_task3_{filename}_{minSupport_task3}.txt"
    with open(output_path, "w") as f:
        for itemset in frequent_itemsets_task3.itertuples():
            # 頻繁項目集和支持度
            f.write(f"{round(itemset.support * 100, 4)}\t{{{' ,'.join(itemset.itemsets)}}}\n")
            

# if __name__ == "__main__":
#     start_time = time.time()

#     optparser = OptionParser()
#     optparser.add_option(
#         "-f", "--inputFile", dest="input", help="filename containing raw data", default=None
#     )
#     optparser.add_option(
#         "-c", "--csvFile", dest="csv", help="filename to save CSV data", default="output_data.csv"
#     )
#     optparser.add_option(
#         "-s", "--minSupport", dest="minS", help="minimum support value", default=0.1, type="float"
#     )
#     (options, args) = optparser.parse_args()

#     if options.input is None:
#         print("No dataset filename specified, system will exit.")
#         sys.exit("System will exit")

#     raw_data_file = options.input
#     csv_data_file = options.csv
#     minSupport_task3 = options.minS
#     output_dir = "result\\output_in_step3"
#     csv_data_file= convertToCSV(raw_data_file, output_dir)

#     transactions = getTransactionList(dataFromFile(csv_data_file))
#     frequent_itemsets_task3 = runFPGrowth(transactions, minSupport_task3)
#     printResults(frequent_itemsets_task3, csv_data_file, minSupport_task3)
#     end_time = time.time()
#     elapsed_time_task3 = end_time - start_time
#     print(f"Computation time for this task: {elapsed_time_task3} seconds")
#     computation_time_path = "script_nameresult\\output_in_step3\\task1\\computation_time_task3.txt"
#     with open(computation_time_path, "a") as f:
#         f.write(f"{csv_data_file},minSupport:{minSupport_task3} => Computation time for this task: {round(elapsed_time_task3, 4)} seconds\n")

if __name__ == "__main__":
    start_time = time.time()

    optparser = OptionParser()
    optparser.add_option(
        "-f", "--inputFile", dest="input", help="filename containing raw data", default=None
    )
    optparser.add_option(
        "-c", "--csvFile", dest="csv", help="filename to save CSV data", default=None
    )
    optparser.add_option(
        "-s", "--minSupport", dest="minS", help="minimum support value", default=0.1, type="float"
    )
    (options, args) = optparser.parse_args()

    if options.input is None:
        print("No dataset filename specified, system will exit.")
        sys.exit("System will exit")

    raw_data_file = options.input
    output_dir = "result\\output_in_step3"  # 指定輸出目錄
    csv_data_file = options.csv if options.csv else convertToCSV(raw_data_file, output_dir)

    transactions = getTransactionList(dataFromFile(csv_data_file))
    frequent_itemsets_task3 = runFPGrowth(transactions, options.minS)
    printResults(frequent_itemsets_task3, os.path.basename(csv_data_file), options.minS)

    end_time = time.time()
    elapsed_time_task3 = end_time - start_time
    print(f"Computation time for this task: {elapsed_time_task3} seconds")
    computation_time_path = "result\\output_in_step3\\task1\\computation_time_task3.txt"
    with open(computation_time_path, "a") as f:
        f.write(f"{os.path.basename(csv_data_file)},minSupport:{options.minS} => Computation time for this task: {round(elapsed_time_task3, 4)} seconds\n")
