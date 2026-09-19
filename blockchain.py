"""
SimpleBlockchain Chain Integrity Module (Lecture 05 / Assignment 5)
Module: BLCH9X2 - Master of Financial Engineering (University of Johannesburg)
Author: Olonda Thoba Holizwi Masuku
"""

from __future__ import annotations

import hashlib
import json
import time
from typing import Any

GENESIS_PREV = "0" * 64


def sha256_hex(data: str) -> str:
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


class Block:
    """Represents a single commit of data with a hash and a pointer to the previous digest."""

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
        blob = json.dumps(payload, sort_keys=True, separators=(",", ":"))
        return sha256_hex(blob)

    def __repr__(self) -> str:
        return f"Block(index={self.index}, hash={self.hash[:12]}...)"


class Blockchain:
    """An ordered sequence of blocks with validation rules for appending and full-chain verification."""

    def __init__(self) -> None:
        self.chain: list[Block] = []
        self.chain.append(self.create_genesis_block())

    def create_genesis_block(self) -> Block:
        return Block(0, [{"note": "genesis"}], GENESIS_PREV, nonce=0, timestamp=0.0)

    def tip(self) -> Block:
        return self.chain[-1]

    def append_block(self, block: Block) -> None:
        """Append only if index, previous_hash, and self-hash checks pass."""
        tip = self.tip()
        if block.index != tip.index + 1:
            raise ValueError(f"bad index: expected {tip.index + 1}, got {block.index}")
        if block.previous_hash != tip.hash:
            raise ValueError("bad previous_hash: does not match chain tip")
        if block.hash != block.compute_hash():
            raise ValueError("stored hash does not match recomputation")
        self.chain.append(block)

    def verify_chain(self, difficulty: int | None = None) -> bool:
        """Return True iff the full chain is internally consistent.

        If difficulty is not None, every non-genesis block hash must start
        with that many hex zeros.
        """
        if not self.chain:
            return False
        genesis = self.chain[0]
        if genesis.index != 0 or genesis.previous_hash != GENESIS_PREV:
            return False
        if genesis.hash != genesis.compute_hash():
            return False

        prefix = ("0" * difficulty) if difficulty is not None else None

        for i in range(1, len(self.chain)):
            cur, prev = self.chain[i], self.chain[i - 1]
            if cur.index != i:
                return False
            if cur.hash != cur.compute_hash():
                return False
            if cur.previous_hash != prev.hash:
                return False
            if prefix is not None and not cur.hash.startswith(prefix):
                return False
        return True

    def __len__(self) -> int:
        return len(self.chain)


def make_next_block(
    chain: Blockchain, transactions: list[Any], nonce: int = 0
) -> Block:
    """Build the next block pointing at the current tip (no mining yet)."""
    tip = chain.tip()
    return Block(tip.index + 1, transactions, tip.hash, nonce=nonce)