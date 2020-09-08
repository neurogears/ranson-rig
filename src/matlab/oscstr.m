function s = oscstr(str)
  s = uint8(str);
  l = length(str) + 1;
  pad = mod(4 - mod(l,4),4);
  s(l + pad) = 0;
end