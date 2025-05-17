import pytest
from aiogram import types
from unittest.mock import AsyncMock

from handlers.client_handlers import process_task_title

@pytest.mark.asyncio
async def test_process_task_title():
    message = types.Message(
        text="Test Title",
        chat=types.Chat(id=123, type="private"),
        from_user=types.User(id=123, first_name="Test")
    )
    state = AsyncMock()
    
    await process_task_title(message, state)
    
    state.proxy.assert_called_once()
    async with state.proxy() as data:
        assert data['title'] == "Test Title"
