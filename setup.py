from typing import List
from setuptools import setup, find_packages
from pathlib import Path

# from mpris_server import __version__


PKGS: list[str] = list({
  'mpris_server',
  'mpris_server.mpris',
  'mpris_server.interfaces',
  *find_packages(),
})

REQS: list[str] = Path('requirements.txt') \
  .read_text() \
  .splitlines()

REQS: list[str] = [
  req
  for req in REQS
  if not req.strip().startswith('#')
]

README: str = Path('README.md').read_text()


setup(
  name="mpris_server",
  version='0.7.0',
  description="⏯️ Publish a MediaPlayer2 MPRIS device to D-Bus.",
  long_description=README,
  long_description_content_type="text/markdown",
  url="https://alexdelorenzo.dev",
  author="Alex DeLorenzo",
  license="AGPL-3.0",
  packages=PKGS,
  zip_safe=True,
  install_requires=REQS,
  python_requires='>=3.11',
)
