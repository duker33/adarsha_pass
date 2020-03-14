import click

from bot import app, drivers


@click.group()
@click.option(
    '-dr', '--driver', prompt='Driver to communicate with IQPark.',
    type=click.Choice(['http', 'selenium'], case_sensitive=False),
    default='http',
)
@click.pass_context
def cli(ctx, driver: str):
    ctx.ensure_object(dict)
    ctx.obj['driver'] = driver


@cli.command()
@click.argument('fio', type=click.STRING, nargs=3)
@click.option(
    '-d', '--date', type=click.DateTime(formats=['%d.%m.%Y', '%Y-%m-%d']),
    prompt='Date for the pass'
)
@click.pass_context
def guest(ctx, fio, date):
    """Fetch pass for one guest."""
    pass_ = app.Pass(app.Guest(*fio), date_=date)
    if ctx.obj['driver'] == 'http':
        driver = drivers.HTTP()
    else:  # it's selenium
        driver = drivers.Selenium()
    driver.order(pass_)


@cli.command()
@click.argument('file', type=click.File())
@click.option(
    '-m', '--month', 'no_dates', type=click.IntRange(1, 12),
    help='Month to order passes.'
)
@click.option(
    '-e', '--dates-to-exclude', 'no_dates', type=click.STRING,
    help='Dates to exclude from the next month.'
)
def pack(month, no_dates):
    """Create passes in pack."""
    # @todo #1:60m  Implement CLI for passes pack creating.
    pass


if __name__ == '__main__':
    cli()
