import os
import subprocess
import shlex
from pexpect.popen_spawn import PopenSpawn



class Command(object):
    def __init__(self, cmd):
        super(Command, self).__init__()
        self.cmd = cmd
        self.subprocess = None
        self.blocking = None

    def __repr__(self):
        return '<Commmand {!r}>'.format(self.cmd)

    @property
    def _popen_args(self):
        # return shlex.split(self.cmd)
        return self.cmd

    @property
    def _default_popen_kwargs(self):
        return {
            'env': os.environ.copy(),
            'stdin': subprocess.PIPE,
            'stdout': subprocess.PIPE,
            'stderr': subprocess.PIPE,
            'universal_newlines': True,
            # 'bufsize': 0,
        }

    @property
    def _default_pexpect_kwargs(self):
        return {
            'env': os.environ.copy(),
        }

    @property
    def std_out(self):
        return self.subprocess.stdout

    @property
    def _pexpect_out(self):
        result = ''

        if self.subprocess.before:
            result += self.subprocess.before

        if isinstance(self.subprocess.after, str):
            result += self.subprocess.after

        result += self.subprocess.read()
        return result

    @property
    def out(self):
        if isinstance(self.subprocess, subprocess.Popen):
            return self.std_out.read()
        else:
            return self._pexpect_out

    @property
    def std_err(self):
        return self.subprocess.stderr

    @property
    def err(self):
        if isinstance(self.subprocess, subprocess.Popen):
            return self.std_err.read()
        else:
            return self._pexpect_out

    @property
    def pid(self):
        """The process' PID."""
        return self.subprocess.pid

    @property
    def return_code(self):
        if isinstance(self.subprocess, subprocess.Popen):
            return self.subprocess.returncode
        else:
            return self.subprocess.returncode
            raise RuntimeError('return codes can only be used for blocking commands.')


    @property
    def std_in(self):
        return self.subprocess.stdin

    def run(self, block=True):
        self.blocking = block

        if self.blocking:
            s = subprocess.Popen(self._popen_args, **self._default_popen_kwargs)
        else:
            s = PopenSpawn(self._popen_args, **self._default_pexpect_kwargs)
        self.subprocess = s

    def expect(self, pattern, timeout=-1):
        if self.blocking:
            raise RuntimeError('expect can only be run on non-blocking commands.')
        """Waits on the following string to appear in std_out"""
        self.subprocess.expect(pattern=pattern, timeout=timeout)

    def send(self, s, end='\n', signal=False):
        """Sends the given string or signal to std_in."""
        if not signal:
            if isinstance(self.subprocess, subprocess.Popen):
                return self.subprocess.communicate(s + end)
            else:
                return self.subprocess.send(s + end)
        else:
            self.subprocess.send_signal(s)

    def terminate(self):
        self.subprocess.terminate()

    def kill(self):
        self.subprocess.kill()

    def block(self):
        """Blocks until process is complete."""
        self.subprocess.wait()


def _expand_args(command):
    """Parses command strings and returns a Popen-ready list."""

    # Prepare arguments.
    if isinstance(command, (str, unicode)):
        splitter = shlex.shlex(command.encode('utf-8'))
        splitter.whitespace = '|'
        splitter.whitespace_split = True
        command = []

        while True:
            token = splitter.get_token()
            if token:
                command.append(token)
            else:
                break

        command = list(map(shlex.split, command))

    return command


def chain(command):
    commands = _expand_args(command)
    data = None

    for command in commands:

        c = run(command, block=False)

        if data:
            c.send(data)
            c.subprocess.sendeof()

        data = c.out
        # c.block()

    return c


def run(command, block=True):
    c = Command(command)
    c.run(block=block)

    if block:
        c.block()

    return c