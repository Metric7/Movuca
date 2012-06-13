# -*- coding: utf-8 -*-

from handlers.base import Base


class Home(Base):
    def start(self):
        from movuca import DataBase, User
        from datamodel.article import Article, ContentType, Category
        from datamodel.page import Page
        from datamodel.ads import Ads
        self.db = DataBase([User, ContentType, Category, Article, Ads, Page])

    def pre_render(self):
        # obrigatorio ter um config, um self.response|request, que tenha um render self.response.render
        self.response = self.db.response
        self.request = self.db.request
        self.config = self.db.config
        #self.view = "app/home.html"
        self.response.meta.title = self.db.config.meta.title
        self.response.meta.description = self.db.config.meta.description
        self.response.meta.keywords = self.db.config.meta.keywords
        self.context.use_facebook = self.db.config.auth.use_facebook
        self.context.use_google = self.db.config.auth.use_google
        self.context.theme_name = self.config.theme.name

        self.context.content_types = self.allowed_content_types()
        self.context.categories = self.allowed_categories()

    def last_articles(self):
        from helpers.article import latest_articles
        self.context.latest_articles = latest_articles(self.db)

    def homeblocks(self):
        self.context.blocks = self.db(self.db.Article.blocks).select()

        self.context.block1 = self.context.blocks.exclude(lambda row: "block1" in row.blocks)
        self.context.block2 = self.context.blocks.exclude(lambda row: "block2" in row.blocks)
        self.context.block3 = self.context.blocks.exclude(lambda row: "block3" in row.blocks)

    def pages(self):
        self.context.pages = self.db(self.db.Page.visibility == 'footer').select()

    # def categories(self):
    #     self.context.categories = []
    #     categories = self.db(self.db.Category).select()
    #     for content in self.context.content_types:
    #         self.context.categories.append({"content_type": content.title,
    #                                         "id": content.id,
    #                                         "categories": categories.exclude(lambda row: row.content_type == content.id)
    #                                        })
        

    def ads(self):
        self.context.ads = self.db(self.db.Ads.place == "top_slider").select(limitby=(0, 5), orderby="<random>")
        if not self.context.ads:
            from gluon.storage import Storage
            self.context.ads = [Storage(id=1, thumbnail='', link=self.db.CURL('contact', 'ads')),
                                Storage(id=2, thumbnail="http://placehold.it/250x220&text=%s" % self.db.T("Your add here!"), link=self.db.CURL('contact', 'ads')),
                                Storage(id=3, thumbnail="http://placekitten.com/250/220", link=self.db.CURL('contact', 'ads')),
                                Storage(id=3, thumbnail="http://placehold.it/250x220&text=%s" % self.db.T("Your Logo"), link=self.db.CURL('contact', 'ads'))
                                ]

    def featured(self):
        self.context.featured = self.db(self.db.Article.featured == True).select(limitby=(0, 4), orderby="<random>")
        if not self.context.featured:
            self.context.featured = self.db((self.db.Article.draft == False) & (self.db.Article.is_active == True)).select(limitby=(0, 4), orderby=~self.db.Article.likes)

    def featured_members(self):
        self.context.featured_members = self.db(self.db.auth_user).select(limitby=(0, 8), orderby="<random>")
