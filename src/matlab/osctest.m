u = udp('127.0.0.1', 4002, 4007);
fopen(u);

oscsend(u, "/gratings", ",ffffffff", 30.0, 0.0, -15.0, 0.0, 0.1, 0.0, 0.0, 2.0); % grating 1
oscsend(u, "/gratings", ",ffffffff", 15.0, 45.0, 15.0, 0.0, 0.2, 0.0, 0.0, 2.0); % grating 2
oscsend(u, "/startgratings", ",i", 0);
oscrecv(u);

oscsend(u, "/go", ",fff", 30.0, 2.0, 0.5); % go trial
oscrecv(u);

oscsend(u, "/nogo", ",fff", 0.0, 2.0, 0.5); % go trial
oscrecv(u);

oscsend(u, "/tile", ",iffsi", 0, 1.25, 1.0, "Black", 0);
oscsend(u, "/tile", ",iffsi", 1, 1.25, 1.0, "White", 0);
oscsend(u, "/tile", ",iffsi", 0, 2.25, 1.0, "White", 0);
oscsend(u, "/tile", ",iffsi", 1, 2.25, 1.0, "Black", 0);
oscsend(u, "/tile", ",iffsi", 2, 1.25, 1.0, "Black", 0);
oscsend(u, "/tile", ",iffsi", 3, 1.25, 1.0, "Transparent", 0);
oscsend(u, "/startcorridor", ",f", 10.0);
oscrecv(u);
fclose(u);