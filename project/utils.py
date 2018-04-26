import datetime


def date_range(from_=None, to=None):
    from_ = from_ or datetime.date.today()
    to = to or datetime.date.today()

    while from_ <= to:
      yield from_
      from_ += datetime.timedelta(days=1)
