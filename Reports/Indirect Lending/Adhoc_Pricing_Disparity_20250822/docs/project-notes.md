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



