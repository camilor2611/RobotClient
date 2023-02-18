from .flowControl.controlError import ControlExecutionAsync
from .flowControl.controlSchema import ControlSchemaAsync
from .spaces.variables import MemoryVariables
from .flowControl.log import custom_logger
from schema import Schema, And, Optional
import pandas as pd
import asyncio
import re


class TransformationPandasError(Exception):
    """Exception class from which every exception in this library will derive.
    It enables other projects using this library to catch all errors coming
    from the library with a single "except" statement
    """
    pass


class NotDataFrameOrSeries(TransformationPandasError):
    """Variable is not DataFrame or Series"""
    pass


class FailedSchema(TransformationPandasError):
    """"""
    pass


class Transformations():
    def __init__(self):
        self.__variables = MemoryVariables()

    def __get_dataframe(self, source):
        val = self.__variables.get(source)
        if isinstance(val, pd.DataFrame) or isinstance(val, pd.Series):
            return val
        else:
            raise NotDataFrameOrSeries(f"{source} is not Dataframe or Series")

    async def __remove_column_to_regex_async(self, df: pd.DataFrame, regex: str):
        match_columns = [str(column) for column in df.columns if re.search(regex, str(column))]
        list_remove = list(
            map(
                lambda name_column: df.drop(name_column, axis=1, inplace=True),
                match_columns
            )
        )
        return list_remove

    @ControlExecutionAsync(custom_logger.info)
    async def remove_columns_to_regex_async(self, source: str, list_regex: list, export_key=''):
        """This function deletes column through regex. In case if It were not removed columns
        generate <WARNING> in status_type return
        Args:
            source (int): This argument is source path on instance of MemoryVariables (self.variables).
            list_regex (list): This argument is the list with all regular expressions that match the columns to be removed.
            export_key (Optional[str]): This argument is source key to exports result to instance of MemoryVariables, if this argument is equal to '' then result will not saved. (Deafult '').
        Returns
            status (bool): with success -> True, with warning -> True, with error -> False.
            status_type (str): with success -> 'success: message', with error -> 'error: <ERROR>',  with warning -> 'warning: <WARNING>'.
            df (DataFrame): success, warning -> processed DataFrame, with error -> False.
        """
        df = self.__get_dataframe(source)
        result_remove = await asyncio.gather(*[self.__remove_column_to_regex_async(df, regex) for regex in list_regex])
        status_type = 'success' if any(result_remove) else 'warning'
        return status_type, df

    @ControlExecutionAsync(custom_logger.info)
    @ControlSchemaAsync(Schema([
            {   
                'column': And(str, len),
                'value': And(str, len),
                Optional('eval'): bool
            }
        ]), "new_columns"
    )
    async def add_columns_async(self, source: str, new_columns: list(), export_key=''):
        df = self.__get_dataframe(source)
        status_type = 'success'
        return status_type, df
