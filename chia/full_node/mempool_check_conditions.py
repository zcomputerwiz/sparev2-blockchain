import logging
import time
from typing import Dict, Optional
from clvm_rs import STRICT_MODE

from chia.consensus.cost_calculator import NPCResult, SpendBundleConditions
from chia.full_node.generator import create_generator_args, setup_generator_args
from chia.types.blockchain_format.program import NIL
from chia.types.coin_record import CoinRecord
from chia.types.condition_with_args import ConditionWithArgs
from chia.types.generator_types import BlockGenerator
from chia.types.blockchain_format.sized_bytes import bytes32
from chia.util.clvm import int_from_bytes
from chia.util.errors import Err
from chia.util.ints import uint32, uint64, uint16
from chia.wallet.puzzles.generator_loader import GENERATOR_FOR_SINGLE_COIN_MOD
from chia.wallet.puzzles.rom_bootstrap_generator import get_generator

GENERATOR_MOD = get_generator()


log = logging.getLogger(__name__)


def mempool_assert_absolute_block_height_exceeds(
    condition: ConditionWithArgs, prev_transaction_block_height: uint32
) -> Optional[Err]:
    """
    Checks if the next block index exceeds the block index from the condition
    """
    try:
        block_index_exceeds_this = int_from_bytes(condition.vars[0])
    except ValueError:
        return Err.INVALID_CONDITION
    if prev_transaction_block_height < block_index_exceeds_this:
        return Err.ASSERT_HEIGHT_ABSOLUTE_FAILED
    return None


def mempool_assert_relative_block_height_exceeds(
    condition: ConditionWithArgs, unspent: CoinRecord, prev_transaction_block_height: uint32
) -> Optional[Err]:
    """
    Checks if the coin age exceeds the age from the condition
    """
    try:
        expected_block_age = int_from_bytes(condition.vars[0])
        block_index_exceeds_this = expected_block_age + unspent.confirmed_block_index
    except ValueError:
        return Err.INVALID_CONDITION
    if prev_transaction_block_height < block_index_exceeds_this:
        return Err.ASSERT_HEIGHT_RELATIVE_FAILED
    return None


def mempool_assert_absolute_time_exceeds(condition: ConditionWithArgs, timestamp: uint64) -> Optional[Err]:
    """
    Check if the current time in seconds exceeds the time specified by condition
    """
    try:
        expected_seconds = int_from_bytes(condition.vars[0])
    except ValueError:
        return Err.INVALID_CONDITION

    if timestamp is None:
        timestamp = uint64(int(time.time()))
    if timestamp < expected_seconds:
        return Err.ASSERT_SECONDS_ABSOLUTE_FAILED
    return None


def mempool_assert_relative_time_exceeds(
    condition: ConditionWithArgs, unspent: CoinRecord, timestamp: uint64
) -> Optional[Err]:
    """
    Check if the current time in seconds exceeds the time specified by condition
    """
    try:
        expected_seconds = int_from_bytes(condition.vars[0])
    except ValueError:
        return Err.INVALID_CONDITION

    if timestamp is None:
        timestamp = uint64(int(time.time()))
    if timestamp < expected_seconds + unspent.timestamp:
        return Err.ASSERT_SECONDS_RELATIVE_FAILED
    return None


def get_name_puzzle_conditions(
    generator: BlockGenerator, max_cost: int, *, cost_per_byte: int, safe_mode: bool
) -> NPCResult:
    block_program, block_program_args = setup_generator_args(generator)
    size_cost = len(bytes(generator.program)) * cost_per_byte
    max_cost -= size_cost
    if max_cost < 0:
        return NPCResult(uint16(Err.INVALID_BLOCK_COST.value), None, uint64(0))

    flags = STRICT_MODE if safe_mode else 0
    try:
        err, result = GENERATOR_MOD.run_as_generator(max_cost, flags, block_program, block_program_args)
        assert (err is None) != (result is None)
        if err is not None:
            return NPCResult(uint16(err), None, uint64(0))
        else:
            return NPCResult(None, result, result.cost + size_cost)
    except Exception as e:
        log.debug(f'get_name_puzzle_condition failed: "{e}"')
        return NPCResult(uint16(Err.GENERATOR_RUNTIME_ERROR.value), None, uint64(0))


def get_puzzle_and_solution_for_coin(generator: BlockGenerator, coin_name: bytes, max_cost: int):
    try:
        block_program = generator.program
        if not generator.generator_args:
            block_program_args = [NIL]
        else:
            block_program_args = create_generator_args(generator.generator_refs())

        cost, result = GENERATOR_FOR_SINGLE_COIN_MOD.run_with_cost(
            max_cost, block_program, block_program_args, coin_name
        )
        puzzle = result.first()
        solution = result.rest().first()
        return None, puzzle, solution
    except Exception as e:
        return e, None, None


def mempool_check_time_locks(
    removal_coin_records: Dict[bytes32, CoinRecord],
    bundle_conds: SpendBundleConditions,
    prev_transaction_block_height: uint32,
    timestamp: uint64,
) -> Optional[Err]:
    """
    Check all time and height conditions against current state.
    """

    if prev_transaction_block_height < bundle_conds.height_absolute:
        return Err.ASSERT_HEIGHT_ABSOLUTE_FAILED
    if timestamp < bundle_conds.seconds_absolute:
        return Err.ASSERT_SECONDS_ABSOLUTE_FAILED

    for spend in bundle_conds.spends:
        unspent = removal_coin_records[spend.coin_id]
        if spend.height_relative is not None:
            if prev_transaction_block_height < unspent.confirmed_block_index + spend.height_relative:
                return Err.ASSERT_HEIGHT_RELATIVE_FAILED
        if timestamp < unspent.timestamp + spend.seconds_relative:
            return Err.ASSERT_SECONDS_RELATIVE_FAILED
    return None
