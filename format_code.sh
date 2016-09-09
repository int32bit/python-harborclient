#!/bin/bash
set -x
find ./ -name "*.py" |xargs yapf -i
