### CoStar Extract

COCC data is transformed into a loader via which is sent via SFTP to CoStar to be loaded into their lender model.

I have the .docx as an external documenation guide, but this will be the technical documentation for the workflow.

#Overview
There are 4 disctinct workflows that run in a certain order to produce the extract .xlsx file
1) CoStarTemplateCopy2.yxmd
- The existing file is overwritten with a blank copy of the template
- Utilizes a cmd.bat file in the Supporting Files folder
2) CoStarMain.yxmd
- This is the main workflow where Permanent and Construction loans are written to the template
3) BCSBParticipation2.yxmd
- Participation % is calculated for bought and sold participation loans
- This complements the Main workflow, as everything on the Permanent and Construction loans show up as full unparticipated loans using NOTEBAL and full appraisal amounts
- The participation tab helps the Lender platform identify all the participations and applies modifications on their end of the model
4) CoStarUploadScript2.yxmd
- This allows the OUTPUT document to be written anywhere and this script moves it to the location that the SFTP will automatically send from
- Currently, this is on the DA-1 drive in Commercial Credit and it's in a folder called CoStar/Upload
- The full location is \\10.161.85.66\Home\Share\Line of Business_Shared Services\Commercial Credit\CoStar\Upload


2/27/24
Going to adjust the template to the newer version to be able to handle rate changes
An analysis of how we want rates to function may be necessary.
- If we code as floating rate, they will just take the spread we gave them (1%) and add it to the index
- Fixed rates will always show the rate we have on core as current interest rate


