css_code = """
        QMessageBox {
            background-color: #ffffff;
            border: 1px solid #cccccc;
            border-radius: 5px;
            color: #333333;
        }

        QMessageBox QPushButton {
            background-color: #e0e0e0;
            border-radius: 10px;
            color: #333333;
            font-size: 18px;
            padding: 10px 20px;
        }

        QMessageBox QPushButton:hover {
            background-color: #d5d5d5;
        }
  
        QInputDialog {
            background-color: #ffffff;
            border: 1px solid #cccccc;
            border-radius: 5px;
            color: #333333;
        }

        QInputDialog QLabel {
            font-size: 18px;
            color: #333333;
        }

        QInputDialog QLineEdit {
            background-color: #e0e0e0;
            border-radius: 10px;
            color: #333333;
            font-size: 18px;
            padding: 10px 20px;
        }

        QInputDialog QPushButton {
            background-color: #e0e0e0;
            border-radius: 10px;
            color: #333333;
            font-size: 18px;
            padding: 10px 20px;
        }

        QInputDialog QPushButton:hover {
            background-color: #d5d5d5;
        }

        QDialog {
            background-color: #ffffff;
            border: 1px solid #cccccc;
            border-radius: 5px;
            color: #333333;
        }
 
        QVBoxLayout {
            margin: 0px;
            padding: 0px;
        }

        QVBoxLayout QTreeView {
            background-color: #ffffff;
            border: 1px solid #cccccc;
            border-radius: 5px;
            color: #333333;
            font-size: 18px;
            margin: 10px;
            padding: 10px;
        }

        QTreeView {
            background-color: #ffffff;
            border: 1px solid #cccccc;
            border-radius: 5px;
            color: #333333;
            font-size: 18px;
            margin: 10px;
            padding: 10px;
        }

        QStandardItemModel {
            background-color: #ffffff;
            border: 1px solid #cccccc;
            border-radius: 5px;
            color: #333333;
            font-size: 18px;
            margin: 10px;
            padding: 10px;
        }

        QStandardItemModel::item {
            margin: 5px;
            padding: 5px;
        }

        QStandardItemModel::item:hover {
            background-color: #e0e0e0;
        }

        QStandardItemModel::item:selected {
            background-color: #d5d5d5;
        }

        QStandardItemModel QScrollBar:vertical {
        background-color: #f0f0f0;
        border-radius: 5px;
        width: 20px;
        }

        QStandardItemModel QScrollBar::handle:vertical {
            background-color: #c0c0c0;
            border-radius: 5px;
        }

        QStandardItemModel QScrollBar::handle:vertical:hover {
            background-color: #a0a0a0;
        }

        QStandardItemModel QScrollBar::sub-line:vertical,
        QStandardItemModel QScrollBar::add-line:vertical {
            background-color: #f0f0f0;
            height: 20px;
        }

        QStandardItemModel QScrollBar::sub-line:vertical:hover,
        QStandardItemModel QScrollBar::add-line:vertical:hover {
            background-color: #d0d0d0;
        }

        QStandardItemModel QScrollBar::sub-line:vertical {
            subcontrol-origin: margin;
            subcontrol-position: top;
        }

        QStandardItemModel QScrollBar::add-line:vertical {
            subcontrol-origin: margin;
            subcontrol-position: bottom;
        }

        QStandardItemModel QScrollBar::up-arrow:vertical,
        QStandardItemModel QScrollBar::down-arrow:vertical {
            background: none;
            border: none;
            color: #333333;
            font-size: 18px;
        }

        QStandardItemModel QScrollBar::up-arrow:vertical {
            qproperty-arrow-border-color: #333333;
            qproperty-arrow-background-color: transparent;
            qproperty-arrow-color: #333333;
            qproperty-arrow-height: 10px;
        }

        QStandardItemModel QScrollBar::up-arrow:vertical:hover {
            qproperty-arrow-color: #ffffff;
        }

        QStandardItemModel QScrollBar::down-arrow:vertical {
            qproperty-arrow-border-color: #333333;
            qproperty-arrow-background-color: transparent;
            qproperty-arrow-color: #333333;
            qproperty-arrow-height: 10px;
        }

        QStandardItemModel QScrollBar::down-arrow:vertical:hover {
            qproperty-arrow-color: #ffffff;
        }

        QDialogButtonBox {
            background-color: #ffffff;
            border: 1px solid #cccccc;
            border-radius: 5px;
            color: #333333;
            font-size: 18px;
            margin: 10px;
            padding: 10px;
        }

        QDialogButtonBox QPushButton {
            background-color: #e0e0e0;
            border-radius: 10px;
            color: #333333;
            font-size: 18px;
            padding: 10px 20px;
        }

        QDialogButtonBox QPushButton:hover {
            background-color: #d5d5d5;
        }
 
        QListWidget {
            background-color: #ffffff;
            border: 1px solid #cccccc;
            border-radius: 5px;
            color: #333333;
            font-size: 18px;
        }

        QListWidget::item {
            padding: 10px;
        }

        QScrollBar:vertical {
            border: none;
            background-color: #f0f0f0;
            width: 20px;
            margin: 0px;
        }

        QScrollBar::handle:vertical {
            background-color: #cccccc;
            border-radius: 10px;
            min-height: 20px;
        }

        QScrollBar::add-line:vertical {
            border: none;
            background-color: none;
        }

        QScrollBar::sub-line:vertical {
            border: none;
            background-color: none;
        }

        QScrollBar::add-page:vertical {
            background-color: none;
        }

        QScrollBar::sub-page:vertical {
            background-color: none;
        }

        QScrollBar:vertical {
    background-color: #f0f0f0;
    border-radius: 5px;
    width: 20px;
        }

        QScrollBar::handle:vertical {
            background-color: #c0c0c0;
            border-radius: 5px;
        }

        QScrollBar::handle:vertical:hover {
            background-color: #a0a0a0;
        }

        QScrollBar::sub-line:vertical,
        QScrollBar::add-line:vertical {
            background-color: #f0f0f0;
            height: 20px;
        }

        QScrollBar::sub-line:vertical:hover,
        QScrollBar::add-line:vertical:hover {
            background-color: #d0d0d0;
        }

        QScrollBar::sub-line:vertical {
            subcontrol-origin: margin;
            subcontrol-position: top;
        }

        QScrollBar::add-line:vertical {
            subcontrol-origin: margin;
            subcontrol-position: bottom;
        }

        QScrollBar::up-arrow:vertical,
        QScrollBar::down-arrow:vertical {
            background: none;
            border: none;
            color: #333333;
            font-size: 18px;
        }

        QScrollBar::up-arrow:vertical {
            qproperty-arrow-border-color: #333333;
            qproperty-arrow-background-color: transparent;
            qproperty-arrow-color: #333333;
            qproperty-arrow-height: 10px;
        }

        QScrollBar::up-arrow:vertical:hover {
            qproperty-arrow-color: #ffffff;
        }

        QScrollBar::down-arrow:vertical {
            qproperty-arrow-border-color: #333333;
            qproperty-arrow-background-color: transparent;
            qproperty-arrow-color: #333333;
            qproperty-arrow-height: 10px;
        }

        QScrollBar::down-arrow:vertical:hover {
            qproperty-arrow-color: #ffffff;
        }

    """