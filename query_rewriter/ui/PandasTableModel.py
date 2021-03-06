from PyQt5.QtCore import QAbstractTableModel
from PyQt5.QtCore import Qt
from pandas import DataFrame


class PandasTableModel(QAbstractTableModel):
    """
    Class to populate a table view with a pandas dataframe
    """

    def __init__(self, data: DataFrame, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self._data: DataFrame = data
        self._headers = list(self._data)

    def rowCount(self, parent=None):
        return len(self._data.values)

    def columnCount(self, parent=None):
        return self._data.columns.size

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.values[index.row()][index.column()])
        return None

    def headerData(self, col, orientation=Qt.Horizontal, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal:
            if role == Qt.DisplayRole:
                return self._data.columns[col].title().replace("_", " ")
        return None

    def sort(self, column: int, order: Qt.SortOrder = ...) -> None:
        super().sort(column, order)
        self.layoutAboutToBeChanged.emit()
        self._data = self._data.sort_values(self._headers[column], ascending=order == Qt.AscendingOrder)
        self.layoutChanged.emit()

    def update_data(self, data: DataFrame):
        self.layoutAboutToBeChanged.emit()
        self._data = data
        self._headers = [column.title() for column in list(self._data)]
        self.layoutChanged.emit()
        self.dataChanged.emit(self.createIndex(0, 0),
                              self.createIndex(self.rowCount(0),
                                               self.columnCount(0)))
