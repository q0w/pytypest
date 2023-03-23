from __future__ import annotations

from typing import Any, Iterator, TypeVar

import pytest

from .._fixture_factory import fixture


K = TypeVar('K')
V = TypeVar('V')


class AttrPatcher:
    def __init__(
        self,
        patcher: pytest.MonkeyPatch,
        target: object | str,
    ) -> None:
        self.__patcher = patcher
        self.__target = target

    def __setattr__(self, name: str, value: object) -> None:
        if name.startswith('_AttrPatcher__'):
            return super().__setattr__(name, value)
        if isinstance(self.__target, str):
            self.__target
            self.__patcher.setattr(f'{self.__target}.{name}', value)
        else:
            self.__patcher.setattr(self.__target, name, value)

    def __delattr__(self, name: str) -> None:
        self.__patcher.delattr(self.__target, name)


@fixture
def patcher(target: object | str) -> Iterator[Any]:
    monkey_patcher = pytest.MonkeyPatch()
    yield AttrPatcher(monkey_patcher, target)
    monkey_patcher.undo()
