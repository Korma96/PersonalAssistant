# PersonalAssistant
 
 Custom personal assistant for recognizing crud operations on alarms and reminders.
 Its output can be used as input for some alarm or calendar api.
 
 Here is an example of using a chatbot:
 
 ![alt text](https://github.com/Korma96/PersonalAssistant/blob/master/example.jpg)
 1. User input
 2. Intent, probability
 3. User input with replaced slots
 4. Recognized slots
 5. Chatbot's answer
 
## Prerequisites
- Python 3.7
- Install libraries from requirements.txt


## Dataset
Facebook Multilingual Task Oriented Dataset
https://github.com/AtmaHou/Task-Oriented-Dialogue-Dataset-Survey


## Training
Library used for chatbot training: https://github.com/tflearn/tflearn


## Project structure
- **dataset/original_data** contains original data from dataset
- **dataset/formatted_data/intent_config.json** file configures which intents and slots will be filtered from dataset
- **dataset/formatted_data/train** folder contains parsed and formatted original data
    - **invalid_data.tsv** contains data from original dataset which is not valid in chatbot context
    - **api.txt** logs recognized slots, which can be used as input for some alarm or calendar api
- **chatbot/data** folder contains model and training_data, model is trained on training_data and training_data is created from formatted data
- **chatbot/code/settings.py** file contains project settings


## How to use it
- Chatbot can be run in two modes:
    - **Accuracy test mode** (checks accuracy on given test dataset)
    - **Manual test mode** (assistant accepts user input and responds to user, additionaly logs recognized slots)
- Before each mode assistant checks if all necessary files are present on given paths. If some of them are missing, they will be recreated from original dataset
- **dataset/formatted_data/intent_config.json** file also configures possible responses to user input, which slots can be recognized in which intent and required slots = slots which must be present in user input
