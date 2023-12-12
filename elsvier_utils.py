# https://dev.elsevier.com/sc_search_tips.html
# https://dev.elsevier.com/scopus.html#!/Scopus_Search/ScopusSearch
api_key = "6f5914ca1357e015db8060b66ebb273e"
query_scopus = "TITLE(black holes) AND OPENACCESS(1)"
url_scopus = f"https://api.elsevier.com/content/search/scopus?query={query_scopus}&apiKey={api_key}"


#############################################################################


query_sciencedirect = "black holes"
url_sciencedirect = f"https://api.elsevier.com/content/search/sciencedirect?query={query_sciencedirect}&apiKey={api_key}"
