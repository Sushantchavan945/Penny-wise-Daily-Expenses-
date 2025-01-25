
from groq import Groq
def generate_Reciepe(items):
    prompt=f'''
        you are recipe suggestion assistant. The user will provide list of ingredients the have
        available, and you will suggest one or more receipes that they can make with those ingredients.
        {items}
    '''

    client=Groq(
        api_key="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"
    )

    completion=client.chat.completions.create(
        model="llama-3.2-1b-preview",
        messages=[
            {'role':'user',
             'content':prompt}

        ],
        temperature=1

    )

    print(completion.choices[0].message.content)

items="Chicken,Tomatoes"
generate_Reciepe(items)