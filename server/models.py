from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    @validates('name')
    def author_name(self, key, nom):
        all_authors = self.query.all()
        author_list = [author.name for author in all_authors]
        if nom == "" or nom is None or nom in author_list:
            raise ValueError
        return nom

    @validates('phone_number')
    def validate_phone_number(self, key, phone):
        digits = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
        for character in phone:
            if character not in digits:
                raise ValueError
        if len(phone) == 10:
            return phone
        else:
            raise ValueError

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  

    @validates('title')
    def title_validation(self, key, my_title):
        click_bait = ["Won't Believe", "Secret", "Top", "Guess"]
        if my_title == "" or my_title is None:
            raise ValueError
        if not any(word in my_title for word in click_bait):
            raise ValueError
        return my_title
    
    @validates('content')
    def content_validation(self, key, my_content):
        if len(my_content) < 250:
            raise ValueError
        return my_content

    @validates('summary')
    def summary_validation(self, key, my_summary):
        if len(my_summary) > 250:
            raise ValueError
        return my_summary
    
    @validates('category')
    def category_validation(self, key, my_category):
        if my_category == "Fiction" or my_category == "Non-Fiction":
            return my_category
        raise ValueError
    


    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
