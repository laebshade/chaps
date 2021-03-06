"""
Chaps, a relative dir pants wrapper for Python targets.

Chaps makes it easier to interact with your Pants Build System without having
to type out lengthy path names.

Note: chaps only works with targets in your current work directory (cwd).  Fall
back to calling pants directly if you need something else.
"""
# pylint: disable=E0401,E0611,E1101

from __future__ import absolute_import, print_function

import chaps_lib as lib

import click


@click.command(name="binary")
@click.argument('args', nargs=-1)
def binary_goal(args):
  """Create a binary using pants."""

  targets = lib.targets(lib.rel_cwd(), args)

  pants_args = "binary {0}".format(targets)
  lib.pants(pants_args)


@click.command(name="fmt")
@click.argument('args', nargs=-1)
def fmt_goal(args):
  """Fix common format issues using pants fmt goal."""
  targets = lib.targets(lib.rel_cwd(), args)
  pants_args = "fmt {0}".format(targets)
  lib.pants(pants_args)


@click.command(name="list")
def list_goal():
  """List relative path pants targets."""
  path = lib.rel_cwd()
  pants_args = "list {0}:".format(path)
  lib.pants_list(pants_args)


@click.command(name="repl")
@click.argument('args', nargs=-1)
def repl_goal(args):
  """Enter an ipython REPL."""
  targets = lib.targets(lib.rel_cwd(), args)
  pants_args = "repl --repl-py-ipython {0}".format(targets)
  lib.pants(pants_args)


@click.command(name="run")
@click.argument('goal')
@click.argument('args', nargs=-1)
def run_goal(goal, args):
  """Run a target using pants."""

  targets = lib.targets(lib.rel_cwd(), [goal])
  run_args = " ".join(args)

  pants_args = "run {0} {1}".format(targets, run_args)
  lib.pants(pants_args)


@click.command(name="clean-all")
def clean_goal():
  """Clean pants."""
  lib.pants("clean-all")


@click.option("--all", default=False, help="Test all targets in path name similar to cwd.")
@click.option("--coverage", default=False, help="Python test coverage.")
@click.option("--failfast", default=False, help="Python stop on first error.")
@click.option("--verbose", default=False, help="Python test verbosity.")
@click.command(name="test")
def test_goal(args, options):
  """Use test.pytest goal with pants."""

  if options.all:
    targets = "%s::" % lib.rel_cwd().replace('src', 'tests')
  else:
    targets = lib.targets(lib.rel_cwd(), args)

  pants_args = "test.pytest  {0} {1} {2}".format(
    "--coverage=%d" % int(options.coverage),
    "--test-pytest-options='%s'" % lib.pytest_options(options),
    targets,
  )
  lib.pants(pants_args)


@click.group()
def cli():
  pass


cli.add_command(binary_goal)
cli.add_command(clean_goal)
cli.add_command(fmt_goal)
cli.add_command(list_goal)
cli.add_command(repl_goal)
cli.add_command(run_goal)
cli.add_command(test_goal)


if __name__ == '__main__':
  cli()
