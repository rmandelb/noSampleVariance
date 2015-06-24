# DESC-LSST hack 
Here is our [hackpad
note](https://hackpad.com/Avoiding-covariances-of-two-point-correlation-functions-dLUkAI5yrSv)


**Note:** This repository should be cloned into
  `$(COSMOSIS-INSTALL-DIR)/cosmosis-standard-library/noSampleVariance/`
  to keep the relative paths to the CosmoSIS modules consistent with
  CosmoSIS practices. The INI files for CosmoSIS runs require this
  relative path setup.

Sukhdeep: I have edited above. The demo6 as I saw it, seemed to assume
everything was in directory 'cosmosis-standard-library'. I added
noSampleVariance so that our work is distinguishable from standard
cosmosis library. I am open to something different, but I think we do
need to agree on where to keep files within cosmosis directory and
from where to run them. All current paths assume that things will run
from cosmosis main directory. Otherwise lot of paths are broken.
