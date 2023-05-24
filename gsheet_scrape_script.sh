#!/usr/bin/env bash
echo $0
eval "$(/Users/jacobhume/opt/anaconda3/bin/conda shell.bash hook)"
cd /Users/jacobhume/PycharmProjects/ChineseAnki
conda activate chinese
python3 /Users/jacobhume/PycharmProjects/ChineseAnki/gsheet_to_anki.py
if [ $? -ne 0 ]; then
  /usr/local/bin/terminal-notifier -message "Run vim /tmp/local.job.stderr" -title "Error in getting gsheet data."
  echo "error notification sent"
fi
