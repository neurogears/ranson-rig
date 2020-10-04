classdef Rig
  properties
    client
  end
  methods
    function obj = Rig(u)
      obj.client = u;
      fopen(obj.client);
    end

    function close(obj)
      fclose(obj.client);
    end

    function resource(obj, path)
      oscsend(obj.client, "/resource", ",s", path);
    end
        
    function preload(obj)
      oscsend(obj.client, "/preload", ",i", 0);
    end
        
    function clear(obj)
      oscsend(obj.client, "/clear", ",i", 0);
    end

    function gratings(obj, g)
      angle = get(g, 'angle', 0.0);
      size = get(g, 'size', 20.0);
      x = get(g, 'x', 0.0);
      y = get(g, 'y', 0.0);
        
      contrast = get(g, 'contrast', 1.0);
      opacity = get(g, 'opacity', 1.0);
      phase = get(g, 'phase', 0.0);
      freq = get(g, 'freq', 0.1);
      speed = get(g, 'speed', 0.0);
      dcycle = get(g, 'dcycle', nan);

      onset = get(g,'onset', 0.0);
      duration = get(g, 'duration', 1.0);
      oscsend(obj.client, "/gratings", ",[ffff][ffffff][ff]", ...
              angle, size, x, y, ...
              contrast, opacity, phase, freq, speed, dcycle, ...
              onset, duration);
    end

    function video(obj, v)
      name = v.name;
      angle = get(v, 'angle', 0.0);
      width = get(v, 'width', 20.0);
      height = get(v, 'height', 20.0);
      x = get(v, 'x', 0.0);
      y = get(v, 'y', 0.0);
        
      loop = get(v, 'loop', 1.0);
      speed = get(v, 'speed', 30.0);
        
      onset = get(v, 'onset', 0.0);
      duration = get(v, 'duration', 2.0);
        
      oscsend(obj.client, "/video", ",[fffff][ffs][ff]", ...
              angle, width, height, x, y, ...
              loop, speed, name, ...
              onset, duration);
    end

    function start(obj)
      oscsend(obj.client, "/start", ",i", 0);
    end

    function success(obj)
      oscsend(obj.client, "/success", ",i", 0);
    end
    
    function failure(obj)
      oscsend(obj.client, "/failure", ",i", 0);
    end
    
    function go(obj, suppress, start, duration, threshold)
      oscsend(obj.client, "/go", ",fffi", suppress, start, duration, threshold);
    end
    
    function nogo(obj, suppress, start, duration, threshold)
      oscsend(obj.client, "/nogo", ",fffi", suppress, start, duration, threshold);
    end

    function interaction(obj, name, type, arguments)
      oscsend(obj.client, sprintf('/interaction/%s', name), sprintf(",%s", type), arguments{:});
    end

    function tile(obj, t)
      wall = t.wall;
      position = get(t, 'position', 0.0);
      extent = get(t, 'extent', 1.0);
      texture = get(t, 'texture', "Transparent");
      oscsend(obj.client, "/tile", ",iffs", ...
              wall, position, extent, texture);
    end
    
    function corridor(obj, c)
      length = c.length;
      width = get(c, 'width', 1.0);
      height = get(c, 'height', 1.0);
      x = get(c, 'x', 0.0);
      y = get(c, 'y', 0.0);
      position = get(c, 'position', 0.0);
      oscsend(obj.client, "/corridor", ",ffffff", ...
              length, width, height, x, y, position);
    end
  end
end

function b = get(a, name, default)
    if isfield(a, name)
        b = getfield(a, name);
    else
        b = default;
    end
end