<p align="center">
    <a href="https://orange3-volcanoes.readthedocs.io/en/latest/index.html">
    <img src="https://raw.githubusercontent.com/AIVolcanoLab/orange3-volcanoes/refs/heads/main/docs/images/Titolo-DOC.png" alt="Orange Volcanoes" height="400">
    </a>
</p>

<p align="center">
    <a href="https://pypi.org/project/orange3-volcanoes/" alt="Latest release">
        <img src="https://img.shields.io/badge/downolad_OV-v1.0.3-orange" />
    </a>
    <a href="https://orange3-volcanoes.readthedocs.io/en/latest/index.html" alt="Documentation">
        <img src="https://img.shields.io/badge/Orange_Volcanoes-Documentation-red">
    </a>
</p>

# Orange Volcanoes
[Orange-Volcanoes] is an extension (add-on) of the open-source [Orange Data Mining] platform, specifically designed to support data-driven investigations in petrology and volcanology.
Through the integration of tools for geochemical analysis into the Orange visual programming environment, Orange-Volcanoes allows researchers to explore, visualize, and interpret complex datasets without a coding background.

[Orange-Volcanoes]: https://orange3-volcanoes.readthedocs.io/en/latest/
[Orange Data Mining]: https://orangedatamining.com/

This add-on enhances the basic functionality of Orange by introducing specialized widgets designed for the specific needs of petrologists and volcanologists. These widgets facilitate geochemical data workflows, enabling tasks such as:

<ol>
     <li> Importing and preparing petrological datasets</li>
     <li> Conducting compositional data analysis (CoDA)</li>
     <li> Cleaning and filtering geochemical analyses of glass and volcanic minerals</li>
     <li> Testing mineral-liquid equilibrium</li>
     <li> Performing thermobarometric calculations, both classical and machine learning-based</li>
</ol>

## Installing

To install Orange-Volcanoes, Orange should be first installed in your computer.

### Installing Orange

In order to install orange follow the procedure on the [Orange download page], or read the instruction in [orange3 GitHub].

[Orange download page]: https://orangedatamining.com/download/
[orange3 GitHub]: https://github.com/biolab/orange3/blob/master/README.md

### Installing Orange-Volcanoes with pip

Once Orange have been correctly installed in a dedicated enviroment, we can proceed installing the Orange-Volcanoes add-on within the same enviroment.
This can be done via [pip install] with the easy command `pip install orange3-volcanoes`

[pip install]: https://pypi.org/project/orange3-volcanoes/

## Running

Make sure you have activated the correct virtual environment. If you follow the conda instructions in [orange3 GitHub]:

```Shell
conda activate orange3
``` 

Run `orange-canvas` or `python3 -m Orange.canvas`. Add `--help` for a list of program options.

Starting up for the first time may take a while.

By running Orange, you will find all the widgets of the Orange-Volcanoes add-on on the left side the main Orange interface where all the other widgets are, grouped under the name of "Volcanoes".

## Developing

Are you interested in developing, expanding Orange Volcanoes?
To contribute, you can either submit a request or report an issue directly on the GitHub Issues page, or reach out via
email at XXX

Are you interested in devoloping your own add-on? Get in touch with the Orange community and follow the instruction listed in [orange3 GitHub]
or summerised here below:

[![GitHub Actions](https://img.shields.io/endpoint.svg?url=https%3A%2F%2Factions-badge.atrox.dev%2Fbiolab%2Forange3%2Fbadge&label=build)](https://actions-badge.atrox.dev/biolab/orange3/goto) [![codecov](https://img.shields.io/codecov/c/github/biolab/orange3)](https://codecov.io/gh/biolab/orange3) [![Contributor count](https://img.shields.io/github/contributors-anon/biolab/orange3)](https://github.com/biolab/orange3/graphs/contributors) [![Latest GitHub commit](https://img.shields.io/github/last-commit/biolab/orange3)](https://github.com/biolab/orange3/commits/master)

Want to write a widget? [Use the Orange3 example add-on template.](https://github.com/biolab/orange3-example-addon)

Want to get involved? Join us on [Discord](https://discord.gg/FWrfeXV), introduce yourself in #general! 

Take a look at our [contributing guide](https://github.com/irgolic/orange3/blob/README-shields/CONTRIBUTING.md) and [style guidelines](https://github.com/biolab/orange-widget-base/wiki/Widget-UI).

Check out our widget development [docs](https://orange-widget-base.readthedocs.io/en/latest/?badge=latest) for a comprehensive guide on writing Orange widgets.





