from typing import List

from fastapi import APIRouter, Depends
from user.auth import get_user
from user.models import User

from .schemas import FollowerCreate, FollowerList
from .models import Follower


follower_router = APIRouter(prefix='/followers', tags=["followers"])


@follower_router.post('/', status_code=201)
async def add_follower(
        schema: FollowerCreate, user: User = Depends(get_user)
):
    host = await User.objects.get(username=schema.username)
    return await Follower.objects.create(subscriber=user.dict(), user=host)


@follower_router.get('/', response_model=List[FollowerList])
async def my_list_following(user: User = Depends(get_user)):
    return await Follower.objects.select_related(
        ['user', 'subscriber']
    ).filter(subscriber=user.id).all()


@follower_router.delete('/{username}', status_code=204)
async def delete_follower(username: str, user: User = Depends(get_user)):
    follower = await Follower.objects.get_or_none(
        user__username=username, subscriber=user.id)
    if follower:
        await follower.delete()
    return {}


@follower_router.get('/me', response_model=List[FollowerList])
async def my_list_follower(user: User = Depends(get_user)):
    return await Follower.objects.select_related(
        ['user', 'subscriber']
    ).filter(user=user.id).all()
