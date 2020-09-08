function oscsend(varargin)
  if nargin < 3
    error(["Invalid call. Use oscsend(u,path,types,arg1,arg2,...)"]);
  end
  u = varargin{1};
  path = oscstr(varargin{2});
  types = varargin{3};
  data = [];
  for i = 4:nargin
    code = types(i-2);
    if code == 'i'
      value = fliplr(typecast(uint32(varargin{i}),'uint8'));
    elseif code == 'f'
      value = fliplr(typecast(single(varargin{i}),'uint8'));
    elseif code == 's'
      value = oscstr(varargin{i});
    else
      error("Unsupported type tag.");
    end
    data = [data value];
  end
  types = oscstr(types);
  fwrite(u,[path types data],'uint8');
end