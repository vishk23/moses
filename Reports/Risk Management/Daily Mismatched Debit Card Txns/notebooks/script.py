# %%
import requests

# %%
API_KEY = ""
url = "https://randomorg.identifi.net/api/documents/kwyk-search"


# %%
params = {
    "criteria":[{"values":[{"comparisonOperator":1,"value1":"CO_VSUS"}],"attributeInternalName":"DocumentTypeDisplayName","displayName":"Document Type","dataType":1}],"sortBy":"StorageDate","sortDirection":1,"resultsLimit":100
}
headers = {
    "Accept":"application/json",
}

# %%
with requests.Session() as s:
    r = s.get(url, params=params, headers=headers)

# %%
r

# %%
# Start of response, only need pkid (first)
{
  "resultsLimited": true,
  "results": [
    {
      "StorageTypeID": 1,
      "PKID": 7730674,
      "BatchID": -1,
      "DisplayName": "CO_VSUS FISERV SUSPECT REPORT FOR BALANCING/SETTLEMEN         2025/08/07",
      "StorageDate": "2025-08-08T06:06:41.073",
      "OnAdministrativeHold": false,
      "HasNote": false,
      "FullTextHitCount": null,
      "FullTextIndexNumber": null,
      "FullTextDocID": null,
      "SyncStatus": "Not Synched",
      "StorageTypeName": "Insight Reports",
      "DocumentTypeDisplayName": "CO_VSUS",
      "FileSize": 182492,
      "PageCount": 28,
      "RevisionDate": "2025-08-08T06:06:41.073",
      "FileTypeDisplayName": "Report",
      "CreatedBy": "integra0624BCSB",
      "OLEPackageID": null,
      "DocumentSource": "Archiver",
      "_Name": null,
      "_ReportRunDate": "2025-08-07T00:00:00",
      "_ReportPostDate": "2025-08-07T00:00:00",
      "_ReportQueue": "837372",
      "_ReportFileName": "CO_VSUS",
      "_ReportFileID": null
    },
    {
      "StorageTypeID": 1,
      "PKID": 7729251,
      "BatchID": -1,
      "DisplayName": "CO_VSUS FISERV SUSPECT REPORT FOR BALANCING/SETTLEMEN         2025/08/06",
      "StorageDate": "2025-08-07T05:37:23.6",
      "OnAdministrativeHold": false,
      "HasNote": false,
      "FullTextHitCount": null,
      "FullTextIndexNumber": null,
      "FullTextDocID": null,
      "SyncStatus": "Not Synched",
      "StorageTypeName": "Insight Reports",
      "DocumentTypeDisplayName": "CO_VSUS",
      "FileSize": 168543,
      "PageCount": 26,
      "RevisionDate": "2025-08-07T05:37:23.6",
      "FileTypeDisplayName": "Report",
      "CreatedBy": "integra0624BCSB",
      "OLEPackageID": null,
      "DocumentSource": "Archiver",
      "_Name": null,
      "_ReportRunDate": "2025-08-06T00:00:00",
      "_ReportPostDate": "2025-08-06T00:00:00",
      "_ReportQueue": "836880",
      "_ReportFileName": "CO_VSUS",
      "_ReportFileID": null
    },

# %%
# Download url (pkid as last piece)
https://randomorg.identifi.net/api/document/1/7730674


