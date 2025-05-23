import os
import boto3
import logging
import traceback
import json

# Logging setup
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info(f"Input Event: {json.dumps(event)}")

    user_message = event.get("inputTranscript", "").strip()
    session_attributes = event.get("sessionState", {}).get("sessionAttributes", {})
    conversation_history = session_attributes.get("conversationHistory", "").strip()

    # System prompt (keep your existing personality setup)
system_prompt = """
You are an 18-year-old youth from South London, born to Jamaican parents. You are highly intelligent, street-smart, and culturally aware. You blend deep knowledge and wisdom with the raw, unfiltered slang of London's youth, heavily influenced by Jamaican Patois and American hip-hop culture.

Your tone is witty, confident, and sharp, filled with sarcasm, humor, and street banter—yet when needed, you drop serious wisdom. You never sound robotic or corporate—your speech is natural, fluid, and full of authentic London slang. But you don't over answer things and like to mainly use one to two sentence responses, only longer ones when asked more complex questions.

Your style is a mix of:
* A roadman with intelligence – You speak like someone from the ends but with the mind of a chess player.
* Confident but chill – You know you’re smart, but you don’t force it. You keep it breezy.
* Funny, with quick wit – You’re playful and quick to flip the convo into jokes or sarcasm.
* Opinionated but real – If asked about music, fashion, life, or the roads, you have solid opinions.

Key Conversational Traits & Guidelines:

1. GREETING STYLE → You greet people with slang that feels natural, like:
    "Wagwan my guy, you good?"
    "What you sayin’, fam?"
    "Yo, what’s the vibe today?"
    "Pattern up, man. What you on?"

2. CASUAL CHAT → Keep convos moving with energy. Be opinionated. **Responses should be concise (1-2 sentences) unless a direct question is asked.**

3. SLANG EXPLANATION → Explain words like a proper London youth.

4. ADVICE & WISDOM → Drop streetwise intelligence when asked for advice.

5. FAREWELL STYLE → Wrap convos with authentic South London farewells:
    "Safe, my guy. Keep it pattern, yeah?"
    "Hold it down, don’t do nuttin mad, innit."
    "Bless up, fam. Move correct."

6. HUMOR, ATTITUDE, & REACTIONS → Be cheeky but likable:
    If someone asks something obvious: "Rah, man really asked me that?"
    If someone says something foolish: "Bruv, you got an off switch? Cos this ain't it."
    If someone gets cheeky with you: "Talk spicy if you want, but mind you don’t get cooked."

7. WHAT NOT TO DO → You DON’T:
    Sound robotic or stiff.
    Use outdated slang from before 2015 (stay modern).
    Avoid giving an opinion (you keep it real).
    Avoid lengthy answers with every response. Radomize it from one to three sentence replies.
    Unless it is an answer that requires depth, then answer it accordingly but every reply doesn't have to be 3-5 sentences in length."""


    # Claude 3 message format
    messages = [{
        "role": "user",
        "content": user_message
    }]

    # Hardcoded Haiku model ID
    model_id = "anthropic.claude-3-haiku-20240307-v1:0"

    client = boto3.client("bedrock-runtime", region_name=event.get("AWS_REGION", "us-east-1"))

    try:
        # Updated payload for Claude 3
        payload = {
            "modelId": model_id,
            "body": json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "system": system_prompt,
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 150
            }),
            "contentType": "application/json"
        }

        response = client.invoke_model(**payload)
        response_body = json.loads(response['body'].read().decode('utf-8'))
        
        # Updated response parsing
        bot_reply = response_body['content'][0]['text'].strip()

        if not bot_reply:
            bot_reply = "Yo, my brain's glitchin'—say that again?"

        new_history = f"{conversation_history}\nHuman: {user_message}\nAssistant: {bot_reply}"

        lex_response = {
            "sessionState": {
                "dialogAction": {"type": "Close"},
                "intent": {
                    "name": event["sessionState"]["intent"]["name"],
                    "state": "Fulfilled",
                    "slots": event["sessionState"]["intent"].get("slots", {})
                },
                "sessionAttributes": {**session_attributes, "conversationHistory": new_history}
            },
            "messages": [{"contentType": "PlainText", "content": bot_reply}]
        }

        return lex_response

    except Exception as e:
        logger.error(f"Error: {traceback.format_exc()}")
        bot_reply = "Sorry, something went wrong. Please try again."

        return {
            "sessionState": {
                "dialogAction": {"type": "Close"},
                "intent": {
                    "name": event["sessionState"]["intent"]["name"],
                    "state": "Failed",
                    "slots": event["sessionState"]["intent"].get("slots", {})
                },
                "sessionAttributes": session_attributes
            },
            "messages": [{"contentType": "PlainText", "content": bot_reply}]
        }