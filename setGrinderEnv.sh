#!/bin/bash
GRINDERPATH=/home/maier/apps/grinder
GRINDERPROPERTIES=grinder.properties
CLASSPATH=$GRINDERPATH/lib/grinder.jar:$CLASSPATH
JAVA_HOME=/opt/jdk_latest
PATH=$JAVA_HOME/bin:$PATH
export CLASSPATH PATH GRINDERPROPERTIES

