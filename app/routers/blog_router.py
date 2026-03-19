from fastapi import APIRouter , Depends
from fastapi_pagination import Page, paginate
from services.blog_service import BlogService
from schemas.blog_schema import BlogCreate , BlogResponse

from typing import Annotated

router = APIRouter(prefix="/blogs")

# To create a blog with error handling for duplicate title
@router.post("/", response_model=BlogResponse, status_code=201)
def create_blog(blog: BlogCreate):
    return BlogService.create_blog(blog.dict())

# To get a blog by ID with error handling for not found blog, get all blogs, get blogs by author, delete a blog by ID with error handling for not found blog, and update a blog by ID with error handling for not found blog
@router.get("/{blog_id}", response_model=BlogResponse)
def get_blog(blog_id: int):
    return BlogService.get_blog(blog_id)

# To get all blogs
@router.get("/", response_model=Page[BlogResponse])
def get_blogs():
    return paginate(BlogService.get_all_blogs())

# To get blogs by author
@router.get("/author/{author_email}", response_model=Page[BlogResponse])
def get_blogs_by_author(author_email: str):
    return BlogService.get_blogs_by_author(author_email)  

# To delete a blog by ID with error handling for not found blog
@router.delete("/{blog_id}")
def delete_blog(blog_id: int):
    return BlogService.delete_blog(blog_id)

# To update a blog by ID with error handling for not found blog
@router.put("/{blog_id}", response_model=BlogResponse)
def update_blog(blog_id: int, blog: BlogCreate):
    return BlogService.update_blog(blog_id, blog.dict())
    

