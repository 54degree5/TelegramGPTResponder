# код написан сухоцким александром
import openai
from telethon import TelegramClient, events

api_id = YOUR_API_ID # в виде инта
api_hash = 'YOUR_API_HASH' # эт типо тут можно достать my.telregram.org или че то такое, хз, сами гуглите, мне лень, я давно там хеш делал
openai_api_key = '**-********************************'  # твой ключ от OpenAI

openai.api_key = openai_api_key

client = TelegramClient('anon', api_id, api_hash) # подключаем клиента, с названием anon, и если есть anon.session уже файл на компе, он войдет автоматически


def generate_gpt3_response(message_to_ask): # фкнкция ответа gpt, ну типо отправляет запрос и возвращает ответ 
    # global ans
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", # тут типа версия gpt для ответа, жду когда мне дадут 4...
        messages=[
            {"role": "user", "content": message_to_ask},
        ],
        temperature=1 # на сколько разнообразнй будет в ответах
    )
    return (completion.choices[0]["message"]["content"]) # просто возвращение ответа
     # код написан 54degree5


@client.on(events.NewMessage) # ждем на клиенте евент: новые сообщения
async def my_event_handler(event):
    if event.is_private and not event.out: # если не в группе и это не я отправил сообщение то продолжаем
        
        try: # пробуем (потом поймете почему)
            recent_messages = await client.get_messages(event.chat_id, limit=200) # берем 200 сообщений из этой переписки, от которой сообщение
            context_lines = [] # надоело писать коменты, сами разберетесь
            for msg in reversed(recent_messages): # лан, шучу, там мы создали список куда будем сообщения записывать, а тут прогоняемся по сообщениям
                if len(str(msg.text)) > 0: # чекаем если это сообщение не гифка или голосовое, видео итп. ну типо если они такие, то они пустые будут, мы их фильтруем нафиг
                    if msg.out: # если сообщение от меня, то добавляем перед ним "user1"
                        context_lines.append(f"user1: {msg.text}") # добавляем в список сообщение с припиской
                    else: # иначе user2, потом поймете почему
                        context_lines.append(f"user2: {msg.text}") # код написан сухоцким александром (тоже добавляем в список сообщение с припиской)

         # код написан сухоцким александром
            context ="You are now my responder for telegram. Read the last messages of the conversation (the messages are sepperated from one another with a '^&' symbols and a new line), and make a response for it in russian, for the last message. You must learn from the messages, how the user1 talks, and pretend to be him. So your goal is to reply to the last message in the conversation and act like a real person, and continue the chat, so act like the user1. If he puts like something in his messages different, copy him. Remember, you are 'user1'. In the output just print the next message to send from user1.\n"+ "\n^&\n".join(context_lines) # ну сначала я капец долго писал этот промпт, его бы еще доработать. короче, он берет этот промпт, и прибавляет к нему потом переписку, разделяя каждое сообщения на \n^&\n, что бы gpt сказать что там короче это разные сообщения. нельзя просто новой строчкой разделять так как в самом сообщении может быть новая строчка, так что будут недоразумения, а он и так не оч умный...
            print(context) # ну типо просто для отладки
            print("Generating response with gpt3...") # тоже
            gpt3_response = generate_gpt3_response(context) # получаем ответ от gpt...
            print("Response: ") # принтим, для отладки
            print(gpt3_response) # да ты сам понять должен
            print("-"*100) # а это разделение разных запросов, что бы "красиво" было
            await event.reply(gpt3_response) # отвечаем на сообщение ответом gpt
        except: # если 200 сообщений это слишком много, то мы пробуем 70. (просто у gpt лимит на кол-во токенов отправленных, мало ли сообщения слишком большие). дальше делаем то же самое что и в первом варике, только с 70 сообщениями, а не с 200
           if event.is_private and not event.out:
                # код написан сухоцким александром
                recent_messages = await client.get_messages(event.chat_id, limit=70) # код написан сухоцким александром
                context_lines = []
                for msg in reversed(recent_messages):
                    if len(str(msg.text)) > 1:
                        if msg.out:  
                            context_lines.append(f"user1: {msg.text}")
                        else:  
                            context_lines.append(f"user2: {msg.text}")
# код написан сухоцким александром
        
                context ="You are now my responder for telegram. Read the last messages of the conversation (the messages are sepperated from one another with a '^&' symbols and a new line), and make a response for it in russian, for the last message. You must learn from the messages, how the user1 talks, and pretend to be him. So your goal is to reply to the last message in the conversation and act like a real person, and continue the chat, so act like the user1. If he puts like something in his messages different, copy him. Remember, you are 'user1' (your name is "Саша"). In the output just print the next message to send from user1.\n"+ "\n^&\n".join(context_lines)
                print(context)
                print("Generating response with gpt3...")
                gpt3_response = generate_gpt3_response(context)
                print("Response: ")
                print(gpt3_response)
                print("-"*100)
                await event.reply(gpt3_response)
 # код написан сухоцким александром


client.start() # ну соответственно запускаем сам клиент
client.run_until_disconnected() # и держим его включенным до конца света
