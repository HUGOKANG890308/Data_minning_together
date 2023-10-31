import time
from itertools import chain, combinations
from collections import defaultdict
from optparse import OptionParser
import sys

# 全局變量
total_frequent_itemsets = 0
statistics_data = []

# 生成子集
def subsets(arr):
    return chain(*[combinations(arr, i + 1) for i, a in enumerate(arr)])

# 返回滿足最小支持度的項目集
def returnItemsWithMinSupport(itemSet, transactionList, minSupport, freqSet):
    _itemSet = set()
    localSet = defaultdict(int)
    for item in itemSet:
        for transaction in transactionList:
            if item.issubset(transaction):
                freqSet[item] += 1
                localSet[item] += 1
    for item, count in localSet.items():
        support = float(count) / len(transactionList)
        if support >= minSupport:
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
def runApriori(data_iter, minSupport):
    global total_frequent_itemsets
    total_frequent_itemsets = 0
    itemSet, transactionList = getItemSetTransactionList(data_iter)
    freqSet = defaultdict(int)
    largeSet = dict()
    oneCSet = returnItemsWithMinSupport(itemSet, transactionList, minSupport, freqSet)
    currentLSet = oneCSet
    k = 2
    while currentLSet != set([]):
        largeSet[k - 1] = currentLSet
        currentLSet = joinSet(currentLSet, k)
        currentCSet = returnItemsWithMinSupport(currentLSet, transactionList, minSupport, freqSet)
        currentLSet = currentCSet
        total_frequent_itemsets += len(currentLSet)
        k = k + 1
    toRetItems = []
    for key, value in largeSet.items():
        toRetItems.extend([(tuple(item), float(freqSet[item]) / len(transactionList)) for item in value])
    return sorted(toRetItems, key=lambda x: x[1])

# 打印 Task 2 結果
def printResultsForTask2(items):
    frequent_closed_itemsets = getFrequentClosedItemsets(items)
    with open(f"result\\{filename}_Result_file_for_Task2.txt", "w") as f:
        f.write(f"{len(frequent_closed_itemsets)}\n")
        for itemset, support in sorted(frequent_closed_itemsets, key=lambda x: x[1], reverse=True):
            f.write(f"{round(support * 100, 1)}%\t{{{' ,'.join(map(str, itemset))}}}\n")

# 從文件中讀取數據
def dataFromFile(fname):
    with open(fname, "r") as file_iter:
        for line in file_iter:
            line = line.strip().rstrip(",")
            record = frozenset(line.split(","))
            yield record

if __name__ == "__main__":
    start_time = time.time()

    optparser = OptionParser()
    optparser.add_option("-f", "--inputFile", dest="input", help="filename containing csv", default=None)
    optparser.add_option("-s", "--minSupport", dest="minS", help="minimum support value", default=0.1, type="float")
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

    minSupport = options.minS
    items = runApriori(inFile, minSupport)
    printResultsForTask2(items)

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Computation time for this task: {elapsed_time} seconds")
    with open("result\\computation_time.txt", "a") as f:
        f.write(f"{filename},minSupport:{minSupport} => Computation time for this task: {round(elapsed_time, 4)} seconds\n")
