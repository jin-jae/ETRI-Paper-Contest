import pandas as pd

if __name__ == "__main__":
    try:
        mvts_res = pd.read_csv("../predictions/tst_result_q_column.csv")
    except Exception as e:
        print(e)
        print("Did you run ./mvts_transformer/mvts_transformer_final.ipynb?")
        exit(1)
    
    try:
        moc_res = pd.read_csv("../predictions/moc_result_s_column.csv")
    except Exception as e:
        print(e)
        print("Did you run ./multi_output_classifier.ipynb?")
        exit(1)

    mvts_res[["S1", "S2", "S3", "S4"]] = moc_res[["S1", "S2", "S3", "S4"]]

    mvts_res.to_csv("../predictions/answer_final.csv", index=False)

    print("Combined TST(Q1-Q3) + MOC(S1-S4)")