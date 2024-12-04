from setuptools import setup

setup(name="Volcanoes",
      packages=["OrangeVolcanoes"],
      package_data={"OrangeVolcanoes": ["icons/*", "doc/*, datasets/*"]},
      classifiers=["Example :: Invalid"],
      entry_points={"orange.widgets": "Volcanoes = OrangeVolcanoes"},
      )