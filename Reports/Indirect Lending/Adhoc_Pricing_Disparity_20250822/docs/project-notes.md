# 2025-08-26
Taking this report request

It is a bit tricky because of the caching of the database

I originally tried to take the cleaned account data as of different dates, but I have only active accounts in my df. That's the nuance.

I have many improvements to make to this reporting layer, but I think this will be a report that I'll do the old fashioned way. 
- Need to get this to Terry by tomorrow


----

Data I need
- Application ID
    - meridian link
- Account Number 
    - osibank/coccdm acctcommon
- Loan Origination Date
    - same
- Applicant Last Name 
    - pers
- Applicant First Name
    - pers
- Co-Applicant Last Name
    - pers after grouping with allroles
- Co-Applicant First Name
    - pers after grouping with allroles
- Applicant Credit Score
    - wh_pers
- Co-Applicant Credit Score
    - wh_pers
- Model Year
    - prop or prop2
- Vehicle Mileage
    - prop or prop2
- Dealer Name
    - ?
- Amount Financed
    - orig_ttl_loan_amt
- Current Balance
    - net balance
- Contract Rate
    - ?
- Buy Rate
    - ?
- Loan Paid or Open
    - status
- Date Closed
    - closedate
    - acctcommon


----

---------------------------------------------------------------------------
TypeError                                 Traceback (most recent call last)
Cell In[6], line 1
----> 1 df = src.account_data_adhoc.core.query_df_on_date()

File c:\Users\w322800\Documents\gh\bcsb-prod\Reports\Indirect Lending\Adhoc_Pricing_Disparity_20250822\src\account_data_adhoc\core.py:55, in query_df_on_date(specified_date)
     52     assert isinstance(specified_date, datetime), "Specified date must be a datetime object"
     53     specified_date = get_last_business_day(specified_date)
---> 55 data = src.account_data_adhoc.fetch_data.fetch_data(specified_date)
     57 # # # Core transformation pipeline
     58 raw_data = src.account_data_adhoc.core_transform.main_pipeline(data)

TypeError: fetch_data() takes 0 positional arguments but 1 was given

----

Do you by any chance have the data we provided the 3rd party for their analysis so I can tie back to my data. I tried to request meridian link data and was told they would have to open a ticket and it be $15k per year's worth of data which sounds absolutely absurd....


---

---------------------------------------------------------------------------
DatabaseError                             Traceback (most recent call last)
File c:\Users\w322800\Documents\gh\bcsb-prod\.venv\Lib\site-packages\sqlalchemy\engine\base.py:1967, in Connection._exec_single_context(self, dialect, context, statement, parameters)
   1966     if not evt_handled:
-> 1967         self.dialect.do_execute(
   1968             cursor, str_statement, effective_parameters, context
   1969         )
   1971 if self._has_events or self.engine._has_events:

File c:\Users\w322800\Documents\gh\bcsb-prod\.venv\Lib\site-packages\sqlalchemy\engine\default.py:951, in DefaultDialect.do_execute(self, cursor, statement, parameters, context)
    950 def do_execute(self, cursor, statement, parameters, context=None):
--> 951     cursor.execute(statement, parameters)

File c:\Users\w322800\Documents\gh\bcsb-prod\.venv\Lib\site-packages\sqlalchemy\connectors\asyncio.py:192, in AsyncAdapt_dbapi_cursor.execute(self, operation, parameters)
    191 except Exception as error:
--> 192     self._adapt_connection._handle_exception(error)

File c:\Users\w322800\Documents\gh\bcsb-prod\.venv\Lib\site-packages\sqlalchemy\connectors\asyncio.py:330, in AsyncAdapt_dbapi_connection._handle_exception(self, error)
    328 exc_info = sys.exc_info()
--> 330 raise error.with_traceback(exc_info[2])

File c:\Users\w322800\Documents\gh\bcsb-prod\.venv\Lib\site-packages\sqlalchemy\connectors\asyncio.py:190, in AsyncAdapt_dbapi_cursor.execute(self, operation, parameters)
    189 try:
--> 190     return self.await_(self._execute_async(operation, parameters))
    191 except Exception as error:

File c:\Users\w322800\Documents\gh\bcsb-prod\.venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py:132, in await_only(awaitable)
    128 # returns the control to the driver greenlet passing it
    129 # a coroutine to run. Once the awaitable is done, the driver greenlet
    130 # switches back to this greenlet with the result of awaitable that is
    131 # then returned to the caller (or raised as error)
--> 132 return current.parent.switch(awaitable)

File c:\Users\w322800\Documents\gh\bcsb-prod\.venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py:196, in greenlet_spawn(fn, _require_await, *args, **kwargs)
    193 try:
    194     # wait for a coroutine from await_only and then return its
    195     # result back to it.
--> 196     value = await result
    197 except BaseException:
    198     # this allows an exception to be raised within
    199     # the moderated greenlet so that it can continue
    200     # its expected flow.

File c:\Users\w322800\Documents\gh\bcsb-prod\.venv\Lib\site-packages\sqlalchemy\dialects\oracle\oracledb.py:771, in AsyncAdapt_oracledb_cursor._execute_async(self, operation, parameters)
    770 else:
--> 771     result = await self._cursor.execute(operation, parameters)
    773 if self._cursor.description and not self.server_side:

File c:\Users\w322800\Documents\gh\bcsb-prod\.venv\Lib\site-packages\oracledb\cursor.py:984, in AsyncCursor.execute(self, statement, parameters, suspend_on_success, **keyword_parameters)
    983 self._impl.suspend_on_success = suspend_on_success
--> 984 await self._impl.execute(self)

File src/oracledb/impl/thin/cursor.pyx:390, in execute()

File src/oracledb/impl/thin/protocol.pyx:855, in _process_single_message()

File src/oracledb/impl/thin/protocol.pyx:856, in oracledb.thin_impl.BaseAsyncProtocol._process_single_message()

File src/oracledb/impl/thin/protocol.pyx:832, in _process_message()

File src/oracledb/impl/thin/messages/base.pyx:102, in oracledb.thin_impl.Message._check_and_raise_exception()

DatabaseError: ORA-01861: literal does not match format string
Help: https://docs.oracle.com/error-help/db/ora-01861/

The above exception was the direct cause of the following exception:

DatabaseError                             Traceback (most recent call last)
Cell In[3], line 1
----> 1 df = src.account_data_adhoc.core.query_df_on_date()

File c:\Users\w322800\Documents\gh\bcsb-prod\Reports\Indirect Lending\Adhoc_Pricing_Disparity_20250822\src\account_data_adhoc\core.py:55, in query_df_on_date(specified_date)
     52     assert isinstance(specified_date, datetime), "Specified date must be a datetime object"
     53     specified_date = get_last_business_day(specified_date)
---> 55 data = src.account_data_adhoc.fetch_data.fetch_data(specified_date)
     57 # # # Core transformation pipeline
     58 raw_data = src.account_data_adhoc.core_transform.main_pipeline(data)

File c:\Users\w322800\Documents\gh\bcsb-prod\Reports\Indirect Lending\Adhoc_Pricing_Disparity_20250822\src\account_data_adhoc\fetch_data.py:110, in fetch_data(specified_date)
     94 wh_pers = text("""
     95 SELECT
     96     *
     97 FROM
     98     OSIBANK.WH_PERS a
     99 """)    
    101 queries = [
    102     {'key':'wh_acctcommon', 'sql':wh_acctcommon, 'engine':2},
    103     {'key':'wh_loans', 'sql':wh_loans, 'engine':2},
   (...)    106     {'key':'wh_pers', 'sql':wh_pers, 'engine':1},
    107 ]
--> 110 data = cdutils.database.connect.retrieve_data(queries)
    111 return data

File ~\Documents\gh\bcsb-prod\cdutils\cdutils\database\connect.py:162, in retrieve_data(queries)
    159     else:
    160         return asyncio.run(run_queries())
--> 162 data = run_sql_queries(queries)
    164 return data

File ~\Documents\gh\bcsb-prod\cdutils\cdutils\database\connect.py:158, in retrieve_data.<locals>.run_sql_queries(queries)
    156 loop = asyncio.get_event_loop()
    157 if loop.is_running():
--> 158     return loop.run_until_complete(run_queries())
    159 else:
    160     return asyncio.run(run_queries())

File c:\Users\w322800\Documents\gh\bcsb-prod\.venv\Lib\site-packages\nest_asyncio.py:98, in _patch_loop.<locals>.run_until_complete(self, future)
     95 if not f.done():
     96     raise RuntimeError(
     97         'Event loop stopped before Future completed.')
---> 98 return f.result()

File ~\AppData\Local\Programs\Python\Python311\Lib\asyncio\futures.py:203, in Future.result(self)
    201 self.__log_traceback = False
    202 if self._exception is not None:
--> 203     raise self._exception.with_traceback(self._exception_tb)
    204 return self._result

File ~\AppData\Local\Programs\Python\Python311\Lib\asyncio\tasks.py:277, in Task.__step(***failed resolving arguments***)
    273 try:
    274     if exc is None:
    275         # We use the `send` method directly, because coroutines
    276         # don't have `__iter__` and `__next__` methods.
--> 277         result = coro.send(None)
    278     else:
    279         result = coro.throw(exc)

File ~\Documents\gh\bcsb-prod\cdutils\cdutils\database\connect.py:154, in retrieve_data.<locals>.run_sql_queries.<locals>.run_queries()
    153 async def run_queries():
--> 154     return await fetch_data(queries)

File ~\Documents\gh\bcsb-prod\cdutils\cdutils\database\connect.py:143, in retrieve_data.<locals>.fetch_data(queries)
    141 try:
    142     tasks = {query['key']: asyncio.create_task(db_handler.query(query['sql'], query['engine'])) for query in queries}
--> 143     results = await asyncio.gather(*tasks.values())
    144     return {key: df for key, df in zip(tasks.keys(), results)}
    145 except Exception as e:

File ~\AppData\Local\Programs\Python\Python311\Lib\asyncio\tasks.py:349, in Task.__wakeup(self, future)
    347 def __wakeup(self, future):
    348     try:
--> 349         future.result()
    350     except BaseException as exc:
    351         # This may also be a cancellation.
    352         self.__step(exc)

File ~\AppData\Local\Programs\Python\Python311\Lib\asyncio\tasks.py:277, in Task.__step(***failed resolving arguments***)
    273 try:
    274     if exc is None:
    275         # We use the `send` method directly, because coroutines
    276         # don't have `__iter__` and `__next__` methods.
--> 277         result = coro.send(None)
    278     else:
    279         result = coro.throw(exc)

File ~\Documents\gh\bcsb-prod\cdutils\cdutils\database\connect.py:122, in retrieve_data.<locals>.DatabaseHandler.query(self, sql_query, engine)
    119     raise ValueError("Engine must be 1 or 2")
    121 async with selected_engine.connect() as connection:
--> 122     result = await connection.execute(sql_query)
    123     rows = result.fetchall()
    124     if not rows:

File c:\Users\w322800\Documents\gh\bcsb-prod\.venv\Lib\site-packages\sqlalchemy\ext\asyncio\engine.py:658, in AsyncConnection.execute(self, statement, parameters, execution_options)
    620 async def execute(
    621     self,
    622     statement: Executable,
   (...)    625     execution_options: Optional[CoreExecuteOptionsParameter] = None,
    626 ) -> CursorResult[Any]:
    627     r"""Executes a SQL statement construct and return a buffered
    628     :class:`_engine.Result`.
    629 
   (...)    656 
    657     """
--> 658     result = await greenlet_spawn(
    659         self._proxied.execute,
    660         statement,
    661         parameters,
    662         execution_options=execution_options,
    663         _require_await=True,
    664     )
    665     return await _ensure_sync_result(result, self.execute)

File c:\Users\w322800\Documents\gh\bcsb-prod\.venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py:201, in greenlet_spawn(fn, _require_await, *args, **kwargs)
    196     value = await result
    197 except BaseException:
    198     # this allows an exception to be raised within
    199     # the moderated greenlet so that it can continue
    200     # its expected flow.
--> 201     result = context.throw(*sys.exc_info())
    202 else:
    203     result = context.switch(value)

File c:\Users\w322800\Documents\gh\bcsb-prod\.venv\Lib\site-packages\sqlalchemy\engine\base.py:1419, in Connection.execute(self, statement, parameters, execution_options)
   1417     raise exc.ObjectNotExecutableError(statement) from err
   1418 else:
-> 1419     return meth(
   1420         self,
   1421         distilled_parameters,
   1422         execution_options or NO_OPTIONS,
   1423     )

File c:\Users\w322800\Documents\gh\bcsb-prod\.venv\Lib\site-packages\sqlalchemy\sql\elements.py:526, in ClauseElement._execute_on_connection(self, connection, distilled_params, execution_options)
    524     if TYPE_CHECKING:
    525         assert isinstance(self, Executable)
--> 526     return connection._execute_clauseelement(
    527         self, distilled_params, execution_options
    528     )
    529 else:
    530     raise exc.ObjectNotExecutableError(self)

File c:\Users\w322800\Documents\gh\bcsb-prod\.venv\Lib\site-packages\sqlalchemy\engine\base.py:1641, in Connection._execute_clauseelement(self, elem, distilled_parameters, execution_options)
   1629 compiled_cache: Optional[CompiledCacheType] = execution_options.get(
   1630     "compiled_cache", self.engine._compiled_cache
   1631 )
   1633 compiled_sql, extracted_params, cache_hit = elem._compile_w_cache(
   1634     dialect=dialect,
   1635     compiled_cache=compiled_cache,
   (...)   1639     linting=self.dialect.compiler_linting | compiler.WARN_LINTING,
   1640 )
-> 1641 ret = self._execute_context(
   1642     dialect,
   1643     dialect.execution_ctx_cls._init_compiled,
   1644     compiled_sql,
   1645     distilled_parameters,
   1646     execution_options,
   1647     compiled_sql,
   1648     distilled_parameters,
   1649     elem,
   1650     extracted_params,
   1651     cache_hit=cache_hit,
   1652 )
   1653 if has_events:
   1654     self.dispatch.after_execute(
   1655         self,
   1656         elem,
   (...)   1660         ret,
   1661     )

File c:\Users\w322800\Documents\gh\bcsb-prod\.venv\Lib\site-packages\sqlalchemy\engine\base.py:1846, in Connection._execute_context(self, dialect, constructor, statement, parameters, execution_options, *args, **kw)
   1844     return self._exec_insertmany_context(dialect, context)
   1845 else:
-> 1846     return self._exec_single_context(
   1847         dialect, context, statement, parameters
   1848     )

File c:\Users\w322800\Documents\gh\bcsb-prod\.venv\Lib\site-packages\sqlalchemy\engine\base.py:1986, in Connection._exec_single_context(self, dialect, context, statement, parameters)
   1983     result = context._setup_result_proxy()
   1985 except BaseException as e:
-> 1986     self._handle_dbapi_exception(
   1987         e, str_statement, effective_parameters, cursor, context
   1988     )
   1990 return result

File c:\Users\w322800\Documents\gh\bcsb-prod\.venv\Lib\site-packages\sqlalchemy\engine\base.py:2355, in Connection._handle_dbapi_exception(self, e, statement, parameters, cursor, context, is_sub_exec)
   2353 elif should_wrap:
   2354     assert sqlalchemy_exception is not None
-> 2355     raise sqlalchemy_exception.with_traceback(exc_info[2]) from e
   2356 else:
   2357     assert exc_info[1] is not None

File c:\Users\w322800\Documents\gh\bcsb-prod\.venv\Lib\site-packages\sqlalchemy\engine\base.py:1967, in Connection._exec_single_context(self, dialect, context, statement, parameters)
   1965                 break
   1966     if not evt_handled:
-> 1967         self.dialect.do_execute(
   1968             cursor, str_statement, effective_parameters, context
   1969         )
   1971 if self._has_events or self.engine._has_events:
   1972     self.dispatch.after_cursor_execute(
   1973         self,
   1974         cursor,
   (...)   1978         context.executemany,
   1979     )

File c:\Users\w322800\Documents\gh\bcsb-prod\.venv\Lib\site-packages\sqlalchemy\engine\default.py:951, in DefaultDialect.do_execute(self, cursor, statement, parameters, context)
    950 def do_execute(self, cursor, statement, parameters, context=None):
--> 951     cursor.execute(statement, parameters)

File c:\Users\w322800\Documents\gh\bcsb-prod\.venv\Lib\site-packages\sqlalchemy\connectors\asyncio.py:192, in AsyncAdapt_dbapi_cursor.execute(self, operation, parameters)
    190     return self.await_(self._execute_async(operation, parameters))
    191 except Exception as error:
--> 192     self._adapt_connection._handle_exception(error)

File c:\Users\w322800\Documents\gh\bcsb-prod\.venv\Lib\site-packages\sqlalchemy\connectors\asyncio.py:330, in AsyncAdapt_dbapi_connection._handle_exception(self, error)
    327 def _handle_exception(self, error: Exception) -> NoReturn:
    328     exc_info = sys.exc_info()
--> 330     raise error.with_traceback(exc_info[2])

File c:\Users\w322800\Documents\gh\bcsb-prod\.venv\Lib\site-packages\sqlalchemy\connectors\asyncio.py:190, in AsyncAdapt_dbapi_cursor.execute(self, operation, parameters)
    184 def execute(
    185     self,
    186     operation: Any,
    187     parameters: Optional[_DBAPISingleExecuteParams] = None,
    188 ) -> Any:
    189     try:
--> 190         return self.await_(self._execute_async(operation, parameters))
    191     except Exception as error:
    192         self._adapt_connection._handle_exception(error)

File c:\Users\w322800\Documents\gh\bcsb-prod\.venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py:132, in await_only(awaitable)
    123     raise exc.MissingGreenlet(
    124         "greenlet_spawn has not been called; can't call await_only() "
    125         "here. Was IO attempted in an unexpected place?"
    126     )
    128 # returns the control to the driver greenlet passing it
    129 # a coroutine to run. Once the awaitable is done, the driver greenlet
    130 # switches back to this greenlet with the result of awaitable that is
    131 # then returned to the caller (or raised as error)
--> 132 return current.parent.switch(awaitable)

File c:\Users\w322800\Documents\gh\bcsb-prod\.venv\Lib\site-packages\sqlalchemy\util\_concurrency_py3k.py:196, in greenlet_spawn(fn, _require_await, *args, **kwargs)
    192 switch_occurred = True
    193 try:
    194     # wait for a coroutine from await_only and then return its
    195     # result back to it.
--> 196     value = await result
    197 except BaseException:
    198     # this allows an exception to be raised within
    199     # the moderated greenlet so that it can continue
    200     # its expected flow.
    201     result = context.throw(*sys.exc_info())

File c:\Users\w322800\Documents\gh\bcsb-prod\.venv\Lib\site-packages\sqlalchemy\dialects\oracle\oracledb.py:771, in AsyncAdapt_oracledb_cursor._execute_async(self, operation, parameters)
    769     result = await self._cursor.execute(operation)
    770 else:
--> 771     result = await self._cursor.execute(operation, parameters)
    773 if self._cursor.description and not self.server_side:
    774     self._rows = collections.deque(await self._cursor.fetchall())

File c:\Users\w322800\Documents\gh\bcsb-prod\.venv\Lib\site-packages\oracledb\cursor.py:984, in AsyncCursor.execute(self, statement, parameters, suspend_on_success, **keyword_parameters)
    982 self._prepare_for_execute(statement, parameters, keyword_parameters)
    983 self._impl.suspend_on_success = suspend_on_success
--> 984 await self._impl.execute(self)

File src/oracledb/impl/thin/cursor.pyx:390, in execute()

File src/oracledb/impl/thin/protocol.pyx:855, in _process_single_message()

File src/oracledb/impl/thin/protocol.pyx:856, in oracledb.thin_impl.BaseAsyncProtocol._process_single_message()

File src/oracledb/impl/thin/protocol.pyx:832, in _process_message()

File src/oracledb/impl/thin/messages/base.pyx:102, in oracledb.thin_impl.Message._check_and_raise_exception()

DatabaseError: (oracledb.exceptions.DatabaseError) ORA-01861: literal does not match format string
Help: https://docs.oracle.com/error-help/db/ora-01861/
[SQL: 
    SELECT
        a.EFFDATE,
        a.ACCTNBR,
        a.OWNERSORTNAME,
        a.PRODUCT,
        a.NOTEOPENAMT,
        a.RATETYPCD,
        a.MJACCTTYPCD,
        a.CURRMIACCTTYPCD,
        a.CURRACCTSTATCD,
        a.NOTEINTRATE,
        a.BOOKBALANCE,
        a.NOTEBAL,
        a.CONTRACTDATE,
        a.DATEMAT,
        a.CLOSEDATE,
        a.TAXRPTFORORGNBR,
        a.TAXRPTFORPERSNBR,
        a.LOANOFFICER,
        a.ACCTOFFICER
    FROM
        COCCDM.WH_ACCTCOMMON a
    WHERE
        (a.CONTRACTDATE >= TO_DATE('2020-01-01 00:00:00''YYYY-MM-DD HH24:MI:SS')) AND
        (a.EFFDATE = TO_DATE('2025-08-25 00:00:00', 'YYYY-MM-DD HH24:MI:SS'))
    ]
(Background on this error at: https://sqlalche.me/e/20/4xp6)

----

Required fields: 
Provide the required fields names or description.	Please segregate each year’s data to a separate tab on the Excel workbook and include the following:  Application ID, Account Number, Loan Origination Date, Applicant Last Name, Applicant First Name, Co-Applicant Last Name, Co-Applicant First Name, Applicant Credit Score, Co-Applicant Credit Score, Model Year, Vehicle Mileage, Dealer Name, Amount Financed, Current Balance, Contract Rate, Buy Rate, Loan Paid or Open, and Date Closed when applicable. 


Excellent. This is a very common requirement—moving from a summary report to a detailed, multi-tab breakdown for end-users. The iterative approach will work perfectly for this.

Your existing function `query_df_on_date()` is the key. We will use it to build a complete dataset of all loan originations within the 2020-2024 period, apply your specific filter criteria, and then format the output exactly as requested.

Here is the updated and detailed plan.

### High-Level Strategy

The plan remains the same at its core but is adapted for the new output requirements:

1.  **Iterate by Month:** We will loop from Jan 2020 to Dec 2024, calling your `query_df_on_date()` function for the last business day of each month.
2.  **Collect Originations:** From each monthly snapshot, we'll collect only the loans originated *within that specific month*.
3.  **Combine & Deduplicate:** All collected monthly originations will be merged into a single, master DataFrame. We'll drop duplicates on `acctnbr` as a safeguard.
4.  **Apply Complex Filter:** We will apply your specified filter: `Category == 'Indirect'` OR `currmiaccttypcd` is in `['CM15', 'CM16']`.
5.  **Prepare and Format:** We'll select, rename, and create columns to match the required field list.
6.  **Export to Multi-Tab Excel:** The final, filtered DataFrame will be split by year, with each year's data written to a separate tab in a single Excel file.

---

### Step-by-Step Implementation

This entire script can be placed in a new file, for example, `create_indirect_loan_report.py`.

#### Step 1: Setup and Date Generation

First, import the necessary libraries and your `query_df_on_date` function. Then, generate the list of monthly dates to iterate over.

```python
import pandas as pd
from datetime import datetime

# Import your existing, trusted function from your project structure
from account_data_adhoc.core import query_df_on_date, get_last_business_day

print("Starting indirect loan report generation...")

# Define the overall date range for the report
start_date = datetime(2020, 1, 1)
end_date = datetime(2024, 12, 31)

# Generate a list of all month-end dates to use for our snapshots
snapshot_dates = pd.date_range(start=start_date, end=end_date, freq='M')

print(f"Generated {len(snapshot_dates)} monthly snapshot dates to process.")
```

#### Step 2: Iteratively Query and Collect Monthly Originations

Loop through the snapshot dates. In each iteration, call your pipeline, and then isolate the loans that were newly originated in that month.

```python
monthly_originations_dfs = []

print("Collecting loan originations month by month...")

for month_end_date in snapshot_dates:
    print(f"--- Processing snapshot for {month_end_date.strftime('%Y-%m')} ---")
    
    # Get a valid business day snapshot date using your existing utility
    snapshot_business_date = datetime.strptime(get_last_business_day(month_end_date), '%Y-%m-%d %H:%M:%S')
    
    # Call your function to get the full, cleaned dataframe for that date
    df_snapshot = query_df_on_date(specified_date=snapshot_business_date)
    
    if df_snapshot.empty:
      print("Snapshot returned empty dataframe, skipping.")
      continue
      
    # Ensure contractdate is a datetime object for comparison
    df_snapshot['contractdate'] = pd.to_datetime(df_snapshot['contractdate'])
    
    # Filter the snapshot to find only loans originated IN THAT SPECIFIC MONTH
    df_month_originations = df_snapshot[
        (df_snapshot['contractdate'].dt.year == month_end_date.year) &
        (df_snapshot['contractdate'].dt.month == month_end_date.month)
    ].copy()
    
    if not df_month_originations.empty:
        print(f"Found {len(df_month_originations)} loans originated in {month_end_date.strftime('%Y-%m')}.")
        monthly_originations_dfs.append(df_month_originations)

print("\nFinished collecting all monthly data.")
```

#### Step 3: Combine, Deduplicate, and Apply Final Filter

Concatenate the list of DataFrames into one, remove any potential duplicates, and then apply your specific business logic to get the final set of indirect loans.

```python
if not monthly_originations_dfs:
    print("No loan originations found in the entire date range. Exiting.")
else:
    # Combine all monthly dataframes into a single master list
    all_originations_df = pd.concat(monthly_originations_dfs, ignore_index=True)

    # Safeguard: Drop duplicates based on the unique account number
    unique_originations_df = all_originations_df.drop_duplicates(subset=['acctnbr'], keep='first')
    print(f"\nTotal unique loans originated (2020-2024): {len(unique_originations_df)}")

    # Apply the required business rule filter
    indirect_loans_df = unique_originations_df[
        (unique_originations_df['Category'] == 'Indirect') |
        (unique_originations_df['currmiaccttypcd'].isin(['CM15', 'CM16']))
    ].copy()

    print(f"Found {len(indirect_loans_df)} unique 'Indirect' loans after filtering.")
```

#### Step 4: Prepare Data for Export (Map and Format)

This is a critical new step. We will create new columns and rename existing ones to match the report specifications.

```python
if not indirect_loans_df.empty:
    print("Preparing final data for export...")

    # 1. Derive the 'Loan Paid or Open' status
    indirect_loans_df['Loan Status'] = 'Open'
    indirect_loans_df.loc[indirect_loans_df['curracctstatcd'] == 'CLOSE', 'Loan Status'] = 'Paid' # Adjust 'CLOSE' if status code is different

    # 2. Add 'contract_year' for splitting into tabs
    indirect_loans_df['contract_year'] = indirect_loans_df['contractdate'].dt.year

    # 3. Define the final column structure and rename
    #    (Placeholders are used for fields not in your repomix's SQL queries)
    final_columns_map = {
        'acctnbr': 'Account Number',
        'contractdate': 'Loan Origination Date',
        'ownersortname': 'Applicant Last Name', # Needs splitting
        # Placeholder columns
        'Applicant First Name': 'N/A',
        'Co-Applicant Last Name': 'N/A',
        'Co-Applicant First Name': 'N/A',
        'Applicant Credit Score': 'N/A',
        'Co-Applicant Credit Score': 'N/A',
        'Model Year': 'N/A',
        'Vehicle Mileage': 'N/A',
        'Dealer Name': 'N/A',
        'Buy Rate': 'N/A',
        # Mapped columns
        'noteopenamt': 'Amount Financed',
        'notebal': 'Current Balance',
        'noteintrate': 'Contract Rate',
        'Loan Status': 'Loan Paid or Open',
        'closedate': 'Date Closed'
    }
    
    # Create placeholder columns so the rename works
    for new_col in final_columns_map.values():
      if new_col not in indirect_loans_df.columns and new_col not in indirect_loans_df.rename(columns=final_columns_map).columns:
          indirect_loans_df[new_col] = 'N/A'
          
    # TODO: Split 'ownersortname' into First and Last names
    # For now, we are just renaming it. You'll need to parse this field.
    
    # Select and rename columns
    report_df = indirect_loans_df.rename(columns=final_columns_map)
    final_report_df = report_df[list(final_columns_map.values())]

```

#### Step 5: Export to Multi-Tab Excel Workbook

Use `pandas.ExcelWriter` to create a single workbook and loop through each year, writing the corresponding data to a new sheet.

```python
    output_filename = 'indirect_loan_report_by_year_2020-2024.xlsx'
    
    with pd.ExcelWriter(output_filename, engine='xlsxwriter') as writer:
        print(f"\nWriting data to {output_filename}...")
        
        # Get the unique years from the data, sorted
        years_to_export = sorted(final_report_df['contract_year'].unique())
        
        for year in years_to_export:
            sheet_name = str(year)
            print(f" - Writing tab: {sheet_name}")
            
            df_year = final_report_df[final_report_df['contract_year'] == year].copy()
            
            # Drop the helper 'contract_year' column before exporting
            df_year.drop(columns=['contract_year'], inplace=True)
            
            df_year.to_excel(writer, sheet_name=sheet_name, index=False)

    print("\nReport generation complete.")

```

### Data Mapping and Missing Fields

**This is important.** Your request includes several fields that are not present in the SQL queries within your `account_data_adhoc/fetch_data.py` file. I have used placeholders in the code above. To get the real data, **you will need to update your SQL queries** to include these fields.

| Required Field | Source Column / Derivation | Action Required |
| :--- | :--- | :--- |
| Application ID | N/A | User stated not required. |
| Account Number | `acctnbr` | **Done.** |
| Loan Origination Date| `contractdate` | **Done.** |
| Applicant Last/First Name | `ownersortname` | **Action Needed:** This field needs to be split into first and last names. |
| Co-Applicant Last/First Name | Not in SQL | **Action Needed:** Must add co-applicant name fields to the query. |
| Applicant Credit Score | Not in SQL | **Action Needed:** Must add credit score field(s) to the query. |
| Co-Applicant Credit Score | Not in SQL | **Action Needed:** Must add co-applicant credit score field to the query. |
| Model Year | Not in SQL | **Action Needed:** Must add model year to the query (likely from a collateral table). |
| Vehicle Mileage | Not in SQL | **Action Needed:** Must add mileage to the query (likely from a collateral table). |
| Dealer Name | Not in SQL | **Action Needed:** Must add dealer name to the query (a critical indirect lending field). |
| Amount Financed | `noteopenamt` | **Done.** |
| Current Balance | `notebal` | **Done.** |
| Contract Rate | `noteintrate` | **Done.** |
| Buy Rate | Not in SQL | **Action Needed:** Must add dealer buy rate to the query. |
| Loan Paid or Open | Derived from `curracctstatcd` | **Done.** |
| Date Closed | `closedate` | **Done.** |


----



# %%
import pandas as pd
from pathlib import Path

# %%
INPUT_PATH = Path(r"C:\Users\w322800\Documents\gh\bcsb-prod\Reports\Indirect Lending\Adhoc_Pricing_Disparity_20250822\output\output.parquet")

# %%
df = pd.read_parquet(INPUT_PATH)

# %%
df

# %%
from deltalake import DeltaTable

# %%
ACCOUNT_DATA = Path(r"C:\Users\w322800\Documents\lakehouse\silver\account")

# %%
active_accounts = DeltaTable(ACCOUNT_DATA).to_pandas()

# %%
active_accounts

# %%
active_accounts = active_accounts[(active_accounts['Category'].isin(['Indirect'])) | (active_accounts['currmiaccttypcd']).isin(['CM15','CM16'])].copy()

# %%
df.info()

# %%
active_accounts_slice = active_accounts[[
    'acctnbr',
    'ownersortname',
    'contractdate',
    'curracctstatcd',
    'noteopenamt',
    'notebal',
    'noteintrate'
]].copy()

# %%
active_accounts_slice = active_accounts_slice.rename(columns={
    'acctnbr': 'Account Number',
    'contractdate': 'Loan Origination Date',
    'ownersortname': 'Applicant Last Name', # Needs splitting
    'noteopenamt': 'Amount Financed',
    'notebal': 'Current Balance',
    'noteintrate': 'Contract Rate',
}).copy()

# %%
active_accounts_slice.info()

# %%
merged_df = pd.merge(df, active_accounts_slice, on='Account Number', how='outer', suffixes=('_df','_active'), indicator=True)

# %%
merged_df

# %%
merged_df.info()

# %%
import numpy as np

# %%
merged_df['Status'] = np.where(merged_df['_merge'] == 'left_only', 'Closed/Charged Off','Active')

# %%


# %%




----

```python
# %%
import numpy as np

# Your Status column is perfect. It correctly identifies loans present
# in the active_accounts table as 'Active'.
merged_df['Status'] = np.where(merged_df['_merge'] == 'left_only', 'Closed/Charged Off','Active')

# %%
# Define the base names of the columns that were duplicated during the merge
cols_to_consolidate = [
    'Loan Origination Date',
    'Applicant Last Name',
    'Amount Financed',
    'Current Balance',
    'Contract Rate'
]

# Consolidate the columns using combine_first
# This method is ideal for this scenario. It takes values from the first
# DataFrame (`_active` columns) and fills any missing (NaN) values with
# data from the second DataFrame (`_df` columns).
# This perfectly matches your logic: "If it's active, use the active data...
# otherwise it should be the left dataframe."
for col in cols_to_consolidate:
    active_col = f'{col}_active'
    df_col = f'{col}_df'
    merged_df[col] = merged_df[active_col].combine_first(merged_df[df_col])

# %%
# Create a list of the original suffixed columns to drop, plus the merge indicator
cols_to_drop = [f'{col}_{suffix}' for col in cols_to_consolidate for suffix in ['df', 'active']]
cols_to_drop.append('_merge')

# Create the final, clean DataFrame
final_df = merged_df.drop(columns=cols_to_drop)


# %%
# As you noted, the 'Applicant Last Name' came from 'ownersortname'
# and may need to be split if the format is 'LAST, FIRST'.
final_df['Applicant Last Name'] = final_df['Applicant Last Name'].str.split(',').str[0].str.strip()

# %%
# final_df is now your fully consolidated DataFrame
final_df.info()

# %%
# Verify the status distribution
print("\nLoan Status Counts:")
print(final_df['Status'].value_counts())

# %%
# Display the head of the final DataFrame
final_df
```

---

Understood. That is a very common restriction in production environments. You have read-only access and need a single, executable SQL query that can handle a list of inputs larger than Oracle's 1000-item limit for an `IN` clause.

The standard and most reliable way to solve this is to programmatically generate a single SQL query that breaks your large list of account numbers into multiple smaller `IN` clauses chained together with `OR`.

Here is the complete process.

### The Strategy: "Chunking" with `OR IN`

We will use Python to take your long list of account numbers and build a `WHERE` clause that looks like this:

```sql
WHERE
(
  ACCTNBR IN (1, 2, ..., 999)
  OR ACCTNBR IN (1000, 1001, ..., 1998)
  OR ACCTNBR IN (1999, 2000, ..., 2997)
  -- and so on...
)
```

This is valid SQL, bypasses the 1000-item limit, and requires no special database permissions.

### Step 1: Python Code to Generate the Oracle SQL

This script will take your `final_df`, generate the dynamic `WHERE` clause, and then embed it into the full Oracle query.

```python
# %%
# --- 1. PREPARE THE ACCOUNT NUMBERS ---
# Get a list of unique account numbers from your DataFrame
account_list = final_df['Account Number'].unique().tolist()

# Define the chunk size (must be <= 1000, 999 is safe)
chunk_size = 999

# %%
# --- 2. BUILD THE DYNAMIC "OR IN" CLAUSE ---

# Check if there are any accounts to even query
if not account_list:
    where_clause = "1 = 2" # A condition that is always false
else:
    # This list will hold each "ACCTNBR IN (...)" string
    in_clauses = []
    
    for i in range(0, len(account_list), chunk_size):
        # Get a slice of the list
        chunk = account_list[i:i + chunk_size]
        
        # Format the chunk into a comma-separated string of numbers
        # (Assuming account numbers do not need string quotes)
        chunk_str = ', '.join(map(str, chunk))
        
        # Create the IN clause for this chunk
        in_clauses.append(f"ACCTNBR IN ({chunk_str})")
    
    # Join all the individual IN clauses together with "OR"
    where_clause = " OR ".join(in_clauses)


# %%
# --- 3. CONSTRUCT THE FULL ORACLE SQL QUERY ---
# This is the same core logic as before, but we are inserting our dynamic WHERE clause.

# Remember to replace YOUR_SCHEMA and ACCT_DATE!
oracle_sql_query = f"""
WITH RankedRecords AS (
    SELECT
        ACCTNBR,
        TAXRPTFORORGNBR,
        TAXRPTFORPERSNBR,
        NOTEINTRATE,
        
        ROW_NUMBER() OVER (PARTITION BY ACCTNBR ORDER BY ACCT_DATE ASC) as RN
        -- ==> IMPORTANT: Replace ACCT_DATE with your daily snapshot date column!
        
    FROM
        YOUR_SCHEMA.WH_ACCTCOMMON -- ==> IMPORTANT: Replace with your schema!
    WHERE
        -- The dynamically generated clause is inserted here
        ({where_clause})
)
SELECT
    ACCTNBR AS "Account Number",
    TAXRPTFORORGNBR,
    TAXRPTFORPERSNBR,
    NOTEINTRATE AS "First Recorded Rate"
FROM
    RankedRecords
WHERE
    RN = 1
"""

# (Optional) You can print the first 500 characters to see what it looks like
# print(oracle_sql_query[:500])

```

### Step 2: Python Code to Execute the Query and Merge

Now you can pass this long `oracle_sql_query` string directly to pandas to execute against your Oracle database.

```python
# %%
# --- 4. EXECUTE THE QUERY AND MERGE THE RESULTS ---

from sqlalchemy import create_engine, text
import pandas as pd

# Establish database connection (replace with your credentials)
db_connection_str = 'oracle+oracledb://USER:PASSWORD@YOUR_HOST:1521/?service_name=YOUR_SERVICE_NAME'
engine = create_engine(db_connection_str)

print("Executing dynamically generated query against Oracle...")

# Use pandas to execute the query and load results directly into a DataFrame
# This may take some time depending on the size of the list and table
enrichment_df = pd.read_sql_query(text(oracle_sql_query), con=engine)

print(f"Successfully fetched enrichment data for {len(enrichment_df)} accounts.")


# %%
# --- 5. MERGE THE ENRICHMENT DATA ---
# This remains the same.
final_df = pd.merge(
    final_df,
    enrichment_df,
    on='Account Number',
    how='left'
)

# %%
final_df.info()
final_df.head()
```

This approach gives you exactly what you asked for: a single, plain SQL query that works within standard Oracle limitations and read-only permissions.

---

import cdutils.database.connect # type: ignore
from sqlalchemy import text # type: ignore
from typing import Optional
from datetime import datetime, timedelta
import pandas as pd

def fetch_data(specified_date: Optional[datetime] = None):
    """
    Main data query
    """
    oracle_sql_query = f"""
    WITH RankedRecords AS (
        SELECT
            ACCTNBR,
            TAXRPTFORORGNBR,
            TAXRPTFORPERSNBR,
            NOTEINTRATE,
            
            ROW_NUMBER() OVER (PARTITION BY ACCTNBR ORDER BY CONTRACTDATE ASC) as RN
            
        FROM
            COCCDM.WH_ACCTCOMMON 
        WHERE
            -- The dynamically generated clause is inserted here
            ({where_clause})
    )
    SELECT
        ACCTNBR AS "Account Number",
        TAXRPTFORORGNBR,
        TAXRPTFORPERSNBR,
        NOTEINTRATE AS "First Recorded Rate"
    FROM
        RankedRecords
    WHERE
        RN = 1
    """

    queries = [
        {'key':'oracle_sql_query', 'sql':oracle_sql_query, 'engine':2},
    ]


    data = cdutils.database.connect.retrieve_data(queries)
    return data

Error:
{
	"name": "ObjectNotExecutableError",
	"message": "Not an executable object: '\\n    WITH RankedRecords AS (\\n        SELECT\\n            ACCTNBR,\\n            TAXRPTFORORGNBR,\\n            TAXRPTFORPERSNBR,\\n            NOTEINTRATE,\\n\\n            ROW_NUMBER() OVER (PARTITION BY ACCTNBR ORDER BY CONTRACTDATE ASC) as RN\\n\\n        FROM\\n            COCCDM.WH_ACCTCOMMON \\n        WHERE\\n            -- The dynamically generated clause is inserted here\\n            (ACCTNBR IN (105936204, 123456789, 15008086, 150101081, 1501589269, 15024334, 150323332, 150416892, 150416917, 150417668, 150417684, 150417725, 150417791, 150417866, 150417882, 150417957, 150418046, 150418369, 150418385, 150418400, 150418426, 150418484, 150418575, 150418608, 150418616, 150418624, 150418632, 150418658, 150418955, 150418963, 150418989, 150419044, 150419119, 150419135, 150419143, 150419169, 150419193, 150419200, 150419234, 150419317, 150419325, 150419341, 150419367, 150419383, 150419482, 150419490, 150419507, 150419515, 150419523, 150419549, 150419599, 150419606, 150419945, 150419961, 150419979, 150419987, 150420009, 150420017, 150420025, 150420041, 150420059, 150420067, 150420083, 150420570, 150420603, 150420637, 150420653, 150420679, 150420695, 150420728, 150420736, 150420744, 150420752, 150420778, 150420786, 150420794, 150420801, 150420819, 150420835, 150420843, 150420877, 150420900, 150420926, 150420934, 150420950, 150420976, 150420992, 150421015, 150421164, 150421213, 150421239, 150421271, 150421354, 150421388, 150421396, 150421403, 150421411, 150421429, 150421445, 150421461, 150421479, 150421495, 150421502, 150421669, 150421677, 150421693, 150421726, 150421742, 150421750, 150421768, 150421776, 150421784, 150421792, 150421809, 150421825, 150421833, 150421841, 150421867, 150421875, 150421883, 150421891, 150421908, 150421916, 150421932, 150421940, 150421958, 150421966, 150421974, 150422104, 150422112, 150422138, 150422146, 150422154, 150422162, 150422170, 150422188, 150422237, 150422245, 150422253, 150422261, 150422279, 150422287, 150422302, 150422310, 150422328, 150422336, 150422576, 150422617, 150422625, 150422641, 150422691, 150422708, 150422724, 150422758, 150422763, 150422774, 150423277, 150423293, 150423300, 150423318, 150423342, 150423368, 150423376, 150423392, 150423409, 150423425, 150423441, 150423475, 150423483, 150423491, 150423508, 150423524, 150423532, 150423540, 150423566, 150423574, 150423582, 150423590, 150423607, 150423615, 150423649, 150423673, 150423681, 150423699, 150423714, 150423722, 150423730, 150423756, 150423772, 150423780, 150423798, 150423805, 150423847, 150423889, 150423897, 150423904, 150424077, 150424085, 150424126, 150424134, 150424142, 150424150, 150424168, 150424176, 150424184, 150424192, 150424209, 150424225, 150424241, 150424259, 150424267, 150424283, 150424308, 150424324, 150424340, 150424358, 150424366, 150424374, 150424382, 150424390, 150424449, 150424457, 150424465, 150424473, 150424663, 150424689, 150424712, 150424738, 150424754, 150424762, 150424796, 150424803, 150424829, 150424837, 150424861, 150424887, 150425075, 150425108, 150425116, 150425124, 150425132, 150425158, 150425166, 150425182, 150425190, 150425207, 150425223, 150425249, 150425398, 150425413, 150425702, 150425728, 150425744, 150425760, 150425786, 150425794, 150425801, 150425827, 150425835, 150425851, 150425885, 150425893, 150425900, 150425926, 150425934, 150425942, 150425950, 150425984, 150425992, 150426099, 150426156, 150426164, 150426172, 150426180, 150426205, 150426239, 150426255, 150426263, 150426271, 150426297, 150426312, 150426320, 150426411, 150426429, 150426479, 150426502, 150426510, 150426578, 150426586, 150426601, 150426627, 150426635, 150426643, 150426651, 150426677, 150426693, 150426700, 150426718, 150426726, 150426734, 150426768, 150426776, 150426784, 150426833, 150426841, 150426867, 150426940, 150426958, 150426982, 150427005, 150427021, 150427039, 150427047, 150427146, 150427154, 150427162, 150427170, 150427196, 150427203, 150427211, 150427229, 150427245, 150427253, 150427261, 150427287, 150427295, 150427302, 150427542, 150427550, 150427609, 150427633, 150427641, 150427659, 150427667, 150427691, 150427774, 150428227, 150428285, 150428300, 150428665, 150428772, 150428855, 150428863, 150428897, 150428912, 150428920, 150428938, 150428970, 150428996, 150429233, 150429241, 150429316, 150429366, 150429382, 150429431, 150429449, 150429465, 150429506, 150429514, 150429522, 150429762, 150429788, 150429803, 150429811, 150429853, 150429879, 150429887, 150429895, 150429944, 150429978, 150429986, 150430206, 150430256, 150430264, 150430272, 150430313, 150430347, 150430371, 150430389, 150430397, 150430404, 150430412, 150430438, 150430941, 150430959, 150430983, 150431006, 150431048, 150431056, 150431064, 150431072, 150431105, 150431189, 150431254, 150431270, 150431311, 150431329, 150431345, 150431387, 150431402, 150431410, 150431444, 150431452, 150431460, 150431478, 150431486, 150431494, 150431501, 150431519, 150431527, 150431543, 150431577, 150431600, 150431618, 150431634, 150431642, 150431650, 150431684, 150431858, 150431882, 150431915, 150431957, 150432038, 150432046, 150432054, 150432062, 150432070, 150432088, 150432103, 150432111, 150432129, 150432137, 150432153, 150432228, 150432244, 150432377, 150432385, 150432418, 150432426, 150432442, 150432450, 150432476, 150432492, 150432509, 150432517, 150432525, 150432533, 150432541, 150432567, 150432575, 150432624, 150432632, 150432640, 150432658, 150432674, 150432848, 150432856, 150432880, 150432898, 150432939, 150432955, 150432963, 150432971, 15043299, 150432997, 150433036, 150433052, 150433060, 150433078, 150433416, 150433424, 150433466, 150433482, 150433531, 150433557, 150433565, 150433573, 150433581, 150433599, 150433606, 150433614, 150433622, 150433656, 150433664, 150433672, 150433680, 150433698, 150433705, 150433713, 150433747, 150433755, 150433763, 150433789, 150433797, 150433804, 150433812, 150433846, 150433862, 150433870, 150433888, 150433896, 150433903, 150433911, 150433929, 150433937, 150433945, 150433953, 150433961, 150433979, 150433987, 150433995, 150434000, 150434018, 150434026, 150434034, 150434042, 150434050, 150434141, 150434159, 150434167, 150434191, 150434208, 150434224, 150434232, 150434240, 150434266, 150434282, 150434290, 150434323, 150434331, 150434414, 150434448, 150434498, 150434505, 150434513, 150434521, 150434539, 150434547, 150434555, 150434597, 150434604, 150434612, 150434646, 150434779, 150434787, 150434795, 150434802, 150434810, 150434828, 150434836, 150434844, 150434886, 150434943, 150434951, 150434969, 150434985, 150435008, 150435016, 150435024, 150435040, 150435058, 150435066, 150435074, 150435082, 150435107, 150435115, 150435131, 150435149, 150435181, 150435199, 150435206, 150435420, 150435438, 150435462, 150435545, 150435553, 150435561, 150435587, 150435595, 150435602, 150435610, 150435628, 150435644, 150435678, 150435777, 150435785, 150436147, 150436155, 150436163, 150436220, 150436246, 150436254, 150436288, 150436296, 150436303, 150436311, 150436329, 150436345, 150436353, 150436379, 150436395, 150436410, 150436444, 150436452, 150436486, 150436501, 150436527, 150436535, 150436551, 150436569, 150436577, 150436585, 150436642, 150436650, 150436741, 150436783, 150436791, 150436808, 150436816, 150436824, 150436832, 150436858, 150436882, 150436890, 150436907, 150436923, 150436931, 150436949, 150436965, 150436973, 150436981, 150436999, 150437012, 150437020, 150437038, 150437046, 150437054, 150437062, 150437070, 150437088, 150437096, 150437103, 150437111, 150437129, 150437145, 150437153, 150437161, 150437187, 150437195, 150437202, 150437228, 150437369, 150437377, 150437400, 150437418, 150437450, 150437468, 150437509, 150437517, 150437525, 150437533, 150437559, 150437567, 150437608, 150437640, 150437658, 150437674, 150437682, 150437690, 150437715, 150437848, 150437856, 150437872, 150437913, 150437939, 150437947, 150437971, 150437989, 150437997, 150438002, 150438036, 150438044, 150438060, 150438078, 150438094, 150438127, 150438143, 150438325, 150438333, 150438341, 150438367, 150438383, 150438432, 150438440, 150438490, 150438515, 150438523, 150438531, 150438549, 150438557, 150438565, 150438573, 150438606, 150438630, 150439042, 150439307, 150439464, 150439547, 150439563, 150439620, 150439886, 150440122, 150440156, 150440221, 150440271, 150440320, 150440338, 150440437, 150440445, 150440453, 150440487, 150440544, 150440685, 150440693, 150440784, 150440974, 150441005, 150441039, 150441047, 150441328, 150441344, 150441378, 150441427, 150441500, 150441518, 150441534, 150441550, 150441568, 150441576, 150441584, 150441641, 150441906, 150442011, 150442102, 150442136, 150442144, 150442152, 150442160, 150442186, 150442219, 150442235, 150442243, 150442277, 150442285, 150442300, 150442318, 150442342, 150442368, 150442392, 150442425, 150442433, 150442706, 150442714, 150442730, 150442805, 150442813, 150442839, 150442871, 150442904, 150442954, 150442988, 150443027, 150443077, 150443093, 150443118, 150443126, 150443134, 150443142, 150443150, 150443168, 150443316, 150443324, 150443332, 150443374, 150443382, 150443390, 150443431, 150443473, 150443481, 150443506, 150443514, 150443522, 150443548, 150443564, 150443572, 150443598, 150443605, 150443621, 150443639, 150443647, 150443671, 150443689, 150443704, 150443712, 150443720, 150443738, 150443845, 150443928, 150443936, 150443952, 150443978, 150444009, 150444025, 150444033, 150444041, 150444091, 150444108, 150444124, 150444140, 150444174, 150444182, 150444207, 150444215, 150444223, 150444372, 150444398, 150444405, 150444455, 150444463, 150444489, 150444497, 150444512, 150444520, 150444538, 150444546, 150444554, 150444570, 150444588, 150445073, 150445099, 150445114, 150445130, 150445148, 150445156, 150445180, 150445205, 150445239, 150445255, 150445271, 150445289, 150445304, 150445403, 150445411, 150445429, 150445437, 150445453, 150445502, 150445586, 150445619, 150445627, 150445635, 150445651, 150445669, 150445677, 150445685, 150445693, 150445700, 150445718, 150445734, 150445742, 150445750, 150445768, 150445776, 150445784, 150445792, 150445809, 150445817, 150445825, 150445841, 150445859, 150445867, 150445883, 150445891, 150446005, 150446047, 150446063, 150446071, 150446089, 150446097, 150446112, 150446120, 150446154, 150446162, 150446170, 150446188, 150446196, 150446203, 150446211, 150446229, 150446237, 150446245, 150446253, 150446261, 150446279, 150446302, 150446310, 150446534, 150446542, 150446609, 150446633, 150446659, 150446667, 150446683, 150446691, 150446716, 150446724, 150446740, 150446758, 150446774, 150446807, 150446815, 150446823, 150446831, 150446849, 150446857, 150446865, 150446873, 150446881, 150446914, 150447037, 150447045, 150447087, 150447110, 150447160, 150447186, 150447194, 150447201, 150447227, 150447235, 150447508, 150447524, 150447532, 150447540, 150447566, 150447590, 150447607, 150447615, 150447623, 150447649, 150447657, 150447665, 150447673, 150447699, 150447706, 150447714, 150447722, 150447730, 150447756, 150447772, 150447805, 150447813, 150447821, 150447863, 150447889, 150447920, 150447938, 150447954, 150447962, 150447970, 150447988, 150447996, 150448001, 150448027, 150448035, 150448043, 150448077, 150448085, 150448093, 150448100, 150448118, 150448126, 150448134, 150448142, 150448150, 150448168, 150448176, 150448184, 150448192, 150448209, 150448217, 150448225, 150448233, 150448308, 150448316, 150448324, 150448332, 150448382, 150448390, 150448415) OR ACCTNBR IN (150448431, 150448449, 150448457, 150448465, 150448530, 150448548, 150448564, 150448572, 150448580, 150448720, 150448738, 150448746, 150448803, 150448811, 150448910, 150448928, 150448936, 150448944, 150448952, 150448978, 150449017, 150449025, 150449116, 150449124, 150449132, 150449140, 150449190, 150449215, 150449231, 150449257, 150449299, 150449603, 150449687, 150449702, 150449819, 150449827, 150449835, 150449968, 150449976, 150450254, 150450262, 150450270, 150450288, 150450337, 150450361, 150450600, 150450626, 150450634, 150450650, 150450668, 150450684, 150450692, 150450709, 150450717, 150450733, 150450808, 150450882, 150450923, 150451054, 150451062, 150451145, 150451161, 150451898, 150451905, 150452276, 150452309, 150452317, 150452359, 150452367, 150452375, 150452383, 150452391, 150452416, 150452549, 150452630, 150452664, 150452705, 150452739, 150452747, 150452995, 150453018, 150453076, 150453084, 150453092, 150453175, 150453183, 150453779, 150453810, 150453886, 150454975, 150454983, 150455014, 150455022, 150455056, 150455080, 150455163, 150455238, 150455246, 150455254, 150455262, 150455759, 150455783, 150455858, 150455866, 150455931, 150455957, 150456012, 150456054, 150456062, 150456070, 150456088, 150456096, 150456103, 150456129, 150456137, 150456179, 150456723, 150456757, 150456814, 150456822, 150456848, 150456872, 150456913, 150456921, 150456939, 150457507, 150457557, 150457573, 150457581, 150457606, 150457622, 150457648, 150457664, 150457763, 150457789, 150457797, 150457804, 150458620, 150458638, 150458646, 150458654, 150458696, 150458711, 150458729, 150458828, 150460237, 150460245, 150460261, 150460295, 150460328, 150460360, 150460378, 150460394, 150460427, 150460435, 150460443, 150460451, 150460469, 150460881, 150460899, 150460906, 150460914, 150460922, 150460948, 150460956, 150460964, 150461003, 150461029, 150461459, 150461532, 150461540, 150461566, 150461574, 150461582, 150461631, 150461649, 150461920, 150462176, 150462184, 150462192, 150462233, 150462241, 150462275, 150462316, 150464260, 150464388, 150464445, 150464495, 150464510, 150465162, 150465336, 150465451, 150466110, 150466706, 150466821, 150466839, 150466996, 150467001, 150467019, 150467027, 150467217, 150467259, 150467291, 150467324, 150467770, 150467803, 150467837, 150467853, 150467887, 150467902, 150467910, 150468116, 150468140, 150468207, 150468215, 150468273, 150468356, 150468364, 150468380, 150468398, 150468570, 150468629, 150468645, 150468687, 150468695, 150468702, 150468728, 150468778, 150468786, 150468801, 150468819, 150468827, 150468835, 150469015, 150469023, 150469057, 150469289, 150469346, 150469453, 150469461, 150469479, 150469495, 150469510, 150469685, 150469768, 150469776, 150469809, 150469940, 150469958, 150469966, 150470020, 150470054, 150470062, 150470096, 150470103, 150470202, 150470244, 150470286, 150470400, 150470426, 150470442, 150470450, 150470476, 150470484, 150470492, 150470509, 150470517, 150470525, 150470533, 150470541, 150470559, 150470567, 150470731, 150470749, 150470757, 150470814, 150470830, 150470856, 150470880, 150470913, 150470939, 150470997, 150471002, 150471028, 150471086, 150471094, 150471101, 150471127, 150471218, 150471234, 150471391, 150471432, 150471482, 150471507, 150471515, 150471557, 150471565, 150471713, 150471721, 150471739, 150471747, 150471755, 150471812, 150471820, 150471846, 150472688, 150472696, 150472703, 150472737, 150472943, 150472951, 150473090, 150473280, 150473305, 150473701, 150473818, 150473909, 150474006, 150474056, 150474064, 150474080, 150474147, 150474238, 150474254, 150474288, 150474303, 150474345, 150474361, 150474569, 150474577, 150474600, 150474642, 150474650, 150474684, 150474717, 150474973, 150474981, 150475062, 150475286, 150475294, 150475335, 150475343, 150475559, 150475624, 150475632, 150475781, 150475814, 150475864, 150475872, 150475939, 150475955, 150476036, 150476086, 150476218, 150476383, 150476424, 150476440, 150476565, 150476713, 150476755, 150476771, 150477042, 150477068, 150477125, 150477167, 150477175, 150477480, 150477505, 150477521, 150477539, 150477555, 150477604, 150477620, 150477703, 150477729, 150477919, 150477993, 150478024, 150478032, 150478040, 150478363, 150478371, 150478389, 150478397, 150478438, 150478462, 150478470, 150478488, 150478496, 150478503, 150478537, 150478785, 150478834, 150478876, 150478884, 150478909, 150478925, 150478941, 150478967, 150479014, 150479197, 150479220, 150479303, 150479311, 150479329, 150479361, 150479395, 150479402, 150479410, 150479428, 150479436, 150479444, 150479478, 150479519, 150479866, 150479874, 150479965, 150479981, 150480277, 150480300, 150480392, 150480623, 150480631, 150480649, 150480657, 150480699, 150480722, 150480748, 150480855, 150480889, 150480904, 150480920, 150481019, 150481027, 150481069, 150481093, 150481100, 150481118, 150481291, 150481415, 150481423, 150481465, 150481473, 150481481, 150481499, 150481506, 150481762, 150481887, 150481910, 150481936, 150481960, 150481978, 150481986, 150482025, 150482033, 150482041, 150482067, 150482075, 150482299, 150482306, 150482322, 150482330, 150482356, 150482364, 150482405, 150482421, 150482439, 150482447, 150482455, 150482471, 150482653, 150482710, 150482728, 150482736, 150482752, 150482760, 150482786, 150482794, 150482801, 150482827, 150482877, 150482885, 150482893, 150482900, 150482918, 150482950, 150482968, 150482976, 150483388, 150483396, 150483403, 150483411, 150483437, 150483461, 150483487, 150483495, 150483502, 150483510, 150483528, 150483536, 150483544, 150483552, 150483601, 150483784, 150483825, 150483875, 150483883, 150483891, 150483908, 150483916, 150483924, 150483932, 150483940, 150483958, 150483966, 150483974, 150483982, 150484021, 150484063, 150484146, 150484211, 150484229, 150484253, 150484261, 150484287, 150484295, 150484302, 150484328, 150484336, 150484352, 150484401, 150484419, 150484443, 150484550, 150484568, 150484584, 150484617, 150484625, 150484633, 150484641, 150484659, 150484675, 150484708, 150484724, 150484732, 150484758, 150484766, 150484774, 150484790, 150484815, 150484831, 150484857, 150484865, 150484998, 150485003, 150485045, 150485079, 150485128, 150485152, 150485160, 150485186, 150485194, 150485201, 150485219, 150485227, 150485235, 150485243, 150485251, 150485574, 150485590, 150485657, 150485665, 150485673, 150485706, 150485722, 150485748, 150485756, 150485764, 150485772, 150485780, 150485798, 150485805, 150485813, 150485821, 150485839, 150485847, 150485855, 150485889, 150485904, 150488073, 150488081, 150488114, 150488130, 150488148, 150488156, 150488164, 150488205, 150488221, 150488239, 150488297, 150488453, 150488461, 150488502, 150488510, 150488536, 150488544, 150488552, 150488560, 150488578, 150488635, 150488643, 150488669, 150488677, 150488693, 150488700, 150488726, 150488742, 150488750, 150488768, 150488776, 150488784, 150488825, 150488833, 150488841, 150488974, 150488990, 150489005, 150489013, 150489071, 150489138, 150489146, 150489154, 150489162, 150489170, 150489196, 150489203, 150489211, 150489229, 150489237, 150489245, 150489261, 150489279, 150489287, 150489295, 150489542, 150489550, 150489568, 150489576, 150489592, 150489617, 150489633, 150489641, 150489675, 150489691, 150489708, 150489740, 150489766, 150490101, 150490143, 150490218, 150490234, 150490242, 150490250, 150490268, 150490276, 150490284, 150490317, 150490325, 150490359, 150490383, 150490507, 150490523, 150490549, 150490606, 150490622, 150490630, 150490648, 150490656, 150490664, 150490672, 150490680, 150490705, 150490721, 150490747, 150490755, 150490789, 150490797, 150490804, 150490820, 150490846, 150490862, 150490870, 150490888, 150490896, 150491042, 150491050, 150491068, 150491092, 150491117, 150491167, 150491191, 150491208, 150491224, 150491232, 150491240, 150491266, 150491331, 150491357, 150491381, 150491399, 150491414, 150491422, 150491430, 150491456, 150491711, 150491745, 150491787, 150491795, 150491810, 150491828, 150491836, 150491844, 150491852, 150491886, 150491927, 150492024, 150492074, 150492131, 150492149, 150492157, 150492165, 150492173, 150492181, 150492199, 150492206, 150492214, 150492222, 150492264, 150492280, 150492305, 150492371, 150492850, 150493163, 150493197, 150493246, 150493262, 150493361, 150493410, 150493436, 150493444, 150493494, 150493634, 150493668, 150493676, 150493816, 150493832, 150493840, 150493858, 150493874, 150493907, 150493923, 150493931, 150493957, 150494054, 150494070, 150494103, 150494111, 150494137, 150494145, 150494244, 150494278, 150494286, 150494335, 150494385, 150494393, 150494400, 150494418, 150494450, 150494476, 150494484, 150494640, 150494898, 150494905, 150494913, 150494939, 150494947, 150495060, 150495078, 150495094, 150495119, 150495143, 150495177, 150495193, 150495218, 150495284, 150495664, 150495680, 150495698, 150495705, 150495713, 150495721, 150495747, 150495755, 150495797, 150495804, 150495812, 150495838, 150495937, 150496068, 150496076, 150496084, 150496159, 150496191, 150496208, 150496216, 150496224, 150496232, 150496240, 150496258, 150496274, 150496290, 150496307, 150496331, 150496357, 150496498, 150496505, 150496513, 150496521, 150496555, 150496612, 150496620, 150496654, 150496688, 150496703, 150496711, 150496737, 150496753, 150496761, 150496787, 150496802, 150496828, 150496844, 150496878, 150496919, 150496935, 150496943, 150496951, 150496977, 150496985, 150497008, 150497016, 150497074, 150497115, 150497131, 150497181, 150497214, 150497222, 150497230, 150497264, 150497339, 150497355, 150497404, 150497412, 150497545, 150497587, 150497735, 150497743, 150497777, 150497785, 150497793, 150497800, 150497818, 150497826, 150497834, 150497850, 150497868, 150497876, 150497884, 150497892, 150497933, 150498311, 150498329, 150498337, 150498345, 150498387, 150498395, 150498402, 150498452, 150498478, 150498501, 150498519, 150498527, 150498535, 150498543, 150498551, 150498577, 150498600, 150498816, 150498824, 150498840, 150498858, 150498866, 150498874, 150498915, 150498923, 150498949, 150498957, 150498965, 150498973, 150498981, 150499012, 150499020, 150499038, 150499070, 150499161, 150499195, 150499210, 150499236, 150499286, 150499294, 150499301, 150499319, 150499327, 150499335, 150499351, 150499377, 150499385, 150499393, 150499400, 150499426, 150499442, 150499575, 150499658, 150499674, 150499715, 150499723, 150499749, 150499757, 150499765, 150499773, 150499781, 150499799, 150499806, 150499814, 150499822, 150499989, 150500025, 150500033, 150500041, 150500059, 150500091, 150500174, 150500223, 150500231, 150500249, 150500257, 150500265, 150500273, 150500299, 150500306, 150500314, 150500322, 150500348, 150500372, 150500380, 150500695, 150500702, 150500728, 150500736, 150500752, 150500760, 150500778, 150500786, 150500794, 150500801, 150500819, 150500827, 150500851, 150500877, 150500893, 150500918, 150500926, 150500934, 150500968, 150501073, 150501114, 150501130, 150501148, 150501156, 150501172, 150501198, 150501213, 150501221, 150501239, 150501255, 150501263, 150501271, 150501289, 150501304) OR ACCTNBR IN (150501312, 150501320, 150501354, 150501370, 150501437, 150501445, 150501453, 150501461, 150501487, 150501495, 150501502, 150501510, 150501528, 150501536, 150501560, 150501601, 150501693, 150501718, 150501726, 150501734, 150501768, 150501784, 150501792, 150501809, 150501825, 150501833, 150501841, 150501859, 150501867, 150501883, 150501908, 150501916, 150501924, 150501932, 150501958, 150501974, 150501982, 150502146, 150502154, 150502162, 150502170, 150502188, 150502196, 150502203, 150502211, 150502261, 150502287, 150502295, 150502302, 150502310, 150502328, 150502336, 150502344, 150502352, 150502378, 150502419, 150502435, 150502443, 150502451, 150502477, 150502485, 150502568, 150502584, 150502675, 150502724, 150502740, 150502815, 150502857, 150502865, 150502873, 150502881, 150502906, 150502914, 150502922, 150502930, 150502948, 150503003, 150503186, 150503201, 150503243, 150503277, 150503326, 150503342, 150503384, 150503392, 150503409, 150503425, 150503433, 150503459, 150503467, 150503475, 150503491, 150503508, 150503524, 150503607, 150503996, 150504001, 150504027, 150504093, 150504118, 150504134, 150504176, 150504473, 150504514, 150504613, 150504704, 150504738, 150504754, 150504770, 150504796, 150504829, 150504837, 150504879, 150504952, 150505190, 150505223, 150505265, 150505330, 150505364, 150505405, 150505744, 150505794, 150505819, 150505827, 150505869, 150505877, 150505950, 150506239, 150506255, 150506263, 150506271, 150506411, 150506461, 150506487, 150506536, 150506594, 150506601, 150506619, 150506627, 150506635, 150506643, 150506734, 150506809, 150506825, 150506859, 150506883, 150506891, 150506924, 150506932, 150506940, 150506958, 150506966, 150506974, 150506982, 150506990, 150507005, 150507021, 150507170, 150507188, 150507196, 150507203, 150507253, 150507336, 150507344, 150507352, 150507360, 150507394, 150507419, 150507427, 150507443, 150507485, 150507500, 150507526, 150507568, 150507592, 150507716, 150507724, 150507732, 150507740, 150507766, 150507899, 150507906, 150507914, 150507922, 150507930, 150507948, 150507956, 150507964, 150507972, 150507980, 150508003, 150508011, 150508029, 150508037, 150508045, 150508053, 150508061, 150508102, 150508342, 150508350, 150508368, 150508384, 150508392, 150508425, 150508491, 150508524, 150508540, 150508558, 150508574, 150508590, 150508607, 150508615, 150508714, 150508730, 150508798, 150508805, 150508821, 150508839, 150508847, 150508855, 150508897, 150508904, 150508912, 150508920, 150508938, 150508954, 150509217, 150509225, 150509233, 150509275, 150509283, 150509291, 150509308, 150509316, 150509324, 150509332, 150509340, 150509358, 150509366, 150509382, 150509390, 150509407, 150509423, 150509431, 150509449, 150509457, 150509465, 150509473, 150509647, 150509655, 150509663, 150509671, 150509689, 150509697, 150509704, 150509712, 150509746, 150509754, 150509762, 150509770, 150509803, 150509811, 150509829, 150509837, 150509853, 150509861, 150509879, 150509887, 150509895, 150509910, 150509936, 150509944, 150509952, 150509960, 150509978, 150509986, 150509994, 150510008, 150510206, 150510214, 150510222, 150510230, 150510248, 150510256, 150510264, 150510272, 150510298, 150510339, 150510660, 150510678, 150510686, 150510694, 150510701, 150510719, 150510727, 150510735, 150510769, 150510777, 150510785, 150510793, 150510800, 150510818, 150510826, 150510834, 150510842, 150510884, 150510909, 150510917, 150510925, 150510941, 150510967, 150510983, 150510991, 150511006, 150511014, 150511056, 150511189, 150511204, 150511246, 150511311, 150511329, 150511345, 150511353, 150511361, 150511379, 150511395, 150511402, 150511410, 150511428, 150511436, 150511444, 150511452, 150511460, 150511478, 150511486, 150511501, 150511527, 150511668, 150511676, 150511684, 150511692, 150511733, 150511741, 150511759, 150511767, 150511775, 150511866, 150511874, 150511890, 150511907, 150511915, 150511923, 150511949, 150511957, 150511965, 150511973, 150511981, 150511999, 150512012, 150512103, 150512137, 150512327, 150512335, 150512343, 150512351, 150512369, 150512377, 150512385, 150512517, 150512525, 150512559, 150512567, 150512575, 150512583, 150512616, 150512624, 150512632, 150512640, 150512658, 150512666, 150512674, 150512690, 150512707, 150512715, 150512765, 150512806, 150512864, 150512880, 150512963, 150512971, 150512989, 150512997, 150513010, 150513028, 150513036, 150513044, 150513052, 150513060, 150514711, 150514729, 150514737, 150514745, 150514753, 150514779, 150514787, 150514795, 150514802, 150514810, 150514836, 150514919, 150514935, 150514951, 150514977, 150515157, 150515165, 150515173, 150515230, 150515256, 150515264, 150515272, 150515298, 150515313, 150515321, 150515339, 150515355, 150515412, 150515438, 150515454, 150515462, 150515503, 150515660, 150515701, 150515719, 150515743, 150515769, 150515777, 150515785, 150515793, 150515800, 150515818, 150515826, 150515834, 150515842, 150515850, 150515868, 150515884, 150515892, 150515909, 150515917, 150515925, 150515941, 150515959, 150515967, 150515975, 150515983, 150516254, 150516311, 150516361, 150516428, 150516717, 150516733, 150516767, 150516816, 150516840, 150516866, 150516874, 150517187, 150517244, 150517442, 150517450, 150517484, 150517517, 150517533, 150517541, 150517559, 150517567, 150517575, 150517583, 150517624, 150517682, 150517715, 150517880, 150517913, 150517939, 150517947, 150517963, 150517989, 150518078, 150518094, 150518101, 150518127, 150518135, 150518143, 150518169, 150518193, 150518200, 150518250, 150518292, 150518416, 150518440, 150518466, 150518474, 150518515, 150518531, 150518557, 150518565, 150518573, 150518581, 150518606, 150518614, 150518622, 150518656, 150518664, 150518680, 150518698, 150518854, 150518862, 150518870, 150518888, 150518896, 150518961, 150518979, 150518987, 150519000, 150519026, 150519117, 150519141, 150519357, 150519365, 150519414, 150519422, 150519448, 150519456, 150519464, 150519472, 150519480, 150519498, 150519505, 150519852, 150519878, 150519886, 150519894, 150519927, 150519943, 150519951, 150519977, 150519985, 150519993, 150520007, 150520015, 150520023, 150520049, 150520073, 150520081, 150520099, 150520106, 150520114, 150520122, 150520148, 150520156, 150520164, 150520198, 150520213, 150520221, 150520239, 150520255, 150520263, 150520289, 150520297, 150520502, 150520510, 150520528, 150520536, 150520544, 150520578, 150520586, 150520643, 150520669, 150520677, 150520693, 150520700, 150520734, 150520768, 150520776, 150520784, 150521013, 150521047, 150521055, 150521063, 150521089, 150521097, 150521104, 150521112, 150521120, 150521138, 150521146, 150521170, 150521188, 150521203, 150521211, 150521469, 150521477, 150521518, 150521526, 150521534, 150521542, 150521550, 150521568, 150521576, 150521584, 150521609, 150521625, 150521633, 150521641, 150521659, 150521691, 150521708, 150522045, 150522053, 150522061, 150522079, 150522095, 150522102, 150522136, 150522144, 150522152, 150522160, 150522201, 150522251, 150522269, 150522293, 150522326, 150522425, 150522441, 150522467, 150522524, 150522532, 150522540, 150522574, 150522582, 150522607, 150522615, 150522631, 150522649, 150522839, 150522847, 150522863, 150522871, 150522889, 150522904, 150522912, 150522920, 150522938, 150522946, 150522954, 150522962, 150522970, 150523043, 150523077, 150523085, 150523093, 150523100, 150523142, 150523324, 150523374, 150523423, 150523457, 150523473, 150523506, 150523514, 150523522, 150523556, 150523580, 150523598, 150523655, 150523663, 150523811, 150523829, 150523837, 150523845, 150523853, 150523861, 150523887, 150523902, 150523928, 150523936, 150523960, 150524041, 150524067, 150524108, 150524116, 150524158, 150524538, 150524554, 150524629, 150524653, 150524679, 150524687, 150524695, 150524702, 150524710, 150524728, 150524736, 150524744, 150524794, 150525015, 150525023, 150525031, 150525049, 150525065, 150525099, 150525106, 150525114, 150525148, 150525156, 150525164, 150525180, 150525198, 150525205, 150525213, 150525221, 150525239, 150525247, 150525263, 150525271, 150525289, 150525297, 150525461, 150525487, 150525495, 150525536, 150525552, 150525560, 150525578, 150525586, 150525594, 150525619, 150525635, 150525643, 150525651, 150525669, 150525677, 150525685, 150525700, 150525734, 150525742, 150525768, 150525776, 150525784, 150525792, 150525817, 150525825, 150525833, 150525841, 150525990, 150526013, 150526021, 150526039, 150526112, 150526120, 150526138, 150526146, 150526154, 150526188, 150526196, 150526203, 150526211, 150526229, 150526237, 150526245, 150526253, 150526261, 150526279, 150526287, 150526344, 150526352, 150526550, 150526576, 150526617, 150526633, 150526641, 150526659, 150526667, 150526691, 150526708, 150526716, 150526724, 150526732, 150526740, 150526774, 150526782, 150526815, 150526823, 150526831, 150526857, 150526865, 150526873, 150526881, 150527293, 150527326, 150527376, 150527433, 150527441, 150527540, 150527558, 150527970, 150527996, 150528085, 150528126, 150528150, 150528192, 150528283, 150528316, 150528358, 150528382, 150528390, 150528738, 150528746, 150528770, 150528811, 150528829, 150528845, 150528853, 150528879, 150528887, 150528910, 150528936, 150528952, 150528960, 150528986, 150529017, 150529067, 150529083, 150529091, 150529231, 150529249, 150529306, 150529314, 150529322, 150529348, 150529364, 150529372, 150529455, 150529489, 150529497, 150529512, 150529520, 150529679, 150529794, 150529827, 150529926, 150529950, 150529976, 150530048, 150530056, 150530072, 150530105, 150530155, 150530163, 150530402, 150530436, 150530444, 150530452, 150530460, 150530494, 150530519, 150530585, 150530600, 150530618, 150530816, 150530824, 150530832, 150530840, 150530858, 150530907, 150530923, 150530931, 150530949, 150530973, 150530981, 150531004, 150531012, 150531046, 150531054, 150531062, 150531070, 150531088, 150531111, 150531129, 150531161, 150531187, 150531195, 150531202, 150531236, 150531492, 150531517, 150531533, 150531541, 150531559, 150531567, 150531575, 150531583, 150531616, 150531624, 150531632, 150531640, 150531658, 150531682, 150531723, 150531731, 150531757, 150531781, 150531799, 150531814, 150531872, 150531898, 150531905, 150531963, 150531971, 150531989, 150532002, 150532010, 150532036, 150532044, 150532052, 150532101, 150532119, 150532127, 150532135, 150532151, 150532169, 150532177, 150532185, 150532218, 150532268, 150532325, 150532333, 150532341, 150532367, 150532375, 150532391, 150532812, 150532854, 150532862, 150532870, 150532911, 150532929, 150532937, 150532945, 150532953, 150532961, 150533026, 150533159, 150533175, 150533448, 150533456, 150533464, 150533472, 150533480, 150533498, 150533505, 150533513, 150533589, 150533620, 150533638, 150533662, 150533729, 150533737, 150533753, 150533761, 150533779, 150533787, 150533802, 150533810, 150533828, 150533852, 150533860, 150533901, 150534131, 150534157, 150534165, 150534181, 150534199, 150534206, 150534214, 150534222, 150534248, 150534272, 150534298, 150534305, 150534313, 150534321, 150534339, 150534347, 150534363, 150534404, 150534412, 150534438, 150534470) OR ACCTNBR IN (150534503, 150534743, 150534793, 150534818, 150534826, 150534834, 150534842, 150534850, 150534876, 150534884, 150534892, 150534909, 150534917, 150534925, 150534975, 150535098, 150535105, 150535113, 150535121, 150535139, 150535147, 150535155, 150535296, 150535337, 150535353, 150535361, 150535387, 150535402, 150535410, 150535428, 150535436, 150535444, 150535452, 150535460, 150535478, 150535486, 150535759, 150535767, 150535775, 150535783, 150535791, 150535808, 150535816, 150535874, 150535882, 150535890, 150535907, 150535915, 150535973, 150535999, 150536004, 150536038, 150536179, 150536244, 150536278, 150536286, 150536301, 150536351, 150536377, 150536385, 150536393, 150536418, 150536426, 150536434, 150536442, 150536468, 150536484, 150536492, 150536509, 150536517, 150536525, 150536541, 150536624, 150536632, 150536640, 150536658, 150536666, 150536674, 150536682, 150536690, 150536707, 150536715, 150536723, 150536773, 150536799, 150537002, 150537028, 150537036, 150537044, 150537052, 150537060, 150537169, 150537173, 150537193, 150537200, 150537226, 150537234, 150537242, 150537284, 150537309, 150537325, 150537367, 150537408, 150537747, 150537755, 150537789, 150537797, 150537804, 150537812, 150537820, 150537838, 150537846, 150537854, 150537862, 150537870, 150538026, 150538092, 150538109, 150538133, 150538175, 150538232, 150538258, 150538282, 150538290, 150538331, 150538349, 150538373, 150538399, 150538711, 150538802, 150538810, 150538852, 150538894, 150539008, 150539024, 150539149, 150539173, 150539181, 150539222, 150539230, 150539280, 150539313, 150539347, 150539438, 150539470, 150539488, 150539503, 150539537, 150539545, 150539579, 150539595, 150539602, 150539686, 150539727, 150539751, 150539777, 150539818, 150539826, 150539892, 150539967, 150539975, 150540146, 150540154, 150540162, 150540170, 150540188, 150540196, 150540203, 150540279, 150540287, 150540295, 150540302, 150540310, 150540336, 150540352, 150540360, 150540378, 150540401, 150540419, 150540485, 150540493, 150540500, 150540542, 150540584, 150540758, 150540831, 150540881, 150540972, 150541029, 150541037, 150541045, 150541053, 150541061, 150541079, 150541087, 150541102, 150541110, 150541128, 150541136, 150541144, 150541178, 150541186, 150541201, 150541219, 150541227, 150541251, 150541368, 150541425, 150541441, 150541467, 150541475, 150541483, 150541508, 150541516, 150541524, 150541540, 150541558, 150541607, 150541615, 150541665, 150541673, 150541756, 150541764, 150541772, 150541813, 150541821, 150541839, 150541889, 150541904, 150541920, 150541938, 150541946, 150541954, 150541962, 150541970, 150541988, 150542001, 150542043, 150542051, 150542291, 150542308, 150542316, 150542324, 150542332, 150542358, 150542366, 150542390, 150542415, 150542431, 150542449, 150542457, 150542465, 150542473, 150542481, 150542499, 150542506, 150542514, 150542522, 150542556, 150542746, 150542770, 150542788, 150542796, 150542837, 150542853, 150542861, 150542879, 150542887, 150542902, 150542928, 150542936, 150542944, 150542952, 150542960, 150542978, 150543009, 150543075, 150543116, 150543249, 150543265, 150543273, 150543281, 150543348, 150543372, 150543398, 150543439, 150543447, 150543463, 150543471, 150543489, 150543497, 150543504, 150543512, 150543520, 150543538, 150543562, 150543570, 150543596, 150543637, 150543645, 150543653, 150543661, 150543687, 150543702, 150543827, 150543843, 150543851, 150543934, 150543942, 150544015, 150544023, 150544049, 150544057, 150544065, 150544073, 150544099, 150544106, 150544114, 150544122, 150544130, 150544148, 150544156, 150544164, 150544172, 150544198, 150544239, 150544247, 150544255, 150544320, 150544429, 150544437, 150544445, 150544560, 150544578, 150544586, 150544594, 150544601, 150544627, 150544635, 150544643, 150544669, 150544677, 150544685, 150544693, 150544700, 150544718, 150544726, 150544734, 150544742, 150544750, 150544768, 150544784, 150544809, 150544817, 150544825, 150544833, 150544841, 150545021, 150545039, 150545055, 150545063, 150545089, 150545104, 150545120, 150545138, 150545146, 150545162, 150545170, 150545188, 150545196, 150545203, 150545211, 150545229, 150545245, 150545310, 150545328, 150545344, 150545352, 150545360, 150545378, 150545386, 150545394, 150545550, 150545576, 150545683, 150545724, 150545740, 150545758, 150545766, 150545774, 150545782, 150545807, 150545815, 150545831, 150546011, 150546029, 150546037, 150546045, 150546053, 150546061, 150546079, 150546087, 150546095, 150546102, 150546110, 150546128, 150546318, 150546334, 150546342, 150546350, 150546368, 150546384, 150546392, 150546409, 150546417, 150546441, 150546459, 150546467, 150546475, 150546483, 150546491, 150546508, 150546516, 150546590, 150546681, 150546699, 150546706, 150546714, 150546722, 150546730, 150546748, 150546772, 150546805, 150546813, 150546821, 150546839, 150546912, 150546920, 150546938, 150546946, 150546954, 150546962, 150546996, 150547035, 150547051, 150547085, 150547118, 150547142, 150547150, 150547168, 150547176, 150547184, 150547192, 150547233, 150547390, 150547423, 150547431, 150547449, 150547457, 150547465, 150547473, 150547481, 150547506, 150547514, 150547530, 150547621, 150547647, 150547655, 150547663, 150547671, 150547689, 150547697, 150547704, 150547712, 150547720, 150547746, 150547754, 150547762, 150547770, 150547788, 150547796, 150547803, 150547829, 150547837, 150548025, 150548067, 150548083, 150548124, 150548281, 150548299, 150548306, 150548322, 150548330, 150548364, 150548398, 150548405, 150548413, 150548421, 150548439, 150548447, 150548455, 150548471, 150548489, 150548497, 150548504, 150548512, 150548520, 150548538, 150548546, 150548554, 150548562, 150548570, 150548588, 150548603, 150548629, 150548645, 150548653, 150548752, 150548760, 150548778, 150548835, 150548843, 150548851, 150548869, 150548877, 150548885, 150548893, 150548984, 150548992, 150549007, 150549023, 150549031, 150549049, 150549065, 150549073, 150549081, 150549106, 150549122, 150549148, 150549156, 150549164, 150549172, 150549180, 150549205, 150549247, 150549403, 150549693, 150549726, 150549750, 150549825, 150549867, 150549875, 150549958, 150549982, 150550046, 150550111, 150550210, 150550244, 150550260, 150550286, 150550343, 150550385, 150550400, 150550434, 150550624, 150550632, 150550640, 150550690, 150550707, 150550715, 150550723, 150550731, 150550765, 150550814, 150550913, 150550939, 150550947, 150550955, 150550963, 150551036, 150551044, 150551086, 150551094, 150551151, 150551177, 150551341, 150551359, 150551391, 150551440, 150551474, 150551515, 150551573, 150551581, 150551599, 150551606, 150551614, 150551622, 150551630, 150551648, 150551656, 150551672, 150551755, 150551763, 150552042, 150552050, 150552068, 150552076, 150552092, 150552117, 150552125, 150552133, 150552240, 150552274, 150552282, 150552315, 150552323, 150552349, 150552357, 150552365, 150552787, 150552802, 150552810, 150552836, 150552844, 150552852, 150552878, 150552886, 150552894, 150552901, 150552919, 150553115, 150553157, 150553173, 150553214, 150553230, 150553256, 150553280, 150553321, 150553339, 150553347, 150553355, 150553371, 150553389, 150553404, 150553412, 150553420, 150553438, 150553446, 150553454, 150553470, 150553652, 150553686, 150553701, 150553719, 150553727, 150553769, 150553777, 150553785, 150553800, 150553818, 150553826, 150553834, 150553842, 150553850, 150553876, 150553884, 150553909, 150553917, 150553925, 150553933, 150553941, 150553959, 150553967, 150553975, 150554072, 150554080, 150554098, 150554155, 150554197, 150554204, 150554212, 150554220, 150554238, 150554254, 150554262, 150554270, 150554296, 150554303, 150554311, 150554337, 150554345, 150554361, 150554379, 150554387, 150554395, 150554402, 150554428, 150554452, 150554460, 150554486, 150554535, 150554543, 150554551, 150554593, 150554767, 150554783, 150554791, 150554808, 150554816, 150554824, 150554840, 150554874, 150554882, 150554907, 150554949, 150555351, 150555385, 150555393, 150555418, 150555426, 150555434, 150555450, 150555484, 150555509, 150555517, 150555541, 150555559, 150555567, 150555575, 150555583, 150555608, 150555616, 150555624, 150555632, 150555640, 150555674, 150555715, 150555723, 150555731, 150555749, 150555757, 150555765, 150555773, 150555781, 150555799, 150555814, 150555830, 150555848, 150555856, 150556052, 150556060, 150556119, 150556143, 150556151, 150556169, 150556177, 150556185, 150556200, 150556218, 150556234, 150556250, 150556268, 150556276, 150556284, 150556292, 150556309, 150556317, 150556325, 150556333, 150556341, 150556367, 150556375, 150556383, 150556466, 150556490, 150556531, 150556549, 150556557, 150556565, 150556581, 150556599, 150556614, 150556622, 150556648, 150556656, 150556664, 150556672, 150556680, 150556698, 150556705, 150556721, 150556862, 150556870, 150556896, 150556937, 150556961, 150556979, 150556987, 150557034, 150557068, 150557076, 150557092, 150557109, 150557117, 150557133, 150557141, 150557159, 150557175, 150557191, 150557224, 150557240, 150557258, 150557266, 150557282, 150557555, 150557571, 150557589, 150557597, 150557604, 150557612, 150557620, 150557646, 150557654, 150557662, 150557670, 150557688, 150557696, 150557703, 150557745, 150557753, 150557795, 150557802, 150557810, 150557828, 150557836, 150557852, 150557860, 150557878, 150557886, 150557894, 150557901, 150558264, 150558272, 150558280, 150558397, 150558404, 150558412, 150558420, 150558438, 150558454, 150558462, 150558488, 150558496, 150558529, 150558537, 150558561, 150558842, 150558850, 150558868, 150558876, 150558884, 150558892, 150558909, 150558917, 150558983, 150559064, 150559072, 150559155, 150559163, 150559171, 150559189, 150559197, 150559204, 150559238, 150559262, 150559270, 150559288, 150559296, 150559303, 150559527, 150559535, 150559577, 150559585, 150559593, 150559634, 150559676, 150559767, 150560053, 150560061, 150560079, 150560087, 150560102, 150560110, 150560144, 150560152, 150560160, 150560178, 150560186, 150560194, 150560201, 150560227, 150560235, 150560243, 150560251, 150560269, 150560285, 150560318, 150560326, 150560334, 150560350, 150560376, 150560482, 150560699, 150560714, 150560730, 150560780, 150560813, 150561019, 150561159, 150561167, 150561175, 150561183, 150561191, 150561216, 150561291, 150561316, 150561431, 150561449, 150561514, 150561548, 150561572, 150561837, 150561861, 150561887, 150561895, 150562215, 150562348, 150562398, 150562801, 150562827, 150562851, 150562885, 150562893, 150563007, 150563015, 150563049, 150563130, 150563156, 150563502, 150563544, 150563560, 150563578, 150563627, 150563643, 150563651, 150563669, 150563677, 150563734, 150563742, 150563750, 150564055, 150564089, 150564097, 150564120, 150564146, 150564203, 150564229, 150564253, 150564261, 150564279, 150564287, 150564310, 150564352, 150564360, 150564542, 150564568, 150564576, 150564584, 150564617, 150564659, 150564675, 150564683, 150564708, 150564716, 150564740, 150564774, 150564790, 150564823, 150564865, 150565053, 150565087, 150565095, 150565102, 150565112, 150565128, 150565136, 150565144, 150565160, 150565178) OR ACCTNBR IN (150565243, 150565269, 150565277, 150565285, 150565293, 150565326, 150565334, 150565350, 150565384, 150565409, 150565730, 150565813, 150565839, 150565847, 150565863, 150565946, 150566001, 150566259, 150566316, 150566423, 150566506, 150566548, 150566986, 150566994, 150567017, 150567025, 150567033, 150567041, 150567059, 150567067, 150567075, 150567083, 150567158, 150567166, 150567174, 150567182, 150567207, 150567215, 150567223, 150567231, 150567265, 150567273, 150567281, 150567306, 150567322, 150567348, 150567364, 150567372, 150567380, 150567405, 150567577, 150567679, 150567695, 150567702, 150567752, 150567801, 150567819, 150567851, 150567885, 150567893, 150567900, 150567918, 150567942, 150567976, 150567984, 150567992, 150568007, 150568023, 150568031, 150568073, 150568081, 150568099, 150568122, 150568130, 150568148, 150568164, 150568172, 150568198, 150568388, 150568411, 150568429, 150568445, 150568453, 150568479, 150568487, 150568502, 150568578, 150568594, 150568635, 150568643, 150568651, 150568677, 150568685, 150568693, 150568718, 150568726, 150568734, 150568750, 150568776, 150568809, 150568817, 150568833, 150568883, 150569203, 150569211, 150569229, 150569237, 150569245, 150569253, 150569279, 150569287, 150569295, 150569328, 150569344, 150569419, 150569435, 150569443, 150569500, 150569518, 150569526, 150569534, 150569542, 150569568, 150569576, 150569584, 150569592, 150569609, 150569625, 150569633, 150569659, 150569675, 150569972, 150569998, 150570010, 150570036, 150570052, 150570060, 150570094, 150570101, 150570127, 150570135, 150570143, 150570151, 150570177, 150570185, 150570193, 150570200, 150570218, 150570226, 150570234, 150570250, 150570268, 150570549, 150570573, 150570656, 150570739, 150570747, 150570755, 150570763, 150570789, 150570804, 150570812, 150570820, 150570846, 150570854, 150570862, 150570870, 150570888, 150570896, 150570903, 150570929, 150570937, 150570945, 150570953, 150570979, 150570987, 150570995, 150571208, 150571315, 150571323, 150571331, 150571349, 150571357, 150571365, 150571373, 150571381, 150571399, 150571406, 150571414, 150571422, 150571430, 150571464, 150571472, 150571480, 150571498, 150571810, 150571828, 150571852, 150571886, 150571901, 150571919, 150571925, 150571935, 150571943, 150571951, 150571977, 150571993, 150572008, 150572016, 150572024, 150572032, 150572074, 150572090, 150572107, 150572123, 150572173, 150572256, 150572298, 150572511, 150572529, 150572545, 150572561, 150572587, 150572595, 150572602, 150572628, 150572636, 150572644, 150572652, 150572678, 150572694, 150572701, 150572719, 150572727, 150572735, 150572743, 150572751, 150572769, 150572777, 150572785, 150572800, 150572842, 150573197, 150573220, 150573238, 150573246, 150573387, 150573486, 150573519, 150573585, 150573593, 150573626, 150573866, 150573874, 150573882, 150573890, 150573965, 150573973, 150574054, 150574062, 150574070, 150574103, 150574161, 150574210, 150574228, 150574236, 150574278, 150574525, 150574533, 150574591, 150574616, 150574632, 150574658, 150574666, 150574682, 150574757, 150574781, 150574814, 150574872, 150574905, 150574947, 150574955, 150574963, 150575127, 150575226, 150575242, 150575268, 150575276, 150575325, 150575341, 150575424, 150575458, 150575474, 150575507, 150575557, 150575581, 150575606, 150575622, 150575929, 150575937, 150575961, 150575995, 150576000, 150576050, 150576068, 150576109, 150576117, 150576133, 150576159, 150576208, 150576232, 150576620, 150576638, 150576646, 150576654, 150576662, 150576688, 150576737, 150576753, 150576779, 150576787, 150576810, 150576860, 150576894, 150576901, 150576977, 150576985, 150577008, 150577016, 150577032, 150577082, 150577214, 150577230, 150577264, 150577313, 150577321, 150577339, 150577355, 150577389, 150577404, 150577438, 150577660, 150577678, 150577694, 150577701, 150577727, 150577735, 150577743, 150577751, 150577777, 150577818, 150577826, 150577834, 150577842, 150577868, 150577876, 150577884, 150577909, 150577917, 150577925, 150577933, 150577941, 150578113, 150578139, 150578155, 150578171, 150578189, 150578197, 150578204, 150578212, 150578220, 150578238, 150578254, 150578270, 150578288, 150578303, 150578311, 150578329, 150578345, 150578353, 150578361, 150578379, 150578402, 150578410, 150578436, 150578783, 150578791, 150578808, 150578832, 150578840, 150578858, 150578866, 150578882, 150578907, 150578923, 150578931, 150578949, 150578957, 150578965, 150578981, 150578999, 150579004, 150579012, 150579020, 150579046, 150579054, 150579062, 150579070, 150579088, 150579103, 150579129, 150579137, 150579145, 150579161, 150579187, 150579195, 150579202, 150579377, 150579400, 150579418, 150579426, 150579434, 150579442, 150579450, 150579468, 150579476, 150579484, 150579492, 150579509, 150579517, 150579525, 150579567, 150579624, 150579640, 150579658, 150579674, 150579707, 150579715, 150579723, 150579731, 150579749, 150579757, 150579765, 150580142, 150580168, 150580176, 150580192, 150580308, 150580332, 150580431, 150580457, 150580465, 150580499, 150580506, 150580514, 150580522, 150580548, 150580564, 150580572, 150580580, 150580598, 150580621, 150580639, 150580647, 150580655, 150580928, 150580944, 150580952, 150580960, 150580978, 150581025, 150581041, 150581059, 150581067, 150581083, 150581091, 150581116, 150581124, 150581140, 150581207, 150581215, 150581223, 150581231, 150581249, 150581257, 150581265, 150581299, 150581306, 150581314, 150581322, 150581348, 150581356, 150581372, 150581380, 150581398, 150581405, 150581421, 150581447, 150581455, 150581463, 150581695, 150581702, 150581710, 150581736, 150581752, 150581760, 150581786, 150581794, 150581801, 150581869, 150581877, 150581885, 150581893, 150581950, 150581976, 150581984, 150581992, 150582007, 150582023, 150582031, 150582049, 150582057, 150582065, 150582073, 150582081, 150582099, 150582106, 150582114, 150582156, 150582164, 150582172, 150582198, 150582213, 150582221, 150582239, 150582247, 150582263, 150582271, 150582289, 150582304, 150582578, 150582586, 150582594, 150582601, 150582627, 150582635, 150582651, 150582677, 150582685, 150582693, 150582700, 150582726, 150582750, 150582768, 150582776, 150582784, 150582792, 150582809, 150582817, 150582825, 150582833, 150582841, 150582859, 150582891, 150582916, 150582924, 150582932, 150582966, 150583203, 150583253, 150583261, 150583279, 150583295, 150583302, 150583344, 150583352, 150583419, 150583477, 150583500, 150583518, 150583526, 150583534, 150583550, 150583568, 150583609, 150583617, 150583625, 150583641, 150583659, 150583667, 150583683, 150584003, 150584061, 150584079, 150584102, 150584128, 150584136, 150584152, 150584160, 150584178, 150584186, 150584194, 150584227, 150584235, 150584269, 150584285, 150584293, 150584300, 150584342, 150584350, 150584376, 150584384, 150584409, 150584417, 150584425, 150584475, 150584649, 150584657, 150584665, 150584673, 150584730, 150584756, 150584764, 150584780, 150584798, 150584805, 150584813, 150584821, 150584847, 150584871, 150584889, 150584904, 150584912, 150584920, 150584938, 150584946, 150584954, 150584962, 150584970, 150584996, 150585001, 150585035, 150585043, 150585051, 150585283, 150585291, 150585308, 150585316, 150585324, 150585332, 150585340, 150585366, 150585382, 150585390, 150585423, 150585431, 150585465, 150585473, 150585481, 150585514, 150585530, 150585548, 150585572, 150585580, 150585671, 150585697, 150585720, 150585902, 150585936, 150585944, 150585952, 150585960, 150585978, 150585986, 150586017, 150586158, 150586166, 150586174, 150586182, 150586190, 150586207, 150586215, 150586223, 150586249, 150586265, 150586281, 150586306, 150586322, 150586330, 150586348, 150586356, 150586372, 150586380, 150586398, 150586413, 150586421, 150586687, 150586695, 150586702, 150586710, 150586728, 150586736, 150586744, 150586801, 150586819, 150586835, 150586851, 150586869, 150586918, 150586950, 150586968, 150586976, 150586984, 150587049, 150587057, 150587065, 150587073, 150587099, 150587130, 150587221, 150587239, 150587247, 150587693, 150587700, 150587718, 150587726, 150587734, 150587742, 150587750, 150587768, 150587776, 150587784, 150587792, 150587809, 150587817, 150587833, 150587841, 150587916, 150587924, 150587932, 150587940, 150587958, 150587966, 150587974, 150587990, 150588013, 150588245, 150588253, 150588261, 150588279, 150588287, 150588295, 150588302, 150588310, 150588328, 150588336, 150588469, 150588493, 150588526, 150588542, 150588568, 150588592, 150588617, 150588625, 150588633, 150588641, 150588667, 150588675, 150588683, 150588691, 150588922, 150588948, 150588964, 150588972, 150588980, 150589029, 150589037, 150589045, 150589053, 150589061, 150589079, 150589095, 150589102, 150589160, 150589178, 150589186, 150589201, 150589227, 150589243, 150589251, 150589277, 150589293, 150589334, 150589342, 150589368, 150589384, 150589392, 150589409, 150589417, 150589425, 150589433, 150589441, 150589459, 150589657, 150589673, 150589714, 150589722, 150589756, 150589764, 150589772, 150589780, 150589839, 150589847, 150589855, 150589889, 150589897, 150589996, 150590208, 150590266, 150590282, 150590331, 150590357, 150590589, 150590604, 150590638, 150590646, 150590662, 150590703, 150590729, 150590753, 150590779, 150590787, 150590810, 150591298, 150591321, 150591339, 150591347, 150591355, 150591363, 150591371, 150591470, 150591496, 150591511, 150591537, 150591553, 150591561, 150591644, 150591652, 150591678, 150591701, 150591727, 150591785, 150591800, 150591850, 150592022, 150592048, 150592056, 150592064, 150592072, 150592080, 150592098, 150592105, 150592113, 150592121, 150592329, 150592379, 150592395, 150592402, 150592410, 150592618, 150592626, 150592692, 150592874, 150592923, 150592931, 150592965, 150592999, 150593004, 150593020, 150593046, 150593062, 150593088, 150593103, 150593111, 150593244, 150593260, 150593301, 150593319, 150593335, 150593343, 150593351, 150593369, 150593377, 150593393, 150593492, 150593517, 150593541, 150593559, 150593567, 150593591, 150593749, 150593773, 150593781, 150593799, 150593806, 150593814, 150593921, 150593947, 150593955, 150593971, 150594002, 150594036, 150594044, 150594078, 150594086, 150594094, 150594127, 150594466, 150594474, 150594565, 150594581, 150594599, 150594606, 150594614, 150594622, 150594630, 150594656, 150594664, 150594672, 150594680, 150594698, 150594705, 150594721, 150594755, 150595000, 150595026, 150595034, 150595042, 150595076, 150595084, 150595092, 150595109, 150595117, 150595125, 150595133, 150595141, 150595159, 150595167, 150595191, 150595208, 150595216, 150595224, 150595274, 150595282, 150595414, 150595422, 150595448, 150595456, 1505954995, 150595505, 150595521, 150595539, 150595547, 150595563, 150595589, 150595638, 150595654, 150595670, 150595703, 150595729, 150595737, 150595745, 150595753, 150595761, 150595779, 150595787, 150595810, 150595828, 150595836, 150596090, 150596107, 150596115, 150596131, 150596157, 150596206, 150596214, 150596230, 150596248, 150596264, 150596280, 150596298, 150596313, 150596339, 150596347, 150596355, 150596363, 150596412, 150596727, 150596769) OR ACCTNBR IN (150596777, 150596793, 150596800, 150596818, 150596834, 150596842, 150596850, 150596868, 150596876, 150596884, 150596909, 150596917, 150596933, 150596959, 150596975, 150596991, 150597022, 150597048, 150597056, 150597064, 150597072, 150597080, 150597428, 150597444, 150597452, 150597478, 150597494, 150597501, 150597519, 150597527, 150597535, 150597543, 150597551, 150597585, 150597618, 150597626, 150597634, 150597642, 150597668, 150597676, 150597717, 150597733, 150597741, 150597759, 150598062, 150598070, 150598088, 150598096, 150598103, 150598111, 150598129, 150598137, 150598145, 150598153, 150598161, 150598179, 150598187, 150598195, 150598202, 150598228, 150598236, 150598244, 150598260, 150598278, 150598294, 150598335, 150598468, 150598525, 150598541, 150598632, 150598640, 150598658, 150598682, 150598690, 150598707, 150598715, 150598723, 150598731, 150598749, 150598757, 150598765, 150598773, 150598781, 150598799, 150598806, 150598814, 150598822, 150598848, 150598856, 150598864, 150598872, 150598880, 150598905, 150598913, 150598921, 150598939, 150598989, 150599151, 150599185, 150599200, 150599234, 150599242, 150599250, 150599268, 150599276, 150599284, 150599292, 150599309, 150599317, 150599325, 150599333, 150599341, 150599391, 150599408, 150599416, 150599424, 150599432, 150599440, 150599458, 150599474, 150599482, 150599490, 150599515, 150599531, 150599549, 150599565, 150599573, 150599581, 150599622, 150599630, 150599820, 150599838, 150599854, 150599896, 150599911, 150599929, 150599937, 150599945, 150599953, 150599979, 150599987, 150599995, 150600007, 150600015, 150600023, 150600031, 150600049, 150600057, 150600099, 150600619, 150600627, 150600643, 150600651, 150600700, 150600718, 150600726, 150600734, 150600742, 150600750, 150600768, 150600776, 150600784, 150600792, 150600817, 150600825, 150600833, 150600841, 150600859, 150601013, 150601021, 150601039, 150601089, 150601097, 150601120, 150601138, 150601146, 150601154, 150601162, 150601170, 150601188, 150601196, 150601229, 150601237, 150601245, 150601253, 150601279, 150601287, 150601302, 150601310, 150601328, 150601336, 150601360, 150601378, 150601401, 150601419, 150601427, 150601435, 150601443, 150601451, 150601469, 150601477, 150601576, 150601592, 150601609, 150601625, 150601633, 150601675, 150601683, 150601691, 150601732, 150601740, 150601782, 150601807, 150601815, 150601831, 150601849, 150601857, 150601865, 150601873, 150601881, 150601899, 150601906, 150601914, 150601948, 150602037, 150602045, 150602053, 150602061, 150602136, 150602144, 150602152, 150602178, 150602186, 150602201, 150602219, 150602227, 150602243, 150602277, 150602300, 150602318, 150602326, 150602334, 150602342, 150602350, 150602368, 150602384, 150602392, 150602417, 150602433, 150602459, 150602615, 150602623, 150602649, 150602657, 150602665, 150602673, 150602681, 150602699, 150602706, 150602714, 150602722, 150602730, 150602748, 150602764, 150602772, 150602780, 150602813, 150602821, 150602839, 150602863, 150602871, 150602889, 150602946, 150602954, 150602970, 150602988, 150603001, 150603043, 150603093, 150603100, 150603150, 150603481, 150603514, 150603522, 150603621, 150603712, 150603788, 150603902, 150603910, 150603960, 150603978, 150604075, 150604124, 150604132, 150604223, 150604249, 150604273, 150604281, 150604299, 150604306, 150604322, 150604398, 150604405, 150604413, 150604570, 150604596, 150604603, 150604611, 150604695, 150604710, 150604728, 150604819, 150604918, 150604934, 150604942, 150604950, 150605065, 150605297, 150605338, 150605346, 150605362, 150605437, 150605453, 150605461, 150605487, 150605495, 150605510, 150605528, 150605536, 150605544, 150605552, 150605560, 150605578, 150605586, 150605594, 150605601, 150605619, 150605867, 150605891, 150605940, 150605974, 150605982, 150605990, 150606013, 150606104, 150606112, 150606120, 150606138, 150606146, 150606154, 150606170, 150606196, 150606500, 150606550, 150606568, 150606576, 150606584, 150606617, 150606675, 150606691, 150606708, 150606716, 150606724, 150606758, 150606782, 150607061, 150607095, 150607102, 150607194, 150607201, 150607235, 150607285, 150607300, 150607318, 150607326, 150607334, 150607384, 150607425, 150607433, 150607681, 150607699, 150607706, 150607714, 150607722, 150607730, 150607748, 150607764, 150607772, 150607813, 150607821, 150607839, 150607847, 150607855, 150607863, 150607871, 150607889, 150607897, 150607904, 150607912, 150607988, 150608001, 150608043, 150608051, 150608069, 150608077, 150608085, 150608093, 150608100, 150608176, 150608188, 150608217, 150608267, 150608283, 150608291, 150608316, 150608332, 150608340, 150608423, 150608449, 150608613, 150608621, 150608639, 150608647, 150608663, 150608671, 150608712, 150608845, 150608853, 150608861, 150608879, 150608887, 150608895, 150608910, 150608936, 150608944, 150608952, 150608960, 150608978, 150608994, 150609009, 150609017, 150609025, 150609033, 150609041, 150609083, 150609421, 150609439, 150609447, 150609455, 150609463, 150609471, 150609489, 150609512, 150609520, 150609538, 150609562, 150609570, 150609596, 150609603, 150609611, 150609637, 150609653, 150609661, 150609679, 150609695, 150609702, 150609710, 150609778, 150609786, 150609819, 150609992, 150610006, 150610030, 150610048, 150610056, 150610080, 150610098, 150610113, 150610121, 150610139, 150610147, 150610155, 150610163, 150610189, 150610197, 150610212, 150610238, 150610246, 150610254, 150610262, 150610270, 150610288, 150610303, 150610311, 150610444, 150610452, 150610494, 150610501, 150610519, 150610593, 150610600, 150610634, 150610642, 150610684, 150610692, 150610709, 150610725, 150610733, 150610741, 150610775, 150610783, 150610791, 150610808, 150610816, 150610824, 150610832, 150610840, 150610858, 150610874, 150610882, 150610981, 150611088, 150611111, 150611129, 150611161, 150611179, 150611195, 150611202, 150611252, 150611260, 150611278, 150611286, 150611294, 150611301, 150611319, 150611327, 150611335, 150611343, 150611351, 150611369, 150611450, 150611468, 150611476, 150611517, 150611525, 150611541, 150611591, 150611608, 150611616, 150611640, 150611658, 150611674, 150611707, 150611715, 150611723, 150611749, 150611806, 150611822, 150611856, 150611864, 150611872, 150611880, 150611898, 150611913, 150611921, 150612218, 150612226, 150612234, 150612242, 150612250, 150612268, 150612391, 150612416, 150612424, 150612432, 150612440, 150612466, 150612474, 150612482, 150612490, 150612507, 150612523, 150612549, 150612606, 150612614, 150612622, 150612771, 150612789, 150612870, 150612888, 150612896, 150612903, 150612911, 150612929, 150612937, 150612945, 150612961, 150612987, 150612995, 150613018, 150613026, 150613034, 150613290, 150613307, 150613331, 150613365, 150613373, 150613381, 150613399, 150613406, 150613414, 150613422, 150613430, 150613448, 150613456, 150613480, 150613498, 150613696, 150613703, 150613711, 150613729, 150613737, 150613745, 150613753, 150613779, 150613787, 150613795, 150613844, 150613860, 150613878, 150613886, 150613901, 150613919, 150613943, 150613977, 150614016, 150614024, 150614032, 150614040, 150614058, 150614222, 150614305, 150614321, 150614371, 150614397, 150614412, 150614420, 150614438, 150614446, 150614818, 150614834, 150614925, 150614941, 150614959, 150614967, 150614975, 150615022, 150615030, 150615262, 150615270, 150615288, 150615337, 150615395, 150615428, 150615478, 150615494, 150615593, 150615626, 150615642, 150615668, 150615676, 150615709, 150615858, 150615949, 150615973, 150615981, 150615999, 150616012, 150616129, 150616153, 150616244, 150616252, 150616286, 150616541, 150616559, 150616567, 150616591, 150616608, 150616682, 150616715, 150616731, 150616749, 150616773, 150616781, 150616806, 150616822, 150616830, 150617127, 150617177, 150617200, 150617218, 150617226, 150617234, 150617242, 150617250, 150617268, 150617276, 150617284, 150617292, 150617367, 150617408, 150617416, 150617424, 150617440, 150617458, 150617466, 150617507, 150617515, 150617672, 150617680, 150617739, 150617747, 150617755, 150617771, 150617789, 150617820, 150617846, 150617870, 150617896, 150617903, 150617911, 150617929, 150617937, 150617945, 150617987, 150618216, 150618224, 150618240, 150618315, 150618323, 150618381, 150618406, 150618414, 150618448, 150618456, 150618513, 150618539, 150618547, 150618555, 150618571, 150618597, 150618604, 150618612, 150618638, 150618646, 150618654, 150618688, 150618703, 150618711, 150618729, 150618761, 150618779, 150618787, 150618943, 150618951, 150618977, 150618985, 150618993, 150619008, 150619016, 150619024, 150619032, 150619058, 150619066, 150619181, 150619280, 150619305, 150619313, 150619321, 150619339, 150619397, 150619404, 150619446, 150619496, 150619511, 150619537, 150619636, 150619941, 150619959, 150620013, 150620021, 150620039, 150620047, 150620089, 150620097, 150620138, 150620146, 150620154, 150620162, 150620170, 150620188, 150620229, 150620237, 150620253, 150620261, 150620279, 150620302, 150620360, 150620378, 150620386, 150620477, 150620500, 150620518, 150620526, 150620542, 150620568, 150620584, 150620609, 150620617, 150620633, 150620659, 150620667, 150620675, 150620683, 150620691, 150620708, 150620716, 150620732, 150620774, 150620790, 150620807, 150620823, 150620849, 150620956, 150621102, 150621144, 150621152, 150621160, 150621178, 150621186, 150621194, 150621201, 150621219, 150621227, 150621235, 150621243, 150621251, 150621269, 150621277, 150621285, 150621293, 150621326, 150621350, 150621368, 150621384, 150621623, 150621714, 150621722, 150621730, 150621748, 150621764, 150621780, 150621805, 150621813, 150621821, 150621839, 150621847, 150621855, 150621863, 150621871, 150621938, 150621946, 150621954, 150621988, 150621996, 150622001, 150622051, 150622085, 150622093, 150622100, 150622548, 150622564, 150622572, 150622613, 150622639, 150622647, 150622655, 150622663, 150622671, 150622689, 150622704, 150622712, 150622720, 150622746, 150622770, 150622796, 150622803, 150622811, 150622837, 150622853, 150622861, 150622902, 150622910, 150622928, 150623075, 150623083, 150623091, 150623108, 150623158, 150623166, 150623174, 150623182, 150623190, 150623207, 150623215, 150623249, 150623265, 150623273, 150623281, 150623299, 150623306, 150623314, 150623322, 150623330, 150623348, 150623356, 150623603, 150623611, 150623629, 150623637, 150623645, 150623653, 150623687, 150623702, 150623736, 150623786, 150623794, 150623819, 150623827, 150623835, 150623843, 150623851, 150623869, 150623877, 150623885, 150623900, 150623926, 150623942, 150623984, 150624015, 150624065, 150624081, 150624122, 150624164, 150624172, 150624221, 150624239, 150624247, 150624255, 150624263, 150624289, 150624297, 150624320, 150624338, 150624346, 150624354, 150624362, 150624370, 150624388, 150624396, 150624403, 150624411, 150624429, 150624453, 150624544, 150624552, 150624586, 150624601, 150624627, 150624677, 150624700, 150624718, 150624726, 150624742, 150624750, 150624776, 150624792, 150624809, 150624833, 150624859, 150625211, 150625229, 150625253, 150625261, 150625279, 150625287, 150625295, 150625302, 150625336) OR ACCTNBR IN (150625352, 150625360, 150625386, 150625394, 150625401, 150625500, 150625518, 150625526, 150625534, 150625542, 150625550, 150625568, 150625576, 150625609, 150625659, 150625667, 150625675, 150625724, 150625732, 150625740, 150625766, 150625774, 150625782, 150625790, 150625807, 150625815, 150625831, 150625849, 150625857, 150625865, 150625881, 150625899, 150626061, 150626087, 150626102, 150626128, 150626136, 150626144, 150626152, 150626160, 150626178, 150626235, 150626300, 150626318, 150626326, 150626334, 150626342, 150626350, 150626376, 150626384, 150626392, 150626409, 150626417, 150626433, 150626441, 150626459, 150626574, 150626582, 150626590, 150626607, 150626615, 150626631, 150626699, 150626805, 150626813, 150626847, 150626889, 150627027, 150627035, 150627043, 150627051, 150627069, 150627077, 150627267, 150627291, 150627324, 150627358, 150627374, 150627382, 150627390, 150627431, 150627449, 150627720, 150627754, 150627762, 150627796, 150627811, 150627829, 150627944, 150627952, 150627960, 150627994, 150628017, 150628025, 150628041, 150628067, 150628083, 150628091, 150628108, 150628124, 150628281, 150628299, 150628306, 150628314, 150628322, 150628348, 150628364, 150628421, 150628439, 150628447, 150628463, 150628471, 150628497, 150628504, 150628520, 150628538, 150628546, 150628554, 150628562, 150628570, 150628588, 150628596, 150628778, 150628786, 150628819, 150628843, 150628869, 150628877, 150628893, 150628900, 150628926, 150628934, 150628942, 150628950, 150628976, 150628992, 150629023, 150629031, 150629099, 150629122, 150629148, 150629156, 150629164, 150629297, 150629304, 150629312, 150629370, 150629388, 150629396, 150629411, 150629437, 150629445, 150629461, 150629487, 150629718, 150629784, 150629809, 150629817, 150629825, 150629833, 150629841, 150629859, 150629867, 150629883, 150629891, 150629908, 150629916, 150629924, 150629932, 150629940, 150629958, 150629974, 150629982, 150630004, 150630012, 150630020, 150630062, 150630070, 150630088, 150630096, 150630228, 150630369, 150630377, 150630385, 150630393, 150630400, 150630418, 150630426, 150630434, 150630442, 150630492, 150630517, 150630525, 150630533, 150630559, 150630567, 150630575, 150630591, 150630608, 150630616, 150630632, 150630640, 150630682, 150630690, 150630707, 150630715, 150630880, 150630905, 150630921, 150630939, 150630947, 150630955, 150630971, 150630989, 150631028, 150631044, 150631052, 150631060, 150631078, 150631086, 150631094, 150631101, 150631119, 150631135, 150631169, 150631177, 150631185, 150631193, 150631200, 150631218, 150631383, 150631416, 150631424, 150631466, 150631523, 150631531, 150631557, 150631565, 150631581, 150631606, 150631614, 150631622, 150631630, 150631648, 150631656, 150631854, 150631862, 150631870, 150631888, 150631896, 150631903, 150631929, 150631945, 150631953, 150631979, 150632018, 150632026, 150632034, 150632042, 150632068, 150632092, 150632373, 150632381, 150632399, 150632464, 150632472, 150632480, 150632513, 150632521, 150632597, 150632604, 150632612, 150632620, 150632638, 150632696, 150632703, 150632711, 150632729, 150632737, 150632753, 150632761, 150632779, 150632802, 150632985, 150633016, 150633032, 150633040, 150633107, 150633115, 150633123, 150633131, 150633157, 150633165, 150633173, 150633214, 150633222, 150633230, 150633256, 150633264, 150633272, 150633280, 150633298, 150633305, 150633321, 150633339, 150633496, 150633503, 150633511, 150633529, 150633537, 150633545, 150633553, 150633561, 150633579, 150633595, 150633602, 150633610, 150633628, 150633636, 150633644, 150633652, 150633660, 150633678, 150633686, 150633694, 150633701, 150633719, 150633727, 150633735, 150633941, 150633983, 150634014, 150634022, 150634048, 150634064, 150634197, 150634204, 150634212, 150634246, 150634262, 150634270, 150634288, 150634501, 150634634, 150634650, 150634676, 150634709, 150634717, 150634725, 150634733, 150634741, 150634759, 150634767, 150634775, 150634783, 150634791, 150634808, 150634816, 150634824, 150635062, 150635070, 150635088, 150635195, 150635210, 150635228, 150635252, 150635294, 150635301, 150635319, 150635343, 150635351, 150635377, 150635385, 150635393, 150635400, 150635418, 150635434, 150635442, 150635450, 150635468, 150635484, 150635492, 150635525, 150635533, 150635591, 150635690, 150635765, 150635773, 150635781, 150635799, 150635814, 150635848, 150635856, 150635864, 150635872, 150635880, 150635905, 150635913, 150635921, 150635947, 150635963, 150635971, 150635989, 150636002, 150636010, 150636028, 150636036, 150636052, 150636060, 150636078, 150636094, 150636101, 150636250, 150636292, 150636309, 150636359, 150636367, 150636408, 150636432, 150636440, 150636482, 150636490, 150636531, 150636565, 150636599, 150636614, 150636705, 150636721, 150636739, 150636797, 150636812, 150636820, 150636846, 150636854, 150636862, 150636896, 150636903, 150636911, 150636929, 150636937, 150636945, 150636953, 150636961, 150636979, 150636987, 150636995, 150637000, 150637018, 150637026, 150637034, 150637042, 150637092, 150637109, 150637323, 150637331, 150637357, 150637365, 150637373, 150637381, 150637406, 150637422, 150637448, 150637456, 150637480, 150637498, 150637505, 150637513, 150637836, 150637860, 150638107, 150638123, 150638149, 150638230, 150638272, 150638313, 150638347, 150638545, 150638678, 150638686, 150638730, 150638735, 150638751, 150638769, 150638785, 150638793, 150638800, 150638818, 150638826, 150638834, 150638842, 150638850, 150638876, 150638892, 150638909, 150638917, 150638933, 150638959, 150638967, 150639212, 150639238, 150639262, 150639270, 150639296, 150639303, 150639337, 150639353, 150639361, 150639402, 150639410, 150639428, 150639436, 150639444, 150639494, 150639501, 150639519, 150639634, 150639668, 150639676, 150639759, 150639767, 150639890, 150639907, 150639915, 150640095, 150640128, 150640186, 150640194, 150640219, 150640227, 150640235, 150640251, 150640318, 150640326, 150640334, 150640368, 150640376, 150640590, 150640607, 150640615, 150640631, 150640657, 150640706, 150640722, 150640730, 150640764, 150640772, 150640780, 150640798, 150640805, 150640813, 150640821, 150640839, 150640847, 150640855, 150640863, 150640889, 150641027, 150641051, 150641069, 150641077, 150641085, 150641093, 150641100, 150641118, 150641134, 150641142, 150641150, 150641168, 150641176, 150641184, 150641192, 150641209, 150641217, 150641241, 150641259, 150641267, 150641382, 150641390, 150641465, 150641499, 150641506, 150641514, 150641522, 150641530, 150641548, 150641556, 150641564, 150641572, 150641639, 150641647, 150641655, 150641663, 150641671, 150641697, 150641712, 150641720, 150641746, 150641788, 150641837, 150641887, 150641928, 150642017, 150642033, 150642041, 150642067, 150642075, 150642083, 150642091, 150642108, 150642116, 150642124, 150642132, 150642140, 150642174, 150642249, 150642265, 150642273, 150642322, 150642364, 150642562, 150642570, 150642588, 150642596, 150642603, 150642611, 150642637, 150642645, 150642653, 150642710, 150642744, 150642752, 150643221, 150643239, 150643255, 150643289, 150643297, 150643304, 150643312, 150643354, 150643396, 150643403, 150643461, 150643479, 150643502, 150643528, 150643544, 150643578, 150643586, 150643627, 150643651, 150643841, 150643859, 150643867, 150643875, 150643883, 150643891, 150643932, 150643990, 150644005, 150644013, 150644021, 150644039, 150644047, 150644055, 150644063, 150644071, 150644089, 150644097, 150644112, 150644120, 150644138, 150644146, 150644336, 150644344, 150644352, 150644394, 150644401, 150644435, 150644443, 150644451, 150644485, 150644493, 150644542, 150644550, 150644568, 150644576, 150644584, 150644592, 150644617, 150644625, 150644766, 150644774, 150644782, 150644790, 150644815, 150644823, 150644831, 150644865, 150644873, 150644881, 150644922, 150644930, 150644964, 150644972, 150645003, 150645243, 150645251, 150645285, 150645293, 150645300, 150645318, 150645334, 150645342, 150645350, 150645368, 150645376, 150645384, 150645409, 150645425, 150645433, 150645441, 150645467, 150645475, 150645483, 150645491, 150645508, 150645516, 150645532, 150645540, 150645558, 150645566, 150645839, 150645847, 150645946, 150645954, 150645962, 150645970, 150645996, 150646001, 150646019, 150646027, 150646035, 150646043, 150646051, 150646069, 150646093, 150646100, 150646142, 150646168, 150646324, 150646340, 150646374, 150646407, 150646415, 150646423, 150646431, 150646449, 150646457, 150646465, 150646481, 150646499, 150646506, 150646514, 150646522, 150646530, 150646548, 150646556, 150646564, 150646639, 150646671, 150646811, 150646829, 150646837, 150646845, 150646853, 150646861, 150646879, 150646887, 150646895, 150646902, 150646944, 150646952, 150646978, 150646986, 150647025, 150647033, 150647041, 150647067, 150647075, 150647083, 150647132, 150647182, 150647190, 150647207, 150647223, 150647249, 150647265, 150647273, 150647299, 150647306, 150647314, 150647330, 150647356, 150647489, 150647497, 150647538, 150647554, 150647570, 150647588, 150647596, 150647611, 150647629, 150647637, 150647645, 150647653, 150647661, 150647679, 150647687, 150647695, 150647702, 150647710, 150647728, 150647736, 150647744, 150647752, 150647760, 150647778, 150648031, 150648049, 150648057, 150648065, 150648081, 150648099, 150648114, 150648122, 150648198, 150648213, 150648221, 150648239, 150648247, 150648255, 150648263, 150648271, 150648289, 150648297, 150648304, 150648312, 150648320, 150648346, 150648643, 150648651, 150648677, 150648685, 150648693, 150648718, 150648726, 150648734, 150648750, 150648768, 150648784, 150648792, 150648809, 150648817, 150648825, 150648833, 150648841, 150648859, 150648867, 150648875, 150648883, 150648891, 150648908, 150648924, 150648932, 150648940, 150648966, 150648974, 150649089, 150649120, 150649138, 150649154, 150649170, 150649229, 150649237, 150649245, 150649253, 150649261, 150649302, 150649310, 150649328, 150649336, 150649352, 150649360, 150649378, 150649386, 150649394, 150649401, 150649419, 150649427, 150649435, 150649443, 150649451, 150649641, 150649667, 150649691, 150649708, 150649724, 150649732, 150649740, 150649758, 150649766, 150649790, 150649823, 150650094, 150650143, 150650151, 150650177, 150650200, 150650268, 150650284, 150650474, 150650490, 150650507, 150650515, 150650656, 150650698, 150650705, 150650713, 150650755, 150650763, 150650789, 150650797, 150650812, 150651133, 150651266, 150651323, 150651331, 150651349, 150651399, 150651555, 150651597, 150651620, 150651638, 150651646, 150651654, 150651662, 150651670, 150651688, 150651696, 150651703, 150651711, 150651729, 150651737, 150651761, 150651802, 150651810, 150651836, 150652058, 150652066, 150652074, 150652082, 150652090, 150652107, 150652115, 150652123, 150652131, 150652149, 150652165, 150652214, 150652222, 150652230, 150652248, 150652264, 150652280, 150652298, 150652305, 150652321, 150652363, 150652412, 150652537, 150652545, 150652553, 150652561, 150652579, 150652587, 150652610, 150652678, 150652686, 150652719, 150652727, 150652735, 150652743, 150652800, 150652818, 150652826, 150652834, 150652842, 150652850, 150652876) OR ACCTNBR IN (150652884, 150653121, 150653139, 150653147, 150653155, 150653163, 150653171, 150653189, 150653197, 150653238, 150653246, 150653254, 150653262, 150653288, 150653303, 150653329, 150653353, 150653361, 150653379, 150653387, 150653395, 150653410, 150653428, 150653444, 150653452, 150653460, 150653486, 150653626, 150653634, 150653759, 150653767, 150653775, 150653783, 150653791, 150653808, 150653816, 150653824, 150653832, 150653874, 150653882, 150653890, 150653907, 150653931, 150653949, 150653957, 150653965, 150653981, 150653999, 150654004, 150654038, 150654179, 150654187, 150654195, 150654202, 150654210, 150654228, 150654236, 150654244, 150654252, 150654260, 150654278, 150654335, 150654343, 150654351, 150654393, 150654418, 150654426, 150654434, 150654442, 150654450, 150654476, 150654624, 150654640, 150654658, 150654666, 150654674, 150654682, 150654690, 150654707, 150654715, 150654723, 150654731, 150654749, 150654757, 150654773, 150654781, 150654880, 150654905, 150654913, 150654939, 150654947, 150654955, 150654971, 150654989, 150654997, 150655002, 150655010, 150655028, 150655036, 150655060, 150655359, 150655367, 150655424, 150655432, 150655440, 150655458, 150655474, 150655870, 150655888, 150655903, 150655911, 150655929, 150655937, 150655945, 150655953, 150656084, 150656092, 150656133, 150656141, 150656159, 150656175, 150656183, 150656191, 150656208, 150656216, 150656224, 150656315, 150656323, 150656331, 150656349, 150656357, 150656365, 150656373, 150656381, 150656399, 150656406, 150656414, 150656430, 150656472, 150656480, 150656498, 150656547, 150656555, 150656563, 150656597, 150656604, 150656620, 150656638, 150656646, 150656654, 150656670, 150656729, 150656894, 150656901, 150656919, 150656927, 150656935, 150656943, 150656951, 150656977, 150656985, 150656993, 150657016, 150657024, 150657058, 150657074, 150657082, 150657107, 150657123, 150657131, 150657149, 150657157, 150657165, 150657173, 150657181, 150657321, 150657339, 150657347, 150657355, 150657363, 150657371, 150657404, 150657412, 150657438, 150657446, 150657454, 150657462, 150657488, 150657496, 150657503, 150657511, 150657529, 150657537, 150657545, 150657553, 150657694, 150657719, 150657727, 150657735, 150657743, 150657751, 150657769, 150657777, 150657793, 150657826, 150657842, 150657850, 150657868, 150657876, 150657917, 150657933, 150657941, 150658337, 150658345, 150658353, 150658361, 150658379, 150658387, 150658410, 150658478, 150658494, 150658519, 150658527, 150658535, 150658543, 150658551, 150658577, 150658600, 150658626, 150658634, 150658642, 150658668, 150658676, 150658684, 150658692, 150658709, 150658824, 150658832, 150658840, 150658874, 150658882, 150658890, 150658907, 150658915, 150658923, 150658931, 150658957, 150658973, 150658981, 150659012, 150659020, 150659038, 150659046, 150659054, 150659062, 150659278, 150659286, 150659294, 150659301, 150659319, 150659327, 150659335, 150659468, 150659476, 150659484, 150659492, 150659509, 150659517, 150659525, 150659533, 150659541, 150659567, 150659575, 150659591, 150659608, 150659616, 150659624, 150659632, 150659640, 150659658, 150659773, 150659799, 150659806, 150659814, 150659822, 150659830, 150659848, 150659856, 150659864, 150659963, 150659971, 150659989, 150659997, 150660001, 150660019, 150660027, 150660035, 150660043, 150660051, 150660069, 150660085, 150660093, 150660100, 150660142, 150660150, 150660415, 150660473, 150660530, 150660548, 150660556, 150660564, 150660572, 150660580, 150660598, 150660605, 150661091, 150661140, 150661249, 150661257, 150661273, 150661281, 150661299, 150661330, 150661364, 150661372, 150661380, 150661398, 150661489, 150661504, 150661546, 150661554, 150661562, 150661596, 150661603, 150661611, 150661778, 150661786, 150661801, 150661827, 150661835, 150661851, 150661900, 150661926, 150661942, 150661950, 150661984, 150662255, 150662271, 150662289, 150662297, 150662304, 150662320, 150662354, 150662370, 150662411, 150662429, 150662437, 150662445, 150662453, 150662461, 150662479, 150662502, 150662528, 150662536, 150662544, 150662552, 150662867, 150662875, 150662883, 150662891, 150662908, 150662924, 150662940, 150662966, 150662974, 150662982, 150662990, 150663005, 150663013, 150663039, 150663047, 150663055, 150663203, 150663229, 150663237, 150663287, 150663310, 150663328, 150663336, 150663344, 150663360, 150663378, 150663401, 150663774, 150663790, 150663807, 150663815, 150663823, 150663865, 150663873, 150663899, 150663906, 150663930, 150663956, 150663972, 150663980, 150663998, 150664029, 150664037, 150664045, 150664053, 150664079, 150664102, 150664136, 150664186, 150664219, 150664459, 150664483, 150664491, 150664508, 150664516, 150664524, 150664540, 150664566, 150664574, 150664590, 150664607, 150664615, 150664623, 150664631, 150664649, 150664657, 150664665, 150664681, 150664706, 150664714, 150664722, 150664748, 150664764, 150664772, 150664780, 150664798, 150664805, 150664813, 150664821, 150664839, 150664847, 150664855, 150664863, 150664871, 150664988, 150665009, 150665019, 150665027, 150665051, 150665069, 150665077, 150665085, 150665100, 150665118, 150665126, 150665134, 150665168, 150665176, 150665184, 150665192, 150665217, 150665225, 150665366, 150665374, 150665382, 150665465, 150665473, 150665481, 150665499, 150665514, 150665522, 150665530, 150665548, 150665580, 150665598, 150665605, 150665621, 150665639, 150665647, 150665663, 150665671, 150665689, 150665944, 150665952, 150665986, 150665994, 150666017, 150666025, 150666033, 150666075, 150666124, 150666158, 150666166, 150666190, 150666215, 150666223, 150666231, 150666348, 150666356, 150666364, 150666372, 150666380, 150666398, 150666497, 150666504, 150666512, 150666520, 150666538, 150666546, 150666554, 150666562, 150666570, 150666588, 150666611, 150666637, 150666900, 150666950, 150666968, 150666976, 150666984, 150666992, 150667007, 150667015, 150667023, 150667065, 150667081, 150667099, 150667106, 150667114, 150667130, 150667156, 150667172, 150667180, 150667213, 150667289, 150667362, 150667370, 150667388, 150667396, 150667445, 150667487, 150667495, 150667544, 150667601, 150667619, 150667627, 150667635, 150667677, 150667685, 150667734, 150667742, 150667924, 150667932, 150667958, 150667974, 150667982, 150667990, 150668005, 150668013, 150668021, 150668039, 150668071, 150668089, 150668328, 150668336, 150668344, 150668352, 150668360, 150668378, 150668427, 150668443, 150668451, 150668469, 150668485, 150668500, 150668518, 150668526, 150668740, 150668758, 150668774, 150668782, 150668790, 150668807, 150668815, 150668831, 150668857, 150668865, 150668899, 150668914, 150668998, 150669003, 150669011, 150669029, 150669037, 150669045, 150669053, 150669079, 150669087, 150669095, 150669110, 150669128, 150669136, 150669144, 150669194, 150669201, 150669219, 150669227, 150669235, 150669293, 150669300, 150669318, 150669326, 150669334, 150669342, 150669350, 150669532, 150669540, 150669566, 150669574, 150669582, 150669590, 150669615, 150669623, 150669631, 150669649, 150669657, 150669665, 150669681, 150669706, 150669722, 150669730, 150669748, 150669839, 150669904, 150669962, 150669988, 150670026, 150670034, 150670042, 150670050, 150670068, 150670076, 150670084, 150670092, 150670109, 150670117, 150670141, 150670266, 150670274, 150670290, 150670307, 150670315, 150670323, 150670331, 150670373, 150670414, 150670448, 150670456, 150670464, 150670472, 150670498, 150670505, 150670844, 150670878, 150670886, 150670927, 150670969, 150670977, 150670993, 150671016, 150671024, 150671040, 150671222, 150671248, 150671305, 150671313, 150671321, 150671339, 150671347, 150671355, 150671404, 150671420, 150671438, 150671496, 150671511, 150671652, 150671727, 150671769, 150671785, 150671793, 150671800, 150671818, 150671826, 150671892, 150671917, 150671925, 150671967, 150671975, 150671991, 150672139, 150672147, 150672155, 150672163, 150672254, 150672303, 150672329, 150672345, 150672353, 150672460, 150672486, 150672494, 150672535, 150672551, 150672577, 150672717, 150672741, 150672759, 150672767, 150672783, 150672791, 150672808, 150672816, 150672824, 150672832, 150672858, 150672874, 150672882, 150673278, 150673319, 150673335, 150673369, 150673377, 150673393, 150673426, 150673434, 150673442, 150673468, 150673476, 150673484, 150673517, 150673525, 150673799, 150673806, 150673814, 150673822, 150673830, 150673848, 150673864, 150673872, 150673898, 150673905, 150673913, 150673921, 150673947, 150673989, 150674002, 150674010, 150674036, 150674044, 150674052, 150674060, 150674078, 150674094, 150674101, 150674292, 150674317, 150674333, 150674375, 150674383, 150674408, 150674416, 150674424, 150674432, 150674440, 150674474, 1506744755, 150674482, 150674523, 150674713, 150674721, 150674747, 150674797, 150674846, 150674862, 150674870, 150674888, 150674903, 150674929, 150674937, 150674945, 150674953, 150674961, 150674979, 150674987, 150674995, 150675000, 150675018, 150675026, 150675034, 150675068, 150675076, 150675084, 150675092, 150675480, 150675513, 150675521, 150675604, 150675612, 150675638, 150675696, 150675703, 150675711, 150675729, 150675745, 150675753, 150675761, 150675779, 150675787, 150675795, 150675802, 150675810, 150675828, 150675836, 150675852, 150675860, 150675878, 150675894, 150675901, 150675919, 150675927, 150675935, 150675943, 150675951, 150675969, 150675977, 150675985, 150675993, 150676149, 150676181, 150676256, 150676264, 150676272, 150676280, 150676298, 150676305, 150676313, 150676321, 150676339, 150676347, 150676355, 150676363, 150676371, 150676389, 150676412, 150676420, 150676496, 150676503, 150676511, 150676529, 150676537, 150676545, 150676561, 150676602, 150676628, 150676636, 150676644, 150676652, 150676660, 150676678, 150676686, 150676701, 150676719, 150676727, 150676743, 150676777, 150677014, 150677030, 150677048, 150677064, 150677080, 150677098, 150677139, 150677147, 150677155, 150677163, 150677171, 150677189, 150677197, 150677204, 150677212, 150677220, 150677238, 150677246, 150677254, 150677262, 150677270, 150677303, 150677311, 150677329, 150677337, 150677345, 150677353, 150677395, 150677402, 150677410, 150677428, 150677436, 150677642, 150677650, 150677676, 150677684, 150677692, 150677709, 150677717, 150677725, 150677733, 150677741, 150677767, 150677775, 150677824, 150677858, 150678377, 150678385, 150678393, 150678442, 150678468, 150678484, 150678517, 150678525, 150678541, 150678545, 150678559, 150678567, 150678583, 150678591, 150678608, 150678616, 150678625, 150678658, 150678674, 150678682, 150678690, 150678707, 150678723, 150678898, 150678921, 150678939, 150678947, 150678963, 150678971, 150678997, 150679002, 150679010, 150679028, 150679036, 150679044, 150679078, 150679094, 150679101, 150679119, 150679127, 150679143, 150679151, 150679169, 150679177, 150679185, 150679193, 150679200, 150679218, 150679234, 150679250, 150679383, 150679391, 150679408, 150679416, 150679432, 150679440, 150679474, 150679523, 150679531, 150679557, 150679565, 150679573, 150679581, 150679622, 150679630, 150679648, 150679656, 150679664, 150679698, 150679789, 150679797, 150679804) OR ACCTNBR IN (150679812, 150679820, 150679838, 150679854, 150679862, 150680091, 150680116, 150680124, 150680356, 150680405, 150680421, 150680439, 150680455, 150680471, 150680497, 150680504, 150680512, 150680538, 150680554, 150680562, 150680588, 150680596, 150680603, 150680611, 150680637, 150680794, 150680801, 150680819, 150680827, 150680835, 150680843, 150680851, 150680869, 150680877, 150680885, 150680918, 150680934, 150680942, 150680950, 150680984, 150680992, 150681015, 150681031, 150681049, 150681057, 150681354, 150681370, 150681388, 150681411, 150681479, 150681536, 150681544, 150681552, 150681578, 150681586, 150681594, 150681627, 150681643, 150681651, 150681833, 150681841, 150681924, 150681940, 150681958, 150681974, 150681982, 150681990, 150682021, 150682039, 150682104, 150682170, 150682196, 150682203, 150682229, 150682237, 150682245, 150682302, 150682336, 150682617, 150682675, 150682691, 150682708, 150682774, 150682782, 150682790, 150682807, 150682815, 150683227, 150683235, 150683277, 150683293, 150683368, 150683392, 150683409, 150683425, 150683433, 150683475, 150683532, 150683699, 150683706, 150683714, 150683722, 150683764, 150683772, 150683863, 150683904, 150683920, 150683946, 150683954, 150683962, 150683970, 150683988, 150683996, 150684027, 150684069, 150684374, 150684382, 150684390, 150684415, 150684423, 150684431, 150684449, 150684457, 150684473, 150684499, 150684514, 150684530, 150684548, 150684556, 150684564, 150684572, 150684671, 150684845, 150684861, 150684879, 150684887, 150684895, 150684902, 150684910, 150684944, 150684952, 150684978, 150684986, 150684994, 150685009, 150685059, 150685091, 150685108, 150685116, 150685124, 150685132, 150685158, 150685166, 150685182, 150685190, 150685299, 150685306, 150685314, 150685330, 150685348, 150685364, 150685405, 150685447, 150685463, 150685512, 150685538, 150685546, 150685562, 150685570, 150685603, 150685611, 150685629, 150685637, 150685645, 150685653, 150685661, 150685950, 150685976, 150685984, 150686015, 150686023, 150686031, 150686057, 150686081, 150686263, 150686271, 150686312, 150686320, 150686346, 150686354, 150686370, 150686396, 150686403, 150686411, 150686461, 150686479, 150686487, 150686669, 150686677, 150686685, 150686693, 150686700, 150686718, 150686723, 150686734, 150686742, 150686750, 150686768, 150686776, 150686841, 150686859, 150686867, 150686908, 150686916, 150686924, 150687005, 150687013, 150687021, 150687039, 150687047, 150687055, 150687089, 150687097, 150687104, 150687112, 150687146, 150687287, 150687302, 150687310, 150687328, 150687336, 150687344, 150687352, 150687360, 150687378, 150687386, 150687394, 150687419, 150687443, 150687477, 150687485, 150687584, 150687609, 150687617, 150687625, 150687659, 150687831, 150687849, 150687873, 150687881, 150687899, 150687906, 150687914, 150687922, 150687930, 150687980, 150688003, 150688011, 150688029, 150688037, 150688136, 150688144, 150688152, 150688178, 150688540, 150688590, 150688607, 150688615, 150688623, 150688631, 150688649, 150688665, 150688699, 150688730, 150688748, 150688756, 150688798, 150688805, 150688813, 150688821, 150688855, 150688863, 150688889, 150688897, 150688920, 150688938, 150688946, 150689142, 150689233, 150689241, 150689259, 150689267, 150689308, 150689316, 150689324, 150689332, 150689340, 150689366, 150689390, 150689407, 150689415, 150689530, 150689548, 150689605, 150689647, 150689671, 150689704, 150689712, 150689720, 150689738, 150689746, 150689754, 150689762, 150689770, 150689788, 150689796, 150689829, 150689837, 150689845, 150689853, 150689861, 150689879, 150689887, 150689902, 150689910, 150689928, 150689936, 150689944, 150689978, 150690048, 150690074, 150690090, 150690107, 150690123, 150690157, 150690199, 150690214, 150690256, 150690264, 150690321, 150690339, 150690355, 150690363, 150690371, 150690553, 150690561, 150690579, 150690589, 150690595, 150690777, 150690800, 150690959, 150691014, 150691022, 150691056, 150691098, 150691105, 150691139, 150691262, 150691270, 150691329, 150691337, 150691345, 150691361, 150691395, 150691402, 150691410, 150691585, 150691593, 150691600, 150691618, 150691626, 150691634, 150691692, 150691709, 150691717, 150691725, 150691741, 150691759, 150691767, 150691775, 150691783, 150691791, 150691808, 150691824, 150691840, 150691858, 150692038, 150692046, 150692054, 150692062, 150692070, 150692103, 150692145, 150692161, 150692195, 150692210, 150692278, 150692294, 150692301, 150692327, 150692335, 150692377, 150692385, 150692418, 150692426, 150692484, 150692517, 150692682, 150692898, 150693002, 150693010, 150693044, 150693052, 150693086, 150693094, 150693101, 150693127, 150693359, 150693367, 150693375, 150693383, 150693573, 150693581, 150693599, 150693606, 150693630, 150693648, 150693656, 150693664, 150693672, 150693721, 150693846, 150693854, 150693870, 150693896, 150693903, 150693911, 150694109, 150694159, 150694175, 150694191, 150694240, 150694258, 150694282, 150694547, 150694555, 150694563, 150694571, 150694589, 150694597, 150694604, 150694612, 150694620, 150694638, 150694662, 150694670, 150694688, 150694703, 150694711, 150694761, 150694779, 150694787, 150694836, 150694844, 150694878, 150694886, 150694985, 150694993, 150695016, 150695024, 150695389, 150695397, 150695404, 150695412, 150695420, 150695454, 150695652, 150695686, 150695727, 150695735, 150695743, 150695751, 150695769, 150695777, 150695785, 150695793, 150695800, 150695826, 150695842, 150695850, 150695991, 150696006, 150696014, 150696022, 150696048, 150696056, 150696064, 150696072, 150696080, 150696098, 150696105, 150696171, 150696303, 150696311, 150696329, 150696337, 150696387, 150696395, 150696494, 150696618, 150696634, 150696650, 150696668, 150696676, 150696684, 150696692, 150696717, 150696725, 150696733, 150696741, 150696759, 150696775, 150696783, 150696791, 150696808, 150696816, 150696824, 150696832, 150696973, 150696981, 150697012, 150697137, 150697260, 150697286, 150697294, 150697301, 150697319, 150697327, 150697335, 150697351, 150697369, 150697434, 150697567, 150697658, 150697674, 150697690, 150697707, 150697715, 150697731, 150697749, 150697773, 150697799, 150697806, 150698341, 150698367, 150698375, 150698391, 150698408, 150698424, 150698432, 150698440, 150698458, 150698474, 150698482, 150698490, 150698507, 150698523, 150698531, 150698549, 150698573, 150698581, 150698599, 150698606, 150698614, 150698622, 150698630, 150698648, 150698656, 150698664, 150698672, 150698680, 150698870, 150698888, 150698903, 150698953, 150698979, 150698995, 150699000, 150699018, 150699042, 150699068, 150699084, 150699109, 150699117, 150699125, 150699133, 150699141, 150699167, 150699175, 150699183, 150699191, 150699208, 150699216, 150699224, 150699232, 150699240, 150699258, 150699266, 150699331, 150699422, 150699480, 150699498, 150699505, 150699521, 150699539, 150699547, 150699571, 150699589, 150699597, 150699604, 150699612, 150699620, 150699646, 150699654, 150699696, 150699737, 150699745, 150699753, 150699787, 150699795, 150699802, 150699810, 150699828, 150699836, 150699844, 150699927, 150700112, 150700120, 150700138, 150700245, 150700287, 150700295, 150700336, 150700344, 150700352, 150700609, 150700667, 150700675, 150700683, 150700708, 150700724, 150700740, 150700766, 150700774, 150700807, 150700823, 150700831, 150700849, 150700857, 150700865, 150700873, 150700881, 150700906, 150700914, 150700980, 150700998, 150701128, 150701136, 150701152, 150701277, 150701285, 150701293, 150701300, 150701318, 150701326, 150701334, 150701342, 150701350, 150701368, 150701376, 150701384, 150701392, 150701409, 150701417, 150701425, 150701441, 150701459, 150701467, 150701623, 150701748, 150701759, 150701764, 150701772, 150701780, 150701798, 150701805, 150701813, 150701839, 150701847, 150701863, 150701871, 150701904, 150701912, 150701938, 150701946, 150701954, 150701970, 150701988, 150702001, 150702019, 150702035, 150702043, 150702051, 150702069, 150702423, 150702431, 150702449, 150702522, 150702530, 150702564, 150702580, 150702605, 150702613, 150702621, 150702639, 150702655, 150702663, 150702671, 150702689, 150702697, 150702704, 150702879, 150702887, 150702895, 150702902, 150702910, 150702928, 150702936, 150702944, 150702952, 150702960, 150703033, 150703041, 150703059, 150703067, 150703075, 150703091, 150703108, 150703132, 150703257, 150703265, 150703330, 150703348, 150703356, 150703364, 150703380, 150703421, 150703439, 150703447, 150703455, 150703463, 150703489, 150703497, 150703520, 150703546, 150703554, 150703562, 150703570, 150703588, 150703596, 150703603, 150703637, 150703778, 150703801, 150703835, 150703869, 150703877, 150703885, 150703893, 150703918, 150704007, 150704015, 150704049, 150704057, 150704073, 150704081, 150704247, 150704263, 150704271, 15070428, 150704304, 150704312, 150704346, 150704354, 150704396, 150704411, 150704429, 150704461, 150704693, 150704700, 150704718, 150704734, 150704792, 150704817, 150704859, 150704883, 150705344, 150705386, 150705394, 150705435, 150705469, 150705493, 150705500, 150705534, 150705550, 150706029, 150706045, 150706095, 150706102, 150706110, 150706128, 150706136, 150706144, 150706152, 150706160, 150706178, 150706186, 150706194, 150706201, 150706219, 150706227, 150706235, 150706251, 150706269, 150706475, 150706483, 150706508, 150706516, 150706524, 150706532, 150706540, 150706558, 150706566, 150706574, 150706582, 150706590, 150706665, 150706699, 150706714, 150706722, 150706730, 150706756, 150706772, 150706780, 150706798, 150706962, 150707043, 150707077, 150707085, 150707093, 150707100, 150707118, 150707126, 150707134, 150707142, 150707150, 150707168, 150707176, 150707184, 150707192, 150707209, 150707217, 150707225, 150707233, 150707241, 150707259, 150707275, 150707283, 150707291, 150707308, 150707316, 150707324, 150707374, 150707506, 150707530, 150707548, 150707556, 150707564, 150707572, 150707580, 150707598, 150707605, 150707613, 150707621, 150707639, 150707655, 150707663, 150707671, 150707704, 150707720, 150707738, 150707754, 150707762, 150707770, 150707796, 150707803, 150707811, 150707829, 150707837, 150707845, 150707853, 150707861, 150707879, 150707910, 150707928, 150707936, 150707944, 150707952, 150708075, 150708108, 150708215, 150708223, 150708231, 150708249, 150708257, 150708273, 150708281, 150708299, 150708314, 150708322, 150708330, 150708348, 150708356, 150708728, 150708752, 150708760, 150708778, 150708786, 150708794, 150708801, 150708819, 150708827, 150708835, 150708843, 150708851, 150708869, 150708885, 150708893, 150708900, 150708918, 150708926, 150708934, 150709065, 150709073, 150709081, 150709099, 150709106, 150709114, 150709122, 150709130, 150709148, 150709156, 150709239, 150709247, 150709255, 150709263, 150709271, 150709289, 150709297, 150709304, 150709312, 150709320, 150709346, 150709354, 150709362, 150709370, 150709388, 150709396, 150709403, 150709411, 150709429, 150709437, 150709445, 150709453, 150709461, 150709479, 150709594, 150709635, 150709643, 150709669, 150709677, 150709684, 150709685, 150709693, 150709700, 150709718, 150709726, 150709734) OR ACCTNBR IN (150709742, 150709776, 150709784, 150709792, 150709809, 150709817, 150709825, 150709833, 150709841, 150709859, 150709867, 150709875, 150709883, 150709891, 150709908, 150709924, 150710153, 150710210, 150710228, 150710236, 150710244, 150710252, 150710294, 150710301, 150710319, 150710327, 150710525, 150710608, 150710616, 150710624, 150710632, 150710640, 150710674, 150710715, 150710723, 150710731, 150710749, 150710757, 150710765, 150710773, 150710781, 150711185, 150711193...(truncated)