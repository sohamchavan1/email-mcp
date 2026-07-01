from langchain_ollama import ChatOllama


class LLMService:

    def __init__(self):

        self.llm = ChatOllama(
            model="qwen3.5:4b",
            temperature=0
        )

    def summarize_email(
        self,
        email_body: str
    ) -> str:

        try:

            prompt = f"""
You are an email assistant.

Summarize the email in:
- 3 to 5 bullet points
- Important decisions
- Action items
- Deadlines (if any)

Email:

{email_body}
"""

            response = self.llm.invoke(
                prompt
            )

            return response.content

        except Exception as e:

            return f"LLM summarization failed: {e}"