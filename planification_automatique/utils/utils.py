from typing import AbstractSet

import pddl.logic.base as logic
from pddl.logic.effects import AndEffect, Forall, When
from pddl.logic.predicates import Predicate


def construct_predicate(predicate: Predicate, action: dict) -> Predicate:
    variables = []
    for term, parameter, obj in zip(
            predicate.terms, action["parameters"], action["objects"]
    ):
        if term == parameter:
            variables.append(obj)
    return Predicate(predicate.name, *variables)


def is_applicable(action: dict, state: AbstractSet[logic.Formula]) -> bool:
    preconditions = action["precondition"]
    if isinstance(preconditions, logic.TrueFormula):
        return True

    elif isinstance(preconditions, logic.FalseFormula):
        return False

    elif isinstance(preconditions, logic.Not):
        new_action = action.copy()
        new_action["precondition"] = preconditions.argument
        return not is_applicable(new_action, state)

    elif isinstance(preconditions, logic.And):
        for operand in preconditions.operands:
            new_action = action.copy()
            new_action["precondition"] = operand
            if not is_applicable(new_action, state):
                return False
        return True

    elif isinstance(preconditions, logic.Or):
        for operand in preconditions.operands:
            new_action = action.copy()
            new_action["precondition"] = operand
            if is_applicable(new_action, state):
                return True
        return False

    elif isinstance(preconditions, Predicate):
        predicate: Predicate = construct_predicate(preconditions, action)
        return predicate in state

    else:
        raise NotImplementedError


def change_state(
        state: AbstractSet[logic.Formula], action: dict
) -> set[logic.Formula]:
    new_state = set(state)
    effect: AndEffect = action["effect"]

    if all(isinstance(operand, Forall) for operand in effect.operands):
        predicates_to_remove: list = []
        predicates_to_add: list = []
        for operand in effect.operands:
            when: When = operand.effect
            for when_effect in when.effect.operands:
                if isinstance(when_effect, Predicate):
                    original_s: Predicate = [s for s in state if s.name == when.condition.name][0]
                    order = [when.condition.terms.index(term) for term in when_effect.terms]
                    new_terms = [original_s.terms[i] for i in order]
                    predicate = Predicate(when_effect.name, *new_terms)
                    predicates_to_add.append(predicate)

                elif isinstance(when_effect, logic.Not):
                    original_s: Predicate = [s for s in state if s.name == when.condition.name][0]
                    order = [when.condition.terms.index(term) for term in
                             when_effect.argument.terms]
                    new_terms = [original_s.terms[i] for i in order]
                    predicate = Predicate(when_effect.argument.name, *new_terms)
                    predicates_to_remove.append(predicate)

                else:
                    raise NotImplementedError

        for predicate in predicates_to_remove:
            if predicate in new_state:
                new_state.remove(predicate)
        for predicate in predicates_to_add:
            new_state.add(predicate)

        return new_state

    for operand in effect.operands:
        if isinstance(operand, logic.Not):
            if isinstance(operand.argument, Predicate):
                predicate: Predicate = construct_predicate(operand.argument, action)
                if predicate in new_state:
                    new_state.remove(predicate)
            else:
                raise NotImplementedError

        elif isinstance(operand, Predicate):
            predicate: Predicate = construct_predicate(operand, action)
            new_state.add(predicate)

        else:
            raise NotImplementedError
    return new_state
