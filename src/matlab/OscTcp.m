classdef OscTcp < Osc
  properties
    client
  end
  methods
    function obj = OscTcp(varargin)
      if nargin < 2
        error(["Invalid call. Use oscsend(u,path,types,arg1,arg2,...)"]);
      end
      obj.client = tcpclient(varargin{1}, varargin{2});
    end

    function send(obj, varargin)
      if nargin < 2
        error(["Invalid call. Use oscsend(u,path,types,arg1,arg2,...)"]);
      end
      message = Osc.format(varargin{:});
      len = fliplr(typecast(uint32(length(message)),'uint8'));
      write(obj.client, [len message]);
    end
    
    function message = receive(obj)
      set(obj.client, 'timeout', 1000);
      datagram = [];
      while (isempty(datagram))
        datagram = read(obj.client,4);
        size = typecast(uint8(fliplr(datagram)),'uint32');
      end
      datagram = [];
      while (isempty(datagram))
        datagram = read(obj.client,size);
      end
      message = Osc.parse(datagram);
    end
    
    function delete(obj)
      % free up any resources, although there is no instruction to close
      % tcpclient connection
      delete(obj.client);
    end
  end
end