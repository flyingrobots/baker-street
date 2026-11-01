"""Bounded capture for reviewed pure-Python probes; not a security sandbox."""
import argparse, hashlib, json, os, resource, selectors, signal, subprocess, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parent

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--role',choices=['holmes','moriarty','checker','repair_checker','front_office'],required=True)
    p.add_argument('--label',required=True)
    p.add_argument('--script',required=True)
    a=p.parse_args()
    if not a.label.replace('-','').replace('_','').isalnum(): p.error('Invalid label')
    role=ROOT/'roles'/a.role
    role.mkdir(parents=True,exist_ok=True)
    script=(ROOT/a.script).resolve()
    if not script.is_relative_to(role.resolve()) or not script.is_file(): p.error('Probe must be in the assigned role directory')
    output=role/a.label
    output.mkdir()
    env={'PATH':os.defpath,'PYTHONDONTWRITEBYTECODE':'1','TMPDIR':str(output)}
    def limits():
        resource.setrlimit(resource.RLIMIT_CPU,(10,10))
        resource.setrlimit(resource.RLIMIT_FSIZE,(1048576,1048576))
        resource.setrlimit(resource.RLIMIT_NOFILE,(64,64))
    cmd=[sys.executable,'-B',str(script)]
    start=time.monotonic()
    proc=subprocess.Popen(cmd,cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True,preexec_fn=limits)
    sel=selectors.DefaultSelector()
    sel.register(proc.stdout,selectors.EVENT_READ,'stdout')
    sel.register(proc.stderr,selectors.EVENT_READ,'stderr')
    streams={'stdout':bytearray(),'stderr':bytearray()}; stopped=None
    try:
        while sel.get_map():
            if time.monotonic()-start>20: raise RuntimeError('wall timeout')
            if sum(f.stat().st_size for f in role.rglob('*') if f.is_file())>1048576: raise RuntimeError('role data limit')
            for key,_ in sel.select(0.05):
                data=os.read(key.fd,8192)
                if not data: sel.unregister(key.fileobj); continue
                streams[key.data].extend(data)
                if len(streams[key.data])>65536: raise RuntimeError('output limit')
        proc.wait(timeout=max(0.01,20-(time.monotonic()-start)))
    except BaseException as e:
        stopped=str(e)
        os.killpg(proc.pid,signal.SIGKILL)
        proc.wait()
    finally:
        sel.close()
        # Child processes must not survive completion of the probe leader.
        try: os.killpg(proc.pid,signal.SIGKILL)
        except ProcessLookupError: pass
    for name,data in streams.items(): (output/(name+'.log')).write_bytes(data[:65536])
    record={'command':['python3','-B',a.script],'cwd':'.','python':sys.version.split()[0],'script_sha256':hashlib.sha256(script.read_bytes()).hexdigest(),'exit_code':proc.returncode,'seconds':round(time.monotonic()-start,4),'stopped':stopped,'controls':{'wall_seconds':20,'cpu_seconds':10,'per_file_bytes':1048576,'role_bytes_monitored':1048576,'per_stream_bytes':65536,'network':'instruction-only prohibition','filesystem':'shared host; no OS read isolation','memory':'no memory quota; reviewed finite tiny probes only'}}
    (output/'run.json').write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps(record,indent=2))
    for name,data in streams.items():
        print(name+':'); print(data[:65536].decode(errors='replace'))
    return proc.returncode if not stopped else 125

if __name__=='__main__': raise SystemExit(main())
