#open json file in MATLAB
fname = 'Qflow_CINE_LVOT_Intersection_Plane_Info.json'; 
fid = fopen(fname); 
raw = fread(fid,inf); 
str = char(raw'); 
fclose(fid); 
val = jsondecode(str);

#fileName = 'Qflow_CINE_LVOT_Intersection_Plane_Info.json'; % filename in JSON extension 
#str = fileread(fileName); % dedicated for reading files as text 
#data = jsondecode(str); % Using the jsondecode function to parse JSON from string 