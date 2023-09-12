#!/bin/bash

cd /home/mastofeed/mastofeed/

sed -i 's/force_mention: True/force_mention: False/g' config.yaml
sed -i 's/user_mention: \"none\"/user_mention: \"kergozh\"/g' config.yaml
sed -i 's/disable_post: False/disable_post: True/g' config.yaml
sed -i 's/loglevel: 20/loglevel: 10/g' config.yaml
          

