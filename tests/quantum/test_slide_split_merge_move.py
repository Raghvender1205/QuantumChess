import unittest

#import shots and delta default values
from . import *

from qchess.quantum_chess import *
from .quantum_test_engine import QuantumTestEngine


class TestSlideSplitMergeMove(unittest.TestCase):
    def test_blocked_split(self):
        engine = QuantumTestEngine()
        engine.add_board_state(
            [
                ['R', 'K', '0'],
                ['0', '0', '0'],
                ['0', '0', '0'],
            ],
            0.25
        )

        engine.add_board_state(
            [
                ['0', 'K', '0'],
                ['0', '0', '0'],
                ['0', '0', 'R'],
            ],
            0.25
        )

        engine.add_board_state(
            [
                ['0', '0', '0'],
                ['K', '0', '0'],
                ['0', '0', 'R'],
            ],
            0.5
        )

        def board_factory(qchess):
            qchess.add_piece(0, 2, Piece(PieceType.ROOK, Color.WHITE))
            qchess.add_piece(1, 1, Piece(PieceType.KING, Color.WHITE))
            qchess.split_move(Point(1, 1), Point(0, 1), Point(1, 0))

        def action(qchess):
            qchess.split_move(Point(0, 2), Point(0, 0), Point(2, 2))
            qchess.engine.collapse_all()

        engine.set_board_factory(3, 3, board_factory)
        engine.set_action(action)
        engine.run_engine(standard_shots)
        engine.run_tests(self, delta=standard_delta)

    def test_blocked_merge(self):
        engine = QuantumTestEngine()
        engine.add_board_state(
            [
                ['R', '0', '0'],
                ['K', '0', '0'],
                ['R', '0', '0'],
            ],
            0.5
        )

        engine.add_board_state(
            [
                ['0', '0', '0'],
                ['0', '0', '0'],
                ['R', 'K', 'R'],
            ],
            0.5
        )

        def board_factory(qchess):
            qchess.add_piece(0, 0, Piece(PieceType.ROOK, Color.WHITE))
            qchess.add_piece(2, 2, Piece(PieceType.ROOK, Color.WHITE))
            qchess.add_piece(0, 2, Piece(PieceType.KING, Color.WHITE))
            qchess.split_move(Point(0, 2), Point(0, 1), Point(1, 2))

        def action(qchess):
            qchess.merge_move(Point(0, 0), Point(2, 2), Point(0, 2))
            qchess.engine.collapse_all()

        engine.set_board_factory(3, 3, board_factory)
        engine.set_action(action)
        engine.run_engine(standard_shots)
        engine.run_tests(self, delta=standard_delta)

    def test_split_both_paths_blocked_entangle(self):
        engine = QuantumTestEngine()
        engine.add_board_state(
            [
                ['R', 'K', 'R'],
                ['K', '0', '0'],
                ['R', '0', '0'],
            ],
            1
        )

        def board_factory(qchess):
            qchess.add_piece(0, 0, Piece(PieceType.ROOK, Color.WHITE))
            qchess.add_piece(1, 1, Piece(PieceType.KING, Color.WHITE))
            qchess.split_move(Point(1, 1), Point(0, 1), Point(1, 0))

        engine.set_board_factory(3, 3, board_factory)
        engine.set_action(lambda qchess: qchess.split_move(
            Point(0, 0), Point(2, 0), Point(0, 2)))
        engine.run_engine(entangle_shots)
        engine.run_tests(self, delta=entangle_delta)

    def test_split_one_path_blocked_entangle(self):
        engine = QuantumTestEngine()
        engine.add_board_state(
            [
                ['0', '0', 'R'],
                ['K', 'K', '0'],
                ['R', '0', '0'],
            ],
            1
        )

        def board_factory(qchess):
            qchess.add_piece(0, 0, Piece(PieceType.ROOK, Color.WHITE))
            qchess.add_piece(1, 2, Piece(PieceType.KING, Color.WHITE))
            qchess.split_move(Point(1, 2), Point(1, 1), Point(0, 1))

        engine.set_board_factory(3, 3, board_factory)
        engine.set_action(lambda qchess: qchess.split_move(
            Point(0, 0), Point(2, 0), Point(0, 2)))
        engine.run_engine(entangle_shots)
        engine.run_tests(self, delta=entangle_delta)

    def test_clear_path_split_capture(self):
        #we don't manually collapse because we want to make sure the move doesn't collapse
        engine = QuantumTestEngine()
        engine.add_board_state(
            [
                ['0', '0', 'R'],
                ['0', '0', '0'],
                ['r', '0', '0'],
            ],
            1
        )

        def board_factory(qchess):
            qchess.add_piece(0, 0, Piece(PieceType.ROOK, Color.WHITE))
            qchess.add_piece(2, 2, Piece(PieceType.ROOK, Color.BLACK))
            qchess.split_move(Point(2, 2), Point(0, 2), Point(2, 0))

        engine.set_board_factory(3, 3, board_factory)
        engine.set_action(lambda qchess: qchess.standard_move(
            Point(0, 0), Point(2, 0)))
        engine.run_engine(entangle_shots)
        engine.run_tests(self, delta=entangle_delta)
