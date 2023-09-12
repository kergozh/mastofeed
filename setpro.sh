#!/bin/bash

cd /home/mastofeed/mastofeed/

sed -i 's/force_mention: True/force_mention: False/g' config.yaml
sed -i 's/user_mention: \"kergozh\"/user_mention: \"none\"/g' config.yaml
sed -i 's/disable_post: True/disable_post: False/g' config.yaml
sed -i 's/loglevel: 10/loglevel: 20/g' config.yaml