"""Ledger Guard plugin — registration.

Exposes exactly one tool, ledger_guard_check, through the public
ctx.register_tool surface. No hooks, no commands, no core overrides,
no network, no credentials.
"""

import logging

from . import schemas, tools

logger = logging.getLogger(__name__)


def register(ctx):
    """Wire schemas to handlers."""
    ctx.register_tool(
        name="ledger_guard_check",
        toolset="ledger-guard",
        schema=schemas.LEDGER_GUARD_CHECK,
        handler=tools.ledger_guard_check,
    )
    logger.debug("ledger-guard: registered ledger_guard_check")
