#version 330 core
layout(location = 0) out float upVelx;
layout(location = 1) out float upVely;
layout(location = 2) out float upVelz;

in vec2 g_TexCoords;
flat in int g_layer;

uniform float ox;
uniform float oy;
uniform float oz;

uniform int layer;

void main()
{
    vec3 Coords3D;
    if(layer < 0)
	  	Coords3D = vec3(gl_FragCoord.xy, g_layer+0.5);
	else
	  	Coords3D = vec3(gl_FragCoord.xy, layer+0.5);
	
	vec3 TexCoords3D = vec3(Coords3D.x*ox, Coords3D.y*oy, Coords3D.z*oz);
	//vec3 TexCoords3D = vec3(g_TexCoords.xy, Coords3D.z*oz);
	
	/*
	vec3 circleCenter = vec3(0.5,0.5,0.05);
	float distance = length(TexCoords3D - circleCenter);
	
	float maxDistance = 0.40;
	
	float taperx = 0.0;
	float tapery = 0.0;
	float taperz = 0.0;
	
	float sigmax = 0.5;
	float sigmay = 0.5;
	float sigmaz = 0.2;
	
	if(distance > maxDistance)
	{
	  taperx = 1.0-exp(-pow((distance-maxDistance)/sigmax,2));
	  tapery = 1.0-exp(-pow((distance-maxDistance)/sigmay,2));
	  taperz = 1.0-exp(-pow((distance-maxDistance)/sigmaz,2));
			  
	  //taper = 0.03*(distance-maxDistance)/(0.5-maxDistance);
	}
	
	upVelx = taperx;
    upVely = tapery;	
    upVelz = taperz;
	*/
	
		
    float taperx = 0.0;
	float tapery = 0.0;
    float taperz = 0.0;
	
	float ftaperx = 0.05;
	float ftapery = 0.05;
    float ftaperz = 0.05;
		
	float ntaperLowx = 0.15;
	float ntaperHighx = 0.15;
	float ntaperLowy = 0.15;
	float ntaperHighy = 0.15;	
	float ntaperLowz = 0.0;
	float ntaperHighz = 0.15;
	
	
    if(TexCoords3D.x < ntaperLowx)
      //taperx = ftaperx;
	  //taperx = exp(-pow(ftaperx*TexCoords3D.x/ntaperLowx,2));
	  taperx = ftaperx*(ntaperLowx-TexCoords3D.x)/ntaperLowx;
    if(TexCoords3D.x > 1.0 - ntaperHighx)
      //taperx = ftaperx;	
	  //taperx = exp(-pow(ftaperx*(1-TexCoords3D.x)/ntaperHighx,2));
	  taperx = ftaperx*(TexCoords3D.x-1.0+ntaperHighx)/ntaperHighx;
 	
    if(TexCoords3D.y < ntaperLowy)
      //tapery = ftapery;
	  //tapery = exp(-pow(ftapery*TexCoords3D.y/ntaperLowy,2));
	  tapery = ftapery*(ntaperLowy-TexCoords3D.y)/ntaperLowy;	
    if(TexCoords3D.y > 1.0 -ntaperHighy)
      //tapery = ftapery; 
      //tapery = exp(-pow(ftapery*(1-TexCoords3D.y)/ntaperHighy,2));
      tapery = ftapery*(TexCoords3D.y-1.0+ntaperHighy)/ntaperHighy;	  
	
    if(TexCoords3D.z < ntaperLowz)
      //taperz = ftaperz;
	  //taperz = exp(-pow(ftaperz*TexCoords3D.z/ntaperLowz,2));
	  taperz = ftaperz*(ntaperLowz-TexCoords3D.z)/ntaperLowz;
    if(TexCoords3D.z > 1.0-ntaperHighz)
      //taperz = ftaperz;
	  //taperz = exp(-pow(ftaperz*(1-TexCoords3D.z)/ntaperHighz,2));
	  taperz = ftaperz*(TexCoords3D.z-1.0+ntaperHighz)/ntaperHighz;
	
	
    upVelx = max(max(taperx,tapery),taperz);
    upVely = max(max(taperx,tapery),taperz);	
    upVelz = max(max(taperx,tapery),taperz);
	
	
}
