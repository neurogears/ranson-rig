function o = oscrecv(u)
  set(u, 'timeout', 500);
  datagram = [];
  while length(datagram) == 0
    datagram = fread(u);
  end
end