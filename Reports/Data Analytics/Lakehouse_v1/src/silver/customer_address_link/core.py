import pandas as pd
import src.config
from deltalake import DeltaTable
import cdutils.customer_dim # type: ignore
import cdutils.input_cleansing # type: ignore
import cdutils.add_effdate # type: ignore

def generate_customer_address_link():
    """
    Genereate silver linking able for address/customer

    Uses customer_id as primary key
    O+orgnbr
    P+persnbr

    Upstream dependencies:
    silver address table

    Bronze persaddruse + orgaddruse
    """
    # Pers handling
    persaddruse = DeltaTable(src.config.BRONZE / "persaddruse").to_pandas()
    persaddruse = cdutils.customer_dim.persify(persaddruse, 'persnbr')
    persaddruse = persaddruse.sort_values(by='effdate', ascending=False)
    persaddruse_no_dupes = persaddruse.drop_duplicates(subset=['customer_id','addrusecd'], keep='first').reset_index(drop=True)
    persaddruse_no_dupes = persaddruse_no_dupes[[
        'customer_id',
        'addrnbr',
        'addrusecd'
    ]].copy()

    # Org handling
    orgaddruse = DeltaTable(src.config.BRONZE / "orgaddruse").to_pandas()
    orgaddruse = cdutils.customer_dim.orgify(orgaddruse, 'orgnbr')
    orgaddruse = orgaddruse.sort_values(by='effdate', ascending=False)
    orgaddruse_no_dupes = orgaddruse.drop_duplicates(subset=['customer_id','addrusecd'], keep='first').reset_index(drop=True)
    orgaddruse_no_dupes = orgaddruse_no_dupes[[
        'customer_id',
        'addrnbr',
        'addrusecd'
    ]].copy()

    # Concat
    concat_df = pd.concat([persaddruse_no_dupes, orgaddruse_no_dupes], ignore_index=True)

    # Add effdate
    concat_df = cdutils.add_effdate.add_effdate(concat_df)
    return concat_df