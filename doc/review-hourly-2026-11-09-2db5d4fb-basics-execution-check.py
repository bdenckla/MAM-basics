import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time
import zipfile

HOME_REPO = Path('/workspace/MAM-basics')
WORK = Path('/workspace/scratch/basics-2db5d4fb-focused')
OUT = Path('/workspace/scratch/basics-2db5d4fb-evidence')
SOURCE = '2db5d4fbe24dab0509a4fb5e92511de1535b3a6f'
PYTHON = str(HOME_REPO/'.venv/bin/python')
COMMANDS = {'foi':[PYTHON,'py/main_foi_features_of_interest.py','--single-threaded'], 'mam-doc':[PYTHON,'py/main_mam_with_doc.py'], 'near-html':[PYTHON,'py/main_near_aleppo.py','--html','--check'], 'tests':[PYTHON,'py/main_test.py','py/tests/test_author_std_table.py','py/tests/test_shared_html_styles.py']}

def git(repo,*args):
    return subprocess.check_output(['git','-C',str(repo),*args])

def write(name,record):
    (OUT/name).write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')

assert git(WORK,'rev-parse','HEAD').decode().strip() == SOURCE
assert not git(WORK,'status','--porcelain=v1','-z')
assert git(HOME_REPO,'rev-parse','HEAD').decode().strip() == 'cb878aef91e692d5561435f00021f73b75868e45'
assert not git(HOME_REPO,'status','--porcelain=v1','-z')
mode = sys.argv[1]
if mode == 'preflight':
    OUT.mkdir(exist_ok=False)
    commands = [[PYTHON,'/workspace/scratch/preflight_nightly_20261108.py',str(WORK)],[PYTHON,'/workspace/scratch/verify_env_scope_20261109.py',str(WORK)]]
    for i,command in enumerate(commands,1):
        result = subprocess.run(command,cwd=WORK,capture_output=True,text=True,encoding='utf-8')
        (OUT/f'environment-{i}.log').write_text(result.stdout+result.stderr,encoding='utf-8',newline='\n')
        assert result.returncode == 0, (command,result.stdout,result.stderr)
    write('preflight.json',dict(source=SOURCE,worktree=str(WORK),home_clone=str(HOME_REPO),interpreter=PYTHON,verified_environment='Python3.13.15; constrained versions/direct requirements/pip check; no unpinned application packages or system/user sites.',instructions={name:git(WORK,'rev-parse','HEAD:'+name).decode().strip() for name in ['AGENTS.md','doc/review-trial.md','doc/periodic-review.md']},scope='Four explicitly requested focused commands only; source/output review and extracted-function probes owned by another reviewer. No private inputs selected, mega, full suite, source refresh, baseline or publication.',commands=commands))
    write('slot.json',dict(state='claimed',claimed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),source=SOURCE,worktree=str(WORK)))
    print('Exact worktree and owning constrained interpreter verified; focused slot claimed.')
else:
    command = COMMANDS[mode]
    assert not (OUT/(mode+'.json')).exists(), mode
    assert not (OUT/'active.json').exists()
    order = list(COMMANDS)
    for prior in order[:order.index(mode)]:
        result = json.loads((OUT/(prior+'.json')).read_text(encoding='utf-8'))
        assert result['exit_code'] == 0 and not result['tracked_changes'] and not result['untracked']
    environment = dict(os.environ,PYTHONUNBUFFERED='1')
    removed = [key for key in ['REPOS_ROOT','REPO_MAM_BASICS_DIR','REPO_MAM_PARSED_DIR'] if environment.pop(key,None) is not None]
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    write('active.json',dict(name=mode,command=command,source=SOURCE,started_utc=started,pid=os.getpid()))
    start = time.monotonic()
    with (OUT/(mode+'.log')).open('w',encoding='utf-8',newline='\n') as log:
        result = subprocess.run(command,cwd=WORK,env=environment,stdout=log,stderr=subprocess.STDOUT)
    elapsed = round(time.monotonic()-start,6)
    assert git(WORK,'rev-parse','HEAD').decode().strip() == SOURCE
    changes = [p.decode('utf-8') for p in git(WORK,'diff','--name-only','-z').split(b'\0') if p]
    untracked = [p.decode('utf-8') for p in git(WORK,'ls-files','--others','--exclude-standard','-z').split(b'\0') if p]
    patch = git(WORK,'diff','--binary','--full-index')
    (OUT/(mode+'.patch')).write_bytes(patch)
    if changes or untracked:
        with zipfile.ZipFile(OUT/(mode+'-differences.zip'),'x',compression=zipfile.ZIP_DEFLATED) as archive:
            archive.writestr('tracked.patch',patch)
            for name in changes:
                archive.writestr('before/'+name,git(WORK,'show','HEAD:'+name))
                archive.writestr('after/'+name,(WORK/name).read_bytes())
            for name in untracked:
                archive.writestr('untracked/'+name,(WORK/name).read_bytes())
    record = dict(source=SOURCE,cwd=str(WORK),command=command,started_utc=started,elapsed_seconds=elapsed,exit_code=result.returncode,tracked_changes=changes,untracked=untracked,patch_sha256=hashlib.sha256(patch).hexdigest(),removed_inherited_path_overrides=removed,source_review='Not repeated; commands executed independently in this exact checkout.')
    write(mode+'.json',record)
    (OUT/'active.json').unlink()
    print(json.dumps(record),flush=True)
