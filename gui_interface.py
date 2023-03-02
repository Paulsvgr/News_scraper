from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QMessageBox, QInputDialog, QLineEdit
from scrape_website import *
from charts import *
import sys
import threading
from css import *

class Menu(QtWidgets.QWidget, Scrape, Charts):
    def __init__(self):
        super().__init__()
        self.init_ui()
        function_thread = threading.Thread(target=self.create_instances)
        function_thread.start()

    def create_instances(self):
        self.enable_buttons(self.buttons_other)
        self.enable_buttons(self.buttons_scrape)
        self.creat_df()
        self.enable_buttons(self.buttons_chart)
        
        
    def enable_buttons(self, buttons_list):
        for button in buttons_list:
            button.setEnabled(True)

    def init_ui(self):
        self.setWindowTitle("News Scraper")
        # Set background color
        self.setStyleSheet("background-color: #F0F0F0;")
    
        # Create buttons
        check_scrape_btn = QtWidgets.QPushButton("Check Latest Scrape")
        check_scrape_btn.clicked.connect(self.latest_scrape)

        scrape_btn = QtWidgets.QPushButton("Scrape")
        scrape_btn.clicked.connect(self.scrape_news)

        list_categories_btn = QtWidgets.QPushButton("List All Categories")
        list_categories_btn.clicked.connect(self.func_list_categories)

        list_words_btn = QtWidgets.QPushButton("List All Words")
        list_words_btn.clicked.connect(self.func_list_words)

        add_category_btn = QtWidgets.QPushButton("Add a Category")
        add_category_btn.clicked.connect(self.func_add_category)

        add_word_btn = QtWidgets.QPushButton("Add a Phrase to a Category")
        add_word_btn.clicked.connect(self.func_add_word)

        add_website_btn = QtWidgets.QPushButton("Add a Website/Domain")
        add_website_btn.clicked.connect(self.func_add_website)

        list_urls_btn = QtWidgets.QPushButton("List All Scraped URLs")
        list_urls_btn.clicked.connect(self.func_list_urls)

        urls_from_date_btn = QtWidgets.QPushButton("Scraped URLs from a Date")
        urls_from_date_btn.clicked.connect(self.func_urls_from_date)

        chart_word_occurance_btn = QtWidgets.QPushButton("Chart Word Occurance")
        chart_word_occurance_btn.clicked.connect(self.func_chart_word_occurance)

        chart_random_word_occurance_btn = QtWidgets.QPushButton("Chart Any Given Word Occurance")
        chart_random_word_occurance_btn.clicked.connect(self.func_chart_any_word_occurance)

        chart_two_words_occurance_btn = QtWidgets.QPushButton("Chart Two Words Occurance")
        chart_two_words_occurance_btn.clicked.connect(self.func_chart_two_words_occurance)

        chart_word_percent_change_btn = QtWidgets.QPushButton("Chart Word Percent Change")
        chart_word_percent_change_btn.clicked.connect(self.func_chart_word_percent_change)

        chart_two_words_percent_change_btn = QtWidgets.QPushButton("Chart Two Words Percent Change")
        chart_two_words_percent_change_btn.clicked.connect(self.func_chart_two_words_percent_change)

        chart_website_cath_btn = QtWidgets.QPushButton("Chart Website Categories")
        chart_website_cath_btn.clicked.connect(self.func_chart_website_cath)

        uppdate_gui_btn = QtWidgets.QPushButton("Uppdate gui interractoin")
        uppdate_gui_btn.clicked.connect(self.uppdate_gui)

        exit_btn = QtWidgets.QPushButton("Exit")
        exit_btn.clicked.connect(self.close)

        button_style = """
            QPushButton {
                background-color: #e0e0e0;
                border-radius: 10px;
                color: #333;
                font-size: 18px;
                padding: 10px 20px;
            }

            QPushButton:hover {
                background-color: #d5d5d5;
            }
        """
        check_scrape_btn.setStyleSheet(button_style)
        scrape_btn.setStyleSheet(button_style)
        list_categories_btn.setStyleSheet(button_style)
        list_words_btn.setStyleSheet(button_style)
        add_category_btn.setStyleSheet(button_style)
        add_word_btn.setStyleSheet(button_style)
        add_website_btn.setStyleSheet(button_style)
        list_urls_btn.setStyleSheet(button_style)
        urls_from_date_btn.setStyleSheet(button_style)
        chart_word_occurance_btn.setStyleSheet(button_style)
        chart_random_word_occurance_btn.setStyleSheet(button_style)
        chart_two_words_occurance_btn.setStyleSheet(button_style)
        chart_word_percent_change_btn.setStyleSheet(button_style)
        chart_two_words_percent_change_btn.setStyleSheet(button_style)
        chart_website_cath_btn.setStyleSheet(button_style)
        uppdate_gui_btn.setStyleSheet(button_style)
        exit_btn.setStyleSheet(button_style)

        # Create layout
        layout = QtWidgets.QVBoxLayout()
        self.buttons_scrape = [check_scrape_btn, scrape_btn, list_categories_btn, list_words_btn,
                                 add_category_btn, add_word_btn, add_website_btn, list_urls_btn,
                                  urls_from_date_btn]
        self.buttons_chart = [chart_word_occurance_btn, chart_random_word_occurance_btn, 
                                chart_two_words_occurance_btn, chart_word_percent_change_btn,
                                 chart_two_words_percent_change_btn, chart_website_cath_btn]
        self.buttons_other = [ uppdate_gui_btn, exit_btn]
        layout.addStretch()
        for button in self.buttons_scrape + self.buttons_chart + self.buttons_other:
            layout.addWidget(button)
            layout.addStretch()
            button.setEnabled(False)

        layout.setSpacing(10)

        self.setLayout(layout)

    def info_box(self, title, phrase):
        QtWidgets.QMessageBox.information(
        self,
        title,
        phrase,
        QtWidgets.QMessageBox.Ok,
        )

    def uppdate_gui(self):
        self.creat_df() 
        self.info_box("Update Status", "Done!")
        
    def func_chart_any_word_occurance(self):
        word, ok = QInputDialog.getText(self, "Enter word", "Enter a random word to see its occurance:")
        check = self.check_if_found(word)
        if word and ok and check is not None:
            self.chart_word_occurance(word)
        else:
           self.info_box("Word not found", f"The word '{word}' wasn't found in any articles")

    def latest_scrape(self):
        date = self.check_latest_date()
        date = date.strftime("%Y-%m-%d")
        message = "Latest scrape was {}\n".format(date)
        self.info_box("Latest Scrape", message)

    def scrape_news(self):
        thread1 = threading.Thread(target=self.info_box("Scrape", self.go()))
        thread2 = threading.Thread(target=self.uppdate_gui())

        # Start the first thread
        thread1.start()

        # Wait for the first thread to complete before starting the second thread
        thread1.join()
        thread2.start()
        
    def func_list(self, my_list, title="List Item"):

        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle(title)
        layout = QtWidgets.QVBoxLayout(dialog)

        tree_view = QtWidgets.QTreeView()
        tree_view.header().hide()
        tree_model = QtGui.QStandardItemModel()
        tree_view.setModel(tree_model)

        category_item = None
        for item in my_list:
            if "word" in title:
                category_item = QtGui.QStandardItem(item + ":")
                tree_model.appendRow(category_item)

                for word in my_list[item]:
                    item_text = QtGui.QStandardItem(word)
                    category_item.appendRow(item_text)

               
            else:
                item_text = QtGui.QStandardItem(item[0])
                tree_model.appendRow(item_text)

        layout.addWidget(tree_view)

        button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)

        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            selected_item = tree_view.currentIndex()
            if selected_item.isValid():
                if "word" in title:
                    return tree_model.itemData(selected_item)
                my_list = [i[0] for i in my_list] 
                return tree_model.itemData(selected_item)[0], int(my_list.index(tree_model.itemData(selected_item)[0])+1)
                
        return None

    def func_list_categories(self):
        self.func_list(self.get_all_categories(), title="List of categories")

    def func_list_words(self):
        self.func_list(self.get_searching_words(), title="List of found words from list cathegory ")

    def func_list_urls(self):
        self.func_list(self.get_all_urls(), title="List of urls")

    def func_urls_from_date(self):
        dates = self.get_dates()
        dates = [[str(date[0].strftime("%Y-%m-%d")), date[1]] for date in dates]
        date_choice = self.func_list(dates, "Choose a date")
        if date_choice:
            urls = self.get_urls_by_date(date_choice[1])
            self.func_list(urls, title=f"List of urls from {date_choice}")
    
    def func_chart_word_occurance(self):
        word = self.func_list(self.get_searching_words(), "Choose a word")
        if word:
            self.chart_word_occurance(word[0])

    def func_chart_two_words_occurance(self):
        word1 = self.func_list(self.get_searching_words(), "Choose the fisrt word")
        if word1:
            word2 = self.func_list(self.get_searching_words(), "Choose the secound word")
        if word1 and word2:
            self.chart_two_words_occurance(word1[0], word2[0])

    def func_chart_word_percent_change(self):
        word = self.func_list(self.get_searching_words(), "Choose a word")
        if word:
            self.chart_word_percent_change(word[0])
    
    def func_chart_two_words_percent_change(self):
        word1 = self.func_list(self.get_searching_words(), "Choose the fisrt word")
        if word1:
            word2 = self.func_list(self.get_searching_words(), "Choose the secound word")
        if word1 and word2:
            self.chart_two_words_percent_change(word1[0], word2[0])

    def func_chart_website_cath(self):
        self.chart_website_cath()

    def func_add_category(self):
        cathegory, ok = QInputDialog.getText(self, "Add Category", "Enter a new category:")
        if ok and cathegory:
            status = self.add_news_category(cathegory)
            if status:
                QMessageBox.information(self, "Success", f"{cathegory} was added to the list of categories.")
            else:
                QMessageBox.warning(self, "Error", f"News category '{cathegory}' already exists.")

    def func_add_word(self):
        cathegory_choice = self.func_list(self.get_all_categories(), "news category")
        if cathegory_choice:
            word_to_add, ok_pressed = QInputDialog.getText(self, "Add Word to Category", f"Enter the word you want to add to the category '{cathegory_choice[0]}':", QLineEdit.Normal, "")
            if ok_pressed:
                status = self.add_word_to_category(word_to_add, cathegory_choice[1])
                if status:
                    QMessageBox.information(self, "Success", f"Added word '{word_to_add}' to news category '{cathegory_choice[0]}'", QMessageBox.Ok)
                else:
                    QMessageBox.warning(self, "Error", f"The word '{word_to_add}' already exists in a category", QMessageBox.Ok)

    def func_add_website(self):
        website_url, ok = QInputDialog.getText(self, "Add Website", "Enter the URL of the website/domain you want to scrape news from:")
        if ok:
            try:
                response = requests.get(website_url, headers=self.headers)
            except requests.exceptions.RequestException:
                QMessageBox.warning(self, "Error", f"Couldn't get any response from '{website_url}'")
            else:
                if response.status_code == 200:
                    website_name_split_www = website_url.split("https://www.")
                    if len(website_name_split_www) == 1:
                        website_name_split_www = website_url.split("https://")
                        if len(website_name_split_www) == 1:
                            website_name_split_www = website_name_split_www[0]                 
                    website_name = website_name_split_www[1].split(".")[0]
                    website_name = website_name.title()
                    status, check = self.add_website(website_name, website_url)
                    if check:
                        QMessageBox.information(self, "Success", f"{website_name} was added to the list of websites.")
                    else:
                        QMessageBox.information(self, "Error", status)
                else:
                    QMessageBox.warning(self, "Error", f"Could not get any good response from {website_url}")



if __name__ == '__main__':
    app = QtWidgets.QApplication([])  # create QApplication instance
    app.setStyleSheet("QWidget {background-color: #ffffff;}")
    
    # Set style sheet for all message boxes
    msg_box_style = css_code

    app.setStyleSheet(msg_box_style) 

    menu = Menu()  # create Menu widget
    menu.show()  # show the Menu widget
    sys.exit(app.exec_()) 
        