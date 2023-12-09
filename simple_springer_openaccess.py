import requests
from urllib.parse import urlparse, ParseResult
from bs4 import BeautifulSoup

# for more info
# https://dev.springernature.com/adding-constraints
query = "black holes"
springer_api_key = "2498a3119bec21389fd480eb1610d3ae"
base_url_springer = "http://api.springernature.com/openaccess/json"
url_params_springer = {
    "api_key": springer_api_key,
    "start": 1,
    "p": 3,  # num of articles
    # "q": "doi:10.1134/S1063779623060096",
    "q": f'title:"{query}"',
    # "date-facet-mode": "between",
    # "date": "2017-01-01 TO 2019-12-31",
    "facet": "language",
    "facet-language": "en",
}

mathjax_cdn_script_tag = """
                        <script
                            type="text/javascript"
                            id="MathJax-script"
                            async
                            src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"
                        ></script>
                """


class SpringerArticle:
    def __init__(self, records: dict = {}):
        self.records: dict = records
        self.creators = records.get("creators")
        self.title = records.get("title")
        self.journal = records["publicationName"]
        self.date = records["publicationDate"]
        self.abstract = self.get_article_abstract()
        self.pdf_page_url = self.get_pdf_page_url()
        # self.download_url = self.get_download_url()

    def get_article_abstract(self) -> str | None:
        data: dict = self.records.get("abstract", None)
        if data:
            return data.get("p")
        return None

    def get_pdf_page_url(self) -> str | None:
        try:
            data: dict = self.records.get("url", None)[0]
            if data:
                return data.get("value")

            return None
        except:
            return None

    @property
    def as_html(self):
        """
        return the article content with it's html code
        """
        try:
            res = requests.get(article.pdf_page_url)
            res.raise_for_status()
            soup = BeautifulSoup(res.content, "html.parser")
            article_body = soup.find("main").find("div", class_="c-article-body")
            article_sections = article_body.find_all(class_="c-article-section")

            allsecs = ""
            for sec in article_sections:
                allsecs = allsecs + str(sec)

            allsecs = allsecs + mathjax_cdn_script_tag
            with open(
                f"{self.title[:5]}full_artical.html", "w", encoding="utf-8"
            ) as file:
                file.write(allsecs)
            return allsecs
        except:
            return None

    @property
    def easy_download_url(self):
        """
        fetch the pdf download url
        by manipulating with the article url
        (replacing 'article' by 'content/pdf' and '.pdf' to the end)
        """
        try:
            res = requests.get(self.pdf_page_url)
            res.raise_for_status()
            return res.url.replace("article", "content/pdf") + ".pdf"
        except:
            return None

    @property
    def download_url(self) -> str | None:
        """
        fetch the pdf download url by scrabing the article page
        """
        page_url = self.get_pdf_page_url()

        response = requests.get(page_url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            try:
                html_url = soup.find("meta", {"name": "citation_fulltext_html_url"})[
                    "content"
                ]
                try:
                    pdf_file_path = (
                        soup.find("body")
                        .find("div", class_="c-pdf-download u-clear-both u-mb-16")
                        .find("a", href=True)["href"]
                    )

                except:
                    pdf_file_path = (
                        soup.find("body")
                        .find("div", class_="c-pdf-download u-clear-both")
                        .find("a", href=True)["href"]
                    )

                parsed_html_url: ParseResult = urlparse(html_url)

                full_pdf_url = f"{parsed_html_url.scheme}://{parsed_html_url.netloc}{pdf_file_path}"
                return full_pdf_url
            except Exception as e:
                print(e)
                return None
        else:
            return None


def springer_search(query: str = query) -> list[SpringerArticle]:
    url_params_springer["q"] = f'title:"{query}"'
    records = requests.get(base_url_springer, params=url_params_springer).json()[
        "records"
    ]

    return [SpringerArticle(record) for record in records]


# print(len(articles))

if __name__ == "__main__":
    for article in springer_search():
        # i += 1
        print("##################################")
        print(article.title)
        print(article.pdf_page_url)
        print(article.download_url)
        print(article.easy_download_url())
        article.as_html
        print("##################################")
