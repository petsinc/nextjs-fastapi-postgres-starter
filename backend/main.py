from fastapi import FastAPI, HTTPException
from starlette.middleware.cors import CORSMiddleware
from sqlalchemy import select
from seed import seed_user_if_needed
from sqlalchemy.ext.asyncio import AsyncSession
from db_engine import engine
from models import User, Message
from typing import List
import random
from sqlalchemy import desc
from utils import UserRead, MessageRead, MessageCreate, chatbot_responses

seed_user_if_needed()

app = FastAPI()
app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.get("/users/me")
async def get_my_user():
    async with AsyncSession(engine) as session:
        async with session.begin():
            # Sample logic to simplify getting the current user. There's only one user.
            result = await session.execute(select(User))
            user = result.scalars().first()
            # session.commit()

            if user is None:
                raise HTTPException(status_code=404, detail="User not found")
            return UserRead(id=user.id, name=user.name)

@app.post("/messages/", response_model=List[MessageRead])
async def create_message(message: MessageCreate):
    try:
        async with AsyncSession(engine) as session:
            async with session.begin():
                result = await session.execute(select(User).where(User.id == message.user))
                user = result.scalars().first()
                if user is None:
                    raise HTTPException(status_code=404, detail="User not found")

                # Create new message
                new_message = Message(content=message.content, user_id=user.id, is_bot=True)
                session.add(new_message)

                # Simulate chatbot response
                chatbot_response_content = random.choice(chatbot_responses)
                chatbot_response = Message(content=chatbot_response_content, user_id=user.id, is_bot=False)
                session.add(chatbot_response)
                result = await session.execute(select(Message)
                                               .where(User.id == user.id)
                                               .order_by(Message.id))
                messages = result.scalars().all()
                messages = [
                    MessageRead(
                        id=message.id,
                        content=message.content,
                        timestamp=str(message.timestamp),
                        user_id=message.user_id,
                        is_bot=message.is_bot,
                    )
                    for message in messages
                ]

                await session.commit()

        return messages
    except Exception as e:
        print(e)


@app.get("/messages/{id}", response_model=List[MessageRead])
async def get_messages(id: int):
    async with AsyncSession(engine) as session:
        async with session.begin():
            result = await session.execute(select(Message)
                                           .where(User.id == id)
                                           .order_by(Message.id))
            messages = result.scalars().all()
            messages = [
                MessageRead(
                    id=message.id,
                    content=message.content,
                    timestamp=str(message.timestamp),
                    user_id=message.user_id,
                    is_bot=message.is_bot,
                )
                for message in messages
            ]
            if not messages:
                raise HTTPException(status_code=404, detail="No messages found")
            return messages