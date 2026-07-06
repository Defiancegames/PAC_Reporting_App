import pandas as pd

from PySide6.QtCore import (
    Qt,
    QAbstractTableModel
)


class DataFrameModel(QAbstractTableModel):

    def __init__(self, dataframe=pd.DataFrame()):
        super().__init__()

        self.dataframe = dataframe

    def rowCount(self, parent=None):

        return len(
            self.dataframe.index
        )

    def columnCount(self, parent=None):

        return len(
            self.dataframe.columns
        )

    def data(self, index, role):

        if role == Qt.DisplayRole:

            return str(
                self.dataframe.iloc[
                    index.row(),
                    index.column()
                ]
            )

        return None

    def headerData(
        self,
        section,
        orientation,
        role
    ):

        if role != Qt.DisplayRole:
            return None

        if orientation == Qt.Horizontal:

            return str(
                self.dataframe.columns[
                    section
                ]
            )

        return str(
            self.dataframe.index[
                section
            ]
        )