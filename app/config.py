import os
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
	from dotenv import load_dotenv  # Uncomment when running locally
	load_dotenv()
except:
	logger.info('dotenv loaded')

OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
