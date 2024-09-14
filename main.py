from ollama import Client
from chat_history import ChatHistory

cot_prompt = open('cot-prompt.txt', 'r').read()
basic_prompt = open('basic-prompt.txt', 'r').read()

cot_model = 'gemma2:9b'
basic_model = 'gemma2:9b'

client = Client(host='http://gpu02:11434')

# Какое число больше 9.000009 или 9.0000011?
basic_history = ChatHistory(system_prompt=basic_prompt, history_limit=4)
while True:
    user_message = input("User: ")

    # Reset chat command
    if user_message.strip() == "/reset":
        basic_history = ChatHistory(system_prompt=basic_prompt, history_limit=4)
        print("History reset completed!")
        continue

    # Skip empty messages from user
    if user_message.strip() == "":
        continue

    # Thinking....
    cot_history = ChatHistory(system_prompt=cot_prompt, history_limit=1)
    cot_history.add_user_message(user_message)
    cot_messages = cot_history.get_messages()

    print(cot_messages)

    cot_response = client.chat(model=cot_model, messages=cot_messages)
    cot_output = cot_response['message']['content']

    print(">>>>>>>>>>THINKING>>>>>>>>>>>>")
    print(cot_output)
    print(">>>>>>>>>/THINKING>>>>>>>>>>>>")

    # Add messages
    basic_history.add_user_message(user_message)
    basic_history.add_think_message(cot_output)

    # Add user message to chat
    basic_history.add_user_message(user_message)
    basic_messages = basic_history.get_messages()

    print(basic_messages)

    basic_response = client.chat(model=basic_model, messages=basic_messages)
    output = basic_response['message']['content']
    basic_history.add_assistant_message(output)

    print("Bot:", output)
    print()
    print("==============================")
    print()
