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

Query live vector datasets
```python
# initialize data store
data_store = tychos.VectorDataStore()

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

## Command-line interface
This library additionally provides a tychos command-line utility to make it easy to interact with the API from your terminal. Run tychos-cli -h for usage.

```sh
tychos-cli query --api-key <YOUR-API-KEY> --name pub-med-abstracts --query-string <"Your query string"> --limit 5

```

## Datasets available
We currently support the full PubMed and ArXiv datasets and have plans to add additional sources in the coming weeks. If there's a particular dataset you'd like to incorporate into your LLM application, feel free to [reach out][twitter] or raise a GitHub issue.

### Vector datasets
| Dataset | Name | Size | Update Cadence | Update Time |
| --------------- | --------------- | --------------- | --------------- | --------------- |
| PubMed Abstracts ([source][pub-med]) | pub-med-abstracts | 35.5M documents | Daily | 07:00 UTC |
| Arxiv Abstracts ([source][arxiv]) | arxiv-abstracts | 2.3M documents | Weekly | 07:00 UTC on Sunday|


## Feedback and support
If you'd like to provide feedback, run into issues, or need support using embeddings, feel free to [reach out][twitter] or raise a GitHub issue.


[api-keys]: https://tychos.ai/
[twitter]: https://twitter.com/etpuisfume
[pub-med]: https://pubmed.ncbi.nlm.nih.gov/download/
[arxiv]: https://info.arxiv.org/help/bulk_data/index.html