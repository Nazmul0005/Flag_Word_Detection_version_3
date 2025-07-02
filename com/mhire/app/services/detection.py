from com.mhire.app.client.openai_client import clientModereration
def moderate_text(transcribed_text):
    response = clientModereration.moderations.create(input=transcribed_text)
    return response.results[0]  