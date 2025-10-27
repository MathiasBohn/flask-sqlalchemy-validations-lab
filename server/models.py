from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators
    @validates('name')
    def validate_name(self, key, name):
        # Check if name is provided (not empty or None)
        if not name:
            raise ValueError("Author must have a name")
        
        # Check for duplicate names
        # Only check if this is a new instance or the name has changed
        existing_author = db.session.query(Author).filter(Author.name == name).first()
        if existing_author and existing_author.id != self.id:
            raise ValueError("Author name must be unique")
        
        return name
    
    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        # Check if phone number is exactly 10 digits
        if phone_number:
            # Remove any non-digit characters for checking
            digits_only = ''.join(filter(str.isdigit, phone_number))
            if len(digits_only) != 10:
                raise ValueError("Phone number must be exactly 10 digits")
        return phone_number

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
    @validates('content')
    def validate_content(self, key, content):
        # Check if content is at least 250 characters
        if not content or len(content) < 250:
            raise ValueError("Post content must be at least 250 characters long")
        return content
    
    @validates('summary')
    def validate_summary(self, key, summary):
        # Check if summary is maximum 250 characters
        if summary and len(summary) > 250:
            raise ValueError("Post summary must be a maximum of 250 characters")
        return summary
    
    @validates('category')
    def validate_category(self, key, category):
        # Check if category is either Fiction or Non-Fiction
        if category not in ['Fiction', 'Non-Fiction']:
            raise ValueError("Post category must be either Fiction or Non-Fiction")
        return category
    
    @validates('title')
    def validate_title(self, key, title):
        # Check if title contains clickbait phrases
        clickbait_phrases = ["Won't Believe", "Secret", "Top", "Guess"]
        
        if not any(phrase in title for phrase in clickbait_phrases):
            raise ValueError("Post title must contain one of the following: 'Won't Believe', 'Secret', 'Top', 'Guess'")
        
        return title

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'