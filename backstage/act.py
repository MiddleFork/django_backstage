"""act.py
Django Backstage 'Act' module"""
import os
import shutil
import backstage

def new_act(self, act_name=None):
    bs_home = os.path.dirname(os.path.abspath(backstage.__file__))
    if act_name is None:
        err = 'Name of new act required'
        print err
        return False
    act_skel = os.path.join(bs_home, 'skel/act')
    act_path = os.path.join(self.PROJECT_ROOT, 'acts/%s' % act_name)
    try:
        shutil.copytree(act_skel, act_path)
    except:
        print 'error copying act skel'
        raise
        return False
    print 'Created Act %s at %s' % (act_name, act_path)
    return True
