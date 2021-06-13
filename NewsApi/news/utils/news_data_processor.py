import pandas as pd


class NewsDataProcessor:
    @staticmethod
    def get_news_data(searched_news):
        articles = searched_news['articles']
        total_results = len(articles)
        title = []
        description = []
        source = []
        url = []

        for i in range(total_results):
            my_articles = articles[i]
            title.append(my_articles['title'])
            source.append(my_articles['source']['name'])
            description.append(my_articles['description'])
            url.append(my_articles['url'])

        df = pd.DataFrame(list(zip(title, source, description, url)),
                          columns=['title', 'source', 'description', 'url'])
        return df
