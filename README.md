<p align="center">
    <a href="https://orange3-volcanoes.readthedocs.io/en/latest/index.html">
    <img src="https://raw.githubusercontent.com/AIVolcanoLab/orange3-volcanoes/refs/heads/main/docs/images/Titolo-DOC.png" alt="Orange Volcanoes" height="400">
    </a>
</p>

<p align="center">
    <a href="https://pypi.org/project/orange3-volcanoes/" title="Latest release">
        <img src="https://img.shields.io/pypi/v/orange3-volcanoes?color=orange" alt="Latest release" />
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
     <li> Importing and preparing petrological datasets;</li>
     <li> Conducting compositional data analysis (CoDA);</li>
     <li> Cleaning and filtering geochemical analyses of glass and volcanic minerals;</li>
     <li> Testing mineral-liquid equilibrium;</li>
     <li> Performing thermobarometric calculations, both classical and machine learning-based;</li>
     <li> Overall, enabling data-driven investigations on petrologic and geochemical data.</li>
</ol>

## Installing Orange-Volcanoes

To install Orange-Volcanoes, please follow the [step by step install] instructions reported in the documentation.

[step by step install]: https://orange3-volcanoes.readthedocs.io/en/latest/installing.html#step-1-installing-anaconda-or-miniconda


## Running Orange-Volcanoes

To run Orange-Volcanoes, please follow the [step by step instructions] reported in the documentation.
For example, if during the install process you created the orange3 envirnoment to host Orange and Orange-Volcanoes:

[step by step instructions]: https://orange3-volcanoes.readthedocs.io/en/latest/installing.html#running

```Shell
conda activate orange3
orange-canvas
``` 

Add `--help` for a list of program options.

Starting up for the first time may take a while.

By running Orange, you will find all the widgets of the Orange-Volcanoes add-on on the left side the main Orange interface where all the other widgets are, grouped under the name of "Volcanoes".

## Developing

Are you interested in developing, expanding or suggest changes in Orange Volcanoes?
To contribute, you can either [submit a request] or [report an issue] directly on the [GitHub], by usining the dedicated "[pull request]" and "[issues]" spaces.

[submit a request]: https://github.com/AIVolcanoLab/orange3-volcanoes/pulls
[report an issue]: https://github.com/AIVolcanoLab/orange3-volcanoes/issues
[pull request]: https://github.com/AIVolcanoLab/orange3-volcanoes/pulls
[issues]: https://github.com/AIVolcanoLab/orange3-volcanoes/issues
[GitHub]: https://github.com/AIVolcanoLab/orange3-volcanoes

