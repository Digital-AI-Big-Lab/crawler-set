from ptt import PTT
import json
from datetime import datetime

# PTT class initial
ptt_targets = {
    "Finance": PTT(board='Finance', crawler_pages=50, sleep=0.1),
    "MobilePay": PTT(board='MobilePay', crawler_pages=50, sleep=0.1),
    "CreditCard": PTT(board='creditcard', crawler_pages=50, sleep=0.1),
    "Bank_Service": PTT(board='Bank_Service', crawler_pages=50, sleep=0.1),
    "Stock": PTT(board='Stock', crawler_pages=50, sleep=0.1),
}

# get data from PTT and save it
def saveLocalData(ptt, target):
    articles = list(ptt.get())
    data_to_save = []
    for article in articles:
        data_to_save.append({
            "title": article["title"],
            "content": article["content"],
            "comments": article["comments"],
            "date": str(article["datetime"])[0:10],
            "month": str(article["datetime"])[0:7],
            "article_id": article["article_id"],
            "comments_1": article["comments_1"]
        })

    # Save as .json format
    with open(f"articles_{target}.json", "w", encoding="utf-8") as f:
        json.dump(data_to_save, f, ensure_ascii=False, indent=4)

    print(f"Data for {target} saved at {datetime.now()}")

# Run the function sequentially 
print(f"Start crawling at : {datetime.now()}")
for target, ptt in ptt_targets.items():
    saveLocalData(ptt, target)

print(f"All crawling finished at : {datetime.now()}")

