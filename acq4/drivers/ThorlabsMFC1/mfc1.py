"""
Thorlabs MFC1 : microscope focus controller based on Trinamic TMCM-140-42-SE
and PDx-140-42-SE.

"""


"""
Hardware notes:

* Although the controller supports up to 64 microsteps per full step, the
  actual microstep size is not constant and becomes very nonlinear at around 
  16 microsteps. Using mixed_decay_threshold=-1 helps somewhat.

* Stall detection only works for a limited range of current + speed + threshold

* Encoder has 4096 values per rotation; gear ratio is 1:5.

* Setting encoder prescaler to 8192 yields +1 per encoder step 
"""
try:
    # this is nicer because it provides deadlock debugging information
    from acq4.util.Mutex import RecursiveMutex as RLock
except ImportError:
    from threading import RLock

from acq4.pyqtgraph import ptime

from .tmcm import TMCM140



def threadsafe(method):
    # decorator for automatic mutex lock/unlock
    def lockMutex(self, *args, **kwds):
        with self.lock:
            return method(self, *args, **kwds)
    return lockMutex


class MFC1(object):
    def __init__(self, port, baudrate=9600):
        self.lock = RLock(debug=True)

        self.mcm = TMCM140(port, baudrate)
        self.mcm.stop_program()
        self.mcm.stop()
        self.mcm.set_params(
            maximum_current=50,
            maximum_acceleration=1000,
            maximum_speed=2000,
            ramp_divisor=7,
            pulse_divisor=3,
            standby_current=0,
            mixed_decay_threshold=-1,
            encoder_prescaler=8192,
            microstep_resolution=5,
            fullstep_threshold=0,
            stall_detection_threshold=0,
        )
        self.mcm.set_global('gp0', self.mcm['encoder_position'])
        self._upload_program()

        self._move_status = {}
        self._last_move_id = -1
        
    def _upload_program(self):
        """Upload a program used to seek to a specific encoder value.
        """
        m = self.mcm
        with m.write_program() as p:
            # start with a brief wait because sometimes the first command may be 
            # ignored.
            p.command('wait', 0, 0, 1)

            # distance = target_position - current_position
            p.get_param('encoder_position')
            p.calcx('load')
            p.get_global('gp0')
            p.calcx('sub')
            p.set_global('gp1', 'accum')
            
            # if dx is 0, stop motor and program
            p.comp(0)
            p.jump('ne', p.count+3)
            p.set_param('target_speed', 0)
            p.set_param('actual_speed', 0)
            p.command('stop', 0, 0, 0)
            
            # calculate distance-to-target where we should begin (de)acccelerating
            # Tx = speed**2 / 1572 
            p.get_param('actual_speed')
            p.calcx('load')
            p.calcx('mul')
            p.calc('div', 1400)
            
            p.calcx('swap')  # invert threshold if v < 0
            p.get_param('actual_speed')
            p.comp(0)
            p.calcx('swap')
            p.jump('ge', p.count+1)
            p.calc('mul', -1)    
            p.set_global('gp2', 'accum')
            
            # calculate desired speed
            p.calcx('swap')
            p.get_global('gp1')
            p.calcx('sub')
            p.calcx('swap')
            p.get_param('actual_speed')
            p.calcx('add')
            p.calc('mul', 2)
            p.calc('div', 3)
            
            # new_speed = clip(new_speed, -2047, 2047)
            max = 2000
            p.comp(max)
            p.jump('gt', p.count+3)
            p.comp(-max)
            p.jump('lt', p.count+3)
            p.jump(p.count+3)
            p.calc('load', max)
            p.jump(p.count+1)
            p.calc('load', -max)
            
            # 0 speed should never be requested if there is an offset
            p.comp(0)
            p.jump('ne', p.count+1)
            p.get_global('gp1')
            
            
            # output and repeat
            p.set_param('target_speed', 'accum')
            #p.set_param('actual_speed', 'accum')
            p.jump(1)

    def position(self):
        """Return the current encoder position.
        """
        return self.mcm['encoder_position']
    
    @threadsafe
    def target_position(self):
        """Return the final target position if the motor is currently moving
        to a specific position.

        If the motor is stopped or freely rotating, return the current position.
        """
        if self.program_running():
            return self.mcm.get_global('gp0')
        else:
            return self.position()

    @threadsafe
    def move(self, position):
        """Move to the requested position.

        If the motor is already moving, then update the target position.
        
        Return an object that may be used to check 
        whether the move is complete.
        """
        id = self._last_move_id

        if self.program_running():
            self._interrupt_move()
            self.mcm.set_global('gp0', position)
            start = ptime.time()
        else:
            self.mcm.set_global('gp0', position)
            self.mcm.start_program()
            start = ptime.time()

        id += 1
        self._last_move_id = id
        self._move_status[id] = {'start': start, 'status': 'moving', 'target': position}
        return id

    @threadsafe
    def move_status(self, id, clear=True):
        """Return the status of a previously requested move.

        The return value is a dict with the following keys:

        * status: 'moving', 'interrupted', 'failed', or 'done'.
        * start: the start time of the move.
        * target: the target position of the move.
        """
        stat = self._move_status[id]
        if stat['status'] == 'moving' and not self.program_running():
            if abs(self.position() - stat['target']) <= 1:
                stat['status'] = 'done'
            else:
                stat['status'] = 'failed'

        if clear and stat['status'] != 'moving':
            del self._move_status[id]

        return stat
        
    @threadsafe
    def rotate(self, speed):
        """Begin rotating at *speed*. Positive values turn right.
        """
        self._interrupt_move()
        self.mcm.stop_program()
        self.mcm.rotate(speed)

    def _interrupt_move(self):
        """If a move is currently in progress, set its state to 'interrupted'
        """
        id = self._last_move_id
        try:
            stat = self.move_status(id, clear=False)
            if stat['status'] == 'moving':
                self._move_status[id]['status'] = 'interrupted'
        except KeyError:
            pass
    
    def stop(self):
        """Immediately stop the motor and any programs running on the motor
        comtrol module.
        """
        self._interrupt_move()
        self.mcm.stop_program()
        self.mcm.stop()

    def program_running(self):
        return self.mcm.get_global('tmcl_application_status') == 1

    def set_encoder(self, x):
        self.mcm['encoder_position'] = x
