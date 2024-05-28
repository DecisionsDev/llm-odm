from langchain_core.tools import BaseTool

from typing import Optional
from langchain_core.callbacks import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain_core.pydantic_v1 import (
    BaseModel,
    Field  
)
import json

class LoanValidationInput(BaseModel):
    loan_amount: str = Field(..., description="The loan amount")
    duration: str = Field(..., description="The duration")
    interest_rates: str = Field(..., description="The interest rates")
class LoanValidationTool(BaseTool):
    return_direct: bool = True
    name = "compute_rules_"
    args_schema = LoanValidationInput

    description = """Use this tool when you need to comppute a loan validation. Make sure you use a input format similar to the JSON below:
    {{ "loan_amount": "The loan amount", "duration": "tbe laon duration", "interest_rates":"the interest rates" }}"""

    def _run(self, loan_amount: str, duration: str, interest_rates: str) -> str:
        """Use the tool."""

        return self.invokeRules(loan_amount,duration,interest_rates)
    
    async def _arun(self, loan_amount: str,duration: str, interest_rates: str) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("API does not support async")
    
    def invokeRules(self, loan_amount,duration,interest_rates):      
#      token = self.getToken();
      loan_amount = str(loan_amount).strip()
      return "LLM extract this informations "+loan_amount+" Duration : "+duration+" and call the rules engine result is a rates of 1.4%"

