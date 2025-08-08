2025-08-08 12:32:32 | INFO | === REPORT RUNNER SESSION START [PROD MODE] ===
2025-08-08 12:32:33 | INFO | DISCOVERY COMPLETE | Found 24 reports | Environment: PROD
2025-08-08 12:32:33 | INFO | LIST ONLY | No reports executed
2025-08-08 12:32:42 | INFO | === REPORT RUNNER SESSION START [PROD MODE] ===
2025-08-08 12:32:42 | INFO | DISCOVERY COMPLETE | Found 24 reports | Environment: PROD
2025-08-08 12:32:42 | INFO | BATCH START | 1 reports | Filter: name = Daily Mismatched Debit Card Txns | Environment: PROD
2025-08-08 12:32:42 | INFO | START | Daily Mismatched Debit Card Txns | Business Line: Risk Management | Environment: PROD
2025-08-08 12:32:42 | INFO | DEBUG | Python executable: C:\Users\w322800\Documents\gh\bcsb-prod\.venv\Scripts\python.exe
2025-08-08 12:32:42 | INFO | DEBUG | Working directory: Reports\Risk Management\Daily Mismatched Debit Card Txns
2025-08-08 12:32:42 | INFO | DEBUG | Command: C:\Users\w322800\Documents\gh\bcsb-prod\.venv\Scripts\python.exe -m src.main
2025-08-08 12:32:46 | ERROR | FAILED | Daily Mismatched Debit Card Txns | Runtime: 0.06 minutes
2025-08-08 12:32:46 | ERROR | Python executable: C:\Users\w322800\Documents\gh\bcsb-prod\.venv\Scripts\python.exe
2025-08-08 12:32:46 | ERROR | Working directory: Reports\Risk Management\Daily Mismatched Debit Card Txns
2025-08-08 12:32:46 | ERROR | Return code: 1
2025-08-08 12:32:46 | ERROR | STDERR:
Traceback (most recent call last):
  File "<frozen runpy>", line 198, in _run_module_as_main
  File "<frozen runpy>", line 88, in _run_code
  File "C:\Users\w322800\Documents\gh\bcsb-prod\Reports\Risk Management\Daily Mismatched Debit Card Txns\src\main.py", line 179, in <module>
    main()
  File "C:\Users\w322800\Documents\gh\bcsb-prod\Reports\Risk Management\Daily Mismatched Debit Card Txns\src\main.py", line 34, in main
    assert len(txt_files) == 1, ("There should only be one file .txt file in " +
           ^^^^^^^^^^^^^^^^^^^
AssertionError: There should only be one file .txt file in \\00-da1\Home\Share\Line of Business_Shared Services\Risk Management\Daily Mismatched Debit Card Txns\input
2025-08-08 12:32:46 | ERROR | STDOUT:
Starting [v1.0.0-prod]
PKID: 7730674
Warning: API fetch skipped/failed: Unexpected JSON response when downloading document: {'applicationId': 1, 'batchId': -1, 'blobName': None, 'diskNumber': 1771, 'displayName': 'CO_VSUS FISERV SUSPECT REPORT FOR BALANCING/SETTLEMEN         2025/08/07', 'displayProfile': None, 'documentId': 7730674, 'documentSource': 'Archiver', 'documentType': 'CO_VSUS', 'documentTypeId': 1203, 'fileNumber': 56, 'fileSizeDescription': '(182492 bytes) 178.21 KB', 'fileSize': 182492, 'fileType': 'Report', 'fileTypeExtension': 'prn', 'isOnline': True, 'isOnAdministrativeHold': False, 'onAdministrativeHoldUserName': None, 'lastSyncDate': '', 'maxReportRows': 61, 'maxReportColumns': 137, 'mimeType': 'text/report', 'notes': [], 'originalFileName': 'CO_VSUS FISERV SUSPECT REPORT FOR BALANCINGSETTLEMEN         20250807.prn', 'pageCount': 28, 'retentionPreventsDelete': False, 'rescanable': False, 'security': {'allowView': True, 'allowRevise': False, 'allowDelete': False, 'allowViewNote': True, 'allowAddNote': True, 'allowChangeNote': False, 'allowIndex': False, 'allowPrint': True, 'allowSecurity': False}, 'storageDate': '2025-08-08T06:06:41.073', 'viewable': True, 'volumeNumber': 3, 'info': [{'version': 1, 'createdBy': 'integra0624BCSB', 'storageDate': '2025-08-08T06:06:41.09', 'downloadUrl': '', 'olePackageId': -1}], 'attributes': [{'required': False, 'multiValueGroupNumber': -1, 'values': ['ZZRPT_upper'], 'id': 40, 'name': 'Report Audit', 'internalName': '_ReportAudit', 'dataType': 1, 'computed': False, 'dataLength': 0, 'dataScale': 0, 'searchable': False, 'detailVisible': False, 'multiValue': False, 'dictionaryType': 0, 'sequence': 0}, {'required': False, 'multiValueGroupNumber': -1, 'values': ['CO_VSUS'], 'id': 42, 'name': 'Report File Name', 'internalName': '_ReportFileName', 'dataType': 1, 'computed': False, 'dataLength': 0, 'dataScale': 0, 'searchable': True, 'detailVisible': False, 'multiValue': False, 'dictionaryType': 0, 'sequence': 0}, {'required': False, 'multiValueGroupNumber': -1, 'values': ['Fiserv', 'Suspect', 'Report', 'for', 'Balancing/Settlemen'], 'id': 37, 'name': 'Report Keyword', 'internalName': '_ReportKeyword', 'dataType': 1, 'computed': False, 'dataLength': 0, 'dataScale': 0, 'searchable': True, 'detailVisible': False, 'multiValue': True, 'dictionaryType': 0, 'sequence': 0}, {'required': False, 'multiValueGroupNumber': -1, 'values': ['2025-08-07T00:00:00'], 'id': 38, 'name': 'Report Post Date', 'internalName': '_ReportPostDate', 'dataType': 4, 'computed': False, 'dataLength': 0, 'dataScale': 0, 'searchable': True, 'detailVisible': False, 'multiValue': False, 'dictionaryType': 0, 'sequence': 0}, {'required': False, 'multiValueGroupNumber': -1, 'values': ['837372'], 'id': 41, 'name': 'Report Queue', 'internalName': '_ReportQueue', 'dataType': 1, 'computed': False, 'dataLength': 0, 'dataScale': 0, 'searchable': True, 'detailVisible': False, 'multiValue': False, 'dictionaryType': 0, 'sequence': 0}, {'required': False, 'multiValueGroupNumber': -1, 'values': ['2025-08-07T00:00:00'], 'id': 36, 'name': 'Report Run Date', 'internalName': '_ReportRunDate', 'dataType': 4, 'computed': False, 'dataLength': 0, 'dataScale': 0, 'searchable': True, 'detailVisible': False, 'multiValue': False, 'dictionaryType': 0, 'sequence': 0}, {'required': False, 'multiValueGroupNumber': -1, 'values': ['REPORT'], 'id': 39, 'name': 'Report Type', 'internalName': '_ReportType', 'dataType': 1, 'computed': False, 'dataLength': 0, 'dataScale': 0, 'searchable': True, 'detailVisible': False, 'multiValue': False, 'dictionaryType': 0, 'sequence': 0}], 'allowStartWorkflow': False}
2025-08-08 12:32:46 | INFO | BATCH COMPLETE | Total: 1 | Successful: 0 | Failed: 1 | Batch Runtime: 0.06 minutes
2025-08-08 12:32:46 | INFO | === REPORT RUNNER SESSION END ===

{
  "applicationId": 1,
  "batchId": -1,
  "blobName": null,
  "diskNumber": 1771,
  "displayName": "CO_VSUS FISERV SUSPECT REPORT FOR BALANCING/SETTLEMEN         2025/08/07",
  "displayProfile": null,
  "documentId": 7730674,
  "documentSource": "Archiver",
  "documentType": "CO_VSUS",
  "documentTypeId": 1203,
  "fileNumber": 56,
  "fileSizeDescription": "(182492 bytes) 178.21 KB",
  "fileSize": 182492,
  "fileType": "Report",
  "fileTypeExtension": "prn",
  "isOnline": true,
  "isOnAdministrativeHold": false,
  "onAdministrativeHoldUserName": null,
  "lastSyncDate": "",
  "maxReportRows": 61,
  "maxReportColumns": 137,
  "mimeType": "text/report",
  "notes": [],
  "originalFileName": "CO_VSUS FISERV SUSPECT REPORT FOR BALANCINGSETTLEMEN         20250807.prn",
  "pageCount": 28,
  "retentionPreventsDelete": false,
  "rescanable": false,
  "security": {
    "allowView": true,
    "allowRevise": false,
    "allowDelete": false,
    "allowViewNote": true,
    "allowAddNote": true,
    "allowChangeNote": false,
    "allowIndex": false,
    "allowPrint": true,
    "allowSecurity": false
  },
  "storageDate": "2025-08-08T06:06:41.073",
  "viewable": true,
  "volumeNumber": 3,
  "info": [
    {
      "version": 1,
      "createdBy": "integra0624BCSB",
      "storageDate": "2025-08-08T06:06:41.09",
      "downloadUrl": "",
      "olePackageId": -1
    }
  ],
  "attributes": [
    {
      "required": false,
      "multiValueGroupNumber": -1,
      "values": [
        "ZZRPT_upper"
      ],
      "id": 40,
      "name": "Report Audit",
      "internalName": "_ReportAudit",
      "dataType": 1,
      "computed": false,
      "dataLength": 0,
      "dataScale": 0,
      "searchable": false,
      "detailVisible": false,
      "multiValue": false,
      "dictionaryType": 0,
      "sequence": 0
    },
    {
      "required": false,
      "multiValueGroupNumber": -1,
      "values": [
        "CO_VSUS"
      ],
      "id": 42,
      "name": "Report File Name",
      "internalName": "_ReportFileName",
      "dataType": 1,
      "computed": false,
      "dataLength": 0,
      "dataScale": 0,
      "searchable": true,
      "detailVisible": false,
      "multiValue": false,
      "dictionaryType": 0,
      "sequence": 0
    },
    {
      "required": false,
      "multiValueGroupNumber": -1,
      "values": [
        "Fiserv",
        "Suspect",
        "Report",
        "for",
        "Balancing/Settlemen"
      ],
      "id": 37,
      "name": "Report Keyword",
      "internalName": "_ReportKeyword",
      "dataType": 1,
      "computed": false,
      "dataLength": 0,
      "dataScale": 0,
      "searchable": true,
      "detailVisible": false,
      "multiValue": true,
      "dictionaryType": 0,
      "sequence": 0
    },
    {
      "required": false,
      "multiValueGroupNumber": -1,
      "values": [
        "2025-08-07T00:00:00"
      ],
      "id": 38,
      "name": "Report Post Date",
      "internalName": "_ReportPostDate",
      "dataType": 4,
      "computed": false,
      "dataLength": 0,
      "dataScale": 0,
      "searchable": true,
      "detailVisible": false,
      "multiValue": false,
      "dictionaryType": 0,
      "sequence": 0
    },
    {
      "required": false,
      "multiValueGroupNumber": -1,
      "values": [
        "837372"
      ],
      "id": 41,
      "name": "Report Queue",
      "internalName": "_ReportQueue",
      "dataType": 1,
      "computed": false,
      "dataLength": 0,
      "dataScale": 0,
      "searchable": true,
      "detailVisible": false,
      "multiValue": false,
      "dictionaryType": 0,
      "sequence": 0
    },
    {
      "required": false,
      "multiValueGroupNumber": -1,
      "values": [
        "2025-08-07T00:00:00"
      ],
      "id": 36,
      "name": "Report Run Date",
      "internalName": "_ReportRunDate",
      "dataType": 4,
      "computed": false,
      "dataLength": 0,
      "dataScale": 0,
      "searchable": true,
      "detailVisible": false,
      "multiValue": false,
      "dictionaryType": 0,
      "sequence": 0
    },
    {
      "required": false,
      "multiValueGroupNumber": -1,
      "values": [
        "REPORT"
      ],
      "id": 39,
      "name": "Report Type",
      "internalName": "_ReportType",
      "dataType": 1,
      "computed": false,
      "dataLength": 0,
      "dataScale": 0,
      "searchable": true,
      "detailVisible": false,
      "multiValue": false,
      "dictionaryType": 0,
      "sequence": 0
    }
  ],
  "allowStartWorkflow": false
}

Request headers:
GET /api/document/1/7730674 HTTP/1.1
Accept: application/json, text/plain, */*
Accept-Encoding: gzip, deflate, br, zstd
Accept-Language: en-US,en;q=0.9
Connection: keep-alive
Cookie: _gcl_au=1.1.1130529669.1754578151; _ga=GA1.1.417761169.1754578152; _reb2buid=b2ba321c-5edd-4215-9ede-f1ac65463a88-1754578151793; _reb2bgeo=%7B%22city%22%3A%22Medway%22%2C%22country%22%3A%22United%20States%22%2C%22countryCode%22%3A%22US%22%2C%22hosting%22%3Afalse%2C%22isp%22%3A%22COCC%22%2C%22lat%22%3A42.1418%2C%22proxy%22%3Afalse%2C%22region%22%3A%22MA%22%2C%22regionName%22%3A%22Massachusetts%22%2C%22status%22%3A%22success%22%2C%22timezone%22%3A%22America%2FNew_York%22%2C%22zip%22%3A%2202053%22%7D; _reb2bresolve=1; _lc2_fpi=b6e18384584e--01k22g3tn4dsjzb0555p9da3wh; _reb2bli=ZGRhMWX0NW1GH1PDO4UzOWQ3MjNlYzhjMDFiMjZmOGVmYjE1NjM1Yzg=; _reb2bsha=ZmNiMGY1MTI4NzIyM2X0NW1GH1PDO4Y5YTZiYjNiYTIxMGE4MjgyOWMzZDgyNGQ3ODk2NGY5ODgyMDNiZjA5ODU2ZTA3N2RjNw==; cf_clearance=WVXpkhFrg0w0mnuwPPbgwWZor0XfSF.i_.FwzLIO_zs-1754661183-1.2.1.1-WOXuSb48aWKo_GENx50YYVIO1026NhJRnaYyo3g7dn383XlvNeoSutEH7dmuODU_wn8FDOT4LYGHp4MvHs9iKbgcbdcD6Ek0LB796oR8H5Fh3xgBvgY1x_WGhDmJNlQm_GOTUdmWhTr95TDVxh9U1L22gsrlU_ZQHhS4Hlt0UHyT9efYy_jzKZdHVsnPYyXt2lbqCRrP0wq874oXLj3gVpH1PRzueK6S_bVwMZusT3w; _reb2bref=https://identifi.net/our-products/integrations/; _ga_SMN0B9HX4F=GS2.1.s1754661182$o2$g1$t1754661205$j37$l0$h0; _ga_VBYEPDK5SS=GS2.1.s1754661183$o2$g1$t1754661205$j38$l0$h0; Identifi-0624BCSB=CfDJ8MZ_282yw9VEs2pwKsklJ7pDu9a-uQjSj03q-oJ8yENOISJNvf5MJyDgP_ONXiGaExI1xI1Tik1OXsvzA6n3KBXr3rMYS63yjhBwdoe7o2wsiYYIRCYjujObn4aPpBg4yCMK7uuVeVeOcVZ5tDBA-EZAVqMBoyRMIkDJ1ENf8BQADRoD9f9siiPMwW7BIWQYxwn61ACcnlROno76hmqOgr7V7WpU8XivzYp8RAV9Vok2hAXvDwqVdPjaOLj3JDLSqtAI_bdjzGQ6nrZ1zutEH48P2pbblV1V7Jc08mChpdp6DiB0AWuvvFzhOp9LQN5_vv9NOlYhytNcuDvKr84oyOj5ZBk4aDR3fb3JLo1mk_scTp4a9EzlYuzZxGsjR-h6SwI2RSuLq7lnksqWOGaGwa8wtpz1xo4FN5yX-A9lyNOW4YsLDEDomz0eXBBdJ9R7rwIu50uFW4mG9UWCkMe7L13RO1vWEesu3HYNAER5kKeeoBNAGdPrASSNnHa_CWnTPq3dCJYBp646iiuW4gImtDX-yhVn8MMQioM9L7VOAJxKKdG-cFCKVJ3wlBp4c2tZW_tQ0aQe8erU3Ou0ROZDtlc
Host: bcsb.identifi.net
Referer: https://bcsb.identifi.net/document/search?Attributes=DocumentTypeDisplayName%7BCO_VSUS%7D&SortBy=StorageDate&SortDirection=1
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36
disable-global-loading-indicator: true
sec-ch-ua: "Not;A=Brand";v="99", "Google Chrome";v="139", "Chromium";v="139"
sec-ch-ua-mobile: ?0
sec-ch-ua-platform: "Windows"
