from fastapi import  HTTPException

from db.db import _db
from db.db import _counter
from core.logger import logger

class BlogService:

    # In a method create a blog, check if title already exists and raise HTTPException if it does. Otherwise, create the blog and return it.
    @staticmethod
    def create_blog(blog_data: dict):

        global _counter
        for b in _db.values():
            if b["title"] == blog_data["title"]:
                logger.info(f"Blog title already exists: {blog_data['title']}")
                raise HTTPException(status_code=400, detail="Blog title already exists")
        blog_id = _counter
        _db[blog_id] = {
            "id": blog_id,
            "title": blog_data["title"],
            "content": blog_data["content"],
            "author_email": blog_data["author_email"]
        }

        _counter += 1
        return _db[blog_id] 
    
    # In a method get_blog, check if blog exists by ID and raise HTTPException if it doesn't. Otherwise, return the blog.
    @staticmethod
    def get_blog(blog_id: int):
        if blog_id not in _db:
            logger.info(f"Blog not found: {blog_id}")
            raise HTTPException(status_code=404, detail="Blog not found")
        return _db[blog_id]
    
    # In a method get_all_blogs, return a list of all blogs in the database.
    @staticmethod
    def get_all_blogs():
        return list(_db.values())
    
    # In a method get_blogs_by_author, return a list of all blogs in the database that match the given author_email.
    @staticmethod
    def get_blogs_by_author(author_email: str):
        return [b for b in _db.values() if b["author_email"] == author_email]
    
    # In a method delete_blog, check if blog exists by ID and raise HTTPException if it doesn't. Otherwise, delete the blog and return a success message.
    @staticmethod   
    def delete_blog(blog_id: int):
        if blog_id not in _db:
            logger.info(f"Blog not found: {blog_id}")
            raise HTTPException(status_code=404, detail="Blog not found")
        del _db[blog_id]
        return {"detail": "Blog deleted successfully"}
    
    # In a method update_blog, check if blog exists by ID and raise HTTPException if it doesn't. Otherwise, update the blog with the given data and return the updated blog.
    @staticmethod
    def update_blog(blog_id: int, blog_data: dict):
        if blog_id not in _db:
            logger.info(f"Blog not found: {blog_id}")
            raise HTTPException(status_code=404, detail="Blog not found")
        _db[blog_id].update(blog_data)
        return _db[blog_id]
    