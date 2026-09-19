"""
SimpleBlockchain Mining & Proof-of-Work Module (Assignment 6)
Module: BLCH9X2 - Master of Financial Engineering (University of Johannesburg)
Author: Olonda Thoba Holizwi Masuku
"""

from __future__ import annotations

import hashlib
import json
import time
from typing import Any

GENESIS_PREV = "0" * 64
BLOCK_REWARD = 50.0


def sha256_hex(data: str) -> str:
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def meets_difficulty(digest: str, difficulty: int) -> bool:
    """Lab rule: hash must start with `difficulty` hex zeros."""
    if difficulty < 0:
        raise ValueError("difficulty must be non-negative")
    return digest.startswith("0" * difficulty)


class Block:
    """Represents a single commit of data with a hash, pointer to previous digest, and nonce."""

    def __init__(
        self,
        index: int,
        transactions: list[Any],
        previous_hash: str,
        nonce: int = 0,
        timestamp: float | None = None,
    ) -> None:
        self.index = index
        self.timestamp = time.time() if timestamp is None else timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.compute_hash()

    def compute_hash(self) -> str:
        payload = {
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
        }
        return sha256_hex(json.dumps(payload, sort_keys=True, separators=(",", ":")))

    def __repr__(self) -> str:
        return f"Block(index={self.index}, nonce={self.nonce}, hash={self.hash[:12]}...)"


class Blockchain:
    """An ordered sequence of blocks with validation rules for appending and PoW verification."""

    def __init__(self) -> None:
        self.chain: list[Block] = [
            Block(0, [{"note": "genesis"}], GENESIS_PREV, 0, 0.0)
        ]

    def tip(self) -> Block:
        return self.chain[-1]

    def append_block(self, block: Block, difficulty: int | None = None) -> None:
        tip = self.tip()
        if block.index != tip.index + 1:
            raise ValueError("bad index")
        if block.previous_hash != tip.hash:
            raise ValueError("bad previous_hash")
        if block.hash != block.compute_hash():
            raise ValueError("bad hash")
        if difficulty is not None and not block.hash.startswith("0" * difficulty):
            raise ValueError("difficulty not met")
        self.chain.append(block)

    def verify_chain(self, difficulty: int | None = None) -> bool:
        if self.chain[0].hash != self.chain[0].compute_hash():
            return False
        for i in range(1, len(self.chain)):
            cur, prev = self.chain[i], self.chain[i - 1]
            if cur.index != i:
                return False
            if cur.hash != cur.compute_hash():
                return False
            if cur.previous_hash != prev.hash:
                return False
            if difficulty is not None and not cur.hash.startswith("0" * difficulty):
                return False
        return True


def mine_block(block: Block, difficulty: int) -> tuple[Block, int, float]:
    """Mine until hash has `difficulty` leading hex zeros. Returns (block, attempts, elapsed_seconds)."""
    if difficulty < 0:
        raise ValueError("difficulty must be non-negative")
    prefix = "0" * difficulty
    nonce = 0
    t0 = time.perf_counter()
    while True:
        block.nonce = nonce
        digest = block.compute_hash()
        if digest.startswith(prefix):
            block.hash = digest
            elapsed = time.perf_counter() - t0
            return block, nonce + 1, elapsed
        nonce += 1


def make_coinbase(miner_address: str, reward: float = BLOCK_REWARD) -> dict[str, Any]:
    """Simplified block-reward transaction (coinbase equivalent)."""
    return {
        "sender": "NETWORK",
        "recipient": miner_address,
        "amount": reward,
        "timestamp": time.time(),
        "type": "coinbase",
    }


def mine_and_append(
    chain: Blockchain,
    mempool: list[Any],
    miner_address: str,
    difficulty: int,
) -> tuple[Block, int, float]:
    """Create block with coinbase + mempool, mine it, append to chain."""
    tip = chain.tip()
    txs = [make_coinbase(miner_address)] + list(mempool)
    block = Block(tip.index + 1, txs, tip.hash)
    mined, attempts, secs = mine_block(block, difficulty)
    chain.append_block(mined, difficulty=difficulty)
    return mined, attempts, secs


def difficulty_study(
    difficulties: tuple[int, ...] = (2, 3, 4),
) -> list[dict[str, Any]]:
    """Run mining at several difficulties; return rows for the A6 report timing table."""
    rows: list[dict[str, Any]] = []
    for d in difficulties:
        blk = Block(1, [{"payload": "study", "d": d}], GENESIS_PREV)
        mined, attempts, secs = mine_block(blk, d)
        rows.append(
            {
                "difficulty": d,
                "attempts": attempts,
                "seconds": secs,
                "hash": mined.hash,
            }
        )
    return rows


