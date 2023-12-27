import base64
import random
import requests
import json
import time
from copyleaks.copyleaks import Copyleaks
from copyleaks.exceptions.command_error import CommandError
from copyleaks.models.submit.document import FileDocument, UrlDocument, OcrFileDocument
from copyleaks.models.submit.properties.scan_properties import ScanProperties
from copyleaks.models.export import *
# Register on https://api.copyleaks.com and grab your secret key (from the dashboard page).
EMAIL_ADDRESS = 'hassan.n.afif@gmail.com'
KEY = 'b079479c-fab3-4c7b-ac89-7f70df9d59a3'

try:
    auth_token = Copyleaks.login(EMAIL_ADDRESS, KEY)
except CommandError as ce:
    response = ce.get_response()
    print(f"An error occurred (HTTP status code {response.status_code}):")
    print(response.content)
    exit(1)

print("Logged successfully!\nToken:")
print(auth_token)


# This example is going to scan a FILE for plagiarism.
# Alternatively, you can scan a URL using the class `UrlDocument`.
with open('hello.txt') as file:
       f = file.read()
print("Submitting a new file...")
BASE64_FILE_CONTENT = base64.b64encode(f.encode()).decode('utf8')  # or read your file and convert it into BASE64 presentation.
FILENAME = "hello.txt"
scan_id = random.randint(100, 100000)  # generate a random scan id
file_submission = FileDocument(BASE64_FILE_CONTENT, FILENAME)
# Once the scan completed on Copyleaks servers, we will trigger a webhook that notify you.
# Write your public endpoint server address. If you testing it locally, make sure that this endpoint
# is publicly available.
scan_properties = ScanProperties('https://your.server/webhook?event={{STATUS}}')
scan_properties.set_sandbox(True)  # Turn on sandbox mode. Turn off on production.
file_submission.set_properties(scan_properties)
Copyleaks.submit_file(auth_token, scan_id, file_submission)  # sending the submission to scanning
print("Send to scanning")
print("You will notify, using your webhook, once the scan was completed.")

export = Export()
export.set_completion_webhook('https://your.server/webhook/export/completion')
crawled = ExportCrawledVersion()  # Uncomment if you want to download the crawled version of your submitted document.
crawled.set_endpoint('https://your.server/webhook/export/crawled')
crawled.set_verb('POST')
export.set_crawled_version(crawled)
print(export)

#AI genereated content detection

headers = {
    "Authorization": "Bearer {auth}"
}

myobj = {
    "text": "This is the text I want to check for AI generated content."
}

response = requests.post(
    "https://api.copyleaks.com/v2/writer-detector/my-custom-id/check",
    headers=headers,
    data=myobj
)

print(response.status_code)
print(response.text)
#Grammar checKing
response = requests.post('https://api.copyleaks.com/v1/writing-feedback/my-custom-id/check', headers=headers, data=myobj)
print(response.status_code)
print(response.text)
# # For each of the results in the Completed Webhook, you will get a unique `id`.
# # In the following example we will export 2 results from Copyleaks's servers:
results1 = ExportResult()
results1.set_id('2b42c39fba')  # change with your result id
results1.set_endpoint('https://your.server/webhook/export/result/2b42c39fba')
results1.set_verb('POST')
results1.set_headers([['key', 'value'], ['key2', 'value2']])

results2 = ExportResult()
results2.set_id('08338e505d')  # change with your result id
results2.set_endpoint('https://your.server/webhook/export/result/08338e505d')
results2.set_verb('POST')
results2.set_headers([['key', 'value'], ['key2', 'value2']])

#export.set_results([results1, results2])

Copyleaks.export(auth_token, scan_id, 'export-id', export)  # 'export-id' value determind by you.

# Wait while Copyleaks servers exporting artifacts...
# Once process completed, you will get the "Export Completed" webhook.
# Read more: https://api.copyleaks.com/documentation/v3/webhooks/export-completed

# # For Repositories:
# repo = SearchRepository()
# repo.set_include_my_submissions(True)
# repo.set_include_others_submissions(True)
# repo.set_id("ID_FETCHED_DASHBOARD")
# scan_properties.set_scanning(Scanning().set_repositories(repo))

# # generate a pdf report:
#pdf = Pdf() # Creating instance of Pdf.
#pdf.set_create(True) # Setting the create pdf to True to generate PDF report.
#scan_properties.set_pdf(pdf) # Will generate PDF report.