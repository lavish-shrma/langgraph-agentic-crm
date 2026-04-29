import asyncio
import logging
from langchain_groq import ChatGroq
from app.config import settings

logger = logging.getLogger(__name__)

# Primary model for general tasks and extraction
primary_llm = ChatGroq(
    api_key=settings.GROQ_API_KEY,
    model="llama-3.3-70b-versatile",
    temperature=0.1,
    max_tokens=2048,
)

# Secondary model for heavier reasoning (summarization)
secondary_llm = ChatGroq(
    api_key=settings.GROQ_API_KEY,
    model="llama-3.3-70b-versatile",
    temperature=0.3,
    max_tokens=2048,
)


async def invoke_with_retry(llm, messages, max_retries=7):
    """Invoke LLM with exponential backoff retry logic.

    Args:
        llm: The LangChain LLM instance.
        messages: List of messages to send.
        max_retries: Maximum number of retries.

    Returns:
        The LLM response.

    Raises:
        Exception: If all retries are exhausted.
    """
    for attempt in range(max_retries):
        try:
            response = await llm.ainvoke(messages)
            return response
        except Exception as e:
            error_msg = str(e)
            logger.warning(f"LLM call attempt {attempt + 1}/{max_retries} failed: {error_msg}")

            if attempt == max_retries - 1:
                logger.error(f"All {max_retries} LLM call attempts failed.")
                raise Exception("AI service temporarily unavailable. Please try again in a moment.")

            # Special handling for 429 (Rate Limit) errors
            if "429" in error_msg:
                wait_time = 30
                logger.info(f"Rate limit hit (429). Waiting {wait_time}s before retry...")
            else:
                # Exponential backoff: 1s, 2s, 4s, 8s, 16s, 32s
                wait_time = 2 ** attempt
                logger.info(f"Retrying in {wait_time}s...")
            
            await asyncio.sleep(wait_time)


def get_primary_llm():
    """Get the primary LLM (llama-3.1-8b-instant (official Groq replacement for decommissioned gemma2-9b-it))."""
    return primary_llm


def get_secondary_llm():
    """Get the secondary LLM (llama-3.3-70b-versatile) for heavier tasks."""
    return secondary_llm
