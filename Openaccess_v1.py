import requests
import json
import csv
import os
from urllib.parse import urlparse, ParseResult
from bs4 import BeautifulSoup

springer_api_key = "2498a3119bec21389fd480eb1610d3ae"

class Springer_Article:
    def __init__(self, records: dict = {}):
        self.records: dict = records
        self.creators = records.get("creators")
        self.title = records.get("title")
        self.journal = records["publicationName"]
        self.date = records["publicationDate"]
        self.abstract = self.get_article_abstract()
        self.pdf_page_url = self.get_pdf_page_url()
        self.citesnumber = "N/A"
        self.full_text = None

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

    def get_download_url(self) -> str | None:
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

    def author(self):
        name_lst = []
        if self.creators == "N/A":
            combine_name = "N/A"
        else:
            for i in self.creators:
                name_lst.append(i["creator"])
            combine_name = ", ".join(name_lst)
        return combine_name

    def significant(self):
        # sentences_lst = self.abstract.split('.')
        try:
            for s in self.abstract:
                if "significan" in s or "associat" in s:
                    return s
        except:
            return "None"

    def conclusion(self):
        # sentences_lst = self.abstract.split('.')
        try:
            for s in self.abstract:
                if "conclu" in s:
                    return s
            return "None"
        except:
            return "None"

    def suggest(self):
        # sentences_lst = self.abstract.split('.')
        try:
            for s in self.abstract:
                if "suggest" in s:
                    return s
            return "None"
        except:
            return "None"

    def get_doi(self):
        if "doi" in self.records:
            return self.records["doi"]
        else:
            return None

    def get_pdf_page(self):
        conts = {}
        doi = self.get_doi()
        if doi:
            url = f"http://api.springernature.com/openaccess/json?q=doi:{doi}&api_key={springer_api_key}"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
            if "records" in data and len(data["records"]) > 0:
                record = data["records"][0]
                if "url" in record:
                    for url_info in record["url"]:
                        pdf_url = url_info["value"]
                        conts["PDF URL"] = pdf_url
                        conts["contentType"] = record["contentType"]
            return conts


# https://dev.springernature.com/adding-constraints
base_url_springer = "http://api.springernature.com/openaccess/json"
url_params_springer = {}
url_params_springer["api_key"] = springer_api_key
url_params_springer["p"] = 200
url_params_springer["q"] = "title: machine learning for cyber attacks"
url_params_springer["date-facet-mode"] = "between"
url_params_springer["date"] = "2017-01-01 TO 2019-12-31"
url_params_springer["facet"] = "language"
url_params_springer["facet-language"] = "nl"
url_params_springer["facet"] = "content-type"
url_params_springer[
    "facet-content-type"
] = "Article"  # Adjusted to only retrieve articles

d_springer = requests.get(base_url_springer, params=url_params_springer)
json_content = d_springer.json()

with open("springer_abstract.json", "w") as fr_springer:
    json.dump(json_content, fr_springer)
# try:
article_insts2 = [Springer_Article(records) for records in json_content["records"]]
# except:
# for i in json_content['records']:
# print(i)
print(len(article_insts2))
for article in article_insts2:
    print(article.title)
    print(article.get_pdf_page_url())

titlelst2 = [i.title for i in article_insts2]
authorlst2 = [i.author() for i in article_insts2]
journallst2 = [i.journal for i in article_insts2]
datelst2 = [i.date for i in article_insts2]
citeslst2 = [i.citesnumber for i in article_insts2]
abstractlst2 = [i.abstract for i in article_insts2]
significantlst2 = [i.significant() for i in article_insts2]
conclusionlst2 = [i.conclusion() for i in article_insts2]
suggestlst2 = [i.suggest() for i in article_insts2]
# full_textlst2 = [i.full_text for i in article_insts2]


# for article in article_insts2:
#     s = article.get_pdf_page()
#     w = s["PDF URL"]
#     response = requests.get(w)

#     if response.status_code == 200:
#         soup = BeautifulSoup(response.content, "html.parser")

#         # file_nam = article.title[:3] + ".txt"

#         # Write the full text to the text file
#         # with open(file_nam, "wb") as fil:
#         # fil.write(response.content)
#         try:
#             html_url = soup.find("meta", {"name": "citation_fulltext_html_url"})[
#                 "content"
#             ]
#             try:
#                 pdf_file_path = (
#                     soup.find("body")
#                     .find("div", class_="c-pdf-download u-clear-both u-mb-16")
#                     .find("a", href=True)["href"]
#                 )

#             except:
#                 pdf_file_path = (
#                     soup.find("body")
#                     .find("div", class_="c-pdf-download u-clear-both")
#                     .find("a", href=True)["href"]
#                 )

#             parsed_html_url: ParseResult = urlparse(html_url)
#             # ParseResult(
#             #     scheme="https",
#             #     netloc="link.springer.com",
#             #     path="/article/10.1007/s40329-014-0062-0",
#             #     params="",
#             #     query="",
#             #     fragment="",
#             # )

#             print(parsed_html_url.geturl())
#             print(pdf_file_path)
#             full_pdf_url = (
#                 f"{parsed_html_url.scheme}://{parsed_html_url.netloc}{pdf_file_path}"
#             )
#             print(full_pdf_url)
#         except Exception as e:
#             print(e)
#             continue

#         pdf_url_response = requests.get(full_pdf_url)

#         if pdf_url_response.status_code == 200:
#             full_pdf = pdf_url_response.content

#             # Extract the title from the PDF URL and use it as the file name

#             file_name = article.title[:3] + ".pdf"

#             # Write the full text to the text file
#             with open(file_name, "wb") as file:
#                 file.write(full_pdf)

#             print("Full Text for", w, "has been saved to", file_name)
#         else:
#             print("Failed to retrieve full text for", w)
#     else:
#         print("Failed to retrieve PDF URL for", w)
#         print("Failed to retrieve full text for", w)


with open("springer_abstract.csv", "w", newline="", encoding="utf-8") as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(
        [
            "title",
            "authors",
            "journal",
            "date",
            "cites number",
            "abstract",
            "significant relationship",
            "conclusion",
            "suggestion",
        ]
    )
    writer.writerows(
        zip(
            titlelst2,
            authorlst2,
            journallst2,
            datelst2,
            citeslst2,
            abstractlst2,
            significantlst2,
            conclusionlst2,
            suggestlst2,
        )
    )
