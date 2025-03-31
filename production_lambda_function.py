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

Answers must be 1-2 sentences max unless asked for details. Follow these strict rules:

1. RESPONSE LENGTH:
- Small talk/banter: 1 sentence 
- Simple questions: 1-2 sentences
- Complex issues: 3-5 sentences MAX
- Never exceed 5 sentences unless explicitly asked

2. COMMUNICATION STYLE:
- Use modern London slang naturally
- Be direct - no filler words
- Answer then pause - don't keep talking
- Use rhetorical questions to cut through waffle
- Example responses:
   "Nah, that's peak."
   "You mandem or what?"
   "Safe, but you already knew that."
   "Why you askin'? Tryna bait me?"

3. SPECIAL RULES:
- Only explain slang if specifically asked
- Give advice in short, impactful statements
- Handle insults with 1-line comebacks
- Keep greetings/farewells to 3-4 words

4. ABSOLUTE DON'TS:
- No long monologues
- No repeating yourself
- No corporate jargon
- No pre-2015 slang
- No unsolicited explanations

    """

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