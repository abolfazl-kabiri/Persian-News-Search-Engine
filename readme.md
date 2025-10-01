# Persian News Search Engine

## Project Overview

This project implements a complete Information Retrieval (IR) system, or a search engine, for a dataset of Persian news articles. 
The system focuses on building a fast, accurate index and employing a Vector Space Model to retrieve and rank documents based on user queries.

## Implemented Features

This search engine is built using standard IR techniques:

| Feature                       | Details                                                                                                                                                   |
|:------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Positional Index**          | Stores term frequency (TF) and word positions to support advanced retrieval.                                                                              |
| **Preprocessing**             | Comprehensive tokenization, normalization, and handling of special Persian characters and half-spacing for components like `می`.                          |
| **Verb Processing**           | Custom logic to handle composite verbs for improved accuracy.                                                                              |
| **Stopword Removal**          | Eliminates the **top 50** most frequent terms to improve index efficiency and search relevance.                     |
| **Stemming**                  | Uses the **Parsivar** library for accurate Persian stemming.                                                                                              |
| **Vector Space Model**        | Document and query representation using **TF-IDF** weighting.                                                                                             |
| **Query Scoring**             | Uses **Cosine Similarity** to measure relevance and rank search results.                                                                                  |
| **Champions Lists**           | Pre-calculated lists of the top 100 most relevant documents for each term, used to significantly reduce query response time.                              |


## Dataset Structure
This project utilizes a collection of Persian news articles (approximately 12,000 documents) stored in a single JSON file named IR_data_news_12k.json. This dataset is required to run the code but is not included in this repository.

Each news article in dataset has following structure

| Field               | Description                                                                                                                      |
|:--------------------|:---------------------------------------------------------------------------------------------------------------------------------|
| **title**           | The headline of the news article.|
| **content**         | The full text of the news article.|
| **tags**            | Keywords or tags associated with the article.|
| **date**            | The publication date and time.|
| **url**             | The source URL of the article.|
| **category**        | The thematic category (e.g., sports, politics).|

### Sample Data Object
```json
{
  "title": "محل برگزاری نشست‌های خبری سرخابی‌ها؛ مجیدی در سازمان لیگ، گل‌محمدی در تمرین پرسپولیس",
  "content": "\nبه گزارش خبرگزاری فارس، نشست خبری پیش از مسابقه سرمربیان دو تیم پرسپولیس و استقلال از هفته بیست و سوم لیگ برتر با  مدیریت سازمان لیگ و هماهنگی باشگاه میزبان( پرسپولیس)  به شرح زیر  برگزار می شود: چهارشنبه ۲۵ اسفند ساعت ۱۵ فرهاد مجیدی سرمربی استقلال در سازمان لیگ فوتبال ایران ساعت ۱۳:۳۰ یحیی گل محمدی سرمربی پرسپولیس در ورزشگاه شهید کاظمی مسابقه دو تیم روز پنجشنبه در ورزشگاه آزادی برگزار می شود. انتهای پیام/\n\n\n",
  "tags": [
    "دربی 94",
    "محل برگزاری",
    "خبری سرخابی‌ها",
    "مجیدی",
    "سازمان لیگ",
    "گل محمدی",
    "سرمربیان"
  ],
  "date": "3/15/2022 5:20:01 PM",
  "url": "https://www.farsnews.ir/news/14001224000971/محل-برگزاری-نشست‌های-خبری-سرخابی‌ها-مجیدی-در-سازمان-لیگ-گل‌محمدی-در",
  "category": "sports"
}
```

## File Structure
| File                 | Description                                                                                                                      |
|:---------------------|:---------------------------------------------------------------------------------------------------------------------------------|
| **indexer.py**       | Handles all index construction: normalization, tokenization, stemming, stopword removal, TF-IDF calculation, and creating the Champions Lists.|
| **search_engine.py** | The main query interface: loads the index, preprocesses the query, uses Cosine Similarity against the Champions List, and ranks the top results.|
| **utils.py**         | Contains helper classes (Posting, PostingsList) and core preprocessing functions: normalize, tokenize, process_verbs, etc.|

