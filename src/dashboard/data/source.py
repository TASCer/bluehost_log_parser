from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import pandas as pd

from ..data.loader import DataSchema
from .loader import DataSchema


@dataclass
class DataSource:
    _data: pd.DataFrame

    def filter(
        self,
        years: Optional[list[str]] = None,
        months: Optional[list[str]] = None,
        codes: Optional[list[str]] = None,
    ) -> DataSource:
        if years is None:
            years = self.unique_years
        if months is None:
            months = self.unique_months
        if codes is None:
            codes = self.unique_codes
        filtered_data = self._data.query(
            "YEAR in @years and MONTH in @months and CODE in @codes"
        )
        return DataSource(filtered_data)

    def create_pivot_table(self) -> pd.DataFrame:
        pt = self._data.pivot_table(
            values=DataSchema.MONTH,
            index=[DataSchema.CODE],
            aggfunc="sum",
            fill_value=0,
            dropna=False,
        )
        return pt.reset_index().sort_values(DataSchema.MONTH, ascending=False)

    @property
    def row_count(self) -> int:
        return self._data.shape[0]

    @property
    def all_years(self) -> list[str]:
        return self._data[DataSchema.YEAR].tolist()

    @property
    def all_months(self) -> list[str]:
        return self._data[DataSchema.MONTH].tolist()

    @property
    def all_codes(self) -> list[str]:
        return self._data[DataSchema.CODE].tolist()

    @property
    def all_amounts(self) -> list[str]:
        return self._data[DataSchema.AMOUNT].tolist()

    @property
    def unique_years(self) -> list[str]:
        return sorted(set(self.all_years), key=int)

    @property
    def unique_months(self) -> list[str]:
        return sorted(set(self.all_months))

    @property
    def unique_codes(self) -> list[str]:
        return sorted(set(self.all_codes))
