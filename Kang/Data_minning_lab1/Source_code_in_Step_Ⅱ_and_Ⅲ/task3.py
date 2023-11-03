import time
from optparse import OptionParser
import sys
from mlxtend.frequent_patterns import fpgrowth
from mlxtend.preprocessing import TransactionEncoder
import pandas as pd
import os
# 從數據中獲取交易列表
def getTransactionList(data_iterator):
    transactionList = []
    for record in data_iterator:
        transaction = list(record)
        transactionList.append(transaction)
    return transactionList



def runFPGrowth(transactionList, minSupport_task3):
    """
    使用 FP-Growth 算法找出頻繁項目集。
    
    :param transactionList: list of lists, 交易列表，每個交易包含一組項目。
    :param minSupport_task3: float, 尋找頻繁項目集時使用的最小支持度閾值。
    :return: DataFrame, 頻繁項目集及其支持度的數據框。
    
    使用範例:
    >>> transactions = [['牛奶', '麵包'], ['牛奶', '尿布'], ['麵包', '尿布', '啤酒'], ['牛奶', '麵包', '尿布', '啤酒']]
    >>> min_support = 0.5
    >>> frequent_itemsets = runFPGrowth(transactions, min_support)
    >>> print(frequent_itemsets)
    """

    # 初始化 TransactionEncoder 來轉換交易數據
    te = TransactionEncoder()
    # 將交易列表轉換為一個 bool 矩陣
    te_ary = te.fit(transactionList).transform(transactionList)
    # 將 bool 矩陣轉換為 DataFrame
    df = pd.DataFrame(te_ary, columns=te.columns_)
    # 使用 FP-Growth 算法找出頻繁項目集，並指定最小支持度
    frequent_itemsets_task3 = fpgrowth(df, min_support=minSupport_task3, use_colnames=True)
    # 返回找到的頻繁項目集
    return frequent_itemsets_task3



def convertToCSV(input_file_path, output_dir):
    """
    將原始數據文件轉換為 CSV 格式。

    :param input_file_path: str, 原始數據文件的完整路徑。假設數據項目是以空格分隔的。
    :param output_dir: str, CSV 文件應該被保存的目錄的路徑。如果此目錄不存在，函數將創建它。
    :return: str, 新創建的 CSV 文件的路徑。

    使用範例:
    >>> input_data = 'path/to/your/datafile.data'
    >>> output_directory = 'path/to/output/directory'
    >>> csv_file_path = convertToCSV(input_data, output_directory)
    >>> print(csv_file_path)
    'path/to/output/directory/datafile.csv'
    """

    # 確保輸出目錄存在，如果不存在，則創建它
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Created directory {output_dir}")

    # 從原始文件名中獲取基本文件名，並將其擴展名從 .data 替換為 .csv
    output_csv_path = os.path.join(output_dir, os.path.basename(input_file_path).replace('.data', '.csv'))

    try:
        # 讀取原始文件並將數據寫入到 CSV 文件中
        with open(input_file_path, 'r') as infile, open(output_csv_path, 'w', newline='') as outfile:
            for line in infile:
                # 假設數據項目是以空格分隔的
                line_items = line.strip().split()
                # 用逗號連接數據項目，創建 CSV 格式的字符串
                csv_line = ','.join(line_items)
                # 將 CSV 字符串寫入文件
                outfile.write(csv_line + '\n')
        print(f"CSV file created at {output_csv_path}")
        return output_csv_path
    except Exception as e:
        # 如果在轉換過程中出現錯誤，打印錯誤訊息並退出程序
        print(f"Error converting to CSV: {e}")
        sys.exit(1)

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
    output_path = f"output_in_step3\\task1\\step_task3_{filename}_{minSupport_task3}.txt"
    with open(output_path, "w") as f:
        for itemset in frequent_itemsets_task3.itertuples():
            # 頻繁項目集和支持度
            f.write(f"{round(itemset.support * 100, 4)}\t{{{' ,'.join(itemset.itemsets)}}}\n")
            


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
    output_dir = "output_in_step3"  # 指定輸出目錄
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)  # 如果目錄不存在，則創建它

    # 如果未指定 csv 文件名，則使用 convertToCSV 函數生成
    csv_data_file = convertToCSV(raw_data_file, output_dir)

    transactions = getTransactionList(dataFromFile(csv_data_file))
    frequent_itemsets_task3 = runFPGrowth(transactions, options.minS)
    printResults(frequent_itemsets_task3, os.path.basename(csv_data_file), options.minS)

    end_time = time.time()
    elapsed_time_task3 = end_time - start_time
    print(f"Computation time for this task: {elapsed_time_task3} seconds")
    computation_time_path = os.path.join(output_dir, "task1\\computation_time_task3.txt")
    with open(computation_time_path, "a") as f:
        f.write(f"{os.path.basename(csv_data_file)},minSupport:{options.minS} => Computation time for this task: {round(elapsed_time_task3, 4)} seconds\n")