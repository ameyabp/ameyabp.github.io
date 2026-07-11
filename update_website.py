import argparse
from datetime import datetime
from pytz import timezone
import os

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
                prog='UpdateWebsite',
                description="Script to push changes to website to github",
            )
    
    parser.add_argument('-m', '--commit_message', required=True)
    parser.add_argument('-f', '--files', nargs='*')

    args = parser.parse_args()

    # get latest update timestamp
    format = "%A, %d %B %Y %H:%M:%S %Z"
    timestamp = datetime.now(timezone('Asia/Kolkata')).strftime(format)
    
    lines = []
    with open('index.html', 'r+') as f:
        lines = f.readlines()
        for i,line in enumerate(lines):
            if "Created using bootstrap. Last updated" in line:
                line = f"\t\t\t\tCreated using bootstrap. Last updated {timestamp}\n"
                break

        lines[i] = line
    os.remove('index.html')

    g = open('index.html', 'w')
    g.writelines(lines)
    g.close()

    # git add
    cmd = "git add index.html"
    if args.files:
        for f in args.files:
            cmd += " " + f
    
    print(cmd)
    os.system(cmd)

    # git commit
    cmd = f"git commit -m \"{args.commit_message}\""
    print(cmd)
    os.system(cmd)

    # git push
    cmd = "git push"
    os.system(cmd)