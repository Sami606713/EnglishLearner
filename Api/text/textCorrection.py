from langchain.prompts import PromptTemplate
from config.model import loadModel

def textCorrection(text:str):
    """
    
    """
    try:
        with open("prpmpts/correction.md","r",encoding="utf-8") as file:
            template = file.read()

        prompt = PromptTemplate(
        input_variables=["sentence"],
        template=template,
        )

        final_prompt = prompt.format(sentence=text)

        model = loadModel()
        corrected_sentence = model.invoke(final_prompt)
        return corrected_sentence.content
    except Exception as e:
        return str(e)
    
if __name__ =="__main__":
    text = "I a am boy"
    print(textCorrection(text))
