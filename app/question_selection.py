import json
from random import choice, sample, shuffle, randint
from typing import Any, Dict, List, Set


class QuestionSelector:

    @classmethod
    def select_questions(cls, question_list: List[Dict[str, Any]], config: Dict[str, Any]) -> List[Dict[str, Any]]:
        method = config["question_selection_method"]
        group_coupled_questions = config["group_coupled_questions"]
        shuffle_questions = config["shuffle_questions"]
        match method:
            case "all":
                question_list = cls._select_all_questions(question_list, group_coupled_questions)
            case "list":
                question_indices = method['question_indices']
                question_list = cls._select_list_questions(question_list, question_indices, group_coupled_questions)
            case "random":
                question_amount = config["question_selection_methods"][method]["question_amount"]
                question_list = cls._select_random_questions(question_list, question_amount, group_coupled_questions)
            case _:
                raise ValueError(f"Invalid question selection method: {method}")
            
        if shuffle_questions:
            shuffle(question_list)

        return question_list

    @staticmethod
    def _select_all_questions(question_list: List[Dict[str, Any]], group_coupled_questions: bool) -> List[Dict[str, Any]]:
        if not group_coupled_questions:
            return question_list
        
        question_set: Set = set(question_list)
        new_question_list = []
        
        while len(question_set) > 0:
            question = question_set.pop()
            new_question_list.append(question)
            for i in question['coupled_question_indices']:
                coupled_question = next((q for q in question_set if q['index'] == i), None)
                if not coupled_question:
                    continue
                question_set.remove(coupled_question)
                new_question_list.append(coupled_question)

        return new_question_list

    @staticmethod
    def _select_list_questions(question_list: List[Dict[str, Any]], question_indices: List[int], _: bool) -> List[Dict[str, Any]]:
        return [question_list[i] for i in question_indices]

    @staticmethod
    def _select_random_questions(question_list: List[Dict[str, Any]], question_amount: int, group_coupled_questions: bool) -> List[Dict[str, Any]]:
        new_question_list = sample(question_list, question_amount)

        if not group_coupled_questions:
            return new_question_list
        
        for question in new_question_list:
            for i in question['coupled_question_indices']:
                if len(list(filter(lambda q: q['index'] == i, new_question_list))) > 0:
                    continue

                question_to_remove = {'coupled_question_indices': [-1]}
                while len(question_to_remove['coupled_question_indices']) > 0:
                    question_to_remove = choice(new_question_list)
                new_question_list.remove(question_to_remove)

                question_to_add = next(filter(lambda q: q['index'] == i, question_list))
                new_question_list.append(question_to_add)

        return new_question_list
