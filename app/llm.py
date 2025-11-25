from openai import OpenAIError, AsyncOpenAI
from tenacity import (retry,
                      stop_after_attempt,
                      wait_exponential,
                      retry_if_exception_type,
                      before_sleep_log,
                      after_log)
from pydantic import BaseModel, Field
from typing import List
from config import OPENAI_API_KEY
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async_openai_client = AsyncOpenAI(api_key=OPENAI_API_KEY)


class GenText(BaseModel):
    text: str = Field(description="The text result of the query")


@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=1, max=10),
    retry=retry_if_exception_type(OpenAIError),
    before_sleep=before_sleep_log(logger, logging.WARNING),
    after=after_log(logger, logging.INFO)
)
async def async_response_openai(
    user_prompt,
    model: str = 'gpt-4o-mini',
    system_prompt: str="You are a helpful assistant.",
    response_model: BaseModel = GenText,
    temperature=0.1) -> BaseModel:
    response = await async_openai_client.responses.parse(
        model=model,
        input=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=temperature,
        text_format=response_model,
    )
    return response.output_parsed


@retry(
    stop=stop_after_attempt(5),
    wait=wait_exponential(multiplier=1, min=1, max=10),
    retry=retry_if_exception_type(OpenAIError),
    before_sleep=before_sleep_log(logger, logging.WARNING),
    after=after_log(logger, logging.INFO)
)
async def async_embed_text(
    text: str,
    model: str = 'text-embedding-3-large'
) -> List[float]:
    response = await async_openai_client.embeddings.create(
        input=text,
        model=model
    )
    return response.data[0].embedding