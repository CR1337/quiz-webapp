import random
from typing import Any, Dict, List
from app.config import Config


class QuestionSelector:
    @classmethod
    def select_questions(cls, question_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        method = Config.get("question_selection_method")
        group_coupled_questions = Config.get("group_coupled_questions")
        shuffle_questions = Config.get("shuffle_questions")
        parameters = Config.get("question_selection_methods")[method]

        match method:
            case "all":
                selected = cls._select_all(question_list)
            case "list":
                question_indices = parameters["question_indices"]
                selected = cls._select_list(question_list, question_indices)
            case "random":
                question_amount = parameters["question_amount"]
                selected = cls._select_random(question_list, question_amount, group_coupled_questions)
            case "random_set":
                question_sets = parameters["question_sets"]
                selected = cls._select_random_set(question_list, question_sets)
            case "exclude_list":
                exclude_indices = parameters["exclude_indices"]
                selected = cls._select_exclude_list(question_list, exclude_indices)
            case _:
                raise ValueError(f"Invalid question selection method: {method}")

        if shuffle_questions:
            selected = cls._shuffle_questions(question_list, selected, group_coupled_questions)

        return selected

    # ---- individual selection methods ----

    @classmethod
    def _select_all(cls, question_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return list(question_list)

    @classmethod
    def _select_list(
        cls, question_list: List[Dict[str, Any]], question_indices: List[int]
    ) -> List[Dict[str, Any]]:
        return [question_list[i] for i in question_indices]

    @classmethod
    def _select_random(
        cls,
        question_list: List[Dict[str, Any]],
        question_amount: int,
        group_coupled_questions: bool,
    ) -> List[Dict[str, Any]]:
        total = len(question_list)
        question_amount = min(question_amount, total)

        candidate_order = list(range(total))
        random.shuffle(candidate_order)

        selected_indices: List[int] = []
        selected_set = set()

        for idx in candidate_order:
            if len(selected_indices) >= question_amount:
                break
            if idx in selected_set:
                continue

            group = [idx]
            if group_coupled_questions:
                coupled = question_list[idx].get("coupled_question_indices", [])
                for c in coupled:
                    if c not in group:
                        group.append(c)

            remaining = question_amount - len(selected_indices)
            new_members = [g for g in group if g not in selected_set]

            # Skip this starting question if its group can't fit within the remaining budget
            if len(new_members) > remaining:
                continue

            for member in new_members:
                selected_indices.append(member)
                selected_set.add(member)

        selected_indices.sort()  # stable, sensible default order before optional shuffle
        return [question_list[i] for i in selected_indices]

    @classmethod
    def _select_random_set(
        cls, question_list: List[Dict[str, Any]], question_sets: List[List[int]]
    ) -> List[Dict[str, Any]]:
        chosen_set = random.choice(question_sets)
        return [question_list[i] for i in chosen_set]

    @classmethod
    def _select_exclude_list(
        cls, question_list: List[Dict[str, Any]], exclude_indices: List[int]
    ) -> List[Dict[str, Any]]:
        exclude_set = set(exclude_indices)
        return [q for i, q in enumerate(question_list) if i not in exclude_set]

    # ---- shuffling (shared, keeps coupled groups together) ----

    @classmethod
    def _shuffle_questions(
        cls,
        question_list: List[Dict[str, Any]],
        selected: List[Dict[str, Any]],
        group_coupled_questions: bool,
    ) -> List[Dict[str, Any]]:
        if not group_coupled_questions:
            shuffled = list(selected)
            random.shuffle(shuffled)
            return shuffled

        # Map each selected question back to its global index in question_list
        global_index_of = {id(q): i for i, q in enumerate(question_list)}
        selected_global_indices = {global_index_of[id(q)] for q in selected}

        visited = set()
        groups: List[List[Dict[str, Any]]] = []

        for q in selected:
            gidx = global_index_of[id(q)]
            if gidx in visited:
                continue

            coupled = question_list[gidx].get("coupled_question_indices", [])
            group_global_indices = [gidx] + [
                c for c in coupled if c in selected_global_indices and c != gidx
            ]

            group_questions = []
            for g in group_global_indices:
                if g not in visited:
                    visited.add(g)
                    group_questions.append(question_list[g])

            groups.append(group_questions)

        random.shuffle(groups)

        result: List[Dict[str, Any]] = []
        for group in groups:
            result.extend(group)

        return result