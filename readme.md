# ROTA
## Rapid Offense Text Autocoder

### ℹ️ Intro

[![HuggingFace Models](https://img.shields.io/badge/%F0%9F%A4%97%20models-2021.05.17.14-blue)](https://huggingface.co/rti-international/rota)
[![GitHub Model Release](https://img.shields.io/github/v/release/RTIInternational/rota?logo=github)](https://github.com/RTIInternational/rota)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4739146.svg)](https://doi.org/10.5281/zenodo.4739146)

Criminal justice research often requires conversion of free-text offense descriptions into overall charge categories to aid analysis. For example, the free-text offense of "eluding a police vehicle" would be coded to a charge category of "Obstruction - Law Enforcement". Since free-text offense descriptions aren't standardized and often need to be categorized in large volumes, this can result in a manual and time intensive process for researchers. ROTA is a machine learning model for converting offense text into offense codes. 

Currently ROTA predicts the *Charge Category* of a given offense text. A *charge category* is one of the headings for offense codes in the [2009 NCRP Codebook: Appendix F](https://www.icpsr.umich.edu/web/NACJD/studies/30799/datadocumentation#).

The model was trained on [publicly available data](https://web.archive.org/web/20201021001250/https://www.icpsr.umich.edu/web/pages/NACJD/guides/ncrp.html) from a crosswalk containing offenses from all 50 states combined with three additional hand-labeled offense text datasets.

For more information on the model, please see the [model repo](https://huggingface.co/rti-international/rota).
