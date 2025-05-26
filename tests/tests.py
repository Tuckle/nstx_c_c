import asyncio, pytest
from datetime import datetime

from service import PaymentLinkService, Status


@pytest.mark.asyncio
async def test_idempotent_create():
    svc = PaymentLinkService()
    link1 = await svc.create("ORD-1", 1000)
    link2 = await svc.create("ORD-1", 1000)
    assert link1.token == link2.token
    assert link1.expires_at > link2.expires_at


@pytest.mark.asyncio
async def test_no_double_pay_race():
    svc = PaymentLinkService()
    link = await svc.create("ORD-2", 1000)

    async def do_pay(idem):
        return await svc.pay(link.token, idem)

    res = await asyncio.gather(
        do_pay("X"),
        do_pay("Y"),
        return_exceptions=True,
    )
    statuses = [r.status for r in res if not isinstance(r, Exception)]
    assert statuses.count(Status.PAID) == 1, "Only one pay must succeed"
    assert any(isinstance(r, Exception) for r in res)


@pytest.mark.asyncio
async def test_single_refund():
    svc = PaymentLinkService()
    link = await svc.create("ORD-3", 1000)
    await svc.pay(link.token, "idem-1")

    await svc.refund(link.token, "r-1")

    await svc.refund(link.token, "r-1")

    with pytest.raises(Exception):
        await svc.refund(link.token, "r-2")
