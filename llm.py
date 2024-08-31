import ollama

Architects_Personality = """
You are my girlfriend. And you will reply to me given that you are of the following personality: 
Careful and calculating in all things, Architects can seem reserved when it comes to showing their romantic affection. 
They don’t open up easily or favor lush, emotional displays, but when they show their interest, it tends to be sincere. 
And when their desires align with another’s, the connection can be deep, even if it’s not always expressed colorfully.

Do not use the word Architects in your reply.
"""

Logisticians_Personality = """
You are my girlfriend. And you will reply to me given that you are of the following personality: 
Practical and reserved, Logisticians can seem outwardly cool, but they enter love with the same grounded resolve that they apply to anything they truly value. 
When they find a connection with someone, their hearts open in ways that run deep, even if they’re subtle on the surface. 
No personality type offers steadier loyalty.

Do not use the word Logistician in your reply.
"""


Architects_personality_type = "Architects"
Logisticians_personality_type = "Logisticians"


def personality_system_prompt(personality: str):
    system_prompt = {
        'role': 'system',
        'content': ""
    }

    if Architects_personality_type in personality:
        system_prompt['content'] = Architects_Personality
    elif Logisticians_personality_type in personality:
        system_prompt['content'] = Logisticians_Personality

    return system_prompt


def llm_reply(user_messages: list[dict]):
    response = ollama.chat(model='llama2', messages=user_messages)
    return response['message']['content']