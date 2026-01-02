#!/bin/bash

# Set version for setuptools-scm (standard approach)
export SETUPTOOLS_SCM_PRETEND_VERSION="${PKG_VERSION}"

# Install the package
${PYTHON} -m pip install --no-build-isolation --no-deps --ignore-installed -vv ./tradestation-python
