# Remembrall
- A custom Alexa skill.
- A voice interfaced pocketbook that can be used in Echo devices.
## Description
- The skill lets you keep note of the items and their locations.
- The skill can handle queries about items at specific locations.
- The skill locates items that were previously noted.
## Example Phrases
- Alexa, open pocket book
- Alexa, tell pocket book that my books are in the cupboard
- Alexa, ask pocket book where my watch is
## Skill API
- The skill api was hosted in AWS Lambda
- The lambda.py file provides the intent handlers for the alexa skill kit
- The skill uses dynamoDB for user data management
- Interactions with dynamoDB is handled using boto3 package
