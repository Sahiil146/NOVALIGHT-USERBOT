# You came all here just to see this?

import os, enum, sys, signal, atexit

_discared = [
    'LRU_ESABATAD',
    'IPA_UKOREH',
    'NOISSES',
    'IRU_OGNOM',
    'NEKOT_TOB',
    'DI_IPA',
    'HSAH_IPA',
    'DROWSSAPSIDER',
    'DROWSSAP_SIDER',
    'NOISSES_CV',
]
__session = {}
Q = lambda i: i[::-1]
__env = {}
_get_sys = {}
_argv = []
_discared = list(
    tuple(
        map(Q, _discared)
    )
)
def bring_back_dot_env():
    if __env:
        with open(".env", "w") as f:
            f.write(__env["_"])

def sys_exit(useless = 0):
    bring_back_dot_env()
    print("Exiting System")
    os._exit(0)

# asst.loop.add_signal_handler(sig, lambda _sig=sig: sys_exit())
def _get_session(self):
   if __session.get(self):
       self.session = __session[self]
def _clear_session(self):
   from telethon.sessions import StringSession
   if self.session and self.session.auth_key:
        ss = self.session
        __session.update({self:ss})
        self.session = StringSession("")
        self.session._dc_id = ss.dc_id

# Class Var Clean up
def cleanup_cache(what_u_doing_here=None):
    from LightUB.configs import Var
    from LightUB import light_bot, asst, vcClient
    try:
#       for sig in (signal.SIGHUP, signal.SIGTERM, signal.SIGINT, signal.SIGUSR1, signal.SIGHUP, signal.SIGILL, signal.SIGBUS, signal.SIGSEGV):
#            asst.loop.add_signal_handler(sig, lambda _sig=sig: sys_exit())
#        atexit.register(sys_exit)
        for i in [
            light_bot,
            asst,
            vcClient
        ]:
            if i:
                setattr(
                    i,
                    "refresh_auth",
                    _get_session
                )
                setattr(i,
                    "clear_auth", _clear_session)
                i.clear_auth(i)
        os_stuff()
#        if os.path.exists("hello"):
#            rem = open("hello", "r").read()
#            update({"_":rem})
#            os.remove("hello")
        _argv.append(sys.argv)
        if len(sys.argv) > 1:
            sys.argv = [sys.argv[0], sys.argv[-1]]
        for z in _discared:
            if z in Var.__dict__.keys():
                _get_sys.update({z: Var.__dict__[z]})
                setattr(Var, z, "")
    except SystemExit:
        sys_exit()


class List(list):
    __doc__ = ""

    @property
    def __setattr__(self):
      raise AttributeError("Core Dumped!")

    __setitem__ = {}.__setitem__

    @property
    def __len__(self):
      return [].__len__

    @property
    def append(self):
        raise AttributeError("Read only Attribute...")

    @property
    def pop(self):
        raise AttributeError("Read only Attribute...")

    @property
    def clear(self):
        raise AttributeError("Read only Attribute...")

    @property
    def extend(self):
        raise AttributeError("Read only Attribute...")

    @property
    def insert(self):
        raise AttributeError("Read only Attribute...")

# Env clean up
def os_stuff():
    all = os.environ
    for z in all.keys():
        for zz in _discared:
            if zz in z:
                all.update({z: ""})

# Getting them back for re-start & soft update
enum._make_class_unpicklable(List)
def call_back():
    if _argv:
        sys.argv = _argv[0]
    from LightUB.configs import Var
#    if __env:
#        open(".env", "w").write(__env["_"])
    for z in _get_sys:
        if _get_sys[z]:
            setattr(Var, z, str(_get_sys[z]))
            os.environ[z] = str(_get_sys[z])

class KEEP_SAFE:
    xbitch=('lave_erongi_',
    'NOISSES',
    'NEKOT_TOB',
    'NOISSES_CV',
    'tseuqeRtnuoccAeteleD',
    'IPA_UKOREH',
    '46esab',
    'hsab',
    'kcab_llac',
    '\(em_teg',
    ')"em"(ytitne_teg',
    ")'em'(ytitne_teg",
    'cexe',
    'enohp',
    'DROWSSAP_SIDER',
    'snodda_daol',
    'snigulp_rehto_daol',
    'metsys.so',
    'ssecorpbus',
    ')(slacol tiawa',
    'cexea',
    ')(evas.noisses.',
    'yek.yek_htua.',
    'DROWSSAP_ATSNI',
    'TES_ATSNI',
    'SODUS',
    'ODUSLLUF',
    'EFAS_PEEK',
    'llahsulf.',
    'sys_teg_',
    'vne.',
    'TSILVED')
    @property
    def All(self):
        xxx = map(
            lambda __:__[::-1],
            self.xbitch)
        return List(list(xxx))

enum._make_class_unpicklable(KEEP_SAFE)
__all__ = ["KEEP_SAFE", "cleanup_cache", "call_back"]
