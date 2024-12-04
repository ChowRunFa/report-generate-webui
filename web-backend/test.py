from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage

class PaperSummarizer:
    def __init__(self, key_word, language, llm_base_url, api_key):
        self.key_word = key_word
        self.language = language
        self.llm = ChatOpenAI(
            model_name="rog",
            openai_api_base=llm_base_url,
            openai_api_key=api_key,
            streaming=False,
        )

    def summarize(self, clip_text):
        messages = [
            SystemMessage(
                role='system',
                content=f"You are a researcher in [{self.key_word}] good at concise paper summaries"
            ),
            SystemMessage(
                role='assistant',
                content=f"<summary> summarized; <Methods> need help. {clip_text}"
            ),
            HumanMessage(
                role='user',
                content=f"""
                    7. Describe the methodological idea with concise {self.language} statements, steps as:
                    - (1):...
                    - (2):...
                    - .......
                    Output as:
                    ## Methods: \n\n
                    - (1):xxx;\n 
                    - (2):xxx;\n 
                    - .......
                """
            )
        ]
        response = self.llm(messages)
        return response.content

# Example usage
if __name__ == "__main__":
    summarizer = PaperSummarizer(
        key_word="AI Research",
        language="English",
        llm_base_url="http://59.77.7.24:8000/v1",
        api_key="EMPTY"
    )
    clip_text = "Example paper content to summarize."
    result = summarizer.summarize(clip_text)
    print("Method Result:\n", result)
