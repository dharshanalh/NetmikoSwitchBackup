from __future__ import print_function
from __future__ import unicode_literals
import time
from netmiko.cisco_base_connection import CiscoSSHConnection


class HPComwareJinhuaBase(CiscoSSHConnection):

    def session_preparation(self):
        """
        Prepare the session after the connection has been established.
        Extra time to read HP banners.
        """
        delay_factor = self.select_delay_factor(delay_factor=0)
        i = 1
        while i <= 4:
            # Comware can have a banner that prompts you to continue
            # 'Press Y or ENTER to continue, N to exit.'
            time.sleep(.5 * delay_factor)
            self.write_channel("\n")
            i += 1
        
        #log into command line mode by command line break
        time.sleep(0.3 * delay_factor)                  # adding a delay to execute the command
        self.write_channel("_cmdline-mode on \n")       # enter command line break command to channel
        self.write_channel("y \n")                      # enter y 
        self.write_channel("Jinhua1920unauthorized\n")  # enter command line break password

        time.sleep(.3 * delay_factor)
        self.clear_buffer()
        self._test_channel_read(pattern=r'[>\]]')
        self.set_base_prompt()
        command = self.RETURN + "screen-length disable"
        self.disable_paging(command=command)
        # Clear the read buffer
        time.sleep(.3 * self.global_delay_factor)
        self.clear_buffer()

    def config_mode(self, config_command='system-view'):
        """Enter configuration mode."""
        return super(HPComwareJinhuaBase, self).config_mode(config_command=config_command)

    def exit_config_mode(self, exit_config='return', pattern=r'>'):
        """Exit config mode."""
        return super(HPComwareJinhuaBase, self).exit_config_mode(exit_config=exit_config,
                                                           pattern=pattern)

    def check_config_mode(self, check_string=']'):
        """Check whether device is in configuration mode. Return a boolean."""
        return super(HPComwareJinhuaBase, self).check_config_mode(check_string=check_string)

    def set_base_prompt(self, pri_prompt_terminator='>', alt_prompt_terminator=']',
                        delay_factor=1):
        """
        Sets self.base_prompt

        Used as delimiter for stripping of trailing prompt in output.

        Should be set to something that is general and applies in multiple contexts. For Comware
        this will be the router prompt with < > or [ ] stripped off.

        This will be set on logging in, but not when entering system-view
        """
        prompt = super(HPComwareJinhuaBase, self).set_base_prompt(
            pri_prompt_terminator=pri_prompt_terminator,
            alt_prompt_terminator=alt_prompt_terminator,
            delay_factor=delay_factor)

        # Strip off leading character
        prompt = prompt[1:]
        prompt = prompt.strip()
        self.base_prompt = prompt
        return self.base_prompt

    def enable(self, cmd='system-view'):
        """enable mode on Comware is system-view."""
        return self.config_mode(config_command=cmd)

    def exit_enable_mode(self, exit_command='return'):
        """enable mode on Comware is system-view."""
        return self.exit_config_mode(exit_config=exit_command)

    def check_enable_mode(self, check_string=']'):
        """enable mode on Comware is system-view."""
        return self.check_config_mode(check_string=check_string)

    def save_config(self, cmd='save force', confirm=False):
        """Save Config."""
        return super(HPComwareJinhuaBase, self).save_config(cmd=cmd, confirm=confirm)


class HPComwareJinhuaSSH(HPComwareJinhuaBase):
    pass


class HPComwareJinhuaTelnet(HPComwareJinhuaBase):
    def __init__(self, *args, **kwargs):
        default_enter = kwargs.get('default_enter')
        kwargs['default_enter'] = '\r\n' if default_enter is None else default_enter
        super(HPComwareJinhuaTelnet, self).__init__(*args, **kwargs)
