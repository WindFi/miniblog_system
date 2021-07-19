# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

import tornado.ioloop
import tornado.web

from sqlalchemy import Column, String, create_engine, INT, VARCHAR, TEXT, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

from mysql.connector.errors import ProgrammingError

from entities.article import ArticleEntity
from encoder import AlchemyEncoder

from paginate import Page, make_html_tag
import time
import json

"""
之后改成从文件读取吧....
"""
def readConfig():
    return 'mysql+mysqlconnector://root:123456aa@localhost:3306/python_blog'


connectionString = readConfig()
engine = create_engine(connectionString)
DBSession = sessionmaker(bind=engine)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

    def post(self):
        self.write('post')

    def put(self):
        self.write('put')

    def delete(self):
        self.write('delete')

class ArticleListHandler(tornado.web.RequestHandler):
    def get(self):
        session = DBSession()
        page = self.get_query_argument('page', 0)
        print(page)
        try:
            session = DBSession()
            articles = session.query(ArticleEntity).limit(30).offset( int(page) * 30).all()
            self.write(json.dumps(articles, default=lambda obj: obj.to_json()))
        except NoResultFound as e:
            self.write('[]')
        except BaseException as e:
            self.write_error(403)
            print(e)
        finally:
            session.close()
    def post(self):
        pass
    def put(self):
        pass
    def delete(self):
        pass
class ArticleHandler(tornado.web.RequestHandler):
    def get(self):
        session = DBSession()
        queryId = self.request.uri.split('/')[-1]
        try:
            session = DBSession()
            articles = session.query(ArticleEntity).filter(ArticleEntity.id == queryId).one()
            self.write(json.dumps(articles, default=lambda obj: obj.to_json()))
        except NoResultFound as e:
            self.write_error(404)
        except BaseException as e:
            self.write_error(403)
        finally:
            session.close()

    def post(self):
        body = json.loads(self.request.body)
        artile = ArticleEntity()
        artile.title = body['title']
        artile.content = body['content']

        session = DBSession()

        try:
            session.add(artile)
            session.flush()
            session.commit()
            self.write(str(artile.id))
        except:
            self.write_error("500", "error")
        finally:
            session.close()

    def put(self):
        body = json.loads(self.request.body)
        session = DBSession()
        queryId = body['id']

        try:
            article = session.query(ArticleEntity) \
                .filter(ArticleEntity.id == queryId) \
                .one()
            article.title = body['title']
            article.content = body['content']
            article.update_time = time.time()
            session.commit()

            self.write("success")
        except BaseException as e:
            print(e)
            self.write_error(400)
        finally:
            session.close()

    def delete(self):
        body = json.loads(self.request.body)
        resourceId = body['id']
        session = DBSession()
        try:
            session.query(ArticleEntity).filter(ArticleEntity.id == resourceId).delete()
            session.commit()
            self.write("delete success")
        except BaseException as e:
            print(e)
            self.write_error(500)
        finally:
            session.close()


def initDataBase():
    session = DBSession()
    try:
        ArticleEntity.meta.create_all(engine)
    except ProgrammingError:
        print("programming error")
    finally:
        session.close()


def startService():
    app = tornado.web.Application([
        (r"/", MainHandler),
        (r"/article/id/[0-9]+", ArticleHandler),
        (r"/article", ArticleListHandler)
    ])
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    initDataBase()
    startService()
