# Tychos Python Library
The Tychos Python library provides convenient access to the Tychos API from
applications written in the Python language. The Tychos API allows you to query live, hosted vector datasets in your LLM application without needing to manage your own vector database / embedding pipelines.

To see the Tychos API in action, you can test out our [PubMed Demo App](https://tychos.ai/demo).

## Installation

You don't need this source code unless you want to modify the package. If you just
want to use the package, just run:

```sh
pip install tychos
```

Install from source with:

```sh
python setup.py install
```
### Requirements

-   Python 2.7+ or Python 3.6+
-   Requests

## Usage

The library needs to be configured with your account's secret key which is
available via the [Tychos Website][api-keys]. Either set the TYCHOS_API_KEY environment variable before using the library:

```python
import tychos
export TYCHOS_API_KEY='sk_a9adj...'
```

Or initialize the VectorDataStore using an API key:
```python
import tychos
data_store = tychos.VectorDataStore(api_key="sk_a9adj...")
```

### Query live vector datasets
```python
# initialize data store
data_store = tychos.VectorDataStore()

# list available datasets
datasets = data_store.list()

# get name of the first dataset's id
print(datasets['data'][0]['name'])

# query a single dataset from the data store object
query_results = data_store.query(
    name = "pub-med-abstracts", # dataset index can be a string or an array
    query_string = "What is the latest research on molecular peptides", # search string
    limit = 5, # number of results
)

# query multiple datasets and return the global top results
query_results = data_store.query(
    name = ["arxiv-abstracts", "pub-med-abstracts"], # dataset index can be a string or an array
    query_string = "What is the latest research on molecular peptides", # search string
    limit = 5, # number of results (across all datasets queried)
)

# print the metadata associated with the first result
print(query_results[0]['payload'])
```

### Filter queries on metadata fields
You can filter queries of individual datasets by passing a query_filter dict that specifies the field, operator and condition to apply. The following operators are currently available:

| Operator | Checks if the field value is... |
| :--- | :--- |
| $eq | **equal to** the specified value|
| $ne | **not equal to** the specified value|
| $in | **within** the specified array|
| $nin | **not within** the specified array|

Example queries using filters:
```python
# filter PubMed query on articles within a particular journal
query_results = data_store.query(
    name = "pub-med-abstracts",
    query_string = "What is the latest research on molecular peptides",
    query_filter = {"Journal": {"$eq":"New England Journal of Medicine"}}
    limit = 5,
)

# filter ArXiv query on papers written by LeCun, Hinton and Bengio
query_results = data_store.query(
    name = "arxiv-abstracts",
    query_string = "What is the latest research on molecular peptides",
    query_filter = {"authors": {"$in":["LeCun", "Hinton", "Bengio"]}}
    limit = 5,
)

```

See the datasets table below for the metadata fields available on each. We are working on adding additional query operators and fields (e.g., date ranges). As we expand datasets, we also plan to make available a set of general filters (e.g., date, author, type) for queries across multiple datasets.

## Command-line interface
This library additionally provides a tychos command-line utility to make it easy to interact with the API from your terminal. Run tychos-cli -h for usage.

```sh
tychos-cli query --api-key <YOUR-API-KEY> --name pub-med-abstracts --query-string <"Your query string"> --limit 5

```

## Datasets available
We currently support a range of pre-print, research, and patent datasets and have plans to add additional sources in the coming weeks. If there's a particular dataset you'd like to incorporate into your LLM application, feel free to [reach out][twitter] or raise a GitHub issue.

### Vector datasets
| Dataset | Name | Size | Syncs | Metadata Fields |
| :--------------- | :--------------- | :--------------- | :--------------- | :--------------------- | 
| PubMed ([source][pub-med]) | pub-med-abstracts | 35.5M documents | Daily at 07:00 UTC | **All fields:**  PMID, PMCID, Title, Abstract, Authors, Abstract_URL, PMC_URL, Journal, Publication Date <br> **Query filterable:** Authors, Journal |
| US Patents ([source][patents]) | us-patents | 6.9M patents | Quarterly at 07:00 UTC (1st of Quarter) | **All fields:** patent_id, title, summary, claims, patent_url, inventors, classification, type, assignees, location, date_filed, date_granted, term <br> **Query filterable:** coming soon! |
| ArXiv ([source][arxiv]) | arxiv-abstracts | 2.3M documents | Weekly at 07:00 UTC (Sunday) | **All fields:** id, doi, paper_title, abstract, authors, categories, abstract_url, full_text_url, journal, pub_date, update_date <br> **Query filterable:** authors, categories, journal |
| BioRxiv ([source][biorxiv]) | biorxiv | 285.5K documents | Monthly at 07:00 UTC (Sunday) | **All fields:** doi, title, abstract, authors, category, jatsxml, author_corresponding, author_corresponding_institution, date, date_timestamp, license, published, type <br> **Query filterable:** authors, category, date_timestamp |
| MedRxiv ([source][medrxiv]) | medrxiv | 58.2K documents | Monthly at 07:00 UTC (Sunday) | **All fields:** doi, title, abstract, authors, category, jatsxml, author_corresponding, author_corresponding_institution, date, date_timestamp, license, published, type <br> **Query filterable:** authors, category, date_timestamp |

## Feedback and support
If you'd like to provide feedback, run into issues, or need support using embeddings, feel free to [reach out][twitter] or raise a GitHub issue.


[api-keys]: https://tychos.ai/
[twitter]: https://twitter.com/etpuisfume
[pub-med]: https://pubmed.ncbi.nlm.nih.gov/download/
[arxiv]: https://info.arxiv.org/help/bulk_data/index.html
[patents]: https://patentsview.org/download/data-download-tables
[biorxiv]: https://www.biorxiv.org/
[medrxiv]: https://www.medrxiv.org/