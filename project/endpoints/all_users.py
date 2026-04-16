from fastapi import APIRouter, HTTPException
from project.dbforapi import s, Person, Post
from project.schemas import PU
from project.CRUD import get_post


router = APIRouter(prefix="/posts", tags=["Для всех"])


@router.get("/all_posts", tags=["Для всех"])
def get_posts():
    posts = get_post()
    return {f"posts: {posts}"}


# для просмотра постов одного пользователя
@router.post("/get_user_post", tags=["Для всех"])
def get_user_post(data: PU):
    user = s.query(Person).filter(Person.email == data.author_email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    posts = s.query(Post.post_content).filter(Post.user_id == user.user_id).all()
    result_post = []
    for post in posts:
        result_post.append(post[0])
    return f"Автор: {data.author_email} контент: {result_post}"