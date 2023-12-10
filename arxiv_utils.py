# https://lukasschwab.me/arxiv.py/arxiv.html
# https://poe.com/chat/2t4f2epll96yl0li4gn

import arxiv

# Construct the default API client.
client = arxiv.Client(page_size=100, delay_seconds=1.0, num_retries=5)

# Search for the 10 most recent articles matching the keyword "quantum."
search = arxiv.Search(
    query="Quantum Gravity",
    max_results=100,
    sort_by=arxiv.SortCriterion.Relevance,
    sort_order=arxiv.SortOrder.Descending,
)

results = client.results(search)

all_results = list(results)
# `results` is a generator; you can iterate over its elements one by one...
for r in client.results(search):
    print("* * * * * * ")
    print(r.title)
    # print(r)
    # print(r.pdf_url)

    print("* * * * * * \n")
# print(all_results[0].summary)

# ...or exhaust it into a list. Careful: this is slow for large results sets.
# print([r.title for r in all_results])
