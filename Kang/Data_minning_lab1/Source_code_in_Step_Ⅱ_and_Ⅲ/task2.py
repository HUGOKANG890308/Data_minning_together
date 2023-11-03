import time
from itertools import chain, combinations
from collections import defaultdict
from optparse import OptionParser
import sys
import os


# 全局變量
total_frequent_itemsets_task2 = 0
statistics_data_task2 = []

# 生成子集
def subsets(arr):
    return chain(*[combinations(arr, i + 1) for i, a in enumerate(arr)])

# 返回滿足最小支持度的項目集
def returnItemsWithminSupport_task2(itemSet, transactionList, minSupport_task2, freqSet):
    _itemSet = set()
    localSet = defaultdict(int)
    for item in itemSet:
        for transaction in transactionList:
            if item.issubset(transaction):
                freqSet[item] += 1
                localSet[item] += 1
    for item, count in localSet.items():
        support = float(count) / len(transactionList)
        if support >= minSupport_task2:
            _itemSet.add(item)
    return _itemSet

# 聯接集合
def joinSet(itemSet, length):
    return set([i.union(j) for i in itemSet for j in itemSet if len(i.union(j)) == length])

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

# 獲取頻繁閉項目集
def getFrequentClosedItemsets(frequent_itemsets):
    # 初始化一個空列表來儲存頻繁閉項目集
    frequent_closed_itemsets = []
    
    # 遍歷所有頻繁項目集
    for i, (itemset1, support1) in enumerate(frequent_itemsets):
        # 初始化一個標記來檢查當前的項目集是否是閉的
        is_closed = True
        
        # 再次遍歷所有頻繁項目集以進行比較
        for j, (itemset2, support2) in enumerate(frequent_itemsets):
            # 檢查當前的項目集（itemset1）是否是另一個項目集（itemset2）的子集，
            # 並且它們的支持度是否相等
            if i != j and itemset1.issubset(itemset2) and support1 == support2:
                # 如果是，則將標記設置為False並中斷循環
                is_closed = False
                break
        # 如果標記仍然是True，則將當前的項目集添加到頻繁閉項目集列表中
        if is_closed:
            frequent_closed_itemsets.append((itemset1, support1))
    # 返回頻繁閉項目集列表
    return frequent_closed_itemsets


# 運行 Apriori 算法
def runApriori(data_iter, minSupport_task2):
    global total_frequent_itemsets_task2
    total_frequent_itemsets_task2 = 0
    itemSet, transactionList = getItemSetTransactionList(data_iter)
    freqSet = defaultdict(int)
    largeSet = dict()
    oneCSet = returnItemsWithminSupport_task2(itemSet, transactionList, minSupport_task2, freqSet)
    currentLSet = oneCSet
    k = 2
    while currentLSet != set([]):
        largeSet[k - 1] = currentLSet
        currentLSet = joinSet(currentLSet, k)
        currentCSet = returnItemsWithminSupport_task2(currentLSet, transactionList, minSupport_task2, freqSet)
        currentLSet = currentCSet
        total_frequent_itemsets_task2 += len(currentLSet)
        k = k + 1
    toRetItems = []
    for key, value in largeSet.items():
        toRetItems.extend([(item, float(freqSet[item]) / len(transactionList)) for item in value])
    return sorted(toRetItems, key=lambda x: x[1])

# 打印 Task 2 結果
def printResultsForTask2(items):
    frequent_closed_itemsets = getFrequentClosedItemsets(items)
    with open(f'output_in_step2\\task2\\Result_file1\\task2_{filename}_{minSupport_task2}.txt', "w") as f:
        f.write(f"{filename} : minimum support = {minSupport_task2}\n")
        f.write(f"{len(frequent_closed_itemsets)}\n")
        for itemset, support in sorted(frequent_closed_itemsets, key=lambda x: x[1], reverse=True):
            f.write(f"{round(support * 100, 1)}%\t{{{' ,'.join(map(str, itemset))}}}\n")

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

    optparser = OptionParser()
    optparser.add_option(
        "-f", "--inputFile", dest="input", help="filename containing csv", default=None
    )
    optparser.add_option(
        "-s", "--minSupport_task2", dest="minS", help="minimum support value", default=0.1, type="float"
    )
    (options, args) = optparser.parse_args()
    filename = options.input
    filename = filename.split("\\")[-1].split('.')[0]

    inFile = None
    if options.input is None:
        inFile = sys.stdin
    elif options.input is not None:
        inFile = dataFromFile(options.input)
    else:
        print("沒有指定數據集文件名，系統將退出")
        sys.exit("系統將退出")

    minSupport_task2 = options.minS
    items = runApriori(inFile, minSupport_task2)
    printResultsForTask2(items)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Computation time for this task: {elapsed_time} seconds")
    with open("output_in_step2\\task2\\computation_time_task2.txt", "a") as f:
        f.write(f"{filename},minSupport_task2:{minSupport_task2} => Computation time for this task: {round(elapsed_time, 4)} seconds\n")
if __name__ == "__main__":
    start_time = time.time()

    optparser = OptionParser()
    optparser.add_option(
        "-f", "--inputFile", dest="input", help="filename containing csv", default=None
    )
    optparser.add_option(
        "-s", "--minSupport_task2", dest="minS", help="minimum support value", default=0.1, type="float"
    )
    (options, args) = optparser.parse_args()
    filename = options.input
    filename = filename.split("\\")[-1].split('.')[0]

    inFile = None
    if options.input is None:
        inFile = sys.stdin
    elif options.input is not None:
        inFile = dataFromFile(options.input)
    else:
        print("沒有指定數據集文件名，系統將退出")
        sys.exit("系統將退出")
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
    
    minSupport_task2 = options.minS
    items = runApriori(inFile, minSupport_task2)
    printResultsForTask2(items)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Computation time for this task: {elapsed_time} seconds")
    with open("output_in_step2\\task2\\computation_time_task2.txt", "a") as f:
        f.write(f"{filename},minSupport_task2:{minSupport_task2} => Computation time for this task: {round(elapsed_time, 4)} seconds\n")
