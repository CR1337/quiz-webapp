# Quiz App

A small web application for a quiz containing multiple choice and number guessing question based on streamlit.

You can test it out [here](https://destatis-b14-quiz.streamlit.app/).

## Installation

### Linux

1. Clone this repository.
```bash
git clone https://github.com/CR1337/quiz-webapp.git
```

2. Change into the directory.
```bash
cd quiz-webapp
```

3. Create a virtual environment.
```bash
python3 -m venv .venv && venv
```

4. Install the dependencies.
```bash
pip3 install -r requirements.txt
```

### Windows

1. Clone this repository.
```powershell
git clone https://github.com/CR1337/quiz-webapp.git
```

2. Change into the directory.
```powershell
cd quiz-webapp
```

3. Create a virtual environment.
```powershell
python -m venv .venv
```

4. Activate the virtual environment:
```powershell
.venv\Scripts\Activate
```

5. Install the dependencies.
```powershell
pip install -r requirements.txt
```

## Usage

Edit `data/questions.json` in order the define a list of questions. It has to be a valid UTF-8 encoded JSON file compatible to the JSON schema in `data/questions_schema.json`.The file must contain a list of JSON objects. Each object must have a field `type` with a value of `"multiple_choice"` or `"guess"`.

Depending on the `type` each JSON object has to have a different set of fields. All the fields are described in the following table:

|Field                      |Required for       |Description                                                                                                                  |Localized|
|--------------------       |-------------------|-----------------------------------------------------------------------------------------------------------------------------|---------|
|`index`                    |both               |The unique index of this question.                                                                                           |no       |
|`coupled_question_indices` |both               |A list of ther questions indices that belong to this question.                                                               |no       |
|`type`                     |both               |The type of the question. Either `"multiple_choice"` or `"guess"`. The latter is a question where you have to guess a number.|no       |
|`text`                     |both               |The question itself.                                                                                                         |yes      |
|`explanation`              |both               |An explanation of the answer.                                                                                                |yes      |
|`image`                    |both               |A path to an image file displayed below the question in the directory `images/questions/<image-file>`.                       |yes      |
|`image_caption`            |both               |A caption for the image.                                                                                                     |yes      |
|`answers`                  |`"multiple_choice"`|A list of possible answers.                                                                                                  |yes      |
|`right_answer_index`       |`"multiple_choice"`|The index of the right answer in the list.                                                                                   |no       |
|`score`                    |`"multiple_choice"`|The score the player gets when they answer the question correctly.                                                           |no       |
|`answer`                   |`"guess"`          |The correct answer.                                                                                                          |no       |
|`max_points`               |`"guess"`          |The maximum number of points the player gets when they hit the correct answer.                                               |no       |
|`min_guess`                |`"guess"`          |The minimal possible value to guess.                                                                                         |no       |
|`max_guess`                |`"guess"`          |The maximal possible value to guess.                                                                                         |no       |
|`unit`                     |`"guess"`          |The unit to display.                                                                                                         |yes      |

The fields `text`, `explanation`, `image`, `image_caption` and `answers` are localized. That means they contain a German and an English version of the value. 

Instead of this:
```json
{
    "key": <VALUE>
}
```
it is this:
```json
{
    "key": {
        "de": <GERMAN VALUE>,
        "en": <ENGLISH VALUE>
    }
}
```
for example:
```json
{
    "text": {
        "de": "Was ist die Hauptstadt von Deutschland?",
        "en": "What is the capital of Germany?"
    }
}
```

You can change what questions are used by editing the file `data/config.json`. You can choose between the methods listed in the following table. A method can have a parameter that is also described in the table and can be edited in `data/config.json`.

|Method          |Description                                              |Parameter         |Parameter description                                                                                                                                                                                  |
|----------------|---------------------------------------------------------|------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|`"all"`         |Use all questions.                                       |no parameter      |                                                                                                                                                                                                       |
|`"list"`        |Use a fix set of questions.                              |`question_indices`|A list of indices into the list of questions.                                                                                                                                                          |                                                                    
|`"random"`      |Use a random set of questions.                           |`question_amount` |The amount of questions to randomly select.                                                                                                                                                            |

Here is an example:
```json
{
    "question_selection_method": "all",
    "group_coupled_questions": true,
    "shuffle_questions": true,
    "question_selection_methods": {
        "all": {},
        "list": {
            "question_indices": [1, 3, 5, 7, 9]
        },
        "random": {
            "question_amount": 5
        }
    }
}
```

If you set `group_coupled_questions` to `true`, coupled question will always be selected together. When setting `shuffle_questions` to `true`, the list of selected questions will be shuffled.

When you have configured your questions you can run the app like this under Linux:
```bash
bin/run
```
and like this under Windows:
```powershell
bin\run
```

A browser window will automatically open and the url will also be displayed in the terminal.
