# import os
# import sys
# from groq import Groq
# from dotenv import load_dotenv
#
# load_dotenv()
# print(repr(os.getenv("GROQ_API_KEY")))
# print(len(os.getenv("GROQ_API_KEY")))
# print(repr(os.getenv("GROQ_API_KEY")))
# def generate_therapy_response(prompt):
#     """print("in me kpa")"""
#     # message = details.text
#     # tone = details.emos
#
#     # prompt = "Tell me a funny story in 2 lines"
#     client = Groq()
#     completion = client.chat.completions.create(
#         model="openai/gpt-oss-120b",
#         messages=[
#             {
#                 "role": "user",
#                 "content": prompt
#             }
#         ],
#         temperature=0.6,
#         max_completion_tokens=4096,
#         top_p=0.95,
#         stream=True,
#         stop=None,
#     )
#     print("completion type", type(completion))
#     print(completion)
#     print("--------____---__--_-__-_-__-__----")
#     response = ""
#     for i, chunk in enumerate(completion):
#         response += chunk.choices[0].delta.content or ""
#         # print(f"lol_{i}", chunk.choices[0].delta.content or "", end="")
#     response = None if response == "" else response
#     print(response)
#
# print("Welcome to BizRise! Your ultimate SME solution\n.")
# print("Let me have your whatsapp message company person: ")
# msg = sys.stdin.read()
# print(msg)
# with open("prompt2.txt", mode="r") as f:
#     prompt = f.read()
# prompt = prompt.replace("{conversation_text}", msg)
# print(prompt)
# generate_therapy_response(prompt)
# #Test prompt injection
#
# """[
#   {
#     "customer_name": "Chinedu",
#     "order_items": [
#       {
#         "item": "pepper soup",
#         "quantity": 1
#       },
#       {
#         "item": "bottles of water",
#         "quantity": 3
#       }
#     ],
#     "delivery_date": null,
#     "payment_status": "Paid",
#     "priority_level": "High",
#     "customer_phone": null,
#     "delivery_location": null,
#     "special_instructions": null
#   }
# ]"""
#
# """{
#   "risk_level": "Scam Likely",
#   "scam_type": "Advance Fee Scam",
#   "red_flags": [
#     "urgent pressure tactics",
#     "request for processing fee",
#     "too-good-to-be-true opportunity",
#     "vague procurement offer",
#     "immediate payment required"
#   ],
#   "explanation": "The message pressures you to pay a fee immediately for an unspecified procurement opportunity, a classic advance‑fee scam pattern.",
#   "recommended_action": "Verify with official source",
#   "confidence_score": 92
# }"""
print(str(None))
