from create_db import *
from db import *
from sqlalchemy.orm import aliased
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

class Charts(Database):
    # Reads fromthe db and creates dictionaries and df
    # To easaly create charts

    def __init__(self) -> None:
        super().__init__()

    def create_dic(self, column_key, column_value):
        # creates dictionory from db table
        with self.session_scope() as session:
            dic = {}
            table = session.query(column_key, column_value).all()
            for row in table:
                dic[row[0]] = row[1]
            return dic

    def create_dic_for_word_in_url(self):
        # creates a dictionary from table word_in_url
        with self.session_scope() as session:
            dic = {}
            table = session.query(Word_in_url.url_id, Word_in_url.word_id, Word_in_url.count).all()
            for row in table:
                if row[0] in dic.keys():
                    dic[row[0]].append([row[1], row[2]])
                else:
                    dic[row[0]] = [[row[1], row[2]]]
            return dic

    def creat_df(self):
        with self.session_scope() as session:
            # Define aliases for the tables to use in the query
            Word = aliased(Words)
            WordInUrl = aliased(Word_in_url)
            Url = aliased(URLs)
            Website = aliased(Websites)
            Date = aliased(Dates)

            # Query to join the tables
            query = session.query(Word.word, WordInUrl.count, Website.website, Date.date).\
                join(WordInUrl, WordInUrl.word_id == Word.id).\
                join(Url, Url.id == WordInUrl.url_id).\
                join(Website, Website.id == Url.website_id).\
                join(Scrapes, Scrapes.url_id == Url.id).\
                join(Date, Date.id == Scrapes.date_id)

            # Get the results
            results = query.all()

        self.create_dic_word_category()

        self.df = pd.DataFrame(results)

        self.df['date'] = pd.to_datetime(self.df['date'])
        self.df['date'] = self.df['date'].dt.strftime('%Y-%m-%d') 

        filtered_rows = []

        # loop through each category and its corresponding list of words
        for category, words in self.word_categories.items():
            # filter the DataFrame to only include rows where the 'words' column is in the list of words for this category
            mask = self.df['word'].isin(words)
            # add a new column to the filtered DataFrame with the category as its value
            filtered = self.df.loc[mask].copy()
            # append the filtered rows to the list of filtered rows
            filtered['category'] = category

            filtered_rows.append(filtered)                                                                          

        # concatenate the filtered rows into a single DataFrame                
        if filtered_rows:                                        
            filtered_df = pd.concat(filtered_rows)
        else:                      
            filtered_df = pd.DataFrame()
        
        self.filtered_df =  filtered_df
        self.words_found = self.word_in_articles()

    def create_dic_word_category(self):
        # creates a dictionary where the keys are the categories and the values their corresponding words
        new_c_id_new_c = self.create_dic(NewsCategory.news_category, NewsCategory.id)
        se_w_se_word_id = self.create_dic(Searching_words.id, Searching_words.word)
        word_id_new_c_id = self.create_dic(Words_cathegorized.word_id, Words_cathegorized.news_category_id)
        self.word_categories = {}
        for cathegory in new_c_id_new_c.keys():
            words = []
            for word_id in word_id_new_c_id.keys():
                if new_c_id_new_c[cathegory] == word_id_new_c_id[word_id]:
                    words.append(se_w_se_word_id[word_id])
            self.word_categories[cathegory] = words

    def word_in_articles(self):
        # returns a list of all the searching words found in all categories
        tdf_groupby_words = self.filtered_df.groupby("word").sum(numeric_only=True)
        self.words_found = [[word, self.filtered_df[self.filtered_df["word"]==word]["category"].unique()[0]] for word in list(tdf_groupby_words.index)]
        self.words_found.sort(key=lambda x: x[1])
        return self.words_found

    def style_chart(self):
        # Set the background color
        plt.rcParams['axes.facecolor'] = '#f0f0f0'
        # Set the font size
        plt.rcParams['font.size'] = 12
        # Set the color of the grid lines
        plt.rcParams['grid.color'] = 'white'
        # Set the style of the grid lines
        plt.rcParams['grid.linestyle'] = '--'
        # Set the width of the grid lines
        plt.rcParams['grid.linewidth'] = 0.5
        # Set the size of the chart
        plt.rcParams['figure.figsize'] = (12, 6)
        plt.rcParams['figure.dpi'] = 100

    def calc_x_points(self):
        # creates values to display on the x axis
        x_points = self.df["date"].unique()
        num_ticks = 5
        if len(x_points) > num_ticks:
            x_points_display = x_points[::len(x_points)//num_ticks]
        else:
            x_points_display = x_points
        return x_points_display
    
    def chart_word_occurance(self, word):
        # create chart of one word
        df_word = self.df[self.df["word"]==word].groupby(["date"]).sum(numeric_only=True)

        plt.plot(df_word.index, df_word['count'], color='b', label=f'{word}')
        plt.xlabel('Date')
        plt.ylabel('Total Count')
        plt.title(f'Total Counts of word "{word}" per Date')

        x_points = self.calc_x_points()

        # rotate the x-tick labels by 45 degrees
        plt.xticks(x_points, rotation=45)

        # apply the style to the chart
        self.style_chart()

        # adjust the spacing between subplots
        plt.subplots_adjust(wspace=0.4)
        plt.legend()
        plt.show()

    def chart_two_words_occurance(self, word1, word2): 
        # creates charts of two words
        df_word1 = self.df[self.df["word"]==word1].groupby(["date"]).sum(numeric_only=True)
        df_word2 = self.df[self.df["word"]==word2].groupby(["date"]).sum(numeric_only=True)

        # create a figure with two subplots
        fig, axs = plt.subplots(1, 3, figsize=(15, 5))
        x_points = self.calc_x_points()

        # plot the first chart
        axs[0].plot(df_word1.index, df_word1['count'], color='b', label=f'{word1}')
        axs[0].set_xlabel('Date')
        axs[0].set_ylabel('Total Count')
        axs[0].set_title(f'Total Counts of word "{word1}" per Date', fontsize=12)

        # set the x-tick labels for the first chart
        axs[0].set_xticks(x_points)
        axs[0].set_xticklabels(x_points, rotation=45)
        axs[0].legend()

        # plot the second chart
        axs[1].plot(df_word2.index, df_word2['count'], color='g', label=f'{word2}')
        axs[1].set_xlabel('Date')
        axs[1].set_ylabel('Total Count')
        axs[1].set_title(f'Total Counts of word "{word2}" per Date', fontsize=12)

        # set the x-tick labels for the second chart
        axs[1].set_xticks(x_points)
        axs[1].set_xticklabels(x_points, rotation=45)
        axs[1].legend()

        # plot the third chart
        axs[2].bar(df_word1.index, df_word1['count'], color='b', label=f'{word1}', alpha=0.5)
        axs[2].bar(df_word2.index, df_word2['count'], color='g', label=f'{word2}', alpha=0.5)

        axs[2].set_xlabel('Date')
        axs[2].set_ylabel('Total Count')
        axs[2].set_title('Total Counts by date', fontsize=12)

        # set the x-tick labels for the third chart
        axs[2].set_xticks(x_points)
        axs[2].set_xticklabels(x_points, rotation=45)

        # change the position of the legend
        axs[2].legend(loc='upper left')

        # add an overall title to the chart
        plt.suptitle(f'Total Counts of Words "{word1}" and "{word2}" per Date', fontsize=16)

        # apply the style to the chart
        self.style_chart()

        # adjust the spacing between subplots
        plt.subplots_adjust(wspace=0.4)
        plt.show()

    def chart_word_percent_change(self, word):
        # creates charts of one word based on percent chage over time
        df_word = self.df[self.df["word"]==word].groupby(["date"]).sum(numeric_only=True)
        df_word["count"] = (df_word["count"]/df_word.loc[df_word.index.min(), "count"]*100)-100
        x_points = self.calc_x_points()
        plt.plot(df_word.index, df_word['count'], color='b', label=f'{word}')
        plt.xlabel('Date')
        plt.ylabel('Change of count in %')
        plt.title(f'Change of count of word "{word}" for each date in %')
        plt.rcParams['axes.titlesize'] = 16
        # rotate the x-tick labels by 45 degrees
        plt.xticks(x_points, rotation=45)
        plt.legend()
        plt.gcf().set_size_inches(15, 8)
        # apply the style to the chart
        self.style_chart()
        # adjust the spacing between subplots
        plt.subplots_adjust(wspace=0.4)
        plt.show()

    def chart_two_words_percent_change(self, word1, word2):
        # creates charts of two words based on percent chage over time
        df_word1 = self.df[self.df["word"]==word1].groupby(["date"]).sum(numeric_only=True)
        df_word1["count"] = (df_word1["count"]/df_word1.loc[df_word1.index.min(), "count"]*100)-100
        df_word2 = self.df[self.df["word"]==word2].groupby(["date"]).sum(numeric_only=True)
        df_word2["count"] = (df_word2["count"]/df_word2.loc[df_word2.index.min(), "count"]*100)-100
        x_points = self.calc_x_points()

        plt.plot(df_word1.index, df_word1['count'], color='b', label=f'{word1}')
        plt.plot(df_word2.index, df_word2['count'], color='g', label=f'{word2}')

        plt.xlabel('date')
        plt.ylabel('Change of count in %')
        plt.title(f'Change of count of word "{word1}" and "{word2}"  for each date in %')
        plt.rcParams['axes.titlesize'] = 16

        # apply the style to the chart
        self.style_chart()

        plt.xticks(x_points, rotation=45)
        plt.legend()
        plt.gcf().set_size_inches(15, 8)
        plt.show()

    def chart_website_cath(self): 
        # creates charts displaying most founded categories in the webbsites
        dfs = {}
        for website in list(self.filtered_df["website"].unique()):
            mask = self.filtered_df["website"]==website
            df_website = self.filtered_df[mask]
            df_cath = df_website.groupby(["category"]).sum(numeric_only=True)
            dfs[website] = df_cath

        # create a figure with one subplot per website
        fig, axs = plt.subplots(1, len(dfs), figsize=(6*len(dfs), 6), squeeze=False)
        patches = []
        for i, df_i in enumerate(list(dfs.keys())):
            n_colors = len(dfs[list(dfs.keys())[0]])
            cmap = plt.get_cmap('tab20')
            colors = cmap(np.linspace(0, 1, n_colors))
            axs[0,i].bar(dfs[df_i].index, dfs[df_i]['count'], color=colors)
            axs[0,i].set_title(f'{df_i}')
            axs[0,i].tick_params(axis='x', which='both', bottom=False, labelbottom=False)
            if i == 0:
                for j, category in enumerate(dfs[df_i].index):
                    patch = mpatches.Patch(color=colors[j], label=category)
                    patches.append(patch)
            self.style_chart()

        # add the legend to the chart
        fig.legend(handles=patches, loc='lower center', ncol=len(dfs[df_i].index))
        # adjust the spacing between subplots
        plt.subplots_adjust(wspace=0.1, left=0.05, right=0.95, bottom=0.15, top=0.85)
        plt.show()

