import xml.etree.cElementTree as XML

import requests

class SoCo(object):
    """A simple class for controlling a Sonos speaker.

    Public functions:
    play -- Plays the currently selected track.
    pause -- Pause the currently playing track.
    stop -- Stop the currently playing track.
    next -- Go to the next track.
    previous -- Go back to the previous track.
    mute -- Mute (or unmute) the speaker.
    set_volume -- Set the volume of the speaker.
    status_light -- Turn on (or off) the Sonos status light.
    get_current_track_info -- Get information about the currently playing track.

    """

    TRANSPORT_ENDPOINT = '/MediaRenderer/AVTransport/Control'
    RENDERING_ENDPOINT = '/MediaRenderer/RenderingControl/Control'
    DEVICE_ENDPOINT = '/DeviceProperties/Control'

    def __init__(self, speaker_ip):
        self.speaker_ip = speaker_ip

    def play(self):
        """Start playing the currently selected track.

        Returns:
        True if the Sonos speaker successfully started playing the track.
        
        If an error occurs, we'll attempt to parse the error and return a UPnP
        error code. If that fails, the raw response sent back from the Sonos
        speaker will be returned.

        """
        action = '"urn:schemas-upnp-org:service:AVTransport:1#Play"'

        body = '<u:Play xmlns:u="urn:schemas-upnp-org:service:AVTransport:1"><InstanceID>0</InstanceID><Speed>1</Speed></u:Play>'

        response = self.__send_command(SoCo.TRANSPORT_ENDPOINT, action, body)

        if (response == '<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"><s:Body><u:PlayResponse xmlns:u="urn:schemas-upnp-org:service:AVTransport:1"></u:PlayResponse></s:Body></s:Envelope>'):
            return True
        else:
            return self.__parse_error(response)

    def pause(self):
        """ Pause the currently playing track.

        Returns:
        True if the Sonos speaker successfully paused the track.
        
        If an error occurs, we'll attempt to parse the error and return a UPnP
        error code. If that fails, the raw response sent back from the Sonos
        speaker will be returned.
        
        """
        action = '"urn:schemas-upnp-org:service:AVTransport:1#Pause"'

        body = '<u:Pause xmlns:u="urn:schemas-upnp-org:service:AVTransport:1"><InstanceID>0</InstanceID><Speed>1</Speed></u:Pause>'

        response = self.__send_command(SoCo.TRANSPORT_ENDPOINT, action, body)

        if (response == '<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"><s:Body><u:PauseResponse xmlns:u="urn:schemas-upnp-org:service:AVTransport:1"></u:PauseResponse></s:Body></s:Envelope>'):
            return True
        else:
            return self.__parse_error(response)

    def stop(self):
        """ Stop the currently playing track.
        
        Returns:
        True if the Sonos speaker successfully stopped the playing track.
        
        If an error occurs, we'll attempt to parse the error and return a UPnP
        error code. If that fails, the raw response sent back from the Sonos
        speaker will be returned.
        
        """
        action = '"urn:schemas-upnp-org:service:AVTransport:1#Stop"'

        body = '<u:Stop xmlns:u="urn:schemas-upnp-org:service:AVTransport:1"><InstanceID>0</InstanceID><Speed>1</Speed></u:Stop>'

        response = self.__send_command(SoCo.TRANSPORT_ENDPOINT, action, body)

        if (response == '<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"><s:Body><u:StopResponse xmlns:u="urn:schemas-upnp-org:service:AVTransport:1"></u:StopResponse></s:Body></s:Envelope>'):
            return True
        else:
            return self.__parse_error(response)

    def next(self):
        """ Go to the next track.
        
        Returns:
        True if the Sonos speaker successfully skipped to the next track.
        
        If an error occurs, we'll attempt to parse the error and return a UPnP
        error code. If that fails, the raw response sent back from the Sonos
        speaker will be returned. Keep in mind that next() can return errors
        for a variety of reasons. For example, if the Sonos is streaming
        Pandora and you call next() several times in quick succession an error
        code will likely be returned (since Pandora has limits on how many
        songs can be skipped).
        
        """
        action = '"urn:schemas-upnp-org:service:AVTransport:1#Next"'

        body = '<u:Next xmlns:u="urn:schemas-upnp-org:service:AVTransport:1"><InstanceID>0</InstanceID><Speed>1</Speed></u:Next>'

        response = self.__send_command(SoCo.TRANSPORT_ENDPOINT, action, body)

        if (response == '<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"><s:Body><u:NextResponse xmlns:u="urn:schemas-upnp-org:service:AVTransport:1"></u:NextResponse></s:Body></s:Envelope>'):
            return True
        else:
            return self.__parse_error(response)

    def previous(self):
        """ Go back to the previously played track.
        
        Returns:
        True if the Sonos speaker successfully went to the previous track.
        
        If an error occurs, we'll attempt to parse the error and return a UPnP
        error code. If that fails, the raw response sent back from the Sonos
        speaker will be returned. Keep in mind that previous() can return errors
        for a variety of reasons. For example, previous() will return an error
        code (error code 701) if the Sonos is streaming Pandora since you can't
        go back on tracks.
        
        """
        action = '"urn:schemas-upnp-org:service:AVTransport:1#Previous"'

        body = '<u:Previous xmlns:u="urn:schemas-upnp-org:service:AVTransport:1"><InstanceID>0</InstanceID><Speed>1</Speed></u:Previous>'

        response = self.__send_command(SoCo.TRANSPORT_ENDPOINT, action, body)

        if (response == '<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"><s:Body><u:PreviousResponse xmlns:u="urn:schemas-upnp-org:service:AVTransport:1"></u:PreviousResponse></s:Body></s:Envelope>'):
            return True
        else:
            return self.__parse_error(response)

    def mute(self, mute):
        """ Mute or unmute the Sonos speaker.

        Arguments:
        mute -- True to mute. False to unmute.
        
        Returns:
        True if the Sonos speaker was successfully muted or unmuted.
        
        If an error occurs, we'll attempt to parse the error and return a UPnP
        error code. If that fails, the raw response sent back from the Sonos
        speaker will be returned.
        
        """
        if mute is True:
            mute_value = '1'
        else:
            mute_value = '0'

        action = '"urn:schemas-upnp-org:service:RenderingControl:1#SetMute"'

        body = '<u:SetMute xmlns:u="urn:schemas-upnp-org:service:RenderingControl:1"><InstanceID>0</InstanceID><Channel>Master</Channel><DesiredMute>' + mute_value + '</DesiredMute></u:SetMute>'

        response = self.__send_command(SoCo.RENDERING_ENDPOINT, action, body)

        if (response == '<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"><s:Body><u:SetMuteResponse xmlns:u="urn:schemas-upnp-org:service:RenderingControl:1"></u:SetMuteResponse></s:Body></s:Envelope>'):
            return True
        else:
            return self.parse(response)

    def set_volume(self, volume):
        """ Set the Sonos speaker volume.

        Arguments:
        volume -- A value between 0 and 100.
        
        Returns:
        True if the Sonos speaker successfully set the volume.
        
        If an error occurs, we'll attempt to parse the error and return a UPnP
        error code. If that fails, the raw response sent back from the Sonos
        speaker will be returned.
        
        """
        action = '"urn:schemas-upnp-org:service:RenderingControl:1#SetVolume"'

        body = '<u:SetVolume xmlns:u="urn:schemas-upnp-org:service:RenderingControl:1"><InstanceID>0</InstanceID><Channel>Master</Channel><DesiredVolume>' + repr(volume) + '</DesiredVolume></u:SetVolume>'

        response = self.__send_command(SoCo.RENDERING_ENDPOINT, action, body)

        if (response == '<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"><s:Body><u:SetVolumeResponse xmlns:u="urn:schemas-upnp-org:service:RenderingControl:1"></u:SetVolumeResponse></s:Body></s:Envelope>'):
            return True
        else:
            return self.__parse_error(response)

    def status_light(self, led_on):
        """ Turn on (or off) the white Sonos status light.

        Turns on or off the little white light on the Sonos speaker. (It's
        between the mute button and the volume up button on the speaker.)

        Arguments:
        led_on -- True to turn on the light. False to turn off the light.
        
        Returns:
        True if the Sonos speaker successfully turned on (or off) the light.
        
        If an error occurs, we'll attempt to parse the error and return a UPnP
        error code. If that fails, the raw response sent back from the Sonos
        speaker will be returned.
        
        """
        if led_on is True:
            led_state = 'On'
        else:
            led_state = 'Off'

        action = '"urn:schemas-upnp-org:service:DeviceProperties:1#SetLEDState"'

        body = '<u:SetLEDState xmlns:u="urn:schemas-upnp-org:service:DeviceProperties:1"><DesiredLEDState>' + led_state + '</DesiredLEDState>'

        response = self.__send_command(SoCo.DEVICE_ENDPOINT, action, body)

        if (response == '<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"><s:Body><u:SetLEDStateResponse xmlns:u="urn:schemas-upnp-org:service:DeviceProperties:1"></u:SetLEDStateResponse></s:Body></s:Envelope>'):
            return True
        else:
            return self.parse(response)

    def get_current_track_info(self):
        """ Get information about the currently playing track.
        
        Returns:
        A dictionary containing the following information about the currently
        playing track: playlist_position, duration, title, artist, album.
        
        If we're unable to return data for a field, we'll return an empty
        string. This can happen for all kinds of reasons so be sure to check
        values. For example, a track may not have complete metadata and be
        missing an album name. In this case track['album'] will be an empty string.
        
        """
        action = '"urn:schemas-upnp-org:service:AVTransport:1#GetPositionInfo"'

        body = '<u:GetPositionInfo xmlns:u="urn:schemas-upnp-org:service:AVTransport:1"><InstanceID>0</InstanceID><Channel>Master</Channel></u:GetPositionInfo>'

        response = self.__send_command(SoCo.TRANSPORT_ENDPOINT, action, body)

        dom = XML.fromstring(response)

        track = {}

        track['playlist_position'] = dom.findtext('.//Track')

        track['duration'] = dom.findtext('.//TrackDuration')

        d = dom.findtext('.//TrackMetaData')

        if d is not '':
            # Track metadata is returned in DIDL-Lite format
            metadata = XML.fromstring(d.encode('utf-8'))

            track['title'] = metadata.findtext('.//{http://purl.org/dc/elements/1.1/}title')
            track['artist'] = metadata.findtext('.//{http://purl.org/dc/elements/1.1/}creator')
            track['album'] = metadata.findtext('.//{urn:schemas-upnp-org:metadata-1-0/upnp/}album')
        else:
            track['title'] = ''
            track['artist'] = ''
            track['album'] = ''

        return track

    def __send_command(self, endpoint, action, body):
        """ Send a raw command to the Sonos speaker.

        Returns:
        The raw response body returned by the Sonos speaker.

        """
        headers = {
            'Content-Type': 'text/xml',
            'SOAPACTION': action
        }

        soap = '<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"><s:Body>' + body + '</s:Body></s:Envelope>'

        r = requests.post('http://' + self.speaker_ip + ':1400' + endpoint, data=soap, headers=headers)

        return r.content

    def __parse_error(self, response):
        """ Parse an error returned from the Sonos speaker.

        Returns:
        The UPnP error code returned by the Sonos speaker.

        If we're unable to parse the error response for whatever reason, the
        raw response sent back from the Sonos speaker will be returned.
        """
        error = XML.fromstring(response)

        errorCode = error.findtext('.//{urn:schemas-upnp-org:control-1-0}errorCode')

        if errorCode is not None:
            return int(errorCode)
        else:
            # Unknown error, so just return the entire response
            return response
