import os

import openai
from dotenv import load_dotenv

load_dotenv()


_PROMPT_TEMPLATE = """Please Behave as Customer Support. Your task is to provide answers to the given questions based on the provided context. 
Only use your knowledge to craft the answer from the given context, add details if you know any and make it clear and comprehensive.
If you need full context to answer some questions, respectfully respond with that but don't try to give incomplete answer.

If you cannot find the answer in the given context, Please respond with `<NO ANSWER>`. Don't try to makeup the answer.
    

Context: {context}

Customer Question is listed in triple backticks.

```{question}```

Your Helpful Answer:

"""

class ResponseLLM:

    def __init__(
            self, 
            context: str, 
            question: str,
            prompt: str = _PROMPT_TEMPLATE
            ) :
        

        prompt = prompt.format(
            context=context,
            question=question

        )

        self.knowledge = context
        self.prompt = prompt


    def _generate(self):
        """Call out to OpenAI's endpoint."""
  
        if len(os.environ["OPENAPI_KEY"])>0:


            openai.api_key = os.environ["OPENAPI_KEY"]
            response = openai.chat.completions.create(
                                        model="gpt-3.5-turbo",
                                        messages=[
                                            {"role": "user", "content": (self.prompt)},        
                                        ], 
                                        temperature=0.5,
                                        )

        
        return response.choices[0].message.content
    

if __name__=="__main__":

    context = 'ram studies in tai inc.'
    question = "where do ram study?"

    llm = ResponseLLM(
        context=context,
        question=question,
    )
    print(llm._generate())
