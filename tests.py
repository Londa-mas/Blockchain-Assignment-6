"""
Assignment 6 Test Suite (tests.py)
Module: BLCH9X2 - Master of Financial Engineering (University of Johannesburg)
Author: Olonda Thoba Holizwi Masuku
"""

from mining import Block, Blockchain, mine_block, make_coinbase, mine_and_append, difficulty_study, GENESIS_PREV

def test_mine_block_meets_difficulty() -> None:
    blk = Block(1, [{"x": 1}], GENESIS_PREV)
    mined, attempts, secs = mine_block(blk, difficulty=2)
    assert mined.hash.startswith("00")
    assert mined.hash == mined.compute_hash()
    assert attempts >= 1
    assert secs >= 0.0

def test_coinbase_shape() -> None:
    tx = make_coinbase("MinerAlice", reward=50.0)
    assert tx["sender"] == "NETWORK"
    assert tx["recipient"] == "MinerAlice"
    assert tx["amount"] == 50.0
    assert "timestamp" in tx

def test_mine_and_append_verifies() -> None:
    chain = Blockchain()
    mined, attempts, secs = mine_and_append(
        chain,
        [{"sender": "A", "recipient": "B", "amount": 1}],
        miner_address="MinerAlice",
        difficulty=2,
    )
    assert mined.hash.startswith("00")
    assert mined.transactions[0]["sender"] == "NETWORK"
    assert mined.transactions[0]["recipient"] == "MinerAlice"
    assert chain.verify_chain(difficulty=2)
    assert attempts >= 1
    assert secs >= 0.0

def test_difficulty_study_three_levels() -> None:
    study_rows = difficulty_study((2, 3))
    assert len(study_rows) == 2
    for row, d in zip(study_rows, (2, 3)):
        assert row["difficulty"] == d
        assert row["hash"].startswith("0" * d)
        assert "attempts" in row
        assert "seconds" in row

if __name__ == "__main__":
    test_mine_block_meets_difficulty()
    test_coinbase_shape()
    test_mine_and_append_verifies()
    test_difficulty_study_three_levels()
    print("All Assignment 6 tests passed successfully!")