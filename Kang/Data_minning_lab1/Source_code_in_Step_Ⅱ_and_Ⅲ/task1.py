
import time
from itertools import chain, combinations
from collections import defaultdict
from optparse import OptionParser
import sys

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

if __name__ == "__main__":
    start_time = time.time()

    optparser = OptionParser()
    optparser.add_option(
        "-f", "--inputFile", dest="input", help="filename containing csv", default=None
    )
    optparser.add_option(
        "-s", "--minSupport_task1", dest="minS", help="minimum support value", default=0.1, type="float"
    )
    (options, args) = optparser.parse_args()
    filename = options.input
    filename = filename.split("\\")[-1].split('.')[0]
    inFile = None
    if options.input is None:
        # 從標準輸入讀取
        inFile = sys.stdin
    elif options.input is not None:
        # 從文件讀取
        inFile = dataFromFile(options.input)
    else:
        print("沒有指定數據集文件名，系統將退出\n")
        sys.exit("系統將退出")
    minSupport_task1 = options.minS
    items = runApriori(inFile, minSupport_task1)
    printResults(items)
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    print(f"Computation time for this task: {elapsed_time} seconds")
    with open("output_in_step2\\task1\\computation_time_task1.txt", "a") as f:
        f.write(f"{filename},minSupport_task1:{minSupport_task1} => Computation time for this task: {round(elapsed_time, 4)} seconds\n")
