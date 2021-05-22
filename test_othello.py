import pytest
import util
import othello

def test_beginning1():
    disks = {(3,3): "x", (4,4): "x", (3,4): "o", (4,3): "o"}
    assert othello.create_beginning_disks(8) == disks

def test_beginning2():
    disks = {(4,4): "x", (5,5): "x", (5,4): "o", (4,5): "o"}
    assert othello.create_beginning_disks(10) == disks

def test_check_move1():
    size = 8
    disks = {(3,3): "x", (4,4): "x", (3,4): "o", (4,3): "o"}
    assert othello.check_possible_move(disks, "x", 8)

def test_check_coordinates1():
    size = 8
    disks ={(0,0): "o", (0,1): "x", (0,2): "x", (0,3): "x", (1,0): "x", (2,0): "x", (3,0): "x"}
    new = (0,0)
    with pytest.raises(ValueError):
        othello.check_coordinates(disks, new, 8)

def test_check_coordinates2():
    disks ={(0,0): "o", (0,1): "x", (0,2): "x", (0,3): "x", (1,0): "x", (2,0): "x", (3,0): "x"}
    new = (10,10)
    with pytest.raises(ValueError):
        othello.check_coordinates(disks, new, 8)

def test_check_coordinates2():
    disks ={(0,0): "o", (0,1): "x", (0,2): "x", (0,3): "x", (1,0): "x", (2,0): "x", (3,0): "x"}
    new = (-1,8)
    with pytest.raises(ValueError):
        othello.check_coordinates(disks, new, 8)

def test_check_move2():
    disks = {(1,1): "x", (2,1): "x", (3,1): "x", (1,2): "x", (1,3): "x", (2,3): "x", (3,3): "x", (3,2): "x", (2,2): "o"}
    assert othello.check_possible_move(disks, "x", 8) == False

def test_check_move3():
    disks = {(1,1): "x", (2,1): "x", (3,1): "x", (1,2): "x", (1,3): "x", (2,3): "x", (3,3): "x", (3,2): "x", (2,2): "o"}
    assert othello.check_possible_move(disks, "o", 8) == True

def test_check_move4():
    disks ={(0,0): "o", (0,1): "x", (0,2): "x", (0,3): "x", (1,0): "x", (2,0): "x", (3,0): "x"}
    assert othello.check_possible_move(disks, "o", 4) == False

def test_check_move5():
    disks ={(0,0): "o", (0,1): "x", (0,2): "x", (0,3): "x", (1,0): "x", (2,0): "x", (3,0): "x"}
    assert othello.check_possible_move(disks, "x", 4) == False

def test_all_moves():
    disks ={(0,0): "o", (0,1): "x", (0,2): "x", (0,3): "x", (1,0): "x", (2,0): "x", (3,0): "x"}
    assert othello.check_all_moves(disks, 4)

def test_all_moves2(): 
    disks ={(0,0): "o", (0,1): "x", (0,2): "x", (0,3): "x", (1,0): "x", (2,0): "x", (3,0): "x"}
    assert othello.check_all_moves(disks, 5) == False

def test_end1():
    disks ={(0,0): "x", (0,1): "x", (0,2): "x", (0,3): "x", (1,0): "x", (2,0): "x", (3,0): "x"}
    assert othello.end(disks, 8)

def test_end2():
    disks ={(0,0): "o", (0,1): "o"}
    assert othello.end(disks, 8)

def test_end3():
    disks ={(0,0): "o", (0,1): "o", (1,0): "x", (1,1): "x"}
    assert othello.end(disks, 2)

def test_winner():
    size = 2
    disks ={(0,0): "o", (0,1): "o", (1,0): "x", (1,1): "x"}
    assert othello.who_wins(disks) == (2,2)

def test_winner2():
    disks ={(0,0): "x", (0,1): "x", (0,2): "x", (0,3): "x", (1,0): "x", (2,0): "x", (3,0): "x"}
    assert othello.who_wins(disks) == (7,0)

def test_winner3():
    disks ={(0,0): "o", (0,1): "o"}
    assert othello.who_wins(disks) == (0,2)

def test_move1(): 
    disks ={(2,2): "x", (1,1): "o", (2,1): "o", (3,1): "o", (1,2): "o", (1,3): "o", (2,3): "o", (3,2): "o", (3,3): "o"}
    tries = {(0,0): [(1,1)], (2,0): [(2,1)], (4,0): [(3,1)], (0,2): [(1,2)], (0,4): [(1,3)], (2,4): [(2,3)], (4,2): [(3,2)], (4,4): [(3,3)]}

    for move, change in tries.items():
        assert util.move(disks, move, "x") == change

def test_move2(): 
    disks ={(2,2): "x", (1,1): "o", (2,1): "o", (3,1): "o", (1,2): "o", (1,3): "o", (2,3): "o", (3,2): "o", (3,3): "o"}
    tries = [(1,0), (3,0), (5,0), (0,1), (0,3), (0,5), (4,1), (4,3), (1,4), (3,4)]

    with pytest.raises(ValueError):
        for move in tries:
            util.move(disks, move, "x")

def test_move3():
    disks ={(0,1): "x", (0,2): "x", (0,3): "x", (1,0): "x", (2,0): "x", (3,0): "x", (1,1): "x", (2,1): "x", (1,2): "x", (2,2): "o", (4,0): "o", (0,4): "o"}
    changes = [(0,1), (0,2), (0,3), (1,0), (2,0), (3,0), (1,1)]
    assert sorted(util.move(disks, (0,0), "o")) == sorted(changes)

def test_reversal():
    disks ={(0,1): "x", (0,2): "x", (0,3): "o"}
    changes = [(0,1), (0,2)]
    assert util.reversal(disks, (0,0), "o", changes) == {(0,1): "o", (0,2): "o", (0,3): "o", (0,0): "o"}