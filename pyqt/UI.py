# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1920, 1080)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.toolBox = QtWidgets.QToolBox(self.centralwidget)
        self.toolBox.setEnabled(True)
        self.toolBox.setObjectName("toolBox")
        self.epub_trans = QtWidgets.QWidget()
        self.epub_trans.setGeometry(QtCore.QRect(0, 0, 1908, 969))
        self.epub_trans.setObjectName("epub_trans")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.epub_trans)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.epub_mode_tab = QtWidgets.QTabWidget(self.epub_trans)
        self.epub_mode_tab.setObjectName("epub_mode_tab")
        self.convert_single = QtWidgets.QWidget()
        self.convert_single.setObjectName("convert_single")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.convert_single)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.open_file_button = QtWidgets.QPushButton(self.convert_single)
        self.open_file_button.setMinimumSize(QtCore.QSize(100, 20))
        self.open_file_button.setObjectName("open_file_button")
        self.horizontalLayout_7.addWidget(self.open_file_button)
        self.file_path_text = QtWidgets.QTextBrowser(self.convert_single)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.file_path_text.sizePolicy().hasHeightForWidth())
        self.file_path_text.setSizePolicy(sizePolicy)
        self.file_path_text.setMinimumSize(QtCore.QSize(0, 20))
        self.file_path_text.setObjectName("file_path_text")
        self.horizontalLayout_7.addWidget(self.file_path_text)
        self.verticalLayout_6.addLayout(self.horizontalLayout_7)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.trans_file_name = QtWidgets.QLabel(self.convert_single)
        self.trans_file_name.setMinimumSize(QtCore.QSize(100, 20))
        self.trans_file_name.setMaximumSize(QtCore.QSize(100, 20))
        self.trans_file_name.setAlignment(QtCore.Qt.AlignCenter)
        self.trans_file_name.setObjectName("trans_file_name")
        self.horizontalLayout_8.addWidget(self.trans_file_name)
        self.trans_file_name_text = QtWidgets.QTextEdit(self.convert_single)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.trans_file_name_text.sizePolicy().hasHeightForWidth())
        self.trans_file_name_text.setSizePolicy(sizePolicy)
        self.trans_file_name_text.setMinimumSize(QtCore.QSize(0, 20))
        self.trans_file_name_text.setObjectName("trans_file_name_text")
        self.horizontalLayout_8.addWidget(self.trans_file_name_text)
        self.verticalLayout_6.addLayout(self.horizontalLayout_8)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.open_folder_after_complete = QtWidgets.QCheckBox(self.convert_single)
        self.open_folder_after_complete.setObjectName("open_folder_after_complete")
        self.horizontalLayout.addWidget(self.open_folder_after_complete)
        self.auto_unzip = QtWidgets.QCheckBox(self.convert_single)
        self.auto_unzip.setObjectName("auto_unzip")
        self.horizontalLayout.addWidget(self.auto_unzip)
        self.auto_convert = QtWidgets.QCheckBox(self.convert_single)
        self.auto_convert.setObjectName("auto_convert")
        self.horizontalLayout.addWidget(self.auto_convert)
        self.verticalLayout_6.addLayout(self.horizontalLayout)
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.chapter_preview = QtWidgets.QLabel(self.convert_single)
        self.chapter_preview.setObjectName("chapter_preview")
        self.horizontalLayout_11.addWidget(self.chapter_preview)
        self.start_trans = QtWidgets.QPushButton(self.convert_single)
        self.start_trans.setObjectName("start_trans")
        self.horizontalLayout_11.addWidget(self.start_trans)
        self.verticalLayout_6.addLayout(self.horizontalLayout_11)
        self.preview_text = QtWidgets.QTextBrowser(self.convert_single)
        self.preview_text.setMinimumSize(QtCore.QSize(0, 60))
        self.preview_text.setObjectName("preview_text")
        self.verticalLayout_6.addWidget(self.preview_text)
        self.verticalLayout_10.addLayout(self.verticalLayout_6)
        self.epub_mode_tab.addTab(self.convert_single, "")
        self.convert_multi = QtWidgets.QWidget()
        self.convert_multi.setObjectName("convert_multi")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.convert_multi)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout()
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.open_folder_button = QtWidgets.QPushButton(self.convert_multi)
        self.open_folder_button.setMinimumSize(QtCore.QSize(100, 20))
        self.open_folder_button.setObjectName("open_folder_button")
        self.horizontalLayout_9.addWidget(self.open_folder_button)
        self.multi_folder_path_text = QtWidgets.QTextBrowser(self.convert_multi)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.multi_folder_path_text.sizePolicy().hasHeightForWidth())
        self.multi_folder_path_text.setSizePolicy(sizePolicy)
        self.multi_folder_path_text.setMinimumSize(QtCore.QSize(0, 20))
        self.multi_folder_path_text.setObjectName("multi_folder_path_text")
        self.horizontalLayout_9.addWidget(self.multi_folder_path_text)
        self.verticalLayout_7.addLayout(self.horizontalLayout_9)
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.multi_trans_folder_path = QtWidgets.QLabel(self.convert_multi)
        self.multi_trans_folder_path.setMinimumSize(QtCore.QSize(100, 20))
        self.multi_trans_folder_path.setMaximumSize(QtCore.QSize(100, 20))
        self.multi_trans_folder_path.setAlignment(QtCore.Qt.AlignCenter)
        self.multi_trans_folder_path.setObjectName("multi_trans_folder_path")
        self.horizontalLayout_10.addWidget(self.multi_trans_folder_path)
        self.multi_trans_file_name_text = QtWidgets.QTextEdit(self.convert_multi)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.multi_trans_file_name_text.sizePolicy().hasHeightForWidth())
        self.multi_trans_file_name_text.setSizePolicy(sizePolicy)
        self.multi_trans_file_name_text.setMinimumSize(QtCore.QSize(0, 20))
        self.multi_trans_file_name_text.setObjectName("multi_trans_file_name_text")
        self.horizontalLayout_10.addWidget(self.multi_trans_file_name_text)
        self.verticalLayout_7.addLayout(self.horizontalLayout_10)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setContentsMargins(0, 0, -1, -1)
        self.horizontalLayout_6.setSpacing(4)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.multi_input_name = QtWidgets.QTextBrowser(self.convert_multi)
        self.multi_input_name.setObjectName("multi_input_name")
        self.horizontalLayout_6.addWidget(self.multi_input_name)
        self.multi_output_name = QtWidgets.QPlainTextEdit(self.convert_multi)
        self.multi_output_name.setObjectName("multi_output_name")
        self.horizontalLayout_6.addWidget(self.multi_output_name)
        self.verticalLayout_7.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.multi_open_folder_after_complete = QtWidgets.QCheckBox(self.convert_multi)
        self.multi_open_folder_after_complete.setObjectName("multi_open_folder_after_complete")
        self.horizontalLayout_5.addWidget(self.multi_open_folder_after_complete)
        self.multi_auto_convert = QtWidgets.QCheckBox(self.convert_multi)
        self.multi_auto_convert.setObjectName("multi_auto_convert")
        self.horizontalLayout_5.addWidget(self.multi_auto_convert)
        self.verticalLayout_7.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.multi_chapter_preview = QtWidgets.QLabel(self.convert_multi)
        self.multi_chapter_preview.setObjectName("multi_chapter_preview")
        self.horizontalLayout_12.addWidget(self.multi_chapter_preview)
        self.multi_start_trans = QtWidgets.QPushButton(self.convert_multi)
        self.multi_start_trans.setObjectName("multi_start_trans")
        self.horizontalLayout_12.addWidget(self.multi_start_trans)
        self.verticalLayout_7.addLayout(self.horizontalLayout_12)
        self.multi_preview_text = QtWidgets.QTextBrowser(self.convert_multi)
        self.multi_preview_text.setMinimumSize(QtCore.QSize(0, 60))
        self.multi_preview_text.setObjectName("multi_preview_text")
        self.verticalLayout_7.addWidget(self.multi_preview_text)
        self.verticalLayout_11.addLayout(self.verticalLayout_7)
        self.epub_mode_tab.addTab(self.convert_multi, "")
        self.verticalLayout_3.addWidget(self.epub_mode_tab)
        self.toolBox.addItem(self.epub_trans, "")
        self.novel_download = QtWidgets.QWidget()
        self.novel_download.setGeometry(QtCore.QRect(0, 0, 1908, 969))
        self.novel_download.setObjectName("novel_download")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.novel_download)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.scarch_online_label = QtWidgets.QLabel(self.novel_download)
        self.scarch_online_label.setAlignment(QtCore.Qt.AlignCenter)
        self.scarch_online_label.setObjectName("scarch_online_label")
        self.horizontalLayout_2.addWidget(self.scarch_online_label)
        self.search_online_text = QtWidgets.QLineEdit(self.novel_download)
        self.search_online_text.setMinimumSize(QtCore.QSize(0, 20))
        self.search_online_text.setObjectName("search_online_text")
        self.horizontalLayout_2.addWidget(self.search_online_text)
        self.start_search__online_button = QtWidgets.QPushButton(self.novel_download)
        self.start_search__online_button.setObjectName("start_search__online_button")
        self.horizontalLayout_2.addWidget(self.start_search__online_button)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.groupbox = QtWidgets.QGroupBox(self.novel_download)
        self.groupbox.setObjectName("groupbox")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.groupbox)
        self.horizontalLayout_3.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout_3.setSpacing(4)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.search_result_text = QtWidgets.QTextBrowser(self.groupbox)
        self.search_result_text.setMinimumSize(QtCore.QSize(0, 60))
        self.search_result_text.setDocumentTitle("")
        self.search_result_text.setObjectName("search_result_text")
        self.horizontalLayout_3.addWidget(self.search_result_text)
        self.verticalLayout.addWidget(self.groupbox)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.storge_name_label = QtWidgets.QLabel(self.novel_download)
        self.storge_name_label.setObjectName("storge_name_label")
        self.horizontalLayout_4.addWidget(self.storge_name_label)
        self.storage_name_text = QtWidgets.QLineEdit(self.novel_download)
        self.storage_name_text.setMinimumSize(QtCore.QSize(0, 20))
        self.storage_name_text.setObjectName("storage_name_text")
        self.horizontalLayout_4.addWidget(self.storage_name_text)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.down_and_trans_button = QtWidgets.QPushButton(self.novel_download)
        self.down_and_trans_button.setObjectName("down_and_trans_button")
        self.verticalLayout_2.addWidget(self.down_and_trans_button)
        self.toolBox.addItem(self.novel_download, "")
        self.page_7 = QtWidgets.QWidget()
        self.page_7.setObjectName("page_7")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.page_7)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.horizontalGroupBox_2 = QtWidgets.QGroupBox(self.page_7)
        self.horizontalGroupBox_2.setObjectName("horizontalGroupBox_2")
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout(self.horizontalGroupBox_2)
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.max_chapter_len = QtWidgets.QSpinBox(self.horizontalGroupBox_2)
        self.max_chapter_len.setObjectName("max_chapter_len")
        self.horizontalLayout_13.addWidget(self.max_chapter_len)
        self.reset_max_chapter_len = QtWidgets.QPushButton(self.horizontalGroupBox_2)
        self.reset_max_chapter_len.setObjectName("reset_max_chapter_len")
        self.horizontalLayout_13.addWidget(self.reset_max_chapter_len)
        self.verticalLayout_9.addWidget(self.horizontalGroupBox_2)
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        self.verticalGroupBox = QtWidgets.QGroupBox(self.page_7)
        self.verticalGroupBox.setObjectName("verticalGroupBox")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.verticalGroupBox)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.white_list = QtWidgets.QPlainTextEdit(self.verticalGroupBox)
        self.white_list.setObjectName("white_list")
        self.verticalLayout_5.addWidget(self.white_list)
        self.whitelist_reset = QtWidgets.QPushButton(self.verticalGroupBox)
        self.whitelist_reset.setObjectName("whitelist_reset")
        self.verticalLayout_5.addWidget(self.whitelist_reset)
        self.horizontalLayout_14.addWidget(self.verticalGroupBox)
        self.verticalGroupBox_2 = QtWidgets.QGroupBox(self.page_7)
        self.verticalGroupBox_2.setObjectName("verticalGroupBox_2")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.verticalGroupBox_2)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.blacklist = QtWidgets.QPlainTextEdit(self.verticalGroupBox_2)
        self.blacklist.setObjectName("blacklist")
        self.verticalLayout_8.addWidget(self.blacklist)
        self.blacklist_reset = QtWidgets.QPushButton(self.verticalGroupBox_2)
        self.blacklist_reset.setObjectName("blacklist_reset")
        self.verticalLayout_8.addWidget(self.blacklist_reset)
        self.horizontalLayout_14.addWidget(self.verticalGroupBox_2)
        self.verticalLayout_9.addLayout(self.horizontalLayout_14)
        self.toolBox.addItem(self.page_7, "")
        self.verticalLayout_4.addWidget(self.toolBox)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1920, 18))
        self.menuBar.setObjectName("menuBar")
        self.menu = QtWidgets.QMenu(self.menuBar)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menuBar)
        self.actionreset = QtWidgets.QAction(MainWindow)
        self.actionreset.setObjectName("actionreset")
        self.menu.addAction(self.actionreset)
        self.menu.addSeparator()
        self.menuBar.addAction(self.menu.menuAction())

        self.retranslateUi(MainWindow)
        self.toolBox.setCurrentIndex(0)
        self.epub_mode_tab.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.open_file_button.setText(_translate("MainWindow", "開啟檔案"))
        self.trans_file_name.setText(_translate("MainWindow", "輸出名稱"))
        self.open_folder_after_complete.setText(_translate("MainWindow", "完成後開啟目錄"))
        self.auto_unzip.setText(_translate("MainWindow", "選取後自動解壓縮"))
        self.auto_convert.setText(_translate("MainWindow", "選取後自動轉換"))
        self.chapter_preview.setText(_translate("MainWindow", "章節預覽"))
        self.start_trans.setText(_translate("MainWindow", "開始轉換"))
        self.preview_text.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'PMingLiU\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'.AppleSystemUIFont\'; font-size:13pt;\"><br /></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'.AppleSystemUIFont\'; font-size:13pt;\"><br /></p></body></html>"))
        self.epub_mode_tab.setTabText(self.epub_mode_tab.indexOf(self.convert_single), _translate("MainWindow", "單次轉換"))
        self.open_folder_button.setText(_translate("MainWindow", "開啟資料夾"))
        self.multi_trans_folder_path.setText(_translate("MainWindow", "輸出目錄"))
        self.multi_open_folder_after_complete.setText(_translate("MainWindow", "完成後開啟目錄"))
        self.multi_auto_convert.setText(_translate("MainWindow", "選取後自動解壓縮"))
        self.multi_chapter_preview.setText(_translate("MainWindow", "章節預覽"))
        self.multi_start_trans.setText(_translate("MainWindow", "開始轉換"))
        self.multi_preview_text.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'PMingLiU\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'.AppleSystemUIFont\'; font-size:13pt;\"><br /></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'.AppleSystemUIFont\'; font-size:13pt;\"><br /></p></body></html>"))
        self.epub_mode_tab.setTabText(self.epub_mode_tab.indexOf(self.convert_multi), _translate("MainWindow", "批量轉換"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.epub_trans), _translate("MainWindow", "epub轉換"))
        self.scarch_online_label.setText(_translate("MainWindow", "搜尋"))
        self.start_search__online_button.setText(_translate("MainWindow", "開始搜尋"))
        self.groupbox.setTitle(_translate("MainWindow", "搜尋結果"))
        self.search_result_text.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'PMingLiU\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'.AppleSystemUIFont\'; font-size:13pt;\"><br /></p></body></html>"))
        self.storge_name_label.setText(_translate("MainWindow", "名稱"))
        self.down_and_trans_button.setText(_translate("MainWindow", "下載並轉換"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.novel_download), _translate("MainWindow", "下載小說"))
        self.horizontalGroupBox_2.setTitle(_translate("MainWindow", "章節名稱最大長度"))
        self.reset_max_chapter_len.setText(_translate("MainWindow", "重置章節名稱最大長度"))
        self.verticalGroupBox.setTitle(_translate("MainWindow", "章節白名單"))
        self.whitelist_reset.setText(_translate("MainWindow", "重置章節白名單"))
        self.verticalGroupBox_2.setTitle(_translate("MainWindow", "章節黑名單"))
        self.blacklist_reset.setText(_translate("MainWindow", "重置章節黑名單"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_7), _translate("MainWindow", "設定"))
        self.menu.setTitle(_translate("MainWindow", "設定"))
        self.actionreset.setText(_translate("MainWindow", "reset"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

