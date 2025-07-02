from com.mhire.app.config.config import OPENAI_API_KEY
import openai
client = openai.OpenAI(api_key = OPENAI_API_KEY)
clientModereration = openai.OpenAI()