from langchain_core.tools import BaseTool
from invokeRuleServer import InvokeRuleServer
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
    loan_amount: int = Field(..., description="The loan amount")
    duration: str = Field(..., description="The duration")
    interest_rates: str = Field(..., description="The interest rates")
class LoanValidationTool(BaseTool):
    return_direct: bool = True
    name = "compute_rules_"
    args_schema = LoanValidationInput
    decisionServer=InvokeRuleServer()
    payload=  {
    "loan": {
        "amount": 300000,
        "duration": 360,
        "yearlyInterestRate": 5,
        "yearlyRepayment": 3,
        "approved": True,
        "messages": []
    },
    "borrower": {
        "name": "string",
        "creditScore": 300,
        "yearlyIncome": 3
        }

    }
    description = """Use this tool when you need to comppute a loan validation. Make sure you use a input format similar to the JSON below:
    {{ "loan_amount": "The loan amount", "duration": "tbe laon duration", "interest_rates":"the interest rates" }}"""

    def _run(self, loan_amount: int, duration: str, interest_rates: str) -> str:
        """Use the tool."""

        return self.invokeRules(loan_amount,duration,interest_rates)
    
    async def _arun(self, loan_amount: str,duration: str, interest_rates: str) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("API does not support async")
    
    def invokeRules(self, loan_amount,duration,interest_rates):      
      payload=self.payload
      payload['loan']['amount']=loan_amount
      result=self.decisionServer.invokeRules(payload)
      response=self.decisionServer.invokeRules(payload)
      return json.dumps(response, indent=2)
