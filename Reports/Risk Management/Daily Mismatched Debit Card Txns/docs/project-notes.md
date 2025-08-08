stdout:
[api_call] FETCH latest -> start
[api_call] SEARCH begin -> url=https://bcsb.identifi.net/api/documents/kwyk-search
[api_call] SEARCH headers keys: ['Accept', 'Content-Type', 'User-Agent', 'disable-global-loading-indicator', 'x-api-key']
[api_call] SEARCH criteria=CO_VSUS sortBy=StorageDate sortDirection=1 limit=100
[api_call] SEARCH response: status=200 ctype=application/json; charset=utf-8 len=98454
[api_call] SEARCH results count=100
[api_call] PKID: 7730674
[api_call] SEARCH first doc has downloadUrl=False
[api_call] FETCH latest -> destination=\\00-da1\Home\Share\Line of Business_Shared Services\Risk Management\Daily Mismatched Debit Card Txns\input\CO_VSUS_7730674.txt
[api_call] FETCH latest -> using override_url=False
[api_call] DOWNLOAD pkid=7730674 -> candidates=['https://bcsb.identifi.net/api/document/1/7730674', 'https://bcsb.identifi.net/api/document/1/7730674/file', 'https://bcsb.identifi.net/api/document/1/7730674/content', 'https://bcsb.identifi.net/api/document/1/7730674?download=true']
[api_call] DOWNLOAD try url=https://bcsb.identifi.net/api/document/1/7730674 -> status=200 ctype=application/json; charset=utf-8
[api_call] DOWNLOAD try url=https://bcsb.identifi.net/api/document/1/7730674 -> got JSON, skipping. Preview={'applicationId': 1, 'batchId': -1, 'blobName': None, 'diskNumber': 1771, 'displayName': 'CO_VSUS FISERV SUSPECT REPORT FOR BALANCING/SETTLEMEN         2025/08/07', 'displayProfile
[api_call] DOWNLOAD try url=https://bcsb.identifi.net/api/document/1/7730674/file -> HTTPError 404 
[api_call] DOWNLOAD try url=https://bcsb.identifi.net/api/document/1/7730674/content -> status=200 ctype=text/report
[api_call] DOWNLOAD success -> wrote bytes=182492 to \\00-da1\Home\Share\Line of Business_Shared Services\Risk Management\Daily Mismatched 
Debit Card Txns\input\CO_VSUS_7730674.txt
Downloaded and saved latest CO_VSUS file to INPUT_DIR: \\00-da1\Home\Share\Line of Business_Shared Services\Risk Management\Daily Mismatched Debit Card Txns\input\CO_VSUS_7730674.txt
Moved CO_VSUS_7730674.txt to input/archive directory.
Moved Daily Posting Sheet 08-07-2025.xlsx to output/archive directory.
Report saved to \\00-da1\Home\Share\Line of Business_Shared Services\Risk Management\Daily Mismatched Debit Card Txns\output\Daily Posting 
Sheet 08-07-2025.xlsx
Complete!
