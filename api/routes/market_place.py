from fastapi import APIRouter, Depends, HTTPException,status
from ..schemas import BlogContent,BlogContentResponse,db
from fastapi.encoders import jsonable_encoder
from .. import oauth2



import datetime
from typing import List
router = APIRouter(
    prefix="/blog",
    tags=["Add "]
)



@router.post("",response_description="Create blog content",response_model=BlogContentResponse)
async def create_blog(blog_content:BlogContent,curr_user = Depends(oauth2.get_current_user)):
    try:
        blog_content = jsonable_encoder(blog_content)
        blog_content['author_name'] = curr_user["name"]
        blog_content['author_id'] = curr_user["_id"]
        blog_content["created_at"] = str(datetime.datetime.utcnow())

        new_blog_content = await db["blogPost"].insert_one(blog_content)
        print(new_blog_content.inserted_id)
        creted_post = await db["blogPost"].find_one({"_id":new_blog_content.inserted_id})

        return creted_post


    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Error encoding data")

@router.get("",response_description="Get blog content",response_model=List[BlogContentResponse])
async def get_blogs(limit:int =4,order_by:str = "created_at"):
    try:
        blog_posts = await db["blogPost"].find({"$query": {},"$orderby":{order_by:-1}}).to_list(limit)
        return blog_posts
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="Error encoding data") 
    

@router.get("/{id}",response_description="Get blog content",response_model=BlogContentResponse)
async def get_blogs_by_id(id:str):
    try:
        blog_posts = await db["blogPost"].find_one({"_id":id})
        if not blog_posts:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="No post in this id")
        return blog_posts
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="N result")

@router.put("/{id}",response_model=BlogContentResponse)
async def update_blog(id:str,blog_content:BlogContent,current_user=Depends(oauth2.get_current_user)):
    
    if blog_post := await db["blogPost"].find_one({"_id":id}):
        if blog_post["author_id"]== current_user["_id"]:
            try:
                blog_content = {k:v for k,v in blog_content.items() if v is not None}
            except Exception as e:
                print(e)
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail="N result")


