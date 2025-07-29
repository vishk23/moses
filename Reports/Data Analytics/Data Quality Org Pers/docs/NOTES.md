## 2025-07-18
Mapped out data sources to be used
Set up skeleton for repository

Janet has her version with notes so I will merge with that at the end
- Note hers does not not exclude items that are no longer linked to active accounts so that is worth knowing
    - We will do a join at the end with hers to update her notes to it. They will have all the same columns (after you do uppercase) and we can take only the columns that don't match in her df and append those to mine.

I've created functions to get the refreshed data as we need on org/pers level. That works and has been tested.

Next, I just need a script that will take in the files to the data/inputs/org and data/inputs/pers folder, merge and append any extra columns she may have. It should be a left join on my dataframes because mine will have the up to date data on active customers and hers may have extra data.

We should be able to drop a file in there (excel). It should assert there is only 1 file in there, read in and it should have all the same columns as my pers completed df or org completed df, plus she would have some extra fields for notes. Her column headers will be all uppercase, so we should convert all of my headers to uppercase before joining to ensure clean merge. It will be a left merge on my dataframes because she will have extra records we don't need and we don't need any of the duplicated columns she'd have, we just want the extra ones (columns I don't have on my side). 

## 2025-07-29 (CD)
Updated configuration system to handle production vs development environments:

**Production Mode** (`REPORT_ENV=prod`):
- Output Path: `\\00-da1\Home\Share\Data & Analytics Initiatives\Project Management\Data_Analytics\Data Quality\Data Quality\Automated Refresh`
- Creates `inputs/org`, `inputs/pers`, and `archive` subdirectories
- Saves both timestamped files and `*_latest.xlsx` for automated access
- Email notifications enabled

**Development Mode** (default):
- Uses local project structure (`outputs/`, `data/inputs/`, `data/archive/`)
- No email notifications
- Local testing and development

The main.py now properly uses config paths and handles both environments seamlessly.

## 2025-07-19
This needs to write to path:
\\00-da1\Home\Share\Data & Analytics Initiatives\Project Management\Data_Analytics\Data Quality\Data Quality\Automated Refresh

✅ **COMPLETED** - Now handled via config.py environment detection

---

I added a few placeholder functions that aren't handled in here into the main.py. This will work