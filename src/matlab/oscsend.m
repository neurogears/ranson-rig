function oscsend(varargin)
  if nargin < 3
    error(["Invalid call. Use oscsend(u,path,types,arg1,arg2,...)"]);
  end
  u = varargin{1};
  path = oscstr(varargin{2});
  types = varargin{3};
  data = [];
  offset = 4;
  for i = 2:length(types)
    code = types(i);
    if code == 'i'
      value = fliplr(typecast(uint32(varargin{offset}),'uint8'));
    elseif code == 'f'
      value = fliplr(typecast(single(varargin{offset}),'uint8'));
    elseif code == 's'
      value = oscstr(varargin{offset});
    elseif code == '['
      continue
    elseif code == ']'
      continue
    else
      error("Unsupported type tag.");
    end
    offset = offset + 1;
    data = [data value];
  end
  types = oscstr(types);
  fwrite(u,[path types data],'uint8');
end