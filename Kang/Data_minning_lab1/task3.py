from mlxtend.frequent_patterns import fpgrowth
from mlxtend.preprocessing import TransactionEncoder
import pandas as pd
from task1 import *

def run_fp_growth(transactions, min_support):
    # 將交易數據轉換為one-hot編碼的DataFrame
    te = TransactionEncoder()
    te_ary = te.fit(transactions).transform(transactions)
    df = pd.DataFrame(te_ary, columns=te.columns_)
    
    # 使用FP-growth算法找到頻繁項目集
    frequent_itemsets = fpgrowth(df, min_support=min_support, use_colnames=True)
    
    # 返回頻繁項目集
    return frequent_itemsets

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
    with open("result\\computation_time_task1.txt", "a") as f:
        f.write(f"{filename},minSupport_task1:{minSupport_task1} => Computation time for this task: {round(elapsed_time, 4)} seconds\n")