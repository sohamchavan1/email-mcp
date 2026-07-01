from llm_service import LLMService

llm = LLMService()

print(
    llm.summarize_email(
        """
Hi Soham,

Your interview is scheduled on Monday at 10 AM.

Please join 15 minutes early.

Regards,
HR Team
"""
    )
)