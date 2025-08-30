#!/bin/bash
# Script to restart Stanford CoreNLP with proper memory settings

echo "Stopping any existing CoreNLP processes..."
pkill -f "StanfordCoreNLPServer" || true

echo "Waiting for processes to stop..."
sleep 2

echo "Starting Stanford CoreNLP with increased memory..."
cd stanford-corenlp-4.5.4

java -Xmx4g -Xms2g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer \
  -port 9000 \
  -timeout 15000 \
  -maxCharLength 2000 \
  -annotators "tokenize,ssplit,pos,ner" \
  -outputFormat json

echo "CoreNLP server started with 4GB heap memory"
echo "Server will be available at http://localhost:9000"
