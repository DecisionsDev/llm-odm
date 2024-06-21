# Demonstration: Power of LLM with Rule Engine

This demonstration aims to prove that using a Large Language Model (LLM) with a rule engine is powerful and effective.

## Sample Sentence

* `Compute a loan validation rate with an amount of $10,000, a duration of 10 years, and an interest rate of 0.01.`

## Scenario

### Using the Chatbot Without the Decision Engine

1. Send this question: `Compute a loan validation rate with an amount of $10,000, a duration of 10 years, and an interest rate of 0.01.`
2. The chatbot returns a response computed by the LLM, which is inconsistent.
3. Send the same question again: `Compute a loan validation rate with an amount of $10,000, a duration of 10 years, and an interest rate of 0.01.`
4. The chatbot returns a response computed by the LLM, which is still inconsistent.

### Using the Chatbot With the Decision Engine

5. Enable the Decision Engine by clicking the `Decision Engine toggle`.
6. Send the sentence again: `Compute a loan validation rate with an amount of $10,000, a duration of 10 years, and an interest rate of 0.01.`
7. The chatbot returns a response computed by the Decision Engine that aligns with the policies.
8. The decisions are explained. You can click on the Rules Link to view them (Username: odmAdmin, Password: odmAdmin).
9. Re-execute the same sentence to confirm the results remain consistent.

## Code

Code, descriptions, and a video can be found at this [location](https://github.com/DecisionsDev/llm-odm/tree/demo-exec/chat-with-decision-service).