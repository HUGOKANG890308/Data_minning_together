import time
from itertools import chain, combinations
from collections import defaultdict
from optparse import OptionParser
import sys
import os

# 統計數據變量
total_frequent_itemsets_task1 = 0
statistics_data_task1 = []
# 生成子集
def subsets(arr):
    return chain(*[combinations(arr, i + 1) for i, a in enumerate(arr)])

# 返回滿足最小支持度的項目集
def returnItemsWithminSupport_task1(itemSet, transactionList, minSupport_task1, freqSet):
    _itemSet = set()
    localSet = defaultdict(int)
    # 剪枝前的候選項目集數
    candidates_before_pruning = len(itemSet)
    
    for item in itemSet:
        for transaction in transactionList:
            if item.issubset(transaction):
                freqSet[item] += 1
                localSet[item] += 1
    # 剪枝後的候選項目集數            
    candidates_after_pruning = 0
    for item, count in localSet.items():
        support = float(count) / len(transactionList)
        if support >= minSupport_task1:
            _itemSet.add(item)
            candidates_after_pruning += 1
            
    statistics_data_task1.append((candidates_before_pruning, candidates_after_pruning))
    return _itemSet

# 聯接集合，生成更大的項目集
def joinSet(itemSet, length):
    return set(
        [i.union(j) for i in itemSet for j in itemSet if len(i.union(j)) == length]
    )
    
# 從數據中獲取項目集和交易列表
def getItemSetTransactionList(data_iterator):
    transactionList = list()
    itemSet = set()
    for record in data_iterator:
        transaction = frozenset(record)
        transactionList.append(transaction)
        for item in transaction:
            itemSet.add(frozenset([item]))
            
    return itemSet, transactionList

# 運行 Apriori 算法
def runApriori(data_iter, minSupport_task1):
    global total_frequent_itemsets_task1
    total_frequent_itemsets_task1 = 0
    itemSet, transactionList = getItemSetTransactionList(data_iter)
    freqSet = defaultdict(int)
    largeSet = dict()
    oneCSet = returnItemsWithminSupport_task1(itemSet, transactionList, minSupport_task1, freqSet)
    currentLSet = oneCSet
    k = 2
    while currentLSet != set([]):
        largeSet[k - 1] = currentLSet
        currentLSet = joinSet(currentLSet, k)
        currentCSet = returnItemsWithminSupport_task1(
            currentLSet, transactionList, minSupport_task1, freqSet
        )
        currentLSet = currentCSet
        total_frequent_itemsets_task1 += len(currentLSet)
        k = k + 1
        
    # 計算支持度
    def getSupport(item):
        return float(freqSet[item]) / len(transactionList)

    toRetItems = []
    for key, value in largeSet.items():
        toRetItems.extend([((item), getSupport(item)) for item in value])
    return sorted(toRetItems, key=lambda x: x[1], reverse=True)  # Sort by support, from large to small
# 打印結果
def printResults(items):
    global total_frequent_itemsets_task1
    with open(f"output_in_step2\\task1\\Result_file1\\step2_task1_{filename}_{minSupport_task1}.txt", "w") as f1, open(f"output_in_step2\\task1\\Result_file2\\step2_task2_{filename}_{minSupport_task1}.txt", "w") as f2:
        f1.write(f"{filename} : minimum support = {minSupport_task1}\n")
        # 已經排序
        for item, support in items:  
            # \t 代表一個制表符（Tab字符），用來對齊
            f1.write(f"{round(support*100,4)}\t{{{' ,'.join(map(str, item))}}}\n")
        
        f2.write(f"total_frequent_itemsets_task1:{total_frequent_itemsets_task1}\n")
        for index, (before, after) in enumerate(statistics_data_task1, 1):
            f2.write(f"{index}\t{before}\t{after}\n")

            
# 從文件中讀取數據
def dataFromFile(fname):
    with open(fname, "r") as file_iter:
        for line in file_iter:
            line = line.strip().rstrip(",")
            # 從第三個元素到列表末尾
            line =','.join(line.split(',')[3:]) 
            record = frozenset(line.split(","))
            yield record
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
if __name__ == "__main__":
    start_time = time.time()

    # 命令行選項解析器
    optparser = OptionParser()
    optparser.add_option("-f", "--inputFile", dest="input", help="包含 .data 或 .csv 的文件名", default=None)
    optparser.add_option("-s", "--minSupport_task1", dest="minS", help="最小支持度值", default=0.1, type="float")

    (options, args) = optparser.parse_args()

    # 檢查是否有指定輸入文件
    if options.input is None:
        print("沒有指定數據集文件名，系統將退出\n")
        sys.exit("系統將退出")
    filename = options.input
    filename = filename.split("\\")[-1].split('.')[0]
    # 檢查輸入文件的副檔名
    input_file_path = options.input
    file_extension = os.path.splitext(input_file_path)[1]

    # 如果是 .data 文件，則轉換為 .csv
    if file_extension.lower() == '.data':
        # 假設輸出目錄與輸入目錄相同
        output_dir = os.path.dirname(input_file_path)
        # 轉換文件並獲取新的文件路徑
        input_file_path = convertToCSV(input_file_path, output_dir)

    # 使用轉換後的文件路徑進行處理
    inFile = dataFromFile(input_file_path)

    # 獲取最小支持度值
    minSupport_task1 = options.minS
    # 執行 Apriori 算法
    items = runApriori(inFile, minSupport_task1)
    # 打印結果
    printResults(items)
    end_time = time.time()
    elapsed_time = end_time - start_time
    # 打印計算時間
    print(f"此任務的計算時間: {elapsed_time} 秒")
    with open("output_in_step2\\task1\\computation_time_task1.txt", "a") as f:
        f.write(f"{filename},minSupport_task1:{minSupport_task1} => Computation time for this task: {round(elapsed_time, 4)} seconds\n")


    # 省略了將計算時間寫入文件的代碼...

# if __name__ == "__main__":
#     start_time = time.time()

#     optparser = OptionParser()
#     optparser.add_option(
#         "-f", "--inputFile", dest="input", help="filename containing csv", default=None
#     )
#     optparser.add_option(
#         "-s", "--minSupport_task1", dest="minS", help="minimum support value", default=0.1, type="float"
#     )
#     (options, args) = optparser.parse_args()
#     filename = options.input
#     filename = filename.split("\\")[-1].split('.')[0]
#     inFile = None
#     if options.input is None:
#         # 從標準輸入讀取
#         inFile = sys.stdin
#     elif options.input is not None:
#         # 從文件讀取
#         inFile = dataFromFile(options.input)
#     else:
#         print("沒有指定數據集文件名，系統將退出\n")
#         sys.exit("系統將退出")
#     minSupport_task1 = options.minS
#     items = runApriori(inFile, minSupport_task1)
#     printResults(items)
#     end_time = time.time()
#     elapsed_time = end_time - start_time
    
#     print(f"Computation time for this task: {elapsed_time} seconds")
#     with open("output_in_step2\\task1\\computation_time_task1.txt", "a") as f:
#         f.write(f"{filename},minSupport_task1:{minSupport_task1} => Computation time for this task: {round(elapsed_time, 4)} seconds\n")
