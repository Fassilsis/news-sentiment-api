import pandas as pd


class NewsDataProcessor:
    @staticmethod
    def get_news_data(searched_news):
        articles = searched_news['articles']
        total_results = len(articles)
        title = []
        description = []
        source = []
        news_url = []
        image_url = []
        published_at = []

        for i in range(total_results):
            my_articles = articles[i]
            title.append(my_articles['title'])
            source.append(my_articles['source']['name'])
            description.append(my_articles['description'])
            news_url.append(my_articles['url'])
            image_url.append(my_articles['urlToImage'])
            published_at.append(my_articles['publishedAt'])

        df = pd.DataFrame(list(zip(title, source, description, news_url, image_url, published_at)),
                          columns=['title', 'source', 'description', 'news_url', 'image_url', 'published_at'])
        return df