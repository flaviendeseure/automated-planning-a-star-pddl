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

        elif isinstance(operand, Forall):
            when: When = operand.effect
            for when_effect in when.effect.operands:
                if isinstance(when_effect, Predicate):
                    s = [s for s in state if s.name == when_effect.name]
                    predicate = Predicate(when_effect.name, *s[0].terms)
                    new_state.add(predicate)

                elif isinstance(when_effect, logic.Not):
                    s = [s for s in state if s.name == when_effect.argument.name]
                    predicate = Predicate(when_effect.argument.name, *s[0].terms)
                    new_state.remove(predicate)

                else:
                    raise NotImplementedError

        else:
            raise NotImplementedError
    return new_state
