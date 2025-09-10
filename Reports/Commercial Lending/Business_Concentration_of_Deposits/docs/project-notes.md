# 2025-08-21
Fixed this up.

Repo could still use cleaning up

The missing items on XAA are due to the accounts being closed or not included on allowed minor list

This was found in exploration notebook.

We can take the _merge right only to get XAA only and then join back active account data to see products:
- IOLTA
- Community checking
- Some personal stuff.

# 2025-08-29
Added new minors for business accounts that we missed on first pass

still needs a revamp. This will simplify pulling from directly 


# 2025-09-09
Hi Chad –

 

I know your schedule is jam packed and we are meeting on Wednesday but, in the interim I just wanted to explain to you that my report is show less fee income than your report is showing.

 

I would expect it to be the same or less but not more.  It could be less because you might be missing certain minors but, I don’t think that is the case.  I wouldn’t expect it to be more though because the fee income data on your report is directly coming from my report.  It either would match on account number or not but, I don’t know how your report is actually showing more.

 

My post ECR fee net number is $50,744.72 which I’ve proofed all the way to Accountings entry they show.

 

Your report post ECR net number is $55,727.65. This is a $4,982.93 difference.

 

Perhaps in between us meeting you’re able to put eyes on this and see what that difference is accounting for?

 

Thanks and talk soon,

Steve

---

I figured it out I think. The way I look at cycle date is to rank them in descending order. This may or may not be the most current month. For some reason, some of the accounts show up with Cycle Date end most recent for 0.0 and others just don't even list a record. I am looking at most recent month on my consolidated report rather than strictly specifying the most recent month is the only allowed one. That would make sense to me.

Can validate the delta afterward because you can take my output(full unadjusted) and then you can take steve's output - do an outer join and you should be able to see the records that show up on his and not on mine and that should be the $ diff
- XAA report will be higher. 


# 2025-09-10

Error:
---------------------------------------------------------------------------
KeyError                                  Traceback (most recent call last)
File c:\Users\w322800\Documents\gh\bcsb-prod\.venv\Lib\site-packages\pandas\core\indexes\base.py:3812, in Index.get_loc(self, key)
   3811 try:
-> 3812     return self._engine.get_loc(casted_key)
   3813 except KeyError as err:

File pandas/_libs/index.pyx:167, in pandas._libs.index.IndexEngine.get_loc()

File pandas/_libs/index.pyx:196, in pandas._libs.index.IndexEngine.get_loc()

File pandas/_libs/hashtable_class_helper.pxi:7088, in pandas._libs.hashtable.PyObjectHashTable.get_item()

File pandas/_libs/hashtable_class_helper.pxi:7096, in pandas._libs.hashtable.PyObjectHashTable.get_item()

KeyError: 'is_target_month'

The above exception was the direct cause of the following exception:

KeyError                                  Traceback (most recent call last)
File c:\Users\w322800\Documents\gh\bcsb-prod\.venv\Lib\site-packages\pandas\core\groupby\generic.py:294, in SeriesGroupBy.aggregate(self, func, engine, engine_kwargs, *args, **kwargs)
    293 try:
--> 294     return self._python_agg_general(func, *args, **kwargs)
    295 except KeyError:
    296     # KeyError raised in test_groupby.test_basic is bc the func does
    297     #  a dictionary lookup on group.name, but group name is not
    298     #  pinned in _python_agg_general, only in _aggregate_named

File c:\Users\w322800\Documents\gh\bcsb-prod\.venv\Lib\site-packages\pandas\core\groupby\generic.py:327, in SeriesGroupBy._python_agg_general(self, func, *args, **kwargs)
    326 obj = self._obj_with_exclusions
--> 327 result = self._grouper.agg_series(obj, f)
    328 res = obj._constructor(result, name=obj.name)

File c:\Users\w322800\Documents\gh\bcsb-prod\.venv\Lib\site-packages\pandas\core\groupby\ops.py:864, in BaseGrouper.agg_series(self, obj, func, preserve_dtype)
    862     preserve_dtype = True
--> 864 result = self._aggregate_series_pure_python(obj, func)
    866 npvalues = lib.maybe_convert_objects(result, try_float=False)

File c:\Users\w322800\Documents\gh\bcsb-prod\.venv\Lib\site-packages\pandas\core\groupby\ops.py:885, in BaseGrouper._aggregate_series_pure_python(self, obj, func)
    884 for i, group in enumerate(splitter):
--> 885     res = func(group)
    886     res = extract_result(res)

File c:\Users\w322800\Documents\gh\bcsb-prod\.venv\Lib\site-packages\pandas\core\groupby\generic.py:324, in SeriesGroupBy._python_agg_general.<locals>.<lambda>(x)
    323     warn_alias_replacement(self, orig_func, alias)
--> 324 f = lambda x: func(x, *args, **kwargs)
    326 obj = self._obj_with_exclusions

Cell In[18], line 38, in create_account_summary_alternative.<locals>.<lambda>(x)
     32 # Aggregate using conditional sums/filters
     33 summary = (xaa_data
     34         .groupby('Debit Account Number')
     35         .agg({
     36             # Latest month aggregations (filtered to target month)
     37             'Analyzed Charges': [
---> 38                 lambda x: x[xaa_data.loc[x.index, 'is_target_month']].sum(),  # Assuming global scope or pass as kwarg; adjust if needed
     39                 lambda x: x[xaa_data.loc[x.index, 'is_trailing_12m']].sum(),
     40             ],
     41             'Combined Result for Settlement Period': [
     42                 lambda x: x[xaa_data.loc[x.index, 'is_target_month']].sum(),
     43                 lambda x: x[xaa_data.loc[x.index, 'is_trailing_12m']].sum()
     44             ],
     45             'Earnings Credit Rate': [
     46                 lambda x: x[xaa_data.loc[x.index, 'is_target_month']].mean(),
     47                 lambda x: x[xaa_data.loc[x.index, 'is_trailing_12m']].mean()
     48             ],
     49             'Primary Officer Name': 'first',
     50             'Secondary Officer Name': 'first',
     51             'Treasury Officer Name': 'first'
     52         })
     53         .reset_index())
     55 # Flatten column names

File c:\Users\w322800\Documents\gh\bcsb-prod\.venv\Lib\site-packages\pandas\core\indexing.py:1184, in _LocationIndexer.__getitem__(self, key)
   1183         return self.obj._get_value(*key, takeable=self._takeable)
-> 1184     return self._getitem_tuple(key)
   1185 else:
   1186     # we by definition only have the 0th axis

File c:\Users\w322800\Documents\gh\bcsb-prod\.venv\Lib\site-packages\pandas\core\indexing.py:1368, in _LocIndexer._getitem_tuple(self, tup)
   1367     tup = self._expand_ellipsis(tup)
-> 1368     return self._getitem_lowerdim(tup)
   1370 # no multi-index, so validate all of the indexers

File c:\Users\w322800\Documents\gh\bcsb-prod\.venv\Lib\site-packages\pandas\core\indexing.py:1065, in _LocationIndexer._getitem_lowerdim(self, tup)
   1062 if is_label_like(key):
   1063     # We don't need to check for tuples here because those are
   1064     #  caught by the _is_nested_tuple_indexer check above.
-> 1065     section = self._getitem_axis(key, axis=i)
   1067     # We should never have a scalar section here, because
   1068     #  _getitem_lowerdim is only called after a check for
   1069     #  is_scalar_access, which that would be.

File c:\Users\w322800\Documents\gh\bcsb-prod\.venv\Lib\site-packages\pandas\core\indexing.py:1431, in _LocIndexer._getitem_axis(self, key, axis)
   1430 self._validate_key(key, axis)
-> 1431 return self._get_label(key, axis=axis)

File c:\Users\w322800\Documents\gh\bcsb-prod\.venv\Lib\site-packages\pandas\core\indexing.py:1381, in _LocIndexer._get_label(self, label, axis)
   1379 def _get_label(self, label, axis: AxisInt):
   1380     # GH#5567 this will fail if the label is not present in the axis.
-> 1381     return self.obj.xs(label, axis=axis)

File c:\Users\w322800\Documents\gh\bcsb-prod\.venv\Lib\site-packages\pandas\core\generic.py:4306, in NDFrame.xs(self, key, axis, level, drop_level)
   4305 if drop_level:
-> 4306     return self[key]
   4307 index = self.columns

File c:\Users\w322800\Documents\gh\bcsb-prod\.venv\Lib\site-packages\pandas\core\frame.py:4107, in DataFrame.__getitem__(self, key)
   4106     return self._getitem_multilevel(key)
-> 4107 indexer = self.columns.get_loc(key)
   4108 if is_integer(indexer):

File c:\Users\w322800\Documents\gh\bcsb-prod\.venv\Lib\site-packages\pandas\core\indexes\base.py:3819, in Index.get_loc(self, key)
   3818         raise InvalidIndexError(key)
-> 3819     raise KeyError(key) from err
   3820 except TypeError:
   3821     # If we have a listlike key, _check_indexing_error will raise
   3822     #  InvalidIndexError. Otherwise we fall through and re-raise
   3823     #  the TypeError.

KeyError: 'is_target_month'

During handling of the above exception, another exception occurred:

KeyError                                  Traceback (most recent call last)
File c:\Users\w322800\Documents\gh\bcsb-prod\.venv\Lib\site-packages\pandas\core\indexes\base.py:3812, in Index.get_loc(self, key)
   3811 try:
-> 3812     return self._engine.get_loc(casted_key)
   3813 except KeyError as err:

File pandas/_libs/index.pyx:167, in pandas._libs.index.IndexEngine.get_loc()

File pandas/_libs/index.pyx:196, in pandas._libs.index.IndexEngine.get_loc()

File pandas/_libs/hashtable_class_helper.pxi:7088, in pandas._libs.hashtable.PyObjectHashTable.get_item()

File pandas/_libs/hashtable_class_helper.pxi:7096, in pandas._libs.hashtable.PyObjectHashTable.get_item()

KeyError: 'is_target_month'

The above exception was the direct cause of the following exception:

KeyError                                  Traceback (most recent call last)
Cell In[18], line 85
     82     return summary[column_order]
     84 # %%
---> 85 summarized_xaa = create_account_summary_alternative(xaa_data, date_col='Cycle End Date')

Cell In[18], line 35, in create_account_summary_alternative(xaa_data, date_col, target_previous_month)
     30 is_trailing_12m = xaa_data[date_col] >= cutoff_date
     32 # Aggregate using conditional sums/filters
     33 summary = (xaa_data
     34         .groupby('Debit Account Number')
---> 35         .agg({
     36             # Latest month aggregations (filtered to target month)
     37             'Analyzed Charges': [
     38                 lambda x: x[xaa_data.loc[x.index, 'is_target_month']].sum(),  # Assuming global scope or pass as kwarg; adjust if needed
     39                 lambda x: x[xaa_data.loc[x.index, 'is_trailing_12m']].sum(),
     40             ],
     41             'Combined Result for Settlement Period': [
     42                 lambda x: x[xaa_data.loc[x.index, 'is_target_month']].sum(),
     43                 lambda x: x[xaa_data.loc[x.index, 'is_trailing_12m']].sum()
     44             ],
     45             'Earnings Credit Rate': [
     46                 lambda x: x[xaa_data.loc[x.index, 'is_target_month']].mean(),
     47                 lambda x: x[xaa_data.loc[x.index, 'is_trailing_12m']].mean()
     48             ],
     49             'Primary Officer Name': 'first',
     50             'Secondary Officer Name': 'first',
     51             'Treasury Officer Name': 'first'
     52         })
     53         .reset_index())
     55 # Flatten column names
     56 summary.columns = [
     57     'Debit Account Number',
     58     'Latest_Month_Analyzed_Charges',
   (...)     66     'Treasury_Officer_Name_XAA'
     67 ]

File c:\Users\w322800\Documents\gh\bcsb-prod\.venv\Lib\site-packages\pandas\core\groupby\generic.py:1432, in DataFrameGroupBy.aggregate(self, func, engine, engine_kwargs, *args, **kwargs)
   1429     kwargs["engine_kwargs"] = engine_kwargs
   1431 op = GroupByApply(self, func, args=args, kwargs=kwargs)
-> 1432 result = op.agg()
   1433 if not is_dict_like(func) and result is not None:
   1434     # GH #52849
   1435     if not self.as_index and is_list_like(func):

File c:\Users\w322800\Documents\gh\bcsb-prod\.venv\Lib\site-packages\pandas\core\apply.py:190, in Apply.agg(self)
    187     return self.apply_str()
    189 if is_dict_like(func):
--> 190     return self.agg_dict_like()
    191 elif is_list_like(func):
    192     # we require a list, but not a 'str'
    193     return self.agg_list_like()

File c:\Users\w322800\Documents\gh\bcsb-prod\.venv\Lib\site-packages\pandas\core\apply.py:423, in Apply.agg_dict_like(self)
    415 def agg_dict_like(self) -> DataFrame | Series:
    416     """
    417     Compute aggregation in the case of a dict-like argument.
    418 
   (...)    421     Result of aggregation.
    422     """
--> 423     return self.agg_or_apply_dict_like(op_name="agg")

File c:\Users\w322800\Documents\gh\bcsb-prod\.venv\Lib\site-packages\pandas\core\apply.py:1603, in GroupByApply.agg_or_apply_dict_like(self, op_name)
   1598     kwargs.update({"engine": engine, "engine_kwargs": engine_kwargs})
   1600 with com.temp_setattr(
   1601     obj, "as_index", True, condition=hasattr(obj, "as_index")
   1602 ):
-> 1603     result_index, result_data = self.compute_dict_like(
   1604         op_name, selected_obj, selection, kwargs
   1605     )
   1606 result = self.wrap_results_dict_like(selected_obj, result_index, result_data)
   1607 return result

File c:\Users\w322800\Documents\gh\bcsb-prod\.venv\Lib\site-packages\pandas\core\apply.py:496, in Apply.compute_dict_like(self, op_name, selected_obj, selection, kwargs)
    493         results += key_data
    494 else:
    495     # key used for column selection and output
--> 496     results = [
    497         getattr(obj._gotitem(key, ndim=1), op_name)(how, **kwargs)
    498         for key, how in func.items()
    499     ]
    500     keys = list(func.keys())
    502 return keys, results

File c:\Users\w322800\Documents\gh\bcsb-prod\.venv\Lib\site-packages\pandas\core\apply.py:497, in <listcomp>(.0)
    493         results += key_data
    494 else:
    495     # key used for column selection and output
    496     results = [
--> 497         getattr(obj._gotitem(key, ndim=1), op_name)(how, **kwargs)
    498         for key, how in func.items()
    499     ]
    500     keys = list(func.keys())
    502 return keys, results

File c:\Users\w322800\Documents\gh\bcsb-prod\.venv\Lib\site-packages\pandas\core\groupby\generic.py:257, in SeriesGroupBy.aggregate(self, func, engine, engine_kwargs, *args, **kwargs)
    255 kwargs["engine"] = engine
    256 kwargs["engine_kwargs"] = engine_kwargs
--> 257 ret = self._aggregate_multiple_funcs(func, *args, **kwargs)
    258 if relabeling:
    259     # columns is not narrowed by mypy from relabeling flag
    260     assert columns is not None  # for mypy

File c:\Users\w322800\Documents\gh\bcsb-prod\.venv\Lib\site-packages\pandas\core\groupby\generic.py:362, in SeriesGroupBy._aggregate_multiple_funcs(self, arg, *args, **kwargs)
    360     for idx, (name, func) in enumerate(arg):
    361         key = base.OutputKey(label=name, position=idx)
--> 362         results[key] = self.aggregate(func, *args, **kwargs)
    364 if any(isinstance(x, DataFrame) for x in results.values()):
    365     from pandas import concat

File c:\Users\w322800\Documents\gh\bcsb-prod\.venv\Lib\site-packages\pandas\core\groupby\generic.py:299, in SeriesGroupBy.aggregate(self, func, engine, engine_kwargs, *args, **kwargs)
    294     return self._python_agg_general(func, *args, **kwargs)
    295 except KeyError:
    296     # KeyError raised in test_groupby.test_basic is bc the func does
    297     #  a dictionary lookup on group.name, but group name is not
    298     #  pinned in _python_agg_general, only in _aggregate_named
--> 299     result = self._aggregate_named(func, *args, **kwargs)
    301     warnings.warn(
    302         "Pinning the groupby key to each group in "
    303         f"{type(self).__name__}.agg is deprecated, and cases that "
   (...)    308         stacklevel=find_stack_level(),
    309     )
    311     # result is a dict whose keys are the elements of result_index

File c:\Users\w322800\Documents\gh\bcsb-prod\.venv\Lib\site-packages\pandas\core\groupby\generic.py:461, in SeriesGroupBy._aggregate_named(self, func, *args, **kwargs)
    455 for name, group in self._grouper.get_iterator(
    456     self._obj_with_exclusions, axis=self.axis
    457 ):
    458     # needed for pandas/tests/groupby/test_groupby.py::test_basic_aggregations
    459     object.__setattr__(group, "name", name)
--> 461     output = func(group, *args, **kwargs)
    462     output = ops.extract_result(output)
    463     if not initialized:
    464         # We only do this validation on the first iteration

Cell In[18], line 38, in create_account_summary_alternative.<locals>.<lambda>(x)
     30 is_trailing_12m = xaa_data[date_col] >= cutoff_date
     32 # Aggregate using conditional sums/filters
     33 summary = (xaa_data
     34         .groupby('Debit Account Number')
     35         .agg({
     36             # Latest month aggregations (filtered to target month)
     37             'Analyzed Charges': [
---> 38                 lambda x: x[xaa_data.loc[x.index, 'is_target_month']].sum(),  # Assuming global scope or pass as kwarg; adjust if needed
     39                 lambda x: x[xaa_data.loc[x.index, 'is_trailing_12m']].sum(),
     40             ],
     41             'Combined Result for Settlement Period': [
     42                 lambda x: x[xaa_data.loc[x.index, 'is_target_month']].sum(),
     43                 lambda x: x[xaa_data.loc[x.index, 'is_trailing_12m']].sum()
     44             ],
     45             'Earnings Credit Rate': [
     46                 lambda x: x[xaa_data.loc[x.index, 'is_target_month']].mean(),
     47                 lambda x: x[xaa_data.loc[x.index, 'is_trailing_12m']].mean()
     48             ],
     49             'Primary Officer Name': 'first',
     50             'Secondary Officer Name': 'first',
     51             'Treasury Officer Name': 'first'
     52         })
     53         .reset_index())
     55 # Flatten column names
     56 summary.columns = [
     57     'Debit Account Number',
     58     'Latest_Month_Analyzed_Charges',
   (...)     66     'Treasury_Officer_Name_XAA'
     67 ]

File c:\Users\w322800\Documents\gh\bcsb-prod\.venv\Lib\site-packages\pandas\core\indexing.py:1184, in _LocationIndexer.__getitem__(self, key)
   1182     if self._is_scalar_access(key):
   1183         return self.obj._get_value(*key, takeable=self._takeable)
-> 1184     return self._getitem_tuple(key)
   1185 else:
   1186     # we by definition only have the 0th axis
   1187     axis = self.axis or 0

File c:\Users\w322800\Documents\gh\bcsb-prod\.venv\Lib\site-packages\pandas\core\indexing.py:1368, in _LocIndexer._getitem_tuple(self, tup)
   1366 with suppress(IndexingError):
   1367     tup = self._expand_ellipsis(tup)
-> 1368     return self._getitem_lowerdim(tup)
   1370 # no multi-index, so validate all of the indexers
   1371 tup = self._validate_tuple_indexer(tup)

File c:\Users\w322800\Documents\gh\bcsb-prod\.venv\Lib\site-packages\pandas\core\indexing.py:1065, in _LocationIndexer._getitem_lowerdim(self, tup)
   1061 for i, key in enumerate(tup):
   1062     if is_label_like(key):
   1063         # We don't need to check for tuples here because those are
   1064         #  caught by the _is_nested_tuple_indexer check above.
-> 1065         section = self._getitem_axis(key, axis=i)
   1067         # We should never have a scalar section here, because
   1068         #  _getitem_lowerdim is only called after a check for
   1069         #  is_scalar_access, which that would be.
   1070         if section.ndim == self.ndim:
   1071             # we're in the middle of slicing through a MultiIndex
   1072             # revise the key wrt to `section` by inserting an _NS

File c:\Users\w322800\Documents\gh\bcsb-prod\.venv\Lib\site-packages\pandas\core\indexing.py:1431, in _LocIndexer._getitem_axis(self, key, axis)
   1429 # fall thru to straight lookup
   1430 self._validate_key(key, axis)
-> 1431 return self._get_label(key, axis=axis)

File c:\Users\w322800\Documents\gh\bcsb-prod\.venv\Lib\site-packages\pandas\core\indexing.py:1381, in _LocIndexer._get_label(self, label, axis)
   1379 def _get_label(self, label, axis: AxisInt):
   1380     # GH#5567 this will fail if the label is not present in the axis.
-> 1381     return self.obj.xs(label, axis=axis)

File c:\Users\w322800\Documents\gh\bcsb-prod\.venv\Lib\site-packages\pandas\core\generic.py:4306, in NDFrame.xs(self, key, axis, level, drop_level)
   4304 if axis == 1:
   4305     if drop_level:
-> 4306         return self[key]
   4307     index = self.columns
   4308 else:

File c:\Users\w322800\Documents\gh\bcsb-prod\.venv\Lib\site-packages\pandas\core\frame.py:4107, in DataFrame.__getitem__(self, key)
   4105 if self.columns.nlevels > 1:
   4106     return self._getitem_multilevel(key)
-> 4107 indexer = self.columns.get_loc(key)
   4108 if is_integer(indexer):
   4109     indexer = [indexer]

File c:\Users\w322800\Documents\gh\bcsb-prod\.venv\Lib\site-packages\pandas\core\indexes\base.py:3819, in Index.get_loc(self, key)
   3814     if isinstance(casted_key, slice) or (
   3815         isinstance(casted_key, abc.Iterable)
   3816         and any(isinstance(x, slice) for x in casted_key)
   3817     ):
   3818         raise InvalidIndexError(key)
-> 3819     raise KeyError(key) from err
   3820 except TypeError:
   3821     # If we have a listlike key, _check_indexing_error will raise
   3822     #  InvalidIndexError. Otherwise we fall through and re-raise
   3823     #  the TypeError.
   3824     self._check_indexing_error(key)

KeyError: 'is_target_month'


Code:
# %%
import os
import sys
from pathlib import Path

# Navigate to project root (equivalent to cd ..)
project_dir = Path(__file__).parent.parent if '__file__' in globals() else Path.cwd().parent
os.chdir(project_dir)

# Add src directory to Python path for imports
src_dir = project_dir / "src"
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

# Set environment for dev testing
os.environ['REPORT_ENV'] = 'dev'

# %%

"""
Main Entry Point
"""
from pathlib import Path

import pandas as pd # type: ignore

import cdutils.pkey_sqlite # type: ignore
import cdutils.filtering # type: ignore
import cdutils.input_cleansing # type: ignore
import cdutils.cmo_append # type: ignore
import src.add_fields
import src.core_transform
import src.output_to_excel
from src._version import __version__
import src.output_to_excel_multiple_sheets
import cdutils.distribution # type: ignore
from datetime import datetime
from dateutil.relativedelta import relativedelta

# def main(production_flag: bool=False):
#     if production_flag:
#         BASE_PATH = Path(r'\\00-DA1\Home\Share\Line of Business_Shared Services')
#         assert "prod" in __version__, (f"Cannot run in production mode without 'prod' in the __version__")
#     else:
#         BASE_PATH = Path('.')



# %%
# Get staging data from the daily deposit update. View dev section of documentation for more detail
INPUT_PATH = Path(r"\\00-da1\Home\Share\Data & Analytics Initiatives\Project Management\Data_Analytics\Daily_Deposit_Update\Production\output\DailyDeposit_staging.xlsx")
data = pd.read_excel(INPUT_PATH)

# Add portfolio key
data = cdutils.pkey_sqlite.add_pkey(data)

# Add int rate
data = src.add_fields.add_noteintrate(data)


# Custom list of minors (Business Deposits)
minors = [
    'CK24', # 1st Business Checking
    'CK12', # Business Checking
    'CK25', # Simple Business Checking
    'CK30', # Business Elite Money Market
    'CK19', # Business Money Market
    'CK22', # Business Premium Plus MoneyMkt
    'CK23', # Premium Business Checking
    'CK40', # Community Assoc Reserve
    'CD67', # Commercial Negotiated Rate
    'CD01', # 1 Month Business CD
    'CD07', # 3 Month Business CD
    'CD17', # 6 Month Business CD
    'CD31', # 1 Year Business CD
    'CD35', # 1 Year Business CD
    'CD37', # 18 Month Business CD
    'CD38', # 2 Year Business CD
    'CD50', # 3 Year Business CD
    'CD53', # 4 Year Business CD
    'CD59', # 5 Year Business CD
    'CD76', # 9 Month Business CD
    'CD84', # 15 Month Business CD
    'CD95', # Business <12 Month Simple CD
    'CD96', # Business >12 Month Simple CD
    'CK28', # Investment Business Checking
    'CK33', # Specialty Business Checking
    'CK34', # ICS Shadow - Business - Demand
    'SV06', # Business Select High Yield
    'CK13',
    'CK15',
    'CK41'
]

# Filter to only business deposit accounts
data = cdutils.filtering.filter_to_business_deposits(data, minors)


# Add CMO
data = cdutils.cmo_append.append_cmo(data)


data_schema = {
    'noteintrate': float
}

data = cdutils.input_cleansing.enforce_schema(data, data_schema).copy()




# %%
# Exclude BCSB internal accounts
data = data[~data['ownersortname'].str.contains('BRISTOL COUNTY SAVINGS', case=False, na=False)].copy()

# %%
data



# %%
# %%







# %%
# %%
ASSETS_PATH = Path('./assets')

files = [f for f in ASSETS_PATH.iterdir() if f.is_file()]

assert len(files) == 1, f"Expected exactly 1 file in {ASSETS_PATH}, found {len(files)}."

file = files[0]
assert file.suffix == '.csv', f"Expected an excel file"

xaa_data = pd.read_csv(file)



# %%
xaa_data

# %%
xaa_data['Cycle End Date'] = pd.to_datetime(xaa_data['Cycle End Date'])

# %%
xaa_data

# %%
xaa_data_rct = xaa_data[xaa_data['Cycle End Date'] == datetime(2025, 7, 31)].copy()

# %%
xaa_data_rct['Combined Result for Settlement Period (Post-ECR)'] = xaa_data_rct['Combined Result for Settlement Period (Post-ECR)'].astype(str).replace({'\$':'',',':''}, regex=True)

# %%
xaa_data_rct['Combined Result for Settlement Period (Post-ECR)'] = pd.to_numeric(xaa_data_rct['Combined Result for Settlement Period (Post-ECR)'], errors='coerce')

# %%
xaa_data_rct['Combined Result for Settlement Period (Post-ECR)'].sum()

# %%
# %%
# xaa_data.info()

#

# %%




# # %%
# xaa_data['Analyzed Charges (Pre-ECR)'] = xaa_data['Analyzed Charges (Pre-ECR)'].str.replace('[\$,]','',regex=True)
# xaa_data['Combined Result for Settlement Period (Post-ECR + Fee-Based Total)'] = xaa_data['Combined Result for Settlement Period (Post-ECR + Fee-Based Total)'].str.replace('[\$,]','',regex=True)

# Rename to match schema from earlier
xaa_data = xaa_data.rename(columns={
    'Analyzed Charges (Pre-ECR)':'Analyzed Charges',
    'Combined Result for Settlement Period (Post-ECR)':'Combined Result for Settlement Period'
})
# fix csv formatting of float fields
cols_to_adjust = ['Analyzed Charges','Combined Result for Settlement Period']

for col in cols_to_adjust:
    xaa_data[col] = xaa_data[col].str.replace(r'[$,]','', regex=True).astype(float)

# %%
xaa_schema = {
    'Analyzed Charges':'float',
    'Combined Result for Settlement Period':'float',
    'Earnings Credit Rate':'float',
    'Debit Account Number':'str'
}
xaa_data = cdutils.input_cleansing.enforce_schema(xaa_data, xaa_schema)

# %%




# %%

from datetime import datetime, timedelta

def create_account_summary_alternative(xaa_data, date_col='cycle_date', target_previous_month=None):
    # Ensure date column is datetime
    xaa_data = xaa_data.copy()
    xaa_data[date_col] = pd.to_datetime(xaa_data[date_col])
    
    # Determine target period (previous month)
    if target_previous_month is None:
        periods = sorted(xaa_data[date_col].dt.to_period('M').unique(), reverse=True)
        if len(periods) < 2:
            raise ValueError("Not enough periods to determine previous month.")
        target_period = periods[1]
    else:
        if isinstance(target_previous_month, str):
            target_period = pd.Period(target_previous_month, freq='M')
        elif isinstance(target_previous_month, pd.Period):
            target_period = target_previous_month
        else:
            raise ValueError("target_previous_month must be a string like '2025-08' or a pd.Period.")
    
    # Filter for the target (previous) month
    is_target_month = (xaa_data[date_col].dt.year == target_period.year) & (xaa_data[date_col].dt.month == target_period.month)
    
    # Calculate trailing cutoff (12 months before the target month's end)
    target_end = target_period.to_timestamp(how='end')
    cutoff_date = target_end - relativedelta(months=12) + relativedelta(days=1)
    is_trailing_12m = xaa_data[date_col] >= cutoff_date
    
    # Aggregate using conditional sums/filters
    summary = (xaa_data
            .groupby('Debit Account Number')
            .agg({
                # Latest month aggregations (filtered to target month)
                'Analyzed Charges': [
                    lambda x: x[xaa_data.loc[x.index, 'is_target_month']].sum(),  # Assuming global scope or pass as kwarg; adjust if needed
                    lambda x: x[xaa_data.loc[x.index, 'is_trailing_12m']].sum(),
                ],
                'Combined Result for Settlement Period': [
                    lambda x: x[xaa_data.loc[x.index, 'is_target_month']].sum(),
                    lambda x: x[xaa_data.loc[x.index, 'is_trailing_12m']].sum()
                ],
                'Earnings Credit Rate': [
                    lambda x: x[xaa_data.loc[x.index, 'is_target_month']].mean(),
                    lambda x: x[xaa_data.loc[x.index, 'is_trailing_12m']].mean()
                ],
                'Primary Officer Name': 'first',
                'Secondary Officer Name': 'first',
                'Treasury Officer Name': 'first'
            })
            .reset_index())
    
    # Flatten column names
    summary.columns = [
        'Debit Account Number',
        'Latest_Month_Analyzed_Charges',
        'Trailing_12M_Analyzed_Charges',
        'Latest_Month_Combined_Result',
        'Trailing_12M_Combined_Result',
        'Latest_Month_ECR',
        'Trailing_12M_Avg_ECR',
        'Primary_Officer_Name_XAA',
        'Secondary_Officer_Name_XAA',
        'Treasury_Officer_Name_XAA'
    ]
    
    # Reorder columns
    column_order = [
        'Debit Account Number',
        'Latest_Month_Analyzed_Charges',
        'Latest_Month_Combined_Result',
        'Trailing_12M_Analyzed_Charges',
        'Trailing_12M_Combined_Result',
        'Latest_Month_ECR',
        'Trailing_12M_Avg_ECR',
        'Primary_Officer_Name_XAA',
        'Secondary_Officer_Name_XAA',
        'Treasury_Officer_Name_XAA'
    ]
    return summary[column_order]

# %%
summarized_xaa = create_account_summary_alternative(xaa_data, date_col='Cycle End Date')



# %%
# %%
summarized_xaa_schema = {
    'Primary_Officer_Name_XAA':'str',
    'Secondary_Officer_Name_XAA':'str',        
    'Treasury_Officer_Name_XAA':'str'
}
summarized_xaa = cdutils.input_cleansing.enforce_schema(summarized_xaa, summarized_xaa_schema)

# %%

# %%
summarized_xaa = summarized_xaa.rename(columns={
    'Debit Account Number':'acctnbr',

}).copy()

assert summarized_xaa['acctnbr'].is_unique, "Duplicates"




# %%





# %%
# %%
merged_data = pd.merge(data, summarized_xaa, on='acctnbr', how='left')

# %%

fill_na_column_list = [
    'Latest_Month_Analyzed_Charges',
    'Latest_Month_Combined_Result',
    'Trailing_12M_Analyzed_Charges',
    'Trailing_12M_Combined_Result',
    'Latest_Month_ECR',
    'Trailing_12M_Avg_ECR',
]
for item in fill_na_column_list:
    merged_data[item] = merged_data[item].fillna(0)


# Sort descending order of notebal
merged_data = merged_data.sort_values(by='notebal', ascending=False)

# %%
# merged_data.info()

# %%
merged_data



# %%
# This part doesn't work. Look at noteinrate, gets weird

# %%
formatted_data = src.core_transform.main_pipeline(merged_data)

# %%
formatted_data

# %%
formatted_data = formatted_data.rename(columns={
    'portfolio_key':'Portfolio Key',
    'product':'Product',
    '3Mo_AvgBal':'3Mo Avg Bal',
    'TTM_AvgBal':'TTM Avg Bal',
    'TTM_DAYS_OVERDRAWN':'TTM Days Overdrawn',
    'TTM_NSF_COUNT':'TTM NSF Count'
}).copy()


# %%
# Create summary sheet

summary_data = formatted_data[~(formatted_data['Portfolio Key'] == "") & (formatted_data['Acct No.'] == "")].copy()
summary_data = summary_data[[
    'Portfolio Key',
    'Borrower Name',
    'Account Officer',
    'Cash Management Officer',
    'Current Balance',
    'Interest Rate',
    '3Mo Avg Bal',
    'TTM Avg Bal',
    'Year Ago Balance',
    'TTM Days Overdrawn',
    'TTM NSF Count',
    'Current Mo Analyzed Fees (Pre-ECR)',
    'Current Mo Net Analyzed Fees (Post-ECR)',
    'TTM Analyzed Fees (Pre-ECR)',
    'TTM Net Analyzed Fees (Post-ECR)',
    'Current ECR'
]].copy()


# %%
# %%
# Output to excel (raw data)
# BASE_PATH = Path('.')
OUTPUT_PATH = BASE_PATH / Path('./output/business_deposits_concentration_with_xaa.xlsx')
with pd.ExcelWriter(OUTPUT_PATH, engine="openpyxl") as writer:
    formatted_data.to_excel(writer, sheet_name='Relationship Detail', index=False)
    summary_data.to_excel(writer, sheet_name='Relationship Summary', index=False)
    merged_data.to_excel(writer, sheet_name='Unformatted', index=False)


# Format excel
src.output_to_excel_multiple_sheets.format_excel_file(OUTPUT_PATH)


# Usage
# # Distribution
recipients = [
    # "chad.doorley@bcsbmail.com"
    "Hasan.Ali@bcsbmail.com",
    "steve.sherman@bcsbmail.com",
    "Michael.Patacao@bcsbmail.com",
    "Jeffrey.Pagliuca@bcsbmail.com",
    "Timothy.Chaves@bcsbmail.com",
    "Isaura.Tavares@bcsbmail.com",
    "Taylor.Tierney@bcsbmail.com",
    "Anderson.Lovos@bcsbmail.com",

]
bcc_recipients = [
    "chad.doorley@bcsbmail.com",
    "businessintelligence@bcsbmail.com"
]

prev_month = datetime.now() - relativedelta(months=1)
result = prev_month.strftime("%B %Y")

subject = f"Business Deposits + XAA Concentration Report - {result}" 
body = "Hi all, \n\nAttached is the Business Deposits + XAA Concentration Report through the most recent month end. If you have any questions, please reach out to BusinessIntelligence@bcsbmail.com\n\n"
attachment_paths = [OUTPUT_PATH]

# cdutils.distribution.email_out(
#     recipients = recipients, 
#     bcc_recipients = bcc_recipients, 
#     subject = subject, 
#     body = body, 
#     attachment_paths = attachment_paths
#     )

if __name__ == '__main__':
print(f"Starting [{__version__}]")
# main(production_flag=True)
main()
print("Complete!")



# %%






